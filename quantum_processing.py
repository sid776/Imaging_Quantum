import numpy as np
import cv2
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from PIL import Image
import os
import json
from datetime import datetime

def quantum_feature_extraction(image_data, n_qubits=8):
    """Enhanced quantum feature extraction with improved circuit design"""
    # Normalize image data
    normalized_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data))
    
    # Create quantum circuit with more qubits for better feature representation
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Initial superposition
    for i in range(n_qubits):
        qc.h(i)
    
    # Apply enhanced quantum operations
    for i in range(n_qubits):
        # Encode classical data with improved rotation angles
        qc.ry(normalized_data[i % len(normalized_data)] * np.pi, i)
        qc.rz(normalized_data[(i + 1) % len(normalized_data)] * np.pi, i)
        
        # Add entanglement for better feature correlation
        if i < n_qubits - 1:
            qc.cx(i, i + 1)
            qc.crz(normalized_data[i] * np.pi, i, i + 1)
    
    # Add quantum fourier transform for frequency analysis
    for i in range(n_qubits):
        for j in range(i):
            qc.cp(np.pi/float(2**(i-j)), j, i)
        qc.h(i)
    
    # Add additional quantum operations for feature enhancement
    for i in range(n_qubits):
        qc.s(i)  # Phase gate for complex features
        if i < n_qubits - 1:
            qc.swap(i, i + 1)  # Mix features
    
    # Inverse quantum fourier transform
    for i in range(n_qubits-1, -1, -1):
        qc.h(i)
        for j in range(i):
            qc.cp(-np.pi/float(2**(i-j)), j, i)
    
    # Measure in different bases for richer feature extraction
    for i in range(n_qubits):
        qc.measure(i, i)
    
    # Execute circuit with increased shots for better accuracy
    backend = AerSimulator()
    result = backend.run(qc, shots=8192).result()
    counts = result.get_counts()
    
    # Enhanced feature extraction with normalization
    features = np.zeros(2**n_qubits)
    total_counts = sum(counts.values())
    for state, count in counts.items():
        features[int(state, 2)] = count / total_counts
    
    # Calculate quantum entropy and additional quantum metrics
    quantum_entropy = -np.sum(features * np.log2(features + 1e-10))
    
    # Calculate additional quantum metrics
    feature_mean = np.mean(features)
    feature_std = np.std(features)
    quantum_contrast = feature_std / (feature_mean + 1e-10)
    
    return features, quantum_entropy, quantum_contrast

def process_image(image_path):
    """Enhanced image processing with improved quantum features and anomaly detection"""
    try:
        # Verify file exists
        if not os.path.exists(image_path):
            return {'success': False, 'error': f'Image file not found: {image_path}'}
            
        # Load and preprocess image with detailed error checking
        image = cv2.imread(image_path)
        if image is None:
            return {'success': False, 'error': f'Failed to load image: {image_path}. Please ensure it is a valid image file.'}
            
        # Convert to grayscale if image is in color
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Verify image dimensions
        if image.size == 0:
            return {'success': False, 'error': 'Image is empty'}
            
        # Create output directories if they don't exist
        processed_dir = 'processed_images'
        os.makedirs(processed_dir, exist_ok=True)
        
        # Generate output path
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(processed_dir, f"{name}_processed{ext}")
        
        # Resize for quantum processing while maintaining aspect ratio
        max_size = 32
        h, w = image.shape
        scale = max_size / max(h, w)
        new_size = (int(w * scale), int(h * scale))
        image_resized = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
        
        # Normalize pixel values
        image_normalized = image_resized.astype(float) / 255.0
        
        # Extract quantum features with increased number of qubits
        quantum_features, quantum_entropy, quantum_contrast = quantum_feature_extraction(
            image_normalized.flatten(), n_qubits=10)
        
        # Calculate enhanced metrics
        brightness = np.mean(image)
        contrast = np.std(image)
        entropy = -np.sum(np.histogram(image, bins=256)[0] * np.log2(np.histogram(image, bins=256)[0] + 1e-10))
        
        # Enhanced anomaly detection with multi-scale approach
        anomalies = []
        
        # Quantum anomaly detection with adaptive threshold
        mean_feature = np.mean(quantum_features)
        std_feature = np.std(quantum_features)
        quantum_threshold = mean_feature + 2 * std_feature  # Dynamic threshold
        
        for i in range(len(quantum_features)):
            if quantum_features[i] > quantum_threshold:
                anomalies.append({
                    'type': 'quantum_anomaly',
                    'location': [i % new_size[0], i // new_size[0]],
                    'severity': (quantum_features[i] - quantum_threshold) / quantum_threshold
                })
        
        # Multi-scale classical anomaly detection
        scales = [(1.0, 100, 200), (0.5, 50, 100), (2.0, 200, 400)]
        for scale_factor, low_threshold, high_threshold in scales:
            scaled_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
            edges = cv2.Canny(scaled_image, low_threshold, high_threshold)
            
            # Use adaptive thresholding
            thresh = cv2.adaptiveThreshold(scaled_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            # Combine edge and threshold detection
            combined = cv2.bitwise_and(edges, thresh)
            points = np.where(combined > 0)
            
            for x, y in zip(points[1], points[0]):
                if np.random.random() < 0.05:  # Sample points
                    # Calculate local statistics
                    local_region = scaled_image[
                        max(0, y-5):min(scaled_image.shape[0], y+6),
                        max(0, x-5):min(scaled_image.shape[1], x+6)
                    ]
                    local_std = np.std(local_region)
                    local_contrast = (np.max(local_region) - np.min(local_region)) / 255.0
                    
                    severity = (local_std * local_contrast) / 255.0
                    if severity > 0.1:  # Filter weak anomalies
                        anomalies.append({
                            'type': f'classical_anomaly_scale_{scale_factor}',
                            'location': [int(x/scale_factor), int(y/scale_factor)],
                            'severity': float(severity)
                        })
        
        # Sort anomalies by severity and remove duplicates
        anomalies.sort(key=lambda x: x['severity'], reverse=True)
        
        # Remove duplicate anomalies that are too close to each other
        filtered_anomalies = []
        for anomaly in anomalies:
            is_duplicate = False
            for existing in filtered_anomalies:
                dist = np.sqrt((anomaly['location'][0] - existing['location'][0])**2 +
                             (anomaly['location'][1] - existing['location'][1])**2)
                if dist < 5:  # Distance threshold
                    is_duplicate = True
                    break
            if not is_duplicate:
                filtered_anomalies.append(anomaly)
        
        # Apply advanced image enhancement
        enhanced = cv2.convertScaleAbs(image, alpha=1.1, beta=5)
        
        # Apply adaptive histogram equalization
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(enhanced)
        
        # Save enhanced image
        cv2.imwrite(output_path, enhanced)
        
        return {
            'success': True,
            'output_path': output_path,
            'metrics': {
                'brightness': float(brightness),
                'contrast': float(contrast),
                'entropy': float(entropy),
                'quantum_entropy': float(quantum_entropy),
                'quantum_contrast': float(quantum_contrast)
            },
            'anomalies': filtered_anomalies[:10],  # Limit to top 10 anomalies
            'image_quality': {
                'resolution': f"{image.shape[1]}x{image.shape[0]}",
                'format': os.path.splitext(image_path)[1],
                'quantum_features': len(quantum_features)
            }
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Error processing image: {str(e)}'}

# Make functions available for import
__all__ = ['process_image', 'quantum_feature_extraction']
