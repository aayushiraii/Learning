DayOne was mostly System setup
Downloading python and Vs code and congifiguring Git 

#Navigation 
pwd        # Show current directory
ls         # List files 
cd folder  # Go into a folder
cd ..      # Go back one folder


#file management
mkdir project     # Create a folder
touch file.py     # Create a file 
rm file.py        # Delete file


#VE
python -m venv venv     # Create virtual environment
source venv/bin/activate   # Activate 
deactivate                 # Exit venv

Basic Git Commands

#Setup
git init                # Initialize repo
git clone <repo-url>    # Clone existing repo

#Tracking Changes
git status              # Check changes
git add file.py         # Add specific file
git add .               # Add all files
git commit -m "message" # Save changes

#Push & Pull
git push origin main    # Upload code
git pull origin main    # Get latest changes

#Remote
git remote add origin <repo-url>

The most common workflow:

git add .
git commit -m "Any mess"
git push

