# Yamaha K-Line Data Logger

This Python script is designed to interface with a Yamaha K-Line ECU through a USB OBD KKL Cable, providing a convenient and organized way to display, log, and manage the received bytes.

## Features:

- **Real-time Byte Display:** The script continuously reads and displays bytes received from the Yamaha K-Line ECU. Bytes are neatly organized by 4-byte, 5-byte, and 6-byte sequences for easy analysis.

- **Log File Creation:** It automatically generates separate log files for each byte sequence length (4, 5, and 6 bytes), allowing you to review the data at your convenience.

- **Device Detection:** The script scans for devices connected to the selected COM port, making it handy for identifying various USB devices, especially useful when multiple devices are connected, such as an AVR microcontroller.

- **COM Port Settings Saved:** Your selected COM port settings are saved, enabling quick and easy resumption of data logging without the need for manual configuration.

- **Pause and Resume Logging:** You can pause and resume the logging process using either Ctrl+C or the Spacebar. Additionally, the script provides a graceful exit option using the ESC key.

## Instructions for Use:

1. Connect your USB OBD KKL Cable to the Yamaha K-Line ECU.

2. Run the script and select the appropriate COM port from the list of available ports.

3. Enjoy real-time byte monitoring, organized display, and automatic log file creation.

4. Pause and resume logging with Ctrl+C or the Spacebar.

5. Exit the script gracefully using the ESC key.

**Note:** This script is particularly useful for Yamaha K-Line enthusiasts and developers who want to monitor and log data from their ECUs for analysis and tuning purposes.
