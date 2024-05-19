import subprocess
from decrypt_file import decrypt_file
from disk import is_disk_connected
import os
import sys


def decrypt_drive(external_drive_path):
    # get current working directory
    cwd = os.getcwd()
    # copy the drive to the current working directory
    ans = subprocess.run(
        ['sudo', 'dd', 'if=' + external_drive_path + '1', 'of=' + cwd + '/drive.img_encrypted.bin'])
    if (ans.returncode != 0):
        print("Error while copying the drive")
        sys.exit(1)
    # copy encryption data to the current working directory
    ans = subprocess.run(
        ['sudo', 'dd', 'if=' + external_drive_path + '2', 'of=' + cwd + '/drive.img_encrypted.key', 'bs=348', 'count=1'])
    if (ans.returncode != 0):
        print("Error while copying the drive")
        sys.exit(1)

    with open(cwd + '/drive.img_encrypted.bin', "rb") as f, open(cwd + '/drive.img_encrypted.key', "rb") as f2:
        encrypted_file = f.read()
        encrypted_key = f2.read()

    os.remove(cwd + '/drive.img_encrypted.bin')
    os.remove(cwd + '/drive.img_encrypted.key')

    # unite the files
    with open(cwd + '/drive.img_encrypted.bin', "wb") as f:
        f.write(encrypted_key + encrypted_file)

    # decrypt the file
    filename = decrypt_file(cwd + '/drive.img_encrypted.bin')
    os.remove(cwd + '/drive.img_encrypted.bin')

    # copy the decrypted drive data to the external drive
    ans = subprocess.run(
        ['sudo', 'dd', 'if=' + filename, 'of=' + external_drive_path + '1'])
    if (ans.returncode != 0):
        print("Error while copying the drive")
        sys.exit(1)

    os.remove(filename)


if __name__ == "__main__":
    external_drive_path = sys.argv[1]

    if (is_disk_connected(external_drive_path)):
        if (input(f"Are you sure you want to encrypt the drive {external_drive_path} (yes/no) ") == "yes" or "y"):
            decrypt_drive(external_drive_path)
