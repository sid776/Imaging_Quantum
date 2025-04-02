import os
import cv2
import numpy as np
from datetime import datetime
import json
from quantum_processing import process_image
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def traditional_image_processing(image_path):
    """Traditional image processing approach"""
    try:
        # Read and preprocess image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return None
        
        # Calculate basic metrics
        brightness = np.mean(image)
        contrast = np.std(image)
        entropy = -np.sum(np.histogram(image, bins=256)[0] * np.log2(np.histogram(image, bins=256)[0] + 1e-10))
        
        # Edge detection
        edges = cv2.Canny(image, 100, 200)
        
        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Find contours for anomaly detection
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Detect anomalies
        anomalies = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Filter small contours
                x, y, w, h = cv2.boundingRect(contour)
                roi = image[y:y+h, x:x+w]
                severity = np.std(roi) / 255.0  # Normalize severity
                if severity > 0.1:  # Filter weak anomalies
                    anomalies.append({
                        'type': 'traditional_anomaly',
                        'location': [int(x), int(y)],
                        'severity': float(severity)
                    })
        
        # Sort anomalies by severity
        anomalies.sort(key=lambda x: x['severity'], reverse=True)
        
        # Apply traditional enhancement
        enhanced = cv2.equalizeHist(image)
        
        # Save enhanced image
        output_dir = 'traditional_results'
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(output_dir, f"{name}_traditional{ext}")
        cv2.imwrite(output_path, enhanced)
        
        return {
            'output_path': output_path,
            'metrics': {
                'brightness': float(brightness),
                'contrast': float(contrast),
                'entropy': float(entropy)
            },
            'anomalies': anomalies[:10]  # Limit to top 10 anomalies
        }
    except Exception as e:
        print(f"Error in traditional processing: {str(e)}")
        return None

def compare_quantum_traditional(image_path):
    """Compare quantum and traditional approaches"""
    # Process with quantum approach
    quantum_result = process_image(image_path)
    if not quantum_result['success']:
        print(f"Error in quantum processing: {quantum_result.get('error', 'Unknown error')}")
        return None
    
    # Process with traditional approach
    traditional_result = traditional_image_processing(image_path)
    if traditional_result is None:
        print("Error in traditional processing")
        return None
    
    # Load processed images
    quantum_image = cv2.imread(quantum_result['output_path'], cv2.IMREAD_GRAYSCALE)
    traditional_image = cv2.imread(traditional_result['output_path'], cv2.IMREAD_GRAYSCALE)
    
    # Ensure images are the same size for comparison
    if quantum_image.shape != traditional_image.shape:
        traditional_image = cv2.resize(traditional_image, (quantum_image.shape[1], quantum_image.shape[0]))
    
    # Calculate comparison metrics
    ssim_score = ssim(quantum_image, traditional_image)
    mse = mean_squared_error(quantum_image.flatten(), traditional_image.flatten())
    
    # Create visual comparison
    comparison_dir = 'comparison_results'
    os.makedirs(comparison_dir, exist_ok=True)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    comparison_path = os.path.join(comparison_dir, f"{name}_comparison.png")
    
    plt.figure(figsize=(15, 5))
    plt.subplot(131)
    plt.imshow(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE), cmap='gray')
    plt.title('Original')
    plt.axis('off')
    
    plt.subplot(132)
    plt.imshow(quantum_image, cmap='gray')
    plt.title('Quantum Processing')
    plt.axis('off')
    
    plt.subplot(133)
    plt.imshow(traditional_image, cmap='gray')
    plt.title('Traditional Processing')
    plt.axis('off')
    
    plt.savefig(comparison_path)
    plt.close()
    
    return {
        'image_path': image_path,
        'quantum_anomalies': len(quantum_result['anomalies']),
        'traditional_anomalies': len(traditional_result['anomalies']),
        'structural_similarity': float(ssim_score),
        'mean_squared_error': float(mse),
        'metrics_comparison': {
            'quantum': quantum_result['metrics'],
            'traditional': traditional_result['metrics']
        },
        'comparison_path': comparison_path
    }

def main():
    """Main function to run comparisons on test images"""
    # Find test images
    test_dir = 'test_data/images'
    test_images = [os.path.join(test_dir, f) for f in os.listdir(test_dir) 
                  if f.endswith(('.png', '.jpg', '.jpeg'))][:5]  # Limit to 5 images
    
    print(f"Found {len(test_images)} images for testing\n")
    
    results = []
    for image_path in test_images:
        print(f"\nProcessing image: {image_path}")
        result = compare_quantum_traditional(image_path)
        if result:
            results.append(result)
            
            # Print comparison summary
            print("\nComparison Summary:")
            print("-" * 50)
            print(f"\nImage: {os.path.basename(image_path)}")
            print(f"Quantum Anomalies: {result['quantum_anomalies']}")
            print(f"Traditional Anomalies: {result['traditional_anomalies']}")
            print(f"Structural Similarity: {result['structural_similarity']:.3f}")
            print(f"Mean Squared Error: {result['mean_squared_error']:.3f}")
            
            print("\nMetrics Comparison:")
            print("Quantum vs Traditional")
            qm = result['metrics_comparison']['quantum']
            tm = result['metrics_comparison']['traditional']
            print(f"Brightness: {qm['brightness']:.2f} vs {tm['brightness']:.2f}")
            print(f"Contrast: {qm['contrast']:.2f} vs {tm['contrast']:.2f}")
            print(f"Entropy: {qm['entropy']:.2f} vs {tm['entropy']:.2f}")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join('comparison_results', f'comparison_{timestamp}.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_path}")

if __name__ == "__main__":
    main() 