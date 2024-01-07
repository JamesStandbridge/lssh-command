# LSSH - SSH Connection Manager

LSSH is a Python-based SSH connection manager that allows users to easily store, manage, and connect to various SSH sessions.

## Features

- Store SSH connection details (username, password, host, and custom label).
- Interactive interface to select and initiate an SSH connection.
- Secure password handling via terminal prompts.
- Easy addition of new SSH connections.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a working Python 3 installation.
- `inquirer` Python package is installed. Install it using `pip install inquirer`.
- `sshpass` is installed if you plan to use password-based authentication (not recommended for security reasons).

```bash
pip install inquirer
brew install hudochenkov/sshpass/sshpass
```

## Installation

LSSH can be cloned and run directly from the repository:

```bash
git clone https://github.com/yourusername/lssh.git
cd lssh
./lssh.py
```

## Usage

To use LSSH, run:

`./lssh.py`

To add a new SSH connection, run:

`./lssh.py --add`

Follow the interactive prompts to enter the connection details.
