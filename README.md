# Quantum Medical Image Scanner

A web application that leverages quantum computing techniques for medical image analysis, anomaly detection, and visualization.

![Quantum Medical Image Scanner](https://via.placeholder.com/1200x630?text=Quantum+Medical+Image+Scanner)

## Overview

The Quantum Medical Image Scanner is a cutting-edge application that demonstrates the potential of quantum computing in medical image processing. It combines modern web technologies with simulated quantum algorithms to analyze medical scan images, detect anomalies, and provide comprehensive visualization of results.

## Features

- **Image Upload**: Upload medical scan images in various formats (JPEG, PNG, etc.)
- **Quantum Image Processing**: Process images using simulated quantum computing techniques
- **Anomaly Detection**: Automatically identify and highlight potential anomalies in medical scans
- **Interactive Visualization**: View processed images alongside metrics and statistical analysis
- **Detailed Metrics**: Get insights through entropy, contrast, and brightness measurements
- **Anomaly Classification**: Classification of different types of anomalies with location data

## Technology Stack

### Frontend
- **Next.js**: React framework for the web interface
- **TypeScript**: Type-safe JavaScript
- **TailwindCSS**: Utility-first CSS framework for styling
- **Chart.js**: JavaScript charting library for data visualization
- **Axios**: Promise-based HTTP client

### Backend
- **Next.js API Routes**: Serverless functions for backend processing
- **Python**: Core language for quantum processing
- **Multer**: File upload handling

### Quantum Processing
- **Qiskit**: IBM's open-source quantum computing framework
- **PennyLane**: Quantum machine learning framework
- **NumPy**: Numerical computing library for Python

### Image Processing
- **PIL/Pillow**: Python Imaging Library
- **Matplotlib**: Plotting library for Python

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- npm or yarn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quantum-medical-image-scanner.git
   cd quantum-medical-image-scanner
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

## Usage Guide

1. **Upload a Medical Scan**:
   - Click on the "Choose File" button and select a medical scan image
   - Click "Upload and Process" to begin the analysis

2. **View Results**:
   - The processed image will be displayed alongside metrics
   - Anomalies are highlighted and detailed in the table
   - Charts show distribution of anomalies and key metrics

3. **Analyze Data**:
   - Review entropy, contrast, and brightness values
   - Check the types and locations of detected anomalies
   - View the summary statistics for a quick overview

## How It Works

The application simulates quantum image processing through the following steps:

1. **Image Upload**: The user uploads a medical scan image through the web interface.

2. **Preprocessing**: The image is converted to grayscale and normalized.

3. **Quantum Processing Simulation**: 
   - In a real quantum application, the image would be encoded into quantum states
   - Quantum circuits would process the image data
   - Measurements would extract processed results
   
   Our simulation demonstrates these concepts without requiring actual quantum hardware.

4. **Anomaly Detection**: Statistical methods identify regions that deviate from normal patterns.

5. **Visualization**: The processed image and analysis are displayed through the web interface.

## Current Limitations

- The quantum algorithms are simulated and not running on actual quantum hardware
- Image resolution is limited for demonstration purposes
- Processing larger images would require more sophisticated quantum algorithms
- This is an educational demonstration rather than a clinical tool

## Future Enhancements

- Integration with real quantum computing backends
- Support for 3D medical scans (CT, MRI volumes)
- Machine learning integration for improved anomaly classification
- Comparative analysis between classical and quantum processing approaches

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- IBM Qiskit team for quantum computing frameworks
- Xanadu for PennyLane quantum machine learning library
- The open-source community for various libraries used in this project

---

**Disclaimer**: This application is for educational and demonstration purposes only. It is not intended for clinical use or medical diagnosis. 
- Next.js and React teams for the web framework 