#!/usr/bin/env python3

"""
SSH Connection Manager

This script provides a command-line interface for managing SSH connections. 
It allows users to securely store, retrieve, and manage their SSH connection 
details in an encrypted format. The script uses the Fernet encryption system 
from the cryptography library to ensure that the stored connection details are secure.

Functions:
    generate_key(password: str) -> bytes:
        Generates a cryptographic key based on a user-provided password using PBKDF2HMAC.
    
    encrypt_data(data: str, password: str) -> bytes:
        Encrypts the given data (string) using a key derived from the provided password.
    
    decrypt_data(token: bytes, password: str) -> str:
        Decrypts the given encrypted token (bytes) using a key derived from the provided password.

    write_encrypted_file(file_path: str, data: bytes, password: str) -> None:
        Writes encrypted data to a file at the specified file path.

    read_encrypted_file(file_path: str, password: str) -> str:
        Reads and decrypts data from a file at the specified file path.

    add_connection() -> None:
        Interactively adds a new SSH connection's details to the encrypted storage.

    delete_connection() -> None:
        Interactively deletes an SSH connection's details from the encrypted storage.

    select_connection() -> None:
        Interactively selects and initiates an SSH connection from the stored connections.

    init() -> None:
        Initializes the encrypted storage with a new password and an empty connection list.

Usage:
    Run the script with different command-line arguments to perform actions:
        --add: To add a new SSH connection.
        --delete: To delete an existing SSH connection.
        --init: To initialize the encrypted storage.
        (No argument): To select and use a stored SSH connection.

Dependencies:
    - cryptography: For encryption and decryption.
    - inquirer: For interactive command-line prompts.
    - getpass: For secure password input.
    - json: For JSON parsing.
    - os, subprocess, sys: Standard Python libraries for system operations.

Note:
    The script assumes an environment capable of executing Python 3 scripts with necessary dependencies installed.

Author: james.standbridge.git@gmail.com
Date: 2023-01-07
"""


import inquirer
import os
import subprocess
import json
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import getpass

CONNECTION_FILE = os.path.expanduser("~/.ssh_connections")

def generate_key(password):
    password = password.encode()  
    salt = b'some_salt' 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_data(data, password):
    key = generate_key(password)
    f = Fernet(key)

    if isinstance(data, str):
        data = data.encode()

    token = f.encrypt(data)
    return token


def decrypt_data(token, password):
    key = generate_key(password)
    f = Fernet(key)
    return f.decrypt(token).decode()

def write_encrypted_file(file_path, data, password):
    with open(file_path, 'wb') as file:
        file.write(data)

def read_encrypted_file(file_path, password):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    return decrypt_data(encrypted_data, password)

def add_connection():
    questions = [
        inquirer.Text('label', message="Enter a label for the connection"),
        inquirer.Text('username', message="Enter the username"),
        inquirer.Password('password', message="Enter the password"),
        inquirer.Text('host', message="Enter the host (IP address or domain name)"),
    ]

    answers = inquirer.prompt(questions)
    connection_info = {
        'label': answers['label'],
        'username': answers['username'],
        'password': answers['password'],
        'host': answers['host'],
    }

    password = getpass.getpass("Enter your encryption password: ")

    try:
        if os.path.isfile(CONNECTION_FILE):
            encrypted_data = read_encrypted_file(CONNECTION_FILE, password)
            connections = json.loads(encrypted_data)
        else:
            connections = []
    except Exception as e:
        print(f"Error reading encrypted file: {e}")
        return

    connections.append(connection_info)

    encrypted_data = encrypt_data(json.dumps(connections), password)
    write_encrypted_file(CONNECTION_FILE, encrypted_data, password)

def delete_connection():
    password = getpass.getpass("Enter your encryption password: ")

    if not os.path.isfile(CONNECTION_FILE):
        print("No connections available.")
        return

    try:
        encrypted_data = read_encrypted_file(CONNECTION_FILE, password)
    except Exception as e:
        print(f"Error reading encrypted file: {e}")
        return

    connections = json.loads(encrypted_data)

    if not connections:
        print("No connections available.")
        return

    connection_labels = [f'{conn["label"]} ({conn["username"]})' for conn in connections]

    questions = [
        inquirer.List('selected_connection',
                      message="Select the connection to delete",
                      choices=connection_labels),
    ]

    answers = inquirer.prompt(questions)
    selected_label = answers['selected_connection']
    selected_conn = next(conn for conn in connections if f'{conn["label"]} ({conn["username"]})' == selected_label)

    connections.remove(selected_conn)

    encrypted_data = encrypt_data(json.dumps(connections), password)
    write_encrypted_file(CONNECTION_FILE, encrypted_data, password)

    print(f"Connection '{selected_conn['label']}' deleted.")


def select_connection():
    password = getpass.getpass("Enter your encryption password: ")

    if not os.path.isfile(CONNECTION_FILE):
        print("No connections available. Please call the script with the --setup option.")
        return

    try:
        encrypted_data = read_encrypted_file(CONNECTION_FILE, password)
    except Exception as e:
        print(f"Error reading encrypted file: {e}")
        return

    connections = json.loads(encrypted_data)

    if not connections:
        print("No connections available. Please call the script with the --add option to add your first connection.")
        return

    BLUE = '\033[94m'
    RESET = '\033[0m'

    connection_labels = [f'{conn["label"]} ({BLUE}{conn["username"]}{RESET})' for conn in connections]

    questions = [
        inquirer.List('selected_connection',
                      message="Select the connection to use",
                      choices=connection_labels),
    ]

    answers = inquirer.prompt(questions)
    selected_label = answers['selected_connection']

    # Trouver la connexion sélectionnée avec une gestion d'erreur
    try:
        selected_conn = next(conn for conn in connections if f'{conn["label"]} ({BLUE}{conn["username"]}{RESET})' == selected_label)
    except StopIteration:
        print(f"No connection found for the selection: {selected_label}")
        return
    
    username = selected_conn['username']
    password = selected_conn['password']
    host = selected_conn['host']

    ssh_command = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{host}"
    print(f"Connecting to {selected_label}...") 

    try:
        subprocess.check_call(ssh_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute subprocess: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

def init():
    password = getpass.getpass("Create a new encryption password: ")
    confirm_password = getpass.getpass("Confirm your encryption password: ")

    if password != confirm_password:
        print("Passwords do not match. Init aborted.")
        return

    initial_data = json.dumps([])

    encrypted_data = encrypt_data(initial_data, password)
    write_encrypted_file(CONNECTION_FILE, encrypted_data, password)

    print("Init completed successfully. File 'ssh_connections' created.")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--add':
            add_connection()
        elif sys.argv[1] == '--delete':
            delete_connection()
        elif sys.argv[1] == '--init':
            init()
        else:
            print("Invalid option. Use --add to add a connection, --delete to delete a connection, or --setup to setup the file.")
    else:
        select_connection()

