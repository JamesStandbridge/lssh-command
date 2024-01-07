# SSH Connection Manager

## Introduction

The SSH Connection Manager is a Python-based command-line tool designed to manage SSH connections securely. It allows users to store, retrieve, and manage SSH connection details in an encrypted format, providing an additional layer of security for sensitive information.

## Requirements

- Python 3.x
- `cryptography` library
- `inquirer` library
- `getpass` library
- `sshpass` for non-interactive password authentication in SSH

## Installation

### Python Dependencies

First, ensure that Python 3 is installed on your system. You can download it from Python's official website.

Once Python is installed, install the required Python libraries using pip:

```bash
pip install cryptography inquirer
```

### sshpass Installation

This script uses `sshpass` for non-interactive SSH login. It's recommended to install `sshpass` from hudochenkov's repository for better security and updates. You can install `sshpass` using Homebrew:

bashCopy code

```bash
brew install hudochenkov/sshpass/sshpass
```

## Usage

To use the SSH Connection Manager, run the script with one of the following command-line arguments:

- `--add`: Add a new SSH connection.
- `--delete`: Delete an existing SSH connection.
- `--init`: Initialize the encrypted storage with a new password.
- _No argument_: Select and use a stored SSH connection.

Example:

```
python ssh_connection_manager.py --add
```

## Contributing

Contributions to the SSH Connection Manager are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT

## Author

james.standbridge.git@gmail.com
https://fr.linkedin.com/in/james-standbridge
