#!/usr/bin/env python3
import os
import subprocess

PROJECT_DIRECTORY = "pdf_pic_converter"
FILES_DIRECTORY = PROJECT_DIRECTORY + "/files"
IMAGE_NAME = "pdf_pic_converter:latest"

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


def get_container_ids_by_tag(tag, server_address=None):
    if server_address:
        command = ["ssh", server_address, "docker", "ps", "-a", "--filter", f"ancestor={tag}", "--format", "{{.ID}}"]
    else:
        command = ["docker", "ps", "-a", "--filter", f"ancestor={tag}", "--format", "{{.ID}}"]

    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )

        container_ids = result.stdout.strip().split('\n')
        return container_ids

    except subprocess.CalledProcessError as e:
        print("Error running docker command:", e)
        return []

def get_image_ids_by_tag(tag, server_address=None):
    if server_address:
        command = ["ssh", server_address, "docker", "images", "crystord:latest", "-q"]
    else:
        command = ["docker", "images", "crystord:latest", "-q"]

    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )

        image_ids = result.stdout.strip().split('\n')
        return image_ids

    except subprocess.CalledProcessError as e:
        print("Error running docker command:", e)
        return []


if __name__ == '__main__':
    result = run_command(["docker", "--version"])
    if result != 0:
        print("Docker is not installed. Please install Docker before runnig this script.")
        exit(1)

    result = run_command(["ls", PROJECT_DIRECTORY])
    if result == 0:
        print("The directory {} already exists. Please delete it before running this script.", PROJECT_DIRECTORY)
        exit(1)

    run_command(["mkdir", "-p", PROJECT_DIRECTORY])
    run_command(["mkdir", "-p", FILES_DIRECTORY])

    os.chdir(PROJECT_DIRECTORY)

    run_command(["wget", "https://raw.githubusercontent.com/aleutheris/pdf_pic_converter/main/main.py"])
    run_command(["wget", "https://raw.githubusercontent.com/aleutheris/pdf_pic_converter/main/Dockerfile"])

    run_command(["python3", "main.py"])
