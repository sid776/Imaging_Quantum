import os
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import quantum_processing as qp
import cv2
from tqdm import tqdm
import requests
import zipfile
import io
import json
import tarfile

def download_sample_dataset():
    """Download sample medical image dataset for testing."""
    # Using a subset of the NIH Chest X-ray Dataset
    url = "https://nihcc.box.com/shared/static/vfk49d74nhbxq3nqjg0900w5nvkorp5c.gz"
    
    print("Downloading sample dataset...")
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
            
            with open("sample_images.tar.gz", "wb") as f:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
            progress_bar.close()
            
            # Extract the dataset
            with tarfile.open("sample_images.tar.gz", "r:gz") as tar:
                tar.extractall("test_data")
            
            print("Dataset downloaded and extracted successfully!")
        else:
            print("Failed to download dataset. Please download manually from: https://nihcc.box.com/v/ChestXray-NIHCC")
    except Exception as e:
        print(f"Error downloading dataset: {str(e)}")
        print("Please download manually from: https://nihcc.box.com/v/ChestXray-NIHCC")

def evaluate_quantum_processing(image_path, ground_truth=None):
    """Evaluate quantum processing on a single image."""
    try:
        # Process image with our quantum method
        result = qp.process_image(image_path)
        
        if result is None:
            return None
        
        # Extract features and metrics
        if 'analysis' in result:  # CT scan
            features = result['analysis']['quantum_features']
            metrics = {
                'hounsfield_units': result['analysis']['hounsfield_units'],
                'density_metrics': result['analysis']['density_metrics']
            }
        else:  # Regular image
            features = result['metrics']['quantum_features']
            metrics = {
                'brightness': result['metrics']['brightness'],
                'contrast': result['metrics']['contrast']
            }
        
        # Calculate anomaly detection performance if ground truth is available
        if ground_truth is not None:
            anomalies = result.get('anomalies', [])
            anomaly_map = np.zeros((8, 8))  # Our processing size
            for anomaly in anomalies:
                if isinstance(anomaly['location'], list):
                    i, j = anomaly['location']
                    anomaly_map[i, j] = anomaly['severity']
                else:
                    i = anomaly['location'] // 8
                    j = anomaly['location'] % 8
                    anomaly_map[i, j] = anomaly['severity']
            
            # Compare with ground truth
            accuracy = accuracy_score(ground_truth.flatten(), (anomaly_map > 0.5).flatten())
            precision = precision_score(ground_truth.flatten(), (anomaly_map > 0.5).flatten())
            recall = recall_score(ground_truth.flatten(), (anomaly_map > 0.5).flatten())
            f1 = f1_score(ground_truth.flatten(), (anomaly_map > 0.5).flatten())
            
            return {
                'features': features,
                'metrics': metrics,
                'anomaly_detection': {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1': f1
                }
            }
        
        return {
            'features': features,
            'metrics': metrics
        }
    
    except Exception as e:
        print(f"Error evaluating image {image_path}: {str(e)}")
        return None

def compare_with_classical(image_path):
    """Compare quantum processing with classical methods."""
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Classical processing
        classical_features = cv2.resize(gray, (8, 8)).flatten() / 255.0
        classical_metrics = {
            'brightness': float(np.mean(classical_features)),
            'contrast': float(np.std(classical_features)),
            'entropy': float(-np.sum(classical_features * np.log2(classical_features + 1e-10)))
        }
        
        # Quantum processing
        quantum_result = qp.process_image(image_path)
        if quantum_result is None:
            return None
        
        if 'analysis' in quantum_result:
            quantum_features = quantum_result['analysis']['quantum_features']
            quantum_metrics = {
                'hounsfield_units': quantum_result['analysis']['hounsfield_units'],
                'density_metrics': quantum_result['analysis']['density_metrics']
            }
        else:
            quantum_features = quantum_result['metrics']['quantum_features']
            quantum_metrics = quantum_result['metrics']
        
        return {
            'classical': {
                'features': classical_features.tolist(),
                'metrics': classical_metrics
            },
            'quantum': {
                'features': quantum_features,
                'metrics': quantum_metrics
            }
        }
    
    except Exception as e:
        print(f"Error comparing methods for {image_path}: {str(e)}")
        return None

def run_comprehensive_tests():
    """Run comprehensive tests on the dataset."""
    # Create results directory if it doesn't exist
    os.makedirs("test_results", exist_ok=True)
    
    # Download sample dataset if not exists
    if not os.path.exists("test_data"):
        download_sample_dataset()
    
    # Initialize results storage
    results = {
        'quantum_vs_classical': [],
        'anomaly_detection': [],
        'processing_times': []
    }
    
    # Test on sample images
    test_images = []
    for root, _, files in os.walk("test_data"):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.dcm')):
                test_images.append(os.path.join(root, file))
    
    # Limit to 300 images
    if len(test_images) > 300:
        print(f"Found {len(test_images)} images, limiting to 300 for disk space")
        # Use a fixed random seed for reproducibility
        np.random.seed(42)
        test_images = np.random.choice(test_images, size=300, replace=False).tolist()
    else:
        print(f"Found {len(test_images)} test images")
    
    # Run tests
    for image_path in tqdm(test_images, desc="Processing images"):
        try:
            # Compare quantum vs classical
            comparison = compare_with_classical(image_path)
            if comparison:
                results['quantum_vs_classical'].append({
                    'image': image_path,
                    'comparison': comparison
                })
            
            # Evaluate quantum processing
            evaluation = evaluate_quantum_processing(image_path)
            if evaluation:
                results['anomaly_detection'].append({
                    'image': image_path,
                    'evaluation': evaluation
                })
            
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            continue
    
    # Save results
    with open("test_results/comprehensive_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Tests completed. Results saved to test_results/comprehensive_test_results.json")

if __name__ == "__main__":
    run_comprehensive_tests() 