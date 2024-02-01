# PalWorld Python Server Helper

A basic Python wrapper for RCON, designed to facilitate server management for PalWorld servers. It offers preliminary support for player join/leave messages, albeit with some limitations. This tool is intended as a temporary solution until a more robust system is developed.

[img](https://www.dropbox.com/scl/fi/97usicmyf6owz5exczbxj/palhelper.png?rlkey=3w7t30q47sx7bh5zr0ovzrdy2&dl=1)

## Features

- Basic RCON command execution
- Support for player join/leave messages (with known quirks)
- Ban/kick by name

## Prerequisites

- Python 3.10 or newer installed and available in your system's PATH
    Your PalWorld server configured to accept RCON commands (RCON port open and enabled in the server's configuration)
    rcon-cli downloaded and accessible

## Installation

1. Configure Your PalWorld Server: Ensure your server is set up to accept RCON commands by configuring the RCON port and enabling it in the server settings.

2. Install Python: Verify that Python 3.10 or newer is installed on your system and that it's added to your system's PATH.

3. Set Up rcon-cli:
    - Download [rcon-cli](https://github.com/gorcon/rcon-cli) for your platform from its GitHub repository releases page.
    - Place the downloaded executable (rcon-cli.exe for Windows or the Unix executable for Linux/Mac) in the serverhelper folder. Alternatively, you can specify a custom path to the executable in the configuration file.

4. Configure the Server Helper: Fill out the provided configuration JSON file with your server's IP address, RCON port, and password.

5. Run the Server Helper BAT (Windows) or SH (Unix): With the above steps completed, the server helper should be ready to use.

## Known Issues

- Duplicate Join Messages: Join messages may trigger twice if a player's nickname differs from their Steam name. The sequence observed is the Steam name joining first, then leaving, followed by the nickname joining. Contributions to address this issue are welcome.