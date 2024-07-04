# Download Organizer

A Python script that automatically organizes files in the Downloads folder into appropriate directories based on their file types. Ideal for users who want to keep their Downloads folder clean and organized.

## Features

- Monitors the Downloads folder for new, modified, or moved files.
- Moves image files (`.png`, `.jpg`, `.jpeg`, `.tif`, `.gif`) to the Pictures folder.
- Moves document files (`.pdf`, `.txt`, `.doc`, `.docx`, `.docm`, `.xml`, `.csv`, `.xlsx`, `.xlsm`, `.xls`, `.pptx`, `.ppt`) to the Documents folder.
- Ignores temporary files (`.tpm`, `.crdownload`).
- Ensures files are fully written before moving them.
- Logs all operations for easy debugging and monitoring.

## Requirements

- Python 3.6+
- `watchdog` library

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/download-organizer.git
    cd download-organizer
    ```

2. **Install the required Python packages:**

    ```sh
    pip install watchdog
    ```

## Usage

1. **Run the script:**

    ```sh
    python main.py
    ```

    The script will start monitoring the Downloads folder and will automatically move files to the appropriate directories.

2. **Customizing Directories:**

    The script defaults to using the following directories:
    - Downloads folder: `~/Downloads`
    - Pictures folder: `~/Pictures`
    - Documents folder: `~/Documents`

    If you need to customize these paths, you can modify the `directory_to_watch`, `image_dir`, and `document_dir` variables in the `main.py` file.
