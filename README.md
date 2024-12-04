# WiFiWalrus - Wi-Fi Network Analysis Tool

WiFiWalrus is an intuitive Wi-Fi network analysis application designed to identify safe and reliable open Wi-Fi networks in public spaces. Optimized for Windows, it uses real Wi-Fi data for scanning. On other operating systems, it runs with simulated data.

## Features

- **Wi-Fi Network Scanning**: On Windows, leverages `netsh wlan show networks mode=Bssid` for real network data.
- **Cross-Platform Compatibility**: Functional on other OS using fake network data.
- **Network Ranking**: Analyzes networks based on security, signal strength, and SSID.
- **User-Friendly Interface**: Built using PyQt5 for smooth navigation and interaction.

## Application Screenshots

Take a look at some of the key features of WiFiWalrus in action:

### Main Interface
![WiFiWalrus Main Interface](https://github.com/IPRO497/WiFiWalrus/raw/main/assets/home_pageSS.png "Main Interface of WiFiWalrus")

### Network Ranking
![WiFiWalrus Network Ranking](https://github.com/IPRO497/WiFiWalrus/raw/main/assets/network_scannerSS.png "Network Ranking in WiFiWalrus")

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.x
- PyQt5

### Cloning the Repository

Clone the WiFiWalrus repository to your local machine using the following commands:

```bash
git clone https://github.com/MitChaudhari/WiFiWalrus.git
```

Then open the project folder
```bash
cd WiFiWalrus
```

### Installing Dependencies

WiFiWalrus requires several Python packages, all of which can be installed via pip. Run the following commands to install the necessary dependencies:

```bash
# PyQt5 for the graphical user interface
pip install PyQt5

# PyQt5 tools for additional resources
pip install pyqt5-tools

# For network scanning functionality on non-Windows systems
pip install subprocess32

# Optional: For enhanced mathematical capabilities (if not included in your Python distribution)
pip install numpy
```

### Running the Application

To start the application, run:

```bash
python main.py
```

This command launches WiFiWalrus, allowing you to scan and analyze Wi-Fi networks.

## Building the Application

Instructions on how to build WiFiWalrus into a standalone executable:

```bash
pyinstaller --windowed --onefile --noconfirm --add-data "path/to/assets;./assets" --icon "path/to/icon.ico" main.py
```

## About the Creator

WiFiWalrus was developed by Mitansh Chaudhari as part of a Cyber Security and Innovation project at IIT Chicago. This application was built with the aim of enhancing public Wi-Fi safety and user awareness.

### Contact
For any questions, concerns, or feedback regarding WiFiWalrus, please feel free to reach out:

- **Mitansh Chaudhari**
- Email: [mchaudhari1@hawk.iit.edu](mailto:mchaudhari1@hawk.iit.edu)

Your input and suggestions are greatly appreciated and will help in further improving this tool.

## License

WiFiWalrus is licensed under the MIT License. This license permits you to use, modify, and distribute the software freely, provided that the original copyright and permission notice are included with any substantial portions of the software.

For the full license text, see the [LICENSE](https://github.com/IPRO497/WiFiWalrus/blob/main/LICENSE.md) file in the GitHub repository.



