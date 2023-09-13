#!/bin/bash

# Function to handle errors
handle_error() {
  echo "Error: $1"
  exit 1
}

# Get version from user
read -p "Enter version: " version

# Get commit hash from user
read -p "Enter commit hash: " commit_hash

# Tag the commit
git tag "$version" "$commit_hash" || handle_error "Failed to tag the commit"

# Build the image
docker build -t chat-app:$version . -f thin.dockerfile || handle_error "Failed to build the image"

#push the tag to github repository
git push origin "$version" || handle_error "failed to push to github"

# Success message
echo "Deployment successful!"