import { NextApiRequest, NextApiResponse } from 'next';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
import { PythonShell } from 'python-shell';

// Configure multer for file uploads
const upload = multer({
  storage: multer.diskStorage({
    destination: './uploads',
    filename: (req, file, cb) => {
      const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
      cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
    },
  }),
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    const filetypes = /jpeg|jpg|png|gif|bmp|tiff/;
    const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = filetypes.test(file.mimetype);

    if (mimetype && extname) {
      return cb(null, true);
    } else {
      cb(new Error('Only image files are allowed!'));
    }
  },
});

// Helper function to process multer upload
const runMiddleware = (req, res, fn) => {
  return new Promise((resolve, reject) => {
    fn(req, res, (result) => {
      if (result instanceof Error) {
        return reject(result);
      }
      return resolve(result);
    });
  });
};

// Make sure uploads directory exists
const ensureUploadsDir = () => {
  const uploadsDir = path.join(process.cwd(), 'uploads');
  if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir, { recursive: true });
  }
  return uploadsDir;
};

export default async function handler(req, res) {
  // Only handle POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Ensure uploads directory exists
    const uploadsDir = ensureUploadsDir();

    // Process the file upload
    await runMiddleware(req, res, upload.single('scan'));

    // Check if file was uploaded
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Get the uploaded file path
    const filePath = path.join(uploadsDir, req.file.filename);

    // Run Python script with PythonShell
    const options = {
      mode: 'json',
      pythonPath: 'python', // Use your system's Python path
      scriptPath: path.join(process.cwd(), 'app/api'),
      args: [filePath],
    };

    PythonShell.run('quantum_processing.py', options).then(results => {
      // Extract the results
      if (results && results.length > 0) {
        const result = results[0];
        
        if (result.success) {
          return res.status(200).json(result);
        } else {
          return res.status(500).json({ error: result.error || 'Processing failed' });
        }
      } else {
        return res.status(500).json({ error: 'No results from quantum processing' });
      }
    }).catch(err => {
      console.error('Python processing error:', err);
      return res.status(500).json({ error: 'Error during quantum processing: ' + err.message });
    });
  } catch (error) {
    console.error('API error:', error);
    return res.status(500).json({ error: 'Error processing upload: ' + error.message });
  }
}

export const config = {
  api: {
    bodyParser: false,
  },
}; 