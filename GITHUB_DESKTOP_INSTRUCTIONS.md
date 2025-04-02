# GitHub Desktop Instructions

## Using GitHub Desktop to Push Your Project

GitHub Desktop is a user-friendly application that allows you to manage Git repositories without using command-line instructions.

### Step 1: Install GitHub Desktop

1. Download GitHub Desktop from: https://desktop.github.com/
2. Install the application on your computer
3. Open GitHub Desktop and sign in to your GitHub account

### Step 2: Add Your Local Repository

1. In GitHub Desktop, click on **File** > **Add local repository**
2. Browse to your project folder: `C:\Users\Siddharth\Downloads\New folder (2)\Quantum_Medical_Image_Scanning`
3. Click **Add Repository**
4. If GitHub Desktop asks if you want to create a repository here, click **Create a Repository**
5. Enter the following details:
   - Name: `Imaging_Quantum`
   - Description: `Quantum Medical Image Scanning application using simulated quantum processing`
   - Keep the local path as is
   - Make sure "Initialize this repository with a README" is **unchecked**
   - Choose a license if desired (MIT License is recommended)
   - Click **Create Repository**

### Step 3: Make Your First Commit

1. You should see a list of all files in your project that will be added
2. Enter a summary for your commit (e.g., "Initial commit of Quantum Medical Image Scanner")
3. Click **Commit to main** (or whatever your default branch is called)

### Step 4: Push to GitHub

1. Click on **Repository** > **Push**
2. If prompted to "Publish this repository to GitHub", click the button
3. In the dialog box:
   - Make sure the name is set to `Imaging_Quantum`
   - Keep your GitHub username (sid776) as the owner
   - Choose whether you want the repository to be Public or Private
   - Click **Publish Repository**

### Step 5: Verify on GitHub

1. After pushing, click on **Repository** > **View on GitHub**
2. This will open a browser tab showing your repository at https://github.com/sid776/Imaging_Quantum
3. Confirm that all your files have been uploaded successfully

### Troubleshooting

- **"This repository already exists on GitHub"**: 
  1. Click on **Repository** > **Repository settings**
  2. Under "Primary remote repository (origin)", click **Change**
  3. Enter `https://github.com/sid776/Imaging_Quantum.git` as the URL
  4. Click **Save**
  5. Try pushing again

- **Authentication Issues**: 
  1. Click on **File** > **Options**
  2. Sign out and sign back in to your GitHub account

- **Unable to Push**: 
  1. Make sure you have write access to the repository
  2. If you forked the repository, make sure you're pushing to your fork 