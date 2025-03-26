import sys
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import random

def quantum_simulation_processing(image_path):
    """
    Simulate quantum image processing for testing the application
    In a real application, this would use actual quantum computing libraries
    """
    try:
        print(f"Loading image from {image_path}")
        # Load and preprocess the image
        try:
            img = Image.open(image_path)
            img = img.convert('L')  # Convert to grayscale
            
            # Resize image to 8x8 for processing
            img = img.resize((8, 8))
            img_array = np.array(img)
            
            # Normalize pixel values to [0, 1]
            img_array = img_array / 255.0
            
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            raise Exception(f"Failed to load or process image: {str(e)}")
        
        print("Processing image")
        # Simulate quantum processing with simple transformations
        processed_image = img_array.copy()
        
        # Apply simple transformations as a placeholder for quantum processing
        # In a real application, this would use actual quantum algorithms
        processed_image = np.sqrt(processed_image)  # Non-linear transformation
        
        # Add some random noise to simulate quantum effects
        noise = np.random.normal(0, 0.1, processed_image.shape)
        processed_image = np.clip(processed_image + noise, 0, 1)
        
        # Calculate metrics
        print("Calculating metrics")
        metrics = {
            'entropy': float(-np.sum(processed_image * np.log2(processed_image + 1e-10))),
            'contrast': float(np.std(processed_image)),
            'brightness': float(np.mean(processed_image))
        }
        
        # Detect anomalies
        print("Detecting anomalies")
        threshold = np.mean(processed_image) + 1.5 * np.std(processed_image)
        anomalies = []
        
        # Add 1-3 random anomalies for demo purposes
        num_anomalies = random.randint(1, 3)
        for _ in range(num_anomalies):
            i, j = random.randint(0, 7), random.randint(0, 7)
            anomaly_type = random.choice(['bright_spot', 'dark_spot', 'irregular_pattern'])
            intensity = float(processed_image[i, j] + random.uniform(0.1, 0.3))
            
            anomalies.append({
                'location': [int(i), int(j)],
                'intensity': intensity,
                'type': anomaly_type
            })
        
        # Save processed image
        print("Saving processed image")
        output_filename = 'processed_' + os.path.basename(image_path)
        output_path = os.path.join('uploads', output_filename)
        
        # Create a higher resolution image for display
        display_img = Image.fromarray((processed_image * 255).astype(np.uint8)).resize((256, 256), Image.LANCZOS)
        display_img.save(output_path)
        
        # Prepare response
        response = {
            'metrics': metrics,
            'anomalies': anomalies,
            'processed_image': '/uploads/' + output_filename  # Path for browser to access
        }
        
        print("Processing complete")
        return response
        
    except Exception as e:
        print(f"Error in quantum processing: {str(e)}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Please provide an image path"}))
        sys.exit(1)
        
    try:
        result = quantum_simulation_processing(sys.argv[1])
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1) 