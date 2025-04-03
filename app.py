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
os.makedirs('processed_images', exist_ok=True)
os.makedirs('traditional_results', exist_ok=True)

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
        
        # Save uploaded file with consistent timestamp format
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
        
        # Save comparison results with proper extension and consistent timestamp
        comparison_filename = f"comparison_{timestamp}.json"
        comparison_filepath = os.path.join('comparison_results', comparison_filename)
        
        # Ensure the comparison results directory exists
        os.makedirs('comparison_results', exist_ok=True)
        
        # Save the comparison results
        with open(comparison_filepath, 'w') as f:
            json.dump({
                'quantum_result': quantum_result,
                'comparison_result': comparison_result,
                'timestamp': timestamp,
                'original_filename': file.filename
            }, f, indent=4)
        
        # Verify comparison results were saved
        if not os.path.exists(comparison_filepath):
            return jsonify({'success': False, 'error': 'Failed to save comparison results'})
        
        return jsonify({
            'success': True,
            'quantum_result': quantum_result,
            'comparison_result': comparison_result,
            'comparison_file': comparison_filename,
            'timestamp': timestamp,
            'message': f'Successfully processed image and saved comparison results as {comparison_filename}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/download/<filename>')
def download(filename):
    try:
        # Determine the directory based on the file type
        if filename.startswith('comparison_'):
            directory = 'comparison_results'
            # For comparison files, read and format as text
            filepath = os.path.join(directory, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    # Format the data as readable text
                    text_content = f"Comparison Analysis Report\n{'='*30}\n\n"
                    text_content += f"Timestamp: {data.get('timestamp', 'N/A')}\n"
                    text_content += f"Original File: {data.get('original_filename', 'N/A')}\n\n"
                    
                    # Add quantum results
                    text_content += "Quantum Processing Results:\n"
                    text_content += "-" * 20 + "\n"
                    quantum_result = data.get('quantum_result', {})
                    for key, value in quantum_result.items():
                        if key != 'success':
                            text_content += f"{key}: {value}\n"
                    
                    # Add comparison results
                    text_content += "\nComparison Results:\n"
                    text_content += "-" * 20 + "\n"
                    comparison_result = data.get('comparison_result', {})
                    for key, value in comparison_result.items():
                        text_content += f"{key}: {value}\n"
                    
                    # Create a response with the formatted text
                    response = flask.Response(text_content, mimetype='text/plain')
                    # Force download with Save As dialog
                    response.headers['Content-Disposition'] = f'attachment; filename="{os.path.splitext(filename)[0]}_analysis.txt"'
                    response.headers['Content-Type'] = 'text/plain'
                    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                    response.headers['Pragma'] = 'no-cache'
                    response.headers['Expires'] = '0'
                    response.headers['X-Content-Type-Options'] = 'nosniff'
                    response.headers['Content-Length'] = len(text_content.encode('utf-8'))
                    response.headers['Content-Transfer-Encoding'] = 'binary'
                    response.headers['Accept-Ranges'] = 'none'
                    return response
            else:
                # If file doesn't exist, return error with available files
                available_files = []
                try:
                    for f in os.listdir(directory):
                        if f.startswith('comparison_') and f.endswith('.json'):
                            available_files.append(f)
                except Exception as e:
                    print(f"Error listing files in {directory}: {str(e)}")
                
                return jsonify({
                    'success': False, 
                    'error': f'File not found: {filename} in {directory}',
                    'available_files': available_files,
                    'message': f'Please select from available files in {directory} or try uploading a new image.',
                    'directory': directory
                })
        elif '_processed' in filename:
            directory = 'processed_images'
        elif '_traditional' in filename:
            directory = 'traditional_results'
        else:
            directory = 'results'
        
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        
        filepath = os.path.join(directory, filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            # Get list of available files in the directory
            available_files = []
            try:
                for f in os.listdir(directory):
                    if directory == 'comparison_results':
                        if f.startswith('comparison_') and f.endswith('.json'):
                            available_files.append(f)
                    elif directory == 'processed_images':
                        if '_processed' in f:
                            available_files.append(f)
                    elif directory == 'traditional_results':
                        if '_traditional' in f:
                            available_files.append(f)
                    else:
                        available_files.append(f)
            except Exception as e:
                print(f"Error listing files in {directory}: {str(e)}")
            
            return jsonify({
                'success': False, 
                'error': f'File not found: {filename} in {directory}',
                'available_files': available_files,
                'message': f'Please select from available files in {directory} or try uploading a new image.',
                'directory': directory
            })
        
        # Get the file extension
        file_ext = os.path.splitext(filename)[1]
        
        # Set appropriate MIME type based on file extension
        mime_types = {
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.tiff': 'image/tiff',
            '.txt': 'text/plain'
        }
        mime_type = mime_types.get(file_ext, 'application/octet-stream')
        
        # Create response with file
        response = send_file(
            filepath,
            mimetype=mime_type,
            as_attachment=True,
            download_name=filename
        )
        
        # Set headers to force download and show save dialog
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Type'] = mime_type
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Length'] = os.path.getsize(filepath)
        response.headers['Content-Transfer-Encoding'] = 'binary'
        response.headers['Accept-Ranges'] = 'none'
        
        return response
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/list-comparisons')
def list_comparisons():
    try:
        # Ensure the directory exists
        os.makedirs('comparison_results', exist_ok=True)
        
        # Get list of comparison files
        comparison_files = []
        for filename in os.listdir('comparison_results'):
            if filename.startswith('comparison_') and filename.endswith('.json'):
                filepath = os.path.join('comparison_results', filename)
                file_stats = os.stat(filepath)
                comparison_files.append({
                    'filename': filename,
                    'timestamp': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'size': file_stats.st_size
                })
        
        # Sort by timestamp, newest first
        comparison_files.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'success': True,
            'files': comparison_files
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 