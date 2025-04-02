import flask
from flask import render_template, request, jsonify, send_file
import os
from datetime import datetime
import json
from quantum_processing import process_image
from compare_approaches import compare_quantum_traditional

app = flask.Flask(__name__)

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('results', exist_ok=True)
os.makedirs('comparison_results', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
            
        # Validate file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
        if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({
                'success': False, 
                'error': f'Invalid file type. Allowed types are: {", ".join(allowed_extensions)}'
            })
        
        # Save uploaded file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Verify file was saved successfully
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'Failed to save uploaded file'})
            
        # Process image with quantum approach
        quantum_result = process_image(filepath)
        if not quantum_result.get('success', False):
            return jsonify({
                'success': False, 
                'error': quantum_result.get('error', 'Failed to process image')
            })
        
        # Compare with traditional approach
        comparison_result = compare_quantum_traditional(filepath)
        if comparison_result is None:
            return jsonify({'success': False, 'error': 'Failed to compare approaches'})
        
        # Save comparison results
        comparison_filename = f"comparison_{timestamp}.json"
        comparison_filepath = os.path.join('comparison_results', comparison_filename)
        with open(comparison_filepath, 'w') as f:
            json.dump({
                'quantum_result': quantum_result,
                'comparison_result': comparison_result
            }, f, indent=4)
        
        return jsonify({
            'success': True,
            'quantum_result': quantum_result,
            'comparison_result': comparison_result
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/download/<filename>')
def download(filename):
    try:
        # Determine the directory based on the file type
        if filename.startswith('comparison_'):
            directory = 'comparison_results'
        else:
            directory = 'results'
        
        filepath = os.path.join(directory, filename)
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 