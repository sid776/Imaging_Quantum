import { NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import { join } from 'path';
import { PythonShell } from 'python-shell';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file uploaded' },
        { status: 400 }
      );
    }

    // Create uploads directory if it doesn't exist
    const uploadsDir = join(process.cwd(), 'uploads');
    try {
      await writeFile(join(uploadsDir, file.name), Buffer.from(await file.arrayBuffer()));
    } catch (error) {
      console.error('Error saving file:', error);
      return NextResponse.json(
        { error: 'Error saving file' },
        { status: 500 }
      );
    }

    // Run Python script
    const options = {
      mode: 'text' as const,
      pythonPath: 'python',
      pythonOptions: ['-u'],
      scriptPath: join(process.cwd()),
      args: [join(uploadsDir, file.name)]
    };

    try {
      const results = await PythonShell.run('quantum_processing.py', options);
      console.log('Python script output:', results);

      // Parse the results
      const result = results[results.length - 1];
      const parsedResult = JSON.parse(result);

      return NextResponse.json(parsedResult);
    } catch (error) {
      console.error('Error running Python script:', error);
      return NextResponse.json(
        { error: 'Error processing image' },
        { status: 500 }
      );
    }
  } catch (error) {
    console.error('Error in upload handler:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 