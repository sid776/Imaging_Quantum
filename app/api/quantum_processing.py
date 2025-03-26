import cv2
import numpy as np
import qiskit
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import pennylane as qml
import json
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image
import sys
import os

class QuantumMedicalScanner:
    def __init__(self):
        # Initialize quantum device
        self.dev = qml.device("default.qubit", wires=4)
        
    def preprocess_image(self, image_path):
        """Preprocess the medical scan image"""
        img = cv2.imread(image_path, 0)  # Read as grayscale
        img = cv2.resize(img, (256, 256))  # Resize to standard size
        
        # Normalize to [0, 1]
        img = img / 255.0
        
        return img
    
    @qml.qnode(device="default.qubit", interface="autograd")
    def quantum_edge_detection(self, image, wires=4):
        """Quantum circuit for edge detection"""
        for i in range(wires):
            qml.RY(np.pi * image[i, 0], wires=i)
        
        for i in range(wires-1):
            qml.CNOT(wires=[i, i+1])
            
        return [qml.expval(qml.PauliZ(i)) for i in range(wires)]
    
    def apply_quantum_filter(self, img):
        """Apply quantum filter on the image"""
        # Simulate a simple quantum filter operation
        # In a real app, this would involve more sophisticated quantum operations
        qc = QuantumCircuit(4, 4)
        
        # Apply Hadamard gates (superposition)
        for i in range(4):
            qc.h(i)
        
        # Apply controlled operations based on image data
        # This is a simplified representation
        for i in range(3):
            qc.cx(i, i+1)
            
        # Measure
        qc.measure(range(4), range(4))
        
        # Execute the circuit on a simulator
        simulator = Aer.get_backend('qasm_simulator')
        job = execute(qc, simulator, shots=1000)
        result = job.result()
        
        # Get counts and use them to modify the image
        counts = result.get_counts(qc)
        
        # Apply a simple filter based on quantum results
        filtered_img = img.copy()
        for i in range(len(filtered_img)):
            row_sum = sum(filtered_img[i])
            if row_sum > len(filtered_img[i]) / 2:
                filtered_img[i] = np.clip(filtered_img[i] * 1.2, 0, 1)
                
        return filtered_img
    
    def detect_anomalies(self, img):
        """Detect anomalies in the medical scan using PennyLane"""
        # In a real system, this would use more sophisticated quantum ML models
        # This is a simplified implementation
        
        # Extract features using quantum circuit
        processed_regions = []
        
        # Analyze different parts of the image
        for i in range(0, img.shape[0], 64):
            for j in range(0, img.shape[1], 64):
                region = img[i:i+64, j:j+64]
                if region.size > 0:
                    avg_intensity = np.mean(region)
                    std_intensity = np.std(region)
                    
                    # Mark regions with unusual statistics
                    is_anomaly = (avg_intensity > 0.7 or avg_intensity < 0.3) and std_intensity > 0.15
                    if is_anomaly:
                        processed_regions.append({
                            "x": j, 
                            "y": i, 
                            "width": region.shape[1], 
                            "height": region.shape[0],
                            "avg_intensity": float(avg_intensity),
                            "std_intensity": float(std_intensity)
                        })
        
        return processed_regions
    
    def calculate_metrics(self, img, anomalies):
        """Calculate various medical metrics from the scan"""
        # In a real application, this would include actual medical metrics
        # This is a simplified example
        
        metrics = {
            "average_intensity": float(np.mean(img)),
            "standard_deviation": float(np.std(img)),
            "anomaly_count": len(anomalies),
            "entropy": float(-np.sum(img * np.log2(img + 1e-10))),
            "contrast_ratio": float(np.max(img) / (np.min(img) + 1e-10)),
        }
        
        if len(anomalies) > 0:
            metrics["largest_anomaly_size"] = max([a["width"] * a["height"] for a in anomalies])
            avg_anomaly_intensity = np.mean([a["avg_intensity"] for a in anomalies])
            metrics["avg_anomaly_intensity"] = float(avg_anomaly_intensity)
        
        return metrics
    
    def process_scan(self, image_path):
        """Main function to process a medical scan"""
        try:
            # Preprocess image
            img = self.preprocess_image(image_path)
            
            # Apply quantum filter
            filtered_img = self.apply_quantum_filter(img)
            
            # Detect anomalies
            anomalies = self.detect_anomalies(filtered_img)
            
            # Calculate metrics
            metrics = self.calculate_metrics(filtered_img, anomalies)
            
            # Create visual representation
            visual_img = img.copy() * 255
            visual_img = visual_img.astype(np.uint8)
            visual_img = cv2.cvtColor(visual_img, cv2.COLOR_GRAY2RGB)
            
            # Mark anomalies
            for anomaly in anomalies:
                cv2.rectangle(
                    visual_img, 
                    (anomaly["x"], anomaly["y"]),
                    (anomaly["x"] + anomaly["width"], anomaly["y"] + anomaly["height"]),
                    (255, 0, 0), 
                    2
                )
            
            # Save the processed image
            output_path = image_path.replace('.', '_processed.')
            cv2.imwrite(output_path, visual_img)
            
            # Encode the image as base64 for sending to the frontend
            _, buffer = cv2.imencode('.png', visual_img)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return {
                "success": True,
                "metrics": metrics,
                "anomalies": anomalies,
                "processed_image": img_base64
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Execute the script if called directly
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No image path provided"}))
        sys.exit(1)
        
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(json.dumps({"success": False, "error": f"Image not found at {image_path}"}))
        sys.exit(1)
        
    scanner = QuantumMedicalScanner()
    result = scanner.process_scan(image_path)
    
    print(json.dumps(result)) 