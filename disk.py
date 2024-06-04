import subprocess

def is_disk_connected(disk_name):
    try:
        result = subprocess.run(['lsblk', '-no', 'NAME'], capture_output=True, text=True, check=True)
        disks = result.stdout.split()
        return disk_name.split('/')[-1] in disks
    except subprocess.CalledProcessError:
        return False
