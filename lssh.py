#!/usr/bin/env python
import inquirer
import os
import subprocess
import json


CONNECTION_FILE = os.path.expanduser("~/.ssh_connections")

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

    with open(CONNECTION_FILE, 'a') as file:
        file.write(json.dumps(connection_info) + '\n')

def select_connection():
    if not os.path.isfile(CONNECTION_FILE):
        print("No connections available.")
        return

    connections = []
    with open(CONNECTION_FILE, 'r') as file:
        for line in file:
            try:
                connections.append(json.loads(line.strip()))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from .ssh_connections: {e}")
                continue  # Skip this line and continue with the next

    BLUE = '\033[94m'
    RESET = '\033[0m'  # Reset to default terminal color

    connection_labels = [f'{conn["label"]} ({BLUE}{conn["username"]}{RESET})' for conn in connections]

    questions = [
        inquirer.List('selected_connection',
                      message="Select the connection to use",
                      choices=connection_labels),
    ]

    answers = inquirer.prompt(questions)
    selected_label = answers['selected_connection']
    selected_conn = next(conn for conn in connections if '{} ({})'.format(conn['label'], conn['username']) == selected_label)

    username = selected_conn['username']
    password = selected_conn['password']
    host = selected_conn['host']

    ssh_command = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{host}"
    print(f"Executing command: {ssh_command}")  # Debugging line to see the command
    
    try:
        # Important: The use of sshpass with passwords is insecure, consider using SSH keys
        subprocess.check_call(ssh_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute subprocess: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--add':
        add_connection()
    else:
        select_connection()
