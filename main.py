#!/usr/bin/env python3
import os
import subprocess

PROJECT_DIRECTORY = "pdf_pic_converter"
FILES_DIRECTORY = PROJECT_DIRECTORY + "/files"
IMAGE_NAME = "pdf_pic_converter:latest"
PDF_FILE_NAME = "yourfile.pdf"

# If docker is not installed, install it
# build image
# run image
# choose pdf file
# convert pdf file to images
# user changes images
# convert images to pdf
# delete container and image


def run_command(command):
    print(f"Running command: {' '.join(command)}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        stdout_line = process.stdout.readline()
        stderr_line = process.stderr.readline()

        if stdout_line == '' and stderr_line == '' and process.poll() is not None:
            break

        if stdout_line:
            print(f"STDOUT: {stdout_line.strip()}")

        if stderr_line:
            print(f"STDERR: {stderr_line.strip()}")

    process.wait()

    print("\n")

    return process.returncode


if __name__ == '__main__':
    run_command(["docker", "build", "-t", IMAGE_NAME, "."])
    run_command(["docker", "run", "--name", "converter", "-v", f"{FILES_DIRECTORY}:/shared", "-it", IMAGE_NAME, "/bin/bash"])

    # Run the command $ pdftoppm /shared/yourfile.pdf /shared/yourimage -jpeg
    run_command(["pdftoppm", f"/shared/{PDF_FILE_NAME}", f"/shared/{PDF_FILE_NAME}", "-jpeg"])

    # Wait for the user to press enter
    input("Press enter when you are done editing the images...")

    # Run the command $ convert /shared/yourimage.jpg /shared/yourfile.pdf
    run_command(["convert", f"/shared/{PDF_FILE_NAME}.jpg", f"/shared/{PDF_FILE_NAME}"])
