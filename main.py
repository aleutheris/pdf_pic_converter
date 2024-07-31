#!/usr/bin/env python3
import subprocess
import pexpect
from PyQt5.QtWidgets import QApplication, QFileDialog


PROJECT_DIRECTORY = "pdf_pic_converter"
FILES_DIRECTORY = "files"
IMAGE_NAME = "pdf-pic-converter"
FILE_NAME_PREFIX = "AA_new_"


def choose_file():
    app = QApplication([])
    file_dialog = QFileDialog()

    file_path, _ = file_dialog.getOpenFileName(
        caption="Select a file",
        filter="All files (*.*);;Text files (*.txt)"
    )

    if file_path:
        print("Selected file:", file_path)
    else:
        print("No file selected")

    app.exit()

    return file_path


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


def clean_up():
    container_ids = get_container_ids_by_tag(IMAGE_NAME)
    for container_id in container_ids:
        run_command(["docker", "rm", container_id])

    image_ids = get_image_ids_by_tag(IMAGE_NAME)
    for image_id in image_ids:
        run_command(["docker", "rmi", image_id])


def get_container_ids_by_tag(tag):
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
    command = ["docker", "images", tag, "-q"]

    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )

        image_ids = result.stdout.strip().split('\n')
        return image_ids

    except subprocess.CalledProcessError as e:
        print("Error running docker command:", e)
        return []


def main():
    try:
        clean_up()

        run_command(["docker", "build", "-t", IMAGE_NAME+":latest", "."])

        command = f"docker run --name converter -v ./{FILES_DIRECTORY}:/{FILES_DIRECTORY} -it {IMAGE_NAME} /bin/bash"
        child = pexpect.spawn(command)

        child.expect("# ")

        child.sendline("echo 'Hello from inside the container!'")
        child.expect("# ")

        file_name = choose_file()
        child.sendline(f"pdftoppm {file_name}.pdf {file_name} -jpeg")
        child.expect("# ")

        input("Press enter when you are done editing the images...")

        child.sendline(f"convert {file_name}*.jpg {FILE_NAME_PREFIX}{file_name}.pdf")
        child.expect("# ")

        child.close()

        run_command(["mv", f"{FILES_DIRECTORY}/{FILE_NAME_PREFIX}{file_name}.pdf", "../"])
        run_command(["cp", "-r", f"{FILES_DIRECTORY}", "../"])

        clean_up()

    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"pexpect error: {e}")
        clean_up()
    except pexpect.exceptions.TIMEOUT as e:
        print(f"pexpect timeout: {e}")
        clean_up()
    except pexpect.exceptions.EOF as e:
        print(f"pexpect EOF: {e}")
        clean_up()
    except Exception as e:
        print(f"Unexpected error: {e}")
        clean_up()


if __name__ == "__main__":
    main()
