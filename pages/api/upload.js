const upload = multer({
  dest: './uploads',
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  },
  limits: {
    fileSize: 50 * 1024 * 1024, // Increased to 50MB for CT scans
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = [
      'image/jpeg',
      'image/jpg',
      'image/png',
      'image/gif',
      'image/bmp',
      'image/tiff',
      'application/dicom',  // DICOM format for CT scans
      'application/octet-stream'  // For raw DICOM files
    ];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only JPEG, PNG, GIF, BMP, TIFF, and DICOM files are allowed.'));
    }
  }
}); 