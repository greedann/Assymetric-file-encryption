# Assymetric-file-encryption
 
## Introduction

This repository contains several Python scripts that implement various cryptographic functions. Most of the functions are cross-platform, but some are only available for Linux.

## Features

* Digital signature generation
* Private key sharing
* Encrypting files with digital signature
* Encrypting files with a password
* File decryption with a private key or password
* Disk encryption/decryption (Linux only)
* Recovery of private key with a preset number of parts

## Installation

Dependencies

`Python3`

To run the application locally you need to clone the repository.
```bash
git clone https://github.com/greedann/Assymetric-file-encryption.git 
cd Assymetric-file-encryption
```
Create virtual environment and install requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Now you ready to go

## Usage

### Generate sertificate
First, to use the cryptographic functions, you need to generate your digital signature and its private key. This can be done as follows:

```bash
python generate_sertificate.py
```

You now have your own certificate that you can use to encrypt your data.

### Encrypt file

To encrypt a file, run the command below
```bash
python encrypt_file.py <filename>
```
Where `filename` is the name of the file in the current directory or the full path to the file. After the command is executed, an encrypted file with the format `.bin` will appear.

### Encrypt drive

To encrypt a drive, run the command below
```bash
python encrypt_drive.py <device>
```
Where `device` is the name of the disk you want to encrypt. After running the command, your disk will be encrypted.

### Decrypt file/drive

For decryption the procedure is very similar, but you need to change `encrypt` to `decrypt` in the commands for encryption. The arguments remain the same.

### Private key restore

If you split your private key into several parts when creating a digital signature, it is possible to restore it. To do this, you need to collect the minimum number of parts (specified at creation) and place them in the `sertificate` directory. And then execute the command

```bash
python restore_private_key.py
```

If the parts of the key were correct and were sufficient, the `private_key.pem` file will appear in the `sertificate` directory, containing your original private key.