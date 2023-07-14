# driveScraper

driveScraper is a command-line tool that allows you to search and copy files with specific extensions from your computer's drives. It provides a user-friendly interface to perform the search and copy operations.

![image](https://github.com/DanielRagusa12/scrapeBot/assets/90298464/9f29295e-0f3b-40a3-b5ef-47b9ed7c614a)


## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)

## Installation

To install and run driveScraper, follow the steps below:

1. Clone the repository:

   ```powershell
   git clone https://github.com/your_username/driveScraper.git
   ```

2. Open a PowerShell session and navigate to the project directory:

   ```powershell
   cd driveScraper
   ```

3. Install the required Python packages by using the `requirements.txt` file:

   ```powershell
   pip install -r requirements.txt
   ```

   This will install all the necessary dependencies for driveScraper.

4. Alternatively, you can also run the `start.ps1` PowerShell script:

   ```powershell
   .\bin\start.ps1
   ```

   This script will handle the installation of Python and its dependencies, create a virtual environment, and install the required Python packages.

## Usage

To run the driveScraper tool, execute the following command in the PowerShell session:

```powershell
python.exe scrapeBot.py
```

The tool will present a series of prompts and options to perform the search and copy operations. Follow the on-screen instructions to provide the necessary inputs.

1. Select a drive: Choose the drive from which you want to search and copy files.

2. Select an extension: Choose the extension of the files you want to search for and copy. You can select from a predefined list or enter a custom extension.

3. Choose an option: After the search is completed, you will be presented with two options:

   - Add To Search: Restart the search process to add more extensions or search on different drives.
   - Copy Found Files: Copy the found files with the selected extension to a "scraped" folder in the project directory.

4. Exiting the program: After copying the files or if you choose to exit the program, the tool will display a message and exit.

Note: The tool will create log files in the "logs" directory to track any errors or found files during the search and copy operations.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

This project makes use of the following third-party libraries:

- [inquirer](https://github.com/magmax/python-inquirer) by magmax
- [rich](https://github.com/willmcgugan/rich) by willmcgugan
- [art](https://github.com/sepandhaghighi/art) by sepandhaghighi

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please create an issue or submit a pull request.
