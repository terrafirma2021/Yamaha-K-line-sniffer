import serial.tools.list_ports
import os
import traceback
import signal  # Import the signal module
import sys
import msvcrt  # Import msvcrt for keyboard input detection on Windows
import threading

# Constants
USART_BAUDRATE_ECU = 16064
DATA_BITS = 8  # 8 data bits
SETTINGS_FILE = 'settings.txt'  # File to store the last used COM port

logging_paused = False  # Flag to track if logging is paused

# Function to create the log files if they don't exist
def create_log_files():
    for filename in ['4Byte.txt', '5Byte.txt', '6Byte.txt']:
        if not os.path.exists(filename):
            with open(filename, 'w'):
                pass

# Function to scan for available COM ports and their descriptions
def scan_com_ports():
    available_ports = list(serial.tools.list_ports.comports())
    return available_ports

# Function to select a COM port
def select_com_port(available_ports):
    print("Available COM ports:")
    for i, port_info in enumerate(available_ports, start=1):
        print(f"{i}. {port_info.device} ({port_info.description})")
    
    while True:
        try:
            choice = int(input("Select a COM port number (1, 2, etc.): "))
            if 1 <= choice <= len(available_ports):
                selected_port = available_ports[choice - 1].device
                return selected_port
            else:
                print("Invalid choice. Please select a valid COM port number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to save the last used COM port to a settings file
def save_last_com_port(com_port):
    with open(SETTINGS_FILE, 'w') as settings_file:
        settings_file.write(com_port)

# Function to load the last used COM port from the settings file
def load_last_com_port():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as settings_file:
            return settings_file.read().strip()
    return None

# Function to handle keyboard input and pause logging
def handle_keyboard_input():
    global logging_paused
    while True:
        key = msvcrt.getch().decode().lower()
        if key == '\x03' or key == ' ':  # Ctrl+C or Spacebar
            logging_paused = not logging_paused
            if logging_paused:
                print("\nLogging paused. Press Spacebar to continue or ESC to quit.")
            else:
                print("\nLogging resumed.")
        elif key == '\x1b':  # ESC
            print("Script ended. Scroll up to view.")
            os._exit(0)  # Terminate the script completely

# Function to receive and log bytes
def receive_and_log(com_port):
    frame_data_4 = []  # Initialize a list to store 4-byte data for a single frame
    frame_data_5 = []  # Initialize a list to store 5-byte data for a single frame
    frame_data_6 = []  # Initialize a list to store 6-byte data for a single frame
    frame_4 = ""  # Initialize frame_4 outside the loop
    frame_5 = ""  # Initialize frame_5 outside the loop
    frame_6 = ""  # Initialize frame_6 outside the loop
    
    try:
        ser = serial.Serial(com_port, baudrate=USART_BAUDRATE_ECU, bytesize=DATA_BITS)
    except serial.SerialException:
        print(f"COM port '{com_port}' not found. Please check your connections and select a valid COM port.")
        return
    
    try:
        while True:
            # Check if logging is paused
            if not logging_paused:
                # Read a byte from the COM port
                try:
                    data_byte = ser.read(1)
                except serial.SerialException:
                    traceback.print_exc()
                    print("An error occurred while reading from the COM port. The script will continue running.")
                    continue

                # Check if the received byte is not empty
                if data_byte:
                    hex_value = data_byte.hex()

                    frame_data_4.append(hex_value)
                    frame_data_5.append(hex_value)
                    frame_data_6.append(hex_value)  # Add the byte to all three lists

                    # If a complete frame is received (4 bytes), log it to 4Byte.txt
                    if len(frame_data_4) == 4:
                        frame_4 = " ".join(frame_data_4)  # Combine the hex values
                        with open('4Byte.txt', 'a') as four_byte_file:
                            four_byte_file.write(frame_4 + '\n')
                        frame_data_4 = []  # Clear the data for the next frame

                    # If a complete frame is received (5 bytes), log it to 5Byte.txt
                    if len(frame_data_5) == 5:
                        frame_5 = " ".join(frame_data_5)  # Combine the hex values
                        with open('5Byte.txt', 'a') as five_byte_file:
                            five_byte_file.write(frame_5 + '\n')
                        frame_data_5 = []  # Clear the data for the next frame

                    # If a complete frame is received (6 bytes), log it to 6Byte.txt
                    if len(frame_data_6) == 6:
                        frame_6 = " ".join(frame_data_6)  # Combine the hex values
                        with open('6Byte.txt', 'a') as six_byte_file:
                            six_byte_file.write(frame_6 + '\n')
                        frame_data_6 = []  # Clear the data for the next frame

                    # Display 4-byte, 5-byte, and 6-byte representations in the terminal with reduced spacing and '|' encasing them
                    formatted_output = f"|{frame_4}|{' ' * 10}|{frame_5}|{' ' * 10}|{frame_6}|"
                    print(formatted_output)
    except KeyboardInterrupt:  # Catch Ctrl+C
        print("Exiting gracefully...")
        ser.close()

# Main script
create_log_files()  # Create log files if they don't exist

last_com_port = load_last_com_port()

if last_com_port:
    print(f"Last used COM port: {last_com_port}")

if last_com_port:
    com_port = last_com_port
else:
    available_ports = scan_com_ports()
    if available_ports:
        com_port = select_com_port(available_ports)
        if com_port:
            save_last_com_port(com_port)
    else:
        print("No COM ports found. Please make sure your device is connected.")

if com_port:
    print("Press Ctrl+C or Spacebar to pause logging.")
    threading.Thread(target=handle_keyboard_input).start()  # Start handling keyboard input in a separate thread
    receive_and_log(com_port)  # Start receiving and logging data
