![image](https://github.com/phantom0004/FuzzFindr-Web-Fuzzing-Tool/assets/42916447/533350d1-c3e6-45c8-a020-1758e963a1dc)

## Overview

FuzzFindr is a robust web fuzzing tool inspired by the popular "ffuf" tool on Kali Linux. Designed to enhance web security testing, FuzzFindr allows users to meticulously fuzz web links using customizable wordlists. It stands out by providing detailed outputs and effectively handling a wide array of HTTP errors, ensuring smooth and efficient operation.

FuzzFindr is accessible to users with varying levels of technical knowledge, simplifying the setup process and enabling effective fuzzing operations. While it may not include all the advanced features of cutting-edge Linux tools, FuzzFindr covers essential functionalities, making it an invaluable resource for security professionals, students, and beginners alike.

### Key Features

- **Detailed HTML Output:** Neatly formats and displays the HTML structure of fuzzed web pages.
- **Error Handling:** Intelligently manages diverse HTTP errors to maintain continuous operation during tests.
- **Customizable Testing:** Supports extensive customization through user-defined wordlists and adjustable operational parameters.

### Usage

- **Clone this repository:** `git clone https://github.com/yourusername/FuzzFindr-Web-Fuzzing-Tool.git`
- **Navigate to files:** `cd FuzzFindr-Web-Fuzzing-Tool`
- **Install requirements:** `pip install -r requirements.txt`
- **Program launch:** `python3 fuzzfindr.py <website_link> "<wordlist_path>"`
- **Example launch:** `python3 fuzzfindr.py https://example.com "wordlist.txt"`

### Program Output Example
_Initial Setup_
![image](https://github.com/phantom0004/FuzzFindr-Web-Fuzzing-Tool/assets/42916447/27175ee5-8f0a-43c2-99ad-149a239acb72)

_Fuzzfindr Enumerating Directories (Verbose Enabled)_
![image](https://github.com/phantom0004/FuzzFindr-Web-Fuzzing-Tool/assets/42916447/aa15bd71-1c80-4c37-8fb9-130e5f54bfe8)

_Fuzzfindr Enumerating Directories (Verbose Disabled)_
![image](https://github.com/phantom0004/FuzzFindr-Web-Fuzzing-Tool/assets/42916447/00936bd2-331d-4a10-8a06-382bbde2e979)

_Fuzzfindr outputting to text file (Silent Verbose)_
![image](https://github.com/phantom0004/FuzzFindr-Web-Fuzzing-Tool/assets/42916447/8f126384-73cb-41af-8d86-8028d7e366fe)

### Current Status

FuzzFindr is actively being developed with plans to improve its performance and expand the informational output on the screen. The goal is to provide a tool that is effective, user-friendly, and adaptable to various web security testing needs.

### Getting Started

To get started with FuzzFindr, clone the repository, configure your wordlist, and begin testing your endpoints for security vulnerabilities. Detailed instructions are available in the "Usage" section.

### Contribute

FuzzFindr is open for contributions! Whether you're interested in fixing bugs, enhancing features, or improving documentation, your input is welcome.

### License

FuzzFindr is released under the MIT License, all rights reserved.
