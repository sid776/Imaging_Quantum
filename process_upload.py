import os
import quantum_processing as qp
import cv2
import matplotlib.pyplot as plt

def process_uploaded_image(image_path):
    """Process a single uploaded image and display results"""
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return
    
    print(f"Processing image: {image_path}")
    
    # Process image using quantum approach
    quantum_result = qp.process_image(image_path)
    if not quantum_result['success']:
        print(f"Error processing image: {quantum_result.get('error', 'Unknown error')}")
        return
    
    # Load and display original and processed images
    original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    processed = cv2.imread(quantum_result['output_path'], cv2.IMREAD_GRAYSCALE)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Display original image
    ax1.imshow(original, cmap='gray')
    ax1.set_title('Original Image')
    ax1.axis('off')
    
    # Display processed image
    ax2.imshow(processed, cmap='gray')
    ax2.set_title('Quantum Processed Image')
    ax2.axis('off')
    
    # Add text with metrics
    metrics_text = f"""
    Metrics:
    Brightness: {quantum_result['metrics']['brightness']:.2f}
    Contrast: {quantum_result['metrics']['contrast']:.2f}
    Entropy: {quantum_result['metrics']['entropy']:.2f}
    Quantum Entropy: {quantum_result['metrics']['quantum_entropy']:.2f}
    
    Anomalies Detected: {len(quantum_result['anomalies'])}
    """
    plt.figtext(0.5, 0.01, metrics_text, ha='center', fontsize=10)
    
    # Save the figure
    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_analysis.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    
    print(f"\nResults saved to: {output_path}")
    print("\nMetrics:")
    for key, value in quantum_result['metrics'].items():
        print(f"{key}: {value:.2f}")
    
    print(f"\nAnomalies detected: {len(quantum_result['anomalies'])}")
    for i, anomaly in enumerate(quantum_result['anomalies'], 1):
        print(f"\nAnomaly {i}:")
        print(f"Type: {anomaly['type']}")
        print(f"Location: {anomaly['location']}")
        print(f"Severity: {anomaly['severity']:.3f}")

if __name__ == "__main__":
    # Get the image path from command line argument or use default
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("Please provide the path to your image:")
        print("python process_upload.py path/to/your/image.jpg")
        sys.exit(1)
    
    process_uploaded_image(image_path) 