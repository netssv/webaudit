#!/bin/bash
# Script to update GitHub repository
# Only run this when specifically requested

echo "Updating GitHub repository..."

# Add all changes
git add .

# Check if there are changes to commit
if [ -n "$(git status --porcelain)" ]; then
    # Ask for commit message
    echo "Enter commit message (or press Enter for default):"
    read commit_message
    
    if [ -z "$commit_message" ]; then
        commit_message="Update web audit tool"
    fi
    
    # Commit changes
    git commit -m "$commit_message"
    
    # Push to GitHub
    git push origin main
    
    echo "Repository updated successfully!"
else
    echo "No changes to commit."
fi
