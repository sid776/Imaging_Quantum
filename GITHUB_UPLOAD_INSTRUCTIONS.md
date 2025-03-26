# GitHub Upload Instructions

## Pushing to https://github.com/sid776/Imaging_Quantum

Follow these steps to push the Quantum Medical Image Scanner project to GitHub:

1. **Install Git** (if not already installed):
   - Download from: https://git-scm.com/downloads
   - Follow the installation instructions
   - Restart your terminal/command prompt after installation

2. **Initialize a Git repository**:
   ```bash
   git init
   ```

3. **Add all files to the repository**:
   ```bash
   git add .
   ```

4. **Commit the changes**:
   ```bash
   git commit -m "Initial commit of Quantum Medical Image Scanner"
   ```

5. **Add the remote repository**:
   ```bash
   git remote add origin https://github.com/sid776/Imaging_Quantum.git
   ```

6. **Push to GitHub**:
   ```bash
   git push -u origin main
   ```
   
   If your default branch is 'master' instead of 'main', use:
   ```bash
   git push -u origin master
   ```

## Authentication

When pushing to GitHub, you'll be prompted for credentials:

- **Username**: Your GitHub username
- **Password**: Use a personal access token (NOT your GitHub password)

### Creating a Personal Access Token:

1. Go to GitHub: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select the necessary scopes (at minimum, select "repo")
4. Click "Generate token"
5. Copy the token (you will only see it once)
6. Use this token as your password when prompted during the push

## Alternative Method: GitHub Desktop

If you prefer a graphical interface:

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in to your GitHub account
3. Choose "Add an Existing Repository from your Hard Drive"
4. Navigate to your project folder
5. Configure the repository settings to point to https://github.com/sid776/Imaging_Quantum
6. Push your changes

## Troubleshooting

- **SSL Certificate Problems**: Try setting
  ```bash
  git config --global http.sslVerify false
  ```
  (Note: This reduces security. Consider a proper fix if used frequently)

- **Authentication Failed**: Make sure you're using a personal access token, not your GitHub password

- **Branch Name Issues**: Check your current branch name with
  ```bash
  git branch
  ```
  Then push to the correct branch 