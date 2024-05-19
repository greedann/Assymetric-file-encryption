import subprocess
from encrypt_file import encrypt_file
from disk import is_disk_connected
import os
import sys


def encrypt_drive(external_drive_path):
    # get current working directory
    cwd = os.getcwd()
    # copy the drive to the current working directory
    ans = subprocess.run(
        ['sudo', 'dd', 'if=' + external_drive_path + '1', 'of=' + cwd + '/drive.img'])
    if (ans.returncode != 0):
        print("Error while copying the drive")
        sys.exit(1)

    # encrypt the file
    encrypted_file = encrypt_file(cwd + '/drive.img', separate_key=True)
    print(f"Drive encrypted to {encrypted_file}")
    os.remove(cwd + '/drive.img')

    # move encrypted files to the external drive
    ans = subprocess.run(
        ['sudo', 'dd', 'if=' + encrypted_file[0], 'of=' + external_drive_path + '1'])
    if (ans.returncode != 0):
        print("Error while copying the drive")
        sys.exit(1)
    os.remove(encrypted_file[0])

    ans = subprocess.run(
        ['sudo', 'dd', 'if=' + encrypted_file[1], 'of=' + external_drive_path + '2'])
    if (ans.returncode != 0):
        print("Error while copying the drive")
        sys.exit(1)
    os.remove(encrypted_file[1])


if __name__ == "__main__":
    external_drive_path = sys.argv[1]
    # check if the drive is connected
    if (is_disk_connected(external_drive_path)):
        if (input(f"Are you sure you want to encrypt the drive {external_drive_path} (yes/no) ") == "yes" or "y"):
            encrypt_drive(external_drive_path)
