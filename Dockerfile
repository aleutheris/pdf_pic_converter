# Use the official Ubuntu base image
FROM ubuntu:latest

# Install poppler-utils and ImageMagick
RUN apt-get update && apt-get install -y \
    poppler-utils \
    imagemagick \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for the shared folder
RUN mkdir -p /files

# Set the working directory
WORKDIR /files

# Set the default command to sleep to keep the container running
CMD ["sleep", "infinity"]
