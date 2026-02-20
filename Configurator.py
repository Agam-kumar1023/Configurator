import socket
import json
import os
from tkinter import Tk, filedialog
from colorama import Fore, Style, init
import time

# Initialize colorama
init()

# === Constants ===
SELECTIONS = {
    1: "Divert-X: Set Parameter - Single",
    2: "Divert-X: Set Parameters - All",
    3: "Divert-X: Check Parameter - Single",
    4: "Divert-X: Check Parameters - All",
    5: "Divert-X: Health Check",
    6: "Divert-X: Set Motor Parameter - Single",
    7: "Divert-X: Set Motor Parameters - All",
    8: "Divert-X: Check Motor Parameter - Single",
    9: "Divert-X: Check Motor Parameters - All",
    10: "Divert-X: Motor Health Check",
    11: "Conveyor Card: Set Parameter - Single",
    12: "Conveyor Card: Set Parameters - All",
    13: "Conveyor Card: Check Parameter - Single",
    14: "Conveyor Card: Check Parameters - All",
    15: "Conveyor Card: Health Check",
    16: "Configure Divert-X using Config File",
    17: "Exit",
    18: "Configure Motor Parameters using Config File"
}

SELECTION_SET_SINGLE_PARAM      = 1
SELECTION_SET_ALL_PARAM         = 2
SELECTION_CHECK_SINGLE_PARAM    = 3
SELECTION_CHECK_ALL_PARAM       = 4
SELECTION_SET_DIVERT_X_HEALTH_CHECK = 5
SELECTION_SET_DIVERT_X_MOTOR_PARAM_SINGLE   = 6
SELECTION_SET_DIVERT_X_MOTOR_PARAM_ALL      = 7
SELECTION_CHECK_DIVERT_X_MOTOR_PARAM_SINGLE = 8
SELECTION_CHECK_DIVERT_X_MOTOR_PARAM_ALL    = 9
SELECTION_SET_DIVERT_X_MOTOR_HEALTH_CHECK   = 10
SELECTION_SET_CONVEYOR_CARD_PARAM_SINGLE   = 11
SELECTION_SET_CONVEYOR_CARD_PARAM_ALL      = 12
SELECTION_CHECK_CONVEYOR_CARD_PARAM_SINGLE = 13
SELECTION_CHECK_CONVEYOR_CARD_PARAM_ALL    = 14
SELECTION_CONVEYOR_CARD_HEALTH_CHECK = 15
SELECTION_CONFIGURE_WITH_FILE = 16
SELECTION_EXIT                  = 17
SELECTION_CONFIGURE_MOTOR_WITH_FILE = 18

CMD_TYPE_CHECK_CONFIG	        = 0x04
CMD_TYPE_SET_CONFIG		        = 0x08
CMD_TYPE_POP_UP_MOTOR_CONTROL	= 0x09
CMD_TYPE_SET_POP_UP_CONFIG		= 0x0A
CMD_TYPE_CHECK_POP_UP_CONFIG	= 0x0B
CMD_TYPE_HEALTH_CHECK			= 0x0C
CMD_TYPE_OUTPUT_PIN_CHECK		= 0x0D

CMD_TYPE_CHECK_PARAM_RESPONSE	= 0x81

CMD_CAN_IN_OUT_CONFIG			= 0x01
CMD_TOTE_DEFAULT_OUT_CONFIG		= 0x02
CMD_WCS_RETRY_COUNTS_CONFIG		= 0x03
CMD_CONVEYOR_MODE_CONFIG		= 0x04
CMD_S1_CAN_ID_CONFIG		    = 0x05
CMD_S2_CAN_ID_CONFIG	        = 0x06
CMD_S3_CAN_ID_CONFIG		    = 0x07
CMD_S4_CAN_ID_CONFIG		    = 0x08
CMD_DIVERT_X_MOTOR_CONTROL_CAN_ID_CONFIG		= 0x09

CMD_BARCODE_1_PORT_CONFIG		= 0x0A
CMD_BARCODE_2_PORT_CONFIG		= 0x0B
CMD_BARCODE_3_PORT_CONFIG		= 0x0C
CMD_BARCODE_4_PORT_CONFIG		= 0x0D
CMD_PARALLEL_TRANSFER_CONFIG	= 0x0E
CMD_TOTE_REJECTION_FLOW_CONFIG	= 0x0F
CMD_URL_CONFIG					= 0x10
CMD_DIVERT_X_IP_CONFIG			= 0x11
CMD_DIVERT_X_SUBNET_CONFIG		= 0x12
CMD_DIVERT_X_GATEWAY_CONFIG		= 0x13
CMD_DEST_IP_CONFIG				= 0x14
CMD_DEST_PORT_CONFIG			= 0x15
CMD_ETH_MASTER_CONFIG			= 0x16
CMD_RESET_POP_UP				= 0x17
CMD_S1_CAN_GATEWAY			    = 0x18
CMD_S2_CAN_GATEWAY			    = 0x19
CMD_S3_CAN_GATEWAY				= 0x1A
CMD_S4_CAN_GATEWAY			    = 0x1B
CMD_DIVERT_X_MOTOR_CONTROL_GATEWAY			= 0x1C
CMD_BARCODE_1_GATEWAY			= 0x1D
CMD_BARCODE_2_GATEWAY			= 0x1E
CMD_BARCODE_3_GATEWAY			= 0x1F
CMD_BARCODE_4_GATEWAY			= 0x20
CMD_POP_TYPE_CONFIG				= 0x21
CMD_DEBUG_MODE_CONFIG			= 0x22
CMD_DEBUG_DEVICE_IP_CONFIG				= 0x23
CMD_DEBUG_DEVICE_PORT_CONFIG			= 0x24
CMD_S1_REVERSE_CMD				= 0x25
CMD_S2_REVERSE_CMD			    = 0x26
CMD_S3_REVERSE_CMD				= 0x27
CMD_S4_REVERSE_CMD			    = 0x28
CMD_S1_SLUG_FREE_DELAY_TIME		= 0x29
CMD_S2_SLUG_FREE_DELAY_TIME		= 0x2A
CMD_S3_SLUG_FREE_DELAY_TIME		= 0x2B
CMD_S4_SLUG_FREE_DELAY_TIME		= 0x2C
CMD_TOTE_RETRY_TIME			    = 0x2D
CMD_S1_TOTE_CENTRE_TIMEOUT	    = 0x2E
CMD_S2_TOTE_CENTRE_TIMEOUT	    = 0x2F
CMD_S3_TOTE_CENTRE_TIMEOUT	    = 0x30
CMD_S4_TOTE_CENTRE_TIMEOUT	    = 0x31
CMD_STORE_PARAMETER					= 0x32
CMD_PLC_LOAD_PRESENCE_FEEDBACK_UPDATE_TIME		= 0x33
CMD_ENABLE_TOTE_TRACKING				= 0x38
CMD_SET_MQTT_BROKER_IP					= 0x37
CMD_SET_MQTT_BROKER_PORT				= 0x39
CMD_SET_REQUEST_TOPIC					= 0x3A
CMD_SET_RESPONSE_TOPIC					= 0x3B

RESP_TYPE_POP_CHECK_RESPONSE	= 0x8A
RESP_TYPE_HEALTH_CHECK			= 0x8B
RESP_TYPE_POP_UP_ERROR_GENERATION	= 0x8C
RESP_POP_UP_ANY_ERROR			= 0x01
RESP_POP_UP_CRATE_JAM_ERROR		= 0x02
CMD_SET_BOOT_MODE				= 0x65
CMD_CHECK_DIVERT_X_ERROR        = 0x01


# === Tri-Motor Variables ===
CMD_MOTOR_RPM					= 0x01
CMD_MOTOR_ACCELERATION			= 0x02
CMD_MOTOR_DECELERATION			= 0x03
CMD_MOTOR_DIRECTION				= 0x04
CMD_TOTAL_CARDS					= 0x05
CMD_CONVEYOR_MODE				= 0x06
CMD_STOP_TIME					= 0x07
CMD_EMPTY_STOP_TIME				= 0x08
CMD_ERROR_DESTINATION_ADDRESS	= 0x09
CMD_UNIQUE_ADDRESS				= 0x0A
CMD_ADDRESSING_MODE				= 0x0B
CMD_RESET_DEVICE				= 0x0C
CMD_MOTOR_OC					= 0x0D
CMD_DEBUG_MODE					= 0x0F
CMD_MOTOR_SUDDEN_STOP			= 0x10
CMD_MOTOR_UV					= 0x11
CMD_MOTOR_OV					= 0x12
CMD_CRATE_JAM_TIME				= 0x13
CMD_MOTOR_TICKS					= 0x14
CMD_MERGE_MODE					= 0x15
CMD_GRAVITY_MODE				= 0x16
CMD_RETRY_TIME					= 0x17
CMD_SLUG_CRATE_JAM_TICKS		= 0x18
CMD_SLUG_NEAR_BOX_TICKS			= 0x19
CMD_BOX_PASS_TIME_THRESHOLD		= 0x1A
CMD_CURRENT_PRINT				= 0x1B
CMD_VOLTAGE_PRINT				= 0x1C
CMD_RPM_PRINT					= 0x1D
CMD_CROSSOVER_MODE				= 0x1E
CMD_REVERSE_MODE				= 0x1F
CMD_SENSOR_MODE					= 0x20
CMD_STORE_PARAMS				= 0x21
CMD_LOG							= 0x22
CMD_MODBUS_MODE					= 0x23
CMD_FW_VERSION					= 0x24

# === Command Types Conveyor Card===
CMD_SET_RPM                         = 0x01
CMD_SET_ACCELERATION                = 0x02
CMD_SET_DECELERATION                = 0x03
CMD_SET_MOTOR_DIRECTION             = 0x04
CMD_SET_TOTAL_CARDS                 = 0x05
CMD_SET_CONVEYOR_MODE               = 0x06
CMD_SET_STOP_TIME                   = 0x07
CMD_SET_EMPTY_STOP_TIME             = 0x08
CMD_SET_ERROR_DESTINATION_ADDRESS   = 0x09
CMD_SET_UNIQUE_ID                   = 0x0A
CMD_SET_ADDRESSING_MODE             = 0x0B
CMD_RESET_DEVICE                    = 0x0C
CMD_SET_MOTOR_ON_TH                 = 0x0D
CMD_SET_MOTOR_OFF_TH                = 0x0E
CMD_SET_DEBUG_MODE                  = 0x0F
CMD_SET_SUDDEN_STOP                 = 0x10
CMD_SET_LOW_VOLTAGE_TH              = 0x11
CMD_SET_HIGH_VOLTAGE_TH             = 0x12
CMD_SET_CRATE_JAM_TIME              = 0x13
CMD_SET_MOTOR_TICKS_TH              = 0x14
CMD_SET_MERGER_MODE                 = 0x15
CMD_SET_GRAVITY_MODE                = 0x16
CMD_SET_CAN_RETRY_TIME              = 0x17
CMD_SET_SLUG_CRATE_JAM_TICKS        = 0x18
CMD_SET_SLUG_NEAR_BOX_TICKS         = 0x19
CMD_SET_BOX_PASS_TIME_TH            = 0x1A
CMD_SET_CURRENT_PRINT               = 0x1B
CMD_SET_VOLTAGE_PRINT               = 0x1C
CMD_SET_RPM_PRINT                   = 0x1D
CMD_SET_CROSSOVER_MODE              = 0x1E
CMD_SET_REVERSE_MODE                = 0x1F
CMD_SET_SENSOR_MODE                 = 0x20
CMD_SET_STORE_PARAMETERS            = 0x21
CMD_SET_LOG_LEVEL                   = 0x22
CMD_SET_MODBUS_MODE                 = 0x23
CMD_SET_BAUDRATE                    = 0x24
CMD_SET_PLC_MOTOR_CONTROL_STOP_TIME = 0x25
CMD_SET_DELAY_SLUG_FREE_TIME        = 0x26
CMD_SET_ERROR_SIGNAL_MODE           = 0x27
CMD_SET_RESET_SIGNAL_MODE           = 0x28
CMD_CAN_ADDRESS_COUNTER             = 0x29

CMD_CHECK_RPM                         = 0x01
CMD_CHECK_ACCELERATION                = 0x02
CMD_CHECK_DECELERATION                = 0x03
CMD_CHECK_MOTOR_DIRECTION             = 0x04
CMD_CHECK_TOTAL_CARDS                 = 0x05
CMD_CHECK_CONVEYOR_MODE               = 0x06
CMD_CHECK_STOP_TIME                   = 0x07
CMD_CHECK_EMPTY_STOP_TIME             = 0x08
CMD_CHECK_ERROR_DESTINATION_ADDRESS   = 0x09
CMD_CHECK_MOTOR_ON_TH                 = 0x0A
CMD_CHECK_MOTOR_OFF_TH                = 0x0B
CMD_CHECK_DEBUG_MODE                  = 0x0C
CMD_CHECK_SUDDEN_STOP                 = 0x0D
CMD_CHECK_LOW_VOLTAGE_TH              = 0x0E
CMD_CHECK_HIGH_VOLTAGE_TH             = 0x0F
CMD_CHECK_CRATE_JAM_TIME              = 0x10
CMD_CHECK_MOTOR_TICKS_TH              = 0x11
CMD_CHECK_MERGER_MODE                 = 0x12
CMD_CHECK_GRAVITY_MODE                = 0x13
CMD_CHECK_CAN_RETRY_TIME              = 0x14
CMD_CHECK_SLUG_CRATE_JAM_TICKS        = 0x15
CMD_CHECK_SLUG_NEAR_BOX_TICKS         = 0x16
CMD_CHECK_BOX_PASS_TIME_TH            = 0x17
CMD_CHECK_CROSSOVER_MODE              = 0x18
CMD_CHECK_REVERSE_MODE                = 0x19
CMD_CHECK_SENSOR_MODE                 = 0x1A
CMD_CHECK_STORE_PARAMETERS            = 0x1B
CMD_CHECK_FIRMWARE_VERSION            = 0x1C
CMD_CHECK_LOG_LEVEL                   = 0x1E
CMD_CHECK_MODBUS_MODE                 = 0x1F
CMD_CHECK_BAUDRATE                    = 0x20
CMD_CHECK_PLC_MOTOR_CONTROL_STOP_TIME = 0x21
CMD_CHECK_DELAY_SLUG_FREE_TIME        = 0x22
CMD_CHECK_ERROR_SIGNAL_MODE           = 0x23
CMD_CHECK_RESET_SIGNAL_MODE           = 0x24

# === Functions ===

def connect_to_server(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        print(f"[✓] Connected to {ip}:{port}")
        return sock
    except Exception as e:
        print(f"[x] Connection error: {e}")
        return None

def send_can_command(sock, command):
    try:
        # print("command : ", command)
        json_data = json.dumps({"SYSTEM_CODE": command})
        sock.sendall(json_data.encode("utf-8") + b'\n')
    except Exception as e:
        print(Fore.RED + f"[x] Sending error: {e}" + Style.RESET_ALL)

# def send_can_command(sock, command):
#     try:
#         json_data = json.dumps({"SYSTEM_CODE": command})
#         sock.sendall(json_data.encode("utf-8") + b'\n')
#     except Exception as e:
#         print(f"[x] Sending error: {e}")

def display_msg_in_out_config(selection_type):
    messages = {
        SELECTION_SET_SINGLE_PARAM: "Set In/Out",
        SELECTION_CHECK_SINGLE_PARAM: "Check In/Out"
    }
    return messages.get(selection_type, "Unknown selection")

def get_validated_input(prompt, valid_range=None, input_type=int):
    """
    Prompts the user for input and validates it.

    Args:
        prompt (str): The input prompt.
        valid_range (list, optional): A list of valid values. Defaults to None.
        input_type (type, optional): The expected input type. Defaults to int.

    Returns:
        input_type: The validated input, or None if invalid.
    """
    while True:
        try:
            value = input_type(input(prompt).strip())
            if valid_range and value not in valid_range:
                print(f"[x] Invalid input! Must be one of {valid_range}.")
                continue
            return value
        except ValueError:
            print("[x] Invalid input! Must be a valid value.")

def get_in_out_params():
    try:
        print("\n[?] Enter In/Out values for S1 to S4 (0: None, 1: Out, 2: In)")
        params = [get_validated_input(f"S{i+1}: ", valid_range=[0, 1, 2]) for i in range(4)]
        return params
    except Exception as e:
        print(f"[x] Unexpected error: {e}")
        return None
    
def get_tote_flow_params():
    """
    Prompts the user to enter tote flow values for S1 to S4 and validates the input.

    Returns:
        list: A list of integers representing the tote flow values for S1 to S4.
        None: If the input is invalid.
    """
    try:
        print("\n[?] Enter tote flow values for S1 to S4 (0: WCS, 1: Straight, 2: Left, 3: Right, 4: I/O)")
        params = [get_validated_input(f"S{i+1}: ", valid_range=[0, 1, 2, 3, 4]) for i in range(4)]
        return params
    except Exception as e:
        print(f"[x] Unexpected error: {e}")
        return None
    
def get_network_params():
    """
    Prompts the user to enter an IP address and validates it.

    Returns:
        list: A list of integers representing the IP address (e.g., [192, 168, 0, 1]).
        None: If the input is invalid.
    """
    try:
        ip_address = input("Enter: ").strip()
        ip_parts = ip_address.split(".")
        
        # Validate the IP address
        if len(ip_parts) == 4:
            ip_parts = [int(part) for part in ip_parts]  # Convert all parts to integers
            if all(0 <= part <= 255 for part in ip_parts):  # Check if all parts are in range
                return ip_parts
        print("[x] Invalid input! Must be a valid IPv4 address.")
        return None
    except ValueError:
        print("[x] Invalid input! Must be a valid IPv4 address.")
        return None

def get_ethernet_retry_time_param():
    try:
        print("\n[?] Enter value for ethernet retry count:")
        retry_time = int(input("Enter ethernet retry count: ").strip())
        return retry_time
    except ValueError:
        print("[x] Invalid input! Must be a valid integer.")
        return None
    
def get_parallel_transfer_params():
    """
    Prompts the user to enter parallel transfer values for S1 to S4 and validates the input.

    Returns:
        list: A list of integers representing the parallel transfer values for S1 to S4.
        None: If the input is invalid.
    """
    try:
        print("\n[?] Enter parallel transfer values for S1 to S4 (0: Disable, 1: Enable)")
        params = []
        for i in range(4):
            while True:
                try:
                    value = int(input(f"S{i+1}: ").strip())
                    if value in [0, 1]:  # Validate input is either 0 or 1
                        params.append(value)
                        break
                    else:
                        print("[x] Invalid input! Must be 0 (Disable) or 1 (Enable).")
                except ValueError:
                    print("[x] Invalid input! Must be an integer.")
        return params
    except Exception as e:
        print(f"[x] Unexpected error: {e}")
        return None

def generate_command_with_flexibility(conveyor_side, card_id, param, cmd_type, decesion_type):
    """
    Generates a command string that can handle both a single parameter, a list of parameters, or a string.

    Args:
        param (int, str, or list): A single parameter (int/str), a list of parameters, or a string.
        cmd_type (int): The command type.

    Returns:
        str: The generated command string.
    """
    prefix = f"{conveyor_side:02X}{card_id:02X}{decesion_type:02X}{cmd_type:02X}"

    if (decesion_type == CMD_TYPE_CHECK_POP_UP_CONFIG) or (decesion_type == CMD_TYPE_CHECK_CONFIG) or (decesion_type == CMD_TYPE_HEALTH_CHECK):
        return prefix
    else:
        try:
            if isinstance(param, list):
                if not param:  # Check for empty list
                    print("[x] Error: Parameter list is empty.")
                    return None
                param = [int(val) for val in param]  # Ensure all elements are integers
                special_cmd_types = {
                    CMD_CAN_IN_OUT_CONFIG,
                    CMD_TOTE_DEFAULT_OUT_CONFIG,
                    CMD_PARALLEL_TRANSFER_CONFIG,
                    CMD_TOTE_REJECTION_FLOW_CONFIG,
                }

                if cmd_type in special_cmd_types:
                    return f"{prefix}{''.join(f'{val:01X}' for val in param)}"
                else:
                    return f"{prefix}{''.join(f'{val:02X}' for val in param)}"
            elif isinstance(param, str):
                return f"{prefix}{param}"  # Append the string directly
            else:
                param = int(param)

                if (decesion_type == CMD_TYPE_SET_CONFIG and (conveyor_side >=1 and conveyor_side <= 4)):
                    special_cmd_types = {
                        CMD_SET_MOTOR_DIRECTION,
                        CMD_SET_TOTAL_CARDS,
                        CMD_SET_CONVEYOR_MODE,
                        CMD_SET_ERROR_DESTINATION_ADDRESS,
                        CMD_SET_UNIQUE_ID,
                        CMD_SET_ADDRESSING_MODE,
                        CMD_RESET_DEVICE,
                         CMD_SET_MERGER_MODE,
                        CMD_SET_GRAVITY_MODE,
                        CMD_SET_SLUG_NEAR_BOX_TICKS,
                        CMD_SET_CURRENT_PRINT,
                        CMD_SET_VOLTAGE_PRINT,
                        CMD_SET_RPM_PRINT,
                        CMD_SET_CROSSOVER_MODE,
                        CMD_SET_REVERSE_MODE,
                        CMD_SET_SENSOR_MODE,
                        CMD_SET_STORE_PARAMETERS,
                        CMD_SET_LOG_LEVEL,
                        CMD_SET_MODBUS_MODE,
                        CMD_SET_BAUDRATE,
                        CMD_SET_ERROR_SIGNAL_MODE,
                        CMD_SET_RESET_SIGNAL_MODE,
                        CMD_CAN_ADDRESS_COUNTER
                    }

                    if cmd_type in special_cmd_types:
                        return f"{prefix}{param:02X}"
                    else:
                        return f"{prefix}{param:04X}"    
                else: 
                    return f"{prefix}{param:04X}"
        except ValueError:
            print("[x] Error: param contains non-integer or invalid values.")
            return None

def parse_system_code(system_code):
    if len(system_code) < 12:
        print("[x] SYSTEM_CODE is too short to parse.")
        return

    prefix = system_code[0:4]  # Bytes 1–4
    conveyor_side = int(system_code[0:2], 16)  # Bytes 1–2
    response_type = system_code[4:6].upper()  # Bytes 5–6
    command_type = str(int(system_code[6:8].upper(), 16))  # Bytes 7–8 (convert to uppercase)
    additional_data = system_code[8:]  # Bytes 9 onward

    if response_type == f"{RESP_TYPE_POP_CHECK_RESPONSE:02X}":
        # Interpret command type
        command_types = {
            "1": "In/Out",
            "2": "Tote Flow",
            "3": "Ethernet Retry Count",
            "4": "Conveyor Mode",
            "5": "S1 CAN ID",
            "6": "S2 CAN ID",
            "7": "S3 CAN ID",
            "8": "S4 CAN ID",
            "9": "Divert-X Motor Control CAN ID",
            "10": "Barcode 1 Port",
            "11": "Barcode 2 Port",
            "12": "Barcode 3 Port",
            "13": "Barcode 4 Port",
            "14": "Parallel Transfer",
            "15": "Tote Rejection Flow",
            "16": "URL",
            "17": "Divert-X IP",
            "18": "Divert-X Subnet",
            "19": "Divert-X Gateway",
            "20": "Destination IP",
            "21": "Destination Port",
            "22": "Ethernet Master",
            "23": "Reset Pop-Up",
            "24": "S1 CAN Gateway",
            "25": "S2 CAN Gateway",
            "26": "S3 CAN Gateway",
            "27": "S4 CAN Gateway",
            "28": "Divert-X Motor Control Gateway",
            "29": "Barcode 1 Gateway",
            "30": "Barcode 2 Gateway",
            "31": "Barcode 3 Gateway",
            "32": "Barcode 4 Gateway",
            "33": "Pop-Up Type",
            "34": "Debug Mode",
            "35": "Debug Device IP",
            "36": "Debug Device Port",
            "37": "S1 Reverse Command",
            "38": "S2 Reverse Command",
            "39": "S3 Reverse Command",
            "40": "S4 Reverse Command",
            "41": "S1 Slug Free Delay Time",
            "42": "S2 Slug Free Delay Time",
            "43": "S3 Slug Free Delay Time",
            "44": "S4 Slug Free Delay Time",
            "45": "Tote Retry Time",
            "46": "S1 Tote Centre Timeout",
            "47": "S2 Tote Centre Timeout",
            "48": "S3 Tote Centre Timeout",
            "49": "S4 Tote Centre Timeout",
            "50": "Store Parameter",
            "51": "PLC Load Presence Feedback Update Time",
            "55": "Set MQTT Broker IP",
            "56": "Enable Tote Tracking",
            "57": "Set MQTT Broker Port",
            "58": "Set Request Topic",
            "59": "Set Response Topic",
        }

        # Interpret additional data
        if command_type == "1":  # In/Out
            config_map = {"0": "None", "1": "Out", "2": "In"}
            for i, char in enumerate(additional_data):
                print(f"{command_types.get(command_type, 'Unknown')} for S{i + 1}: {config_map.get(char, 'Unknown')}")
        elif command_type == "2":  # Tote Flow
            flow_map = {"0": "WCS", "1": "Straight", "2": "Left", "3": "Right", "4": "I/O"}
            for i, char in enumerate(additional_data):
                print(f"{command_types.get(command_type, 'Unknown')} for S{i + 1}: {flow_map.get(char, 'Unknown')}")
        elif command_type == "3":  # Ethernet Retry Count
            print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data, 16)}")
        elif command_type == "4":  # Conveyor Mode
            mode_map = {"1": "Singulated", "2": "Slug", "3": "Disable"}
            print(f"{command_types.get(command_type, 'Unknown')}: {mode_map.get(str(int(additional_data, 16)), 'Unknown')}")
        elif command_type in ["5", "6", "7", "8", "9"]:  # S1-S5 CAN ID
            print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data, 16)}")
        elif command_type in ["10", "11", "12", "13"]:  # Barcode Ports
            print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data, 16)}")
        elif command_type == "14":  # Parallel Transfer
            transfer_map = {"0": "Disable", "1": "Enable"}
            for i, char in enumerate(additional_data):
                print(f"{command_types.get(command_type, 'Unknown')}: {transfer_map.get(char, 'Unknown')}")
        elif command_type == "15":  # Tote Rejection Flow
            flow_map = {"0": "WCS", "1": "Straight", "2": "Left", "3": "Right", "4": "I/O"}
            for i, char in enumerate(additional_data):
                print(f"{command_types.get(command_type, 'Unknown')}: {flow_map.get(char, 'Unknown')}")
        elif command_type == "16":  # URL
            print(f"URL: {additional_data}")
        elif command_type in ["17", "18", "19", "20", "35"]:  # IP/Subnet/Gateway/Destination IP/Debug Device IP
            ip_parts = [str(int(additional_data[i:i+2], 16)) for i in range(0, len(additional_data), 2)]
            print(f"{command_types.get(command_type)}: {'.'.join(ip_parts)}")
        elif command_type == "21":  # Destination Port
            print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data, 16)}")
        elif command_type == "22":  # Ethernet Master
            master_map = {"0": "No Master", "1": "WCS", "2": "PLC"}
            print(f"{command_types.get(command_type, 'Unknown')}: {master_map.get(str(int(additional_data, 16)), 'Unknown')}")
        elif command_type in ["24", "25", "26", "27"]:  # S1-S4 CAN Gateway
            print(f"{command_types.get(command_type, 'Unknown')}: {'Enable' if additional_data == '01' else 'Disable'}")
        elif command_type in ["28", "29", "30", "31", "32"]:  # Barcode Gateways
            print(f"{command_types.get(command_type, 'Unknown')}: {'Enable' if additional_data == '01' else 'Disable'}")
        elif command_type == "33":  # Pop-Up Type
            popup_map = {"1": "Ninety Degree", "2": "Diverter Left", "3": "Diverter Right", "4": "Gateway"}
            print(f"{command_types.get(command_type, 'Unknown')}: {popup_map.get(str(int(additional_data, 16)), 'Unknown')}")
        elif command_type == "34":  # Debug Mode
            debug_map = {"0": "Disable", "1": "UART", "3": "Ethernet"}
            print(f"{command_types.get(command_type, 'Unknown')}: {debug_map.get(str(int(additional_data, 16)), 'Unknown')}")
        elif command_type == "36":  # Debug Device Port
            print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data, 16)}")
        elif command_type in ["37", "38", "39", "40"]:  # S1-S4 Reverse Command
            print(f"{command_types.get(command_type, 'Unknown')}: {'Enable' if additional_data == '01' else 'Disable'}")
        elif command_type in ["41", "42", "43", "44"]:  # S1-S4 Slug Free Delay Time
            print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data, 16)} ms")
        elif command_type == "45":  # Tote Retry Time
            print(f"Tote Retry Time: {int(additional_data, 16)} ms")
        elif command_type in ["46", "47", "48", "49"]:  # S1-S4 Tote Centre Timeout
            print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data, 16)} ms")
        elif command_type == "50":  # Store Parameter
            print(f"{command_types.get(command_type, 'Unknown')}: {'Stored' if additional_data == '01' else 'Not Stored'}")
        elif command_type == "51":  # PLC Load Presence Feedback Update Time
            print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data, 16)} ms")
        elif command_type == "55":  # Set MQTT Broker IP
            ip_parts = [str(int(additional_data[i:i+2], 16)) for i in range(0, len(additional_data), 2)]
            print(f"{command_types.get(command_type)}: {'.'.join(ip_parts)}")
        elif command_type == "56":  # Enable Tote Tracking
            tracking_map = {"0": "Disable", "1": "CAN", "2": "Ethernet"}
            print(f"{command_types.get(command_type, 'Unknown')}: {tracking_map.get(str(int(additional_data, 16)), 'Unknown')}")
        elif command_type == "57":  # Set MQTT Broker Port
            print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data, 16)}")
        elif command_type == "58":  # Set Request Topic
            print(f"{command_types.get(command_type, 'Unknown')}: {additional_data}")
        elif command_type == "59":  # Set Response Topic
            print(f"{command_types.get(command_type, 'Unknown')}: {additional_data}")
        else:
            print(f"[x] Unknown command type: {command_type}")
    elif response_type == f"{CMD_TYPE_CHECK_PARAM_RESPONSE:02X}":
        # Interpret command type
        if (conveyor_side == 5):
            command_types = {
                str(CMD_MOTOR_RPM): "Motor RPM",
                str(CMD_MOTOR_ACCELERATION): "Acceleration",
                str(CMD_MOTOR_DECELERATION): "Deceleration",
                str(CMD_STOP_TIME): "Stop Time",
                str(CMD_EMPTY_STOP_TIME): "Empty Stop Time",
                str(CMD_MOTOR_OC): "Motor Overcurrent",
                str(CMD_MOTOR_SUDDEN_STOP): "Motor Sudden Stop",
                str(CMD_MOTOR_UV): "Motor Undervoltage",
                str(CMD_MOTOR_OV): "Motor Overvoltage",
                str(CMD_MOTOR_TICKS): "Motor Ticks",
                str(CMD_STORE_PARAMS): "Store Parameters",        
            }

            if command_type in command_types:
                print(f"{command_types[command_type]}: {int(additional_data, 16)}")
            else:
                print(f"[x] Unknown command type in response: {command_type}")
        else:
            command_types = {
                str(CMD_CHECK_RPM): "Motor RPM",
                str(CMD_CHECK_ACCELERATION): "Acceleration",
                str(CMD_CHECK_DECELERATION): "Deceleration",
                str(CMD_CHECK_MOTOR_DIRECTION): "Motor Direction",
                str(CMD_CHECK_TOTAL_CARDS): "Total Cards",
                str(CMD_CHECK_CONVEYOR_MODE): "Conveyor Mode",
                str(CMD_CHECK_STOP_TIME): "Stop Time",
                str(CMD_CHECK_EMPTY_STOP_TIME): "Empty Stop Time",
                str(CMD_CHECK_ERROR_DESTINATION_ADDRESS): "Error Destination Address",
                str(CMD_CHECK_MOTOR_ON_TH): "Motor Overcurrent",
                str(CMD_CHECK_DEBUG_MODE): "Debug Mode",
                str(CMD_CHECK_MERGER_MODE): "Merger Mode",
                str(CMD_CHECK_SUDDEN_STOP): "Motor Sudden Stop",
                str(CMD_CHECK_LOW_VOLTAGE_TH): "Motor Undervoltage",
                str(CMD_CHECK_HIGH_VOLTAGE_TH): "Motor Overvoltage",
                str(CMD_CHECK_CRATE_JAM_TIME): "Crate Jam Time",
                str(CMD_CHECK_SENSOR_MODE): "Sensor Mode",
                str(CMD_CHECK_STORE_PARAMETERS): "Store Parameters",
                str(CMD_CHECK_FIRMWARE_VERSION): "Firmware Version",
                str(CMD_CHECK_GRAVITY_MODE): "Gravity Mode",
                str(CMD_CHECK_CAN_RETRY_TIME): "Retry Time",
                str(CMD_CHECK_SLUG_CRATE_JAM_TICKS): "Slug Crate Jam Ticks",
                str(CMD_CHECK_SLUG_NEAR_BOX_TICKS): "Slug Near Box Ticks",
                str(CMD_CHECK_BOX_PASS_TIME_TH): "Box Pass Time Threshold",
                str(CMD_CHECK_CROSSOVER_MODE): "Crossover Mode",
                str(CMD_CHECK_MOTOR_TICKS_TH): "Motor Ticks",
                str(CMD_CHECK_LOG_LEVEL): "Log Level",
                str(CMD_CHECK_MODBUS_MODE): "Modbus Mode",
                str(CMD_CHECK_BAUDRATE): "Baudrate",
                str(CMD_CHECK_PLC_MOTOR_CONTROL_STOP_TIME): "PLC Motor Control Stop Time",
                str(CMD_CHECK_DELAY_SLUG_FREE_TIME): "Delay Slug Free Time",
                str(CMD_CHECK_ERROR_SIGNAL_MODE): "Error Signal Mode",
                str(CMD_CHECK_RESET_SIGNAL_MODE): "Reset Signal Mode",      
            }

            special_cmd_types = {
                str(CMD_CHECK_MOTOR_DIRECTION),
                str(CMD_CHECK_TOTAL_CARDS),
                str(CMD_CHECK_CONVEYOR_MODE),
                str(CMD_CHECK_ERROR_DESTINATION_ADDRESS),
                str(CMD_CHECK_SUDDEN_STOP),
                str(CMD_CHECK_MERGER_MODE),
                str(CMD_CHECK_GRAVITY_MODE),
                str(CMD_CHECK_SLUG_NEAR_BOX_TICKS),
                str(CMD_CHECK_DEBUG_MODE),
                str(CMD_CHECK_SENSOR_MODE),
                str(CMD_CHECK_STORE_PARAMETERS),
                str(CMD_CHECK_LOG_LEVEL),
                str(CMD_CHECK_MODBUS_MODE),
                str(CMD_CHECK_BAUDRATE),
                str(CMD_CHECK_ERROR_SIGNAL_MODE),
                str(CMD_CHECK_RESET_SIGNAL_MODE),
                str(CMD_CHECK_LOW_VOLTAGE_TH),
                str(CMD_CHECK_HIGH_VOLTAGE_TH),
                str(CMD_CHECK_CROSSOVER_MODE),
            }

            if command_type in command_types:
                if command_type in special_cmd_types:

                    # Handle special case for CMD_SET_CONVEYOR_MODE
                    if command_type == str(CMD_CHECK_MOTOR_DIRECTION):
                        direction_map = {"0": "Clockwise", "1": "Anti-Clockwise"}
                        print(f"{command_types.get(command_type, 'Unknown')}: {direction_map.get(str(int(additional_data[0:2], 16)), 'Unknown')}")
                    elif command_type == str(CMD_CHECK_CONVEYOR_MODE):
                        mode_map = {"1": "Singulated", "2": "Slug", "3": "Disable"}
                        print(f"{command_types.get(command_type, 'Unknown')}: {mode_map.get(str(int(additional_data[0:2], 16)), 'Unknown')}")
                    elif command_type == str(CMD_CHECK_MERGER_MODE):
                        merger_map = {"0": "Disable", "1": "Enable", "2": "Zippy Mode",} 
                        print(f"{command_types.get(command_type, 'Unknown')}: {merger_map.get(str(int(additional_data[0:2], 16)), 'Unknown')}")
                    elif command_type == str(CMD_CHECK_GRAVITY_MODE):
                        gravity_map = {"0": "Disable", "1": "Enable"}
                        print(f"{command_types.get(command_type, 'Unknown')}: {gravity_map.get(str(int(additional_data[0:2], 16)), 'Unknown')}")
                    elif command_type == str(CMD_CHECK_SENSOR_MODE):
                        sensor_map = {"0": "Dark", "1": "Light"}
                        print(f"{command_types.get(command_type, 'Unknown')}: {sensor_map.get(str(int(additional_data[0:2], 16)), 'Unknown')}")
                    elif (command_type == str(CMD_CHECK_STORE_PARAMETERS) or command_type == str(CMD_CHECK_LOG_LEVEL) or command_type == str(CMD_CHECK_MODBUS_MODE) or command_type == str(CMD_CHECK_DEBUG_MODE) or command_type == str(CMD_CHECK_SUDDEN_STOP) or command_type == str(CMD_CHECK_CROSSOVER_MODE)):
                        store_map = {"0": "Disable", "1": "Enable"}
                        print(f"{command_types.get(command_type, 'Unknown')}: {store_map.get(str(int(additional_data[0:2], 16)), 'Unknown')}")
                    elif command_type == str(CMD_CHECK_BAUDRATE):
                        baudrate_map = {
                            "0": "9600",
                            "1": "115200",
                        }
                        print(f"{command_types.get(command_type, 'Unknown')}: {baudrate_map.get(str(int(additional_data[0:2], 16)), 'Unknown')}")
                    elif command_type == str(CMD_CHECK_ERROR_SIGNAL_MODE):
                        error_signal_map = {"0": "Stable", "1": "Pulsating"}
                        print(f"{command_types.get(command_type, 'Unknown')}: {error_signal_map.get(str(int(additional_data[0:2], 16)), 'Unknown')}")
                    elif command_type == str(CMD_CHECK_RESET_SIGNAL_MODE):
                        reset_signal_map = {"0": "Stable", "1": "Pulsating"}
                        print(f"{command_types.get(command_type, 'Unknown')}: {reset_signal_map.get(str(int(additional_data[0:2], 16)), 'Unknown')}")
                    else:
                        print(f"{command_types.get(command_type, 'Unknown')}: {int(additional_data[0:2], 16)}")
                else:
                    if (command_type == str(CMD_CHECK_FIRMWARE_VERSION)):
                        firmware_version = int(additional_data[0:2], 16)
                        print(f"{command_types.get(command_type, 'Unknown')}: {((firmware_version & 0xFF00)>> 8)}.{(firmware_version & 0x00FF)}")
                    else:
                        print(f"{command_types[command_type]}: {int(additional_data, 16)}")
            else:
                print(f"[x] Unknown command type in response: {command_type}")
    elif response_type == f"{RESP_TYPE_HEALTH_CHECK:02X}":
        # Interpret error type

        no_error = 0
        start_up_tote_error = 1
        crate_jam_error = 2
        tri_motor_error = 3
        tote_misalligned_error = 4
        extra_direction_error = 5
        can_heartbeat_err = 6
        no_direction_error = 7

        # Interpret command type]
        health_check_map = {
            str(no_error): "Healthy",
            str(start_up_tote_error): "Start Up Tote Error",
            str(crate_jam_error): "Crate Jam Error",
            str(tri_motor_error): "Tri Motor Error",
            str(tote_misalligned_error): "Tote Misaligned Error",
            str(extra_direction_error): "Extra Direction Error",
            str(can_heartbeat_err): "CAN Heartbeat Error",
            str(no_direction_error): "No Direction Error",
        }
        print(f" Divert-X Health Check: {health_check_map.get(str(int(additional_data[0:5], 16)), 'Unknown')}")
    else:
        print(f"[x] Unknown response type: {response_type}")

def get_conveyor_side():
    valid_conveyor_side = [1, 2, 3, 4, 5]
    while True:
        try:
            conveyor_side = int(input(Fore.CYAN + "Enter Conveyor Side (1: S1, 2: S2, 3: S3, 4: S4, 5: Divert-X Motors): " + Style.RESET_ALL))
            if conveyor_side in valid_conveyor_side:
                return conveyor_side
            else:
                print(Fore.RED + f"[x] Invalid conveyor_side! Must be one of {valid_conveyor_side}." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[x] Invalid input! Must be an integer." + Style.RESET_ALL)


def get_motor_type():
    valid_motor_types = [1, 2, 3]
    while True:
        try:
            motor_type = int(input(Fore.CYAN + "Enter Motor Type (1: Roller, 2: Belt, 3: Lifter): " + Style.RESET_ALL))
            if motor_type in valid_motor_types:
                return motor_type
            else:
                print(Fore.RED + f"[x] Invalid motor type! Must be one of {valid_motor_types}." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[x] Invalid input! Must be an integer." + Style.RESET_ALL)


# === Main Program ===

def load_configuration_file():
    """Open file dialog to select and load a configuration file."""
    try:
        # Create a hidden root window
        root = Tk()
        root.withdraw()  # Hide the main window
        root.attributes('-topmost', True)  # Bring the dialog to the front
        
        # Set to None initially
        file_path = None
        
        try:
            # Open file dialog
            file_path = filedialog.askopenfilename(
                title="Select Configuration File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
        finally:
            # Make sure to destroy the root window
            root.destroy()
        
        if not file_path:  # User cancelled the dialog
            print(Fore.YELLOW + "[!] No file selected." + Style.RESET_ALL)
            return None
        
        # Load and validate JSON file
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
            print(Fore.BLUE + f"[✓] Configuration file '{os.path.basename(file_path)}' loaded successfully!" + Style.RESET_ALL)
            return config
        except json.JSONDecodeError:
            print(Fore.RED + f"[x] Error: Invalid JSON in file '{os.path.basename(file_path)}'" + Style.RESET_ALL)
            return None
        except Exception as e:
            print(Fore.RED + f"[x] Error reading file: {str(e)}" + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + f"[x] Error: {str(e)}" + Style.RESET_ALL)            
        return None

def format_config_value(value, indent=2):
    """Format configuration value with proper indentation and line breaks."""
    if isinstance(value, dict):
        if not value:
            return "{}"
        max_key_len = max(len(str(k)) for k in value.keys())
        lines = []
        for k, v in value.items():
            if isinstance(v, dict):
                # For nested dictionaries, format with indentation
                sub_indent = ' ' * (indent + 2)
                formatted_value = format_config_value(v, indent + 2)
                lines.append(f"{k}:{formatted_value}")
            else:
                lines.append(f"{k}: {v}")
        return '\n' + ' ' * indent + ('\n' + ' ' * indent).join(lines)
    return str(value)

def apply_motor_config(sock,config):
    if not config:
        print(Fore.RED + "[x] No configuration provided to apply." + Style.RESET_ALL)
        return False
    
    print("\n" + Fore.CYAN + "=== Configuration ===" + Style.RESET_ALL + "\n")


    motor_params = config.get("MotorParameters", {})

    parameter_order = [
        ("MotorRPM", "Motor RPM"),
        ("Acceleration", "Acceleration"),
        ("Deceleration", "Deceleration"),
        ("StopTime", "Stop Time"),
        ("EmptyStopTime", "Empty Stop Time"),
        ("MotorOvercurrent", "Motor Overcurrent"),
        ("MotorSuddenStop", "Motor Sudden Stop"),
        ("MotorUndervoltage", "Motor Undervoltage"),
        ("MotorOvervoltage", "Motor Overvoltage"),
        ("MotorTicks", "Motor Ticks"),
        ("StoreParameters", "Store Parameters")
    ]

    display_order = ["Roller", "Belt", "Lifter"]

    if not isinstance(motor_params, dict):
        print(Fore.RED + "[x] Invalid format: 'MotorParameters' section missing or malformed." + Style.RESET_ALL)
    else:
        print(Fore.CYAN + "\n[✓] Motor Parameters:\n" + Style.RESET_ALL)

        for motor in display_order:
            params = motor_params.get(motor)
            if not params:
                print(Fore.RED + f"[x] Missing section for: {motor}" + Style.RESET_ALL)
                continue

            print(Fore.YELLOW + f"[{motor}]" + Style.RESET_ALL)
            for key, label in parameter_order:
                value = params.get(key, "N/A")
                print(f"{label:<22}: {value}")
            print()

    while True:
        confirm = input(Fore.CYAN + "Do you want to apply this configuration? (yes/no): " + Style.RESET_ALL).strip().lower()
        if confirm in ['y', 'yes']:
            print(Fore.GREEN + "[✓] Applying configuration..." + Style.RESET_ALL)
            # Print and send the Store Parameter command as an example
            motor_ids = {
            "Roller": "01",
            "Belt": "02",
            "Lifter": "03"
            }
            device_id = "05"
            command_type = "08"

            # Command IDs for each parameter
            param_cmds = {
                "StoreParameters": ("21", "0001"),
                "MotorRPM": "01",
                "Acceleration": "02",
                "Deceleration": "03",
                "StopTime": "07",
                "EmptyStopTime": "08",
                "MotorOvercurrent": "0D",
                "MotorSuddenStop": "10",
                "MotorUndervoltage": "11",
                "MotorOvervoltage": "12",
                "MotorTicks": "14"
            }

            for motor_name, motor_data in config["MotorParameters"].items():
                if motor_name not in motor_ids:
                    continue

                motor_id = motor_ids[motor_name]

                # 1. Enable store param
                store_cmd = device_id + motor_id + command_type + param_cmds["StoreParameters"][0] + param_cmds["StoreParameters"][1]
                print(f"Sending store param enable for {motor_name}: {store_cmd}")
                send_can_command(sock,store_cmd)
                time.sleep(0.2)

        # 2. Send all parameters
                for param, cmd_id in param_cmds.items():
                    if param == "StoreParameters":
                        continue  # already handled

                    value = motor_data.get(param)
                    if value is None:
                        continue

                    # Special case: MotorSuddenStop is boolean (0/1)
                    if param == "MotorSuddenStop":
                        value_hex = "0001" if value else "0000"
                    else:
                        value_hex = to_hex_str(value, 4)

                    full_cmd = device_id + motor_id + command_type + cmd_id + value_hex
                    print(f"Sending {param} ({value}) to {motor_name}: {full_cmd}")
                    send_can_command(sock,full_cmd)
                    time.sleep(0.2)

            return True

def to_hex_str(val, length=4):
    """Convert integer to zero-padded hex string (length in hex digits)."""
    return format(val, '0{}X'.format(length)).upper()

def apply_config(sock, config):
    """
    Apply configuration from a dictionary to the device.
    
    Args:
        sock: The socket connection to the device
        config: Dictionary containing configuration parameters
        
    Returns:
        bool: True if configuration was applied, False otherwise
    """
    if not config:
        print(Fore.RED + "[x] No configuration provided to apply." + Style.RESET_ALL)
        return False
    
    # Print configuration header
    print("\n" + Fore.CYAN + "=== Configuration ===" + Style.RESET_ALL + "\n")
    
    # Define the order and grouping of sections with their display names
    sections = [
        ('In/Out Configuration', [('InOut', '')]),
        ('Tote Flow', [('ToteFlow', '')]),
        ('Network Settings', [
            ('EthernetRetryCount', ''),
            ('DivertX', 'DivertX'),
            ('Destination', 'Destination'),
            ('EthernetMaster', '')
        ]),
        ('Conveyor Settings', [
            ('ConveyorMode', ''),
            ('PopUpType', ''),
            ('StoreParameter', '')
        ]),
        ('CAN Configuration', [
            ('CAN_ID', 'CAN IDs'),
            ('CANGateways', 'Gateways')
        ]),
        ('Barcode Settings', [('BarcodePorts', 'Ports')]),
        ('Transfer Settings', [
            ('ParallelTransfer', 'Parallel Transfer'),
            ('ToteRejectionFlow', 'Tote Rejection Flow')
        ]),
        ('Timing Settings', [
            ('SlugFreeDelayTime', 'Slug Free Delay Time'),
            ('ToteRetryTime', 'Tote Retry Time'),
            ('ToteCentreTimeout', 'Tote Centre Timeout'),
            ('PLCLoadPresenceFeedbackUpdateTime', 'PLC Load Presence Feedback Update Time')
        ]),
        ('Debug Settings', [('Debug', '')]),
        ('Reverse Commands', [('ReverseCommand', '')])
    ]
    
    # Print each section with proper formatting
    for section_name, section_items in sections:
        print(Fore.YELLOW + section_name + ":" + Style.RESET_ALL)
        section_has_content = False
        
        for key, display_name in section_items:
            if key in config:
                value = config[key]
                if value is not None:  # Only process non-None values
                    section_has_content = True
                    if isinstance(value, dict):
                        # For dictionary values, print each key-value pair with indentation
                        if display_name:  # If there's a display name for this subsection
                            print(f"  {display_name}:")
                            indent = '    '
                        else:
                            indent = '  '
                        
                        for k, v in value.items():
                            print(f"{indent}{k}: {v}")
                    else:
                        # For non-dictionary values, just print the key and value
                        print(f"  {key}: {value}")
        
        if section_has_content:
            print()  # Add empty line between sections


def apply_motor_config(sock, config):
    import os
    import json
    from colorama import Fore, Style

    # Try to get the motor parameters from the provided config dict
    motor_params = None
    if config and isinstance(config, dict):
        motor_params = config.get('MotorParameters')
    # If not in config, try to load from file
    if not motor_params:
        json_path = os.path.join(os.path.dirname(__file__), 'motor_parameters.json')
        try:
            with open(json_path, 'r') as f:
                file_data = json.load(f)
                motor_params = file_data.get('MotorParameters', {})
        except Exception as e:
            print(Fore.RED + f"[x] Failed to load motor_parameters.json: {e}" + Style.RESET_ALL)
            return False

    print("\n" + Fore.CYAN + "=== Motor Parameters Configuration ===" + Style.RESET_ALL + "\n")

    def format_dict(d, indent=2):
        for key, value in d.items():
            if isinstance(value, dict):
                print(' ' * indent + Fore.YELLOW + f"{key}:" + Style.RESET_ALL)
                format_dict(value, indent + 2)
            else:
                print(' ' * indent + f"{key}: {value}")

    if not motor_params:
        print(Fore.RED + "[x] No motor parameters found to display." + Style.RESET_ALL)
        return False

    for motor_type, params in motor_params.items():
        print(Fore.GREEN + f"{motor_type}:" + Style.RESET_ALL)
        format_dict(params, indent=2)
        print()  # Blank line between sections

    # Ask user for confirmation
    while True:
        user_input = input(Fore.CYAN + "Do you want to apply these motor parameters? (yes/no): " + Style.RESET_ALL).strip().lower()
        if user_input in ['y', 'yes']:
            print(Fore.GREEN + "[✓] Applying motor parameters..." + Style.RESET_ALL)
            return True
        elif user_input in ['n', 'no']:
            print(Fore.YELLOW + "[!] Skipping motor parameter application." + Style.RESET_ALL)
            return False
        else:
            print(Fore.RED + "[x] Please enter 'yes' or 'no'." + Style.RESET_ALL)

    # Print any error messages if they exist
    if 'URLCheck' in config and 'Error' in config['URLCheck']:
        print(Fore.RED + "Note: URL Check Error - " + str(config['URLCheck']['Error']) + Style.RESET_ALL + "\n")
    
    # Ask for user confirmation
    while True:
        confirm = input(Fore.CYAN + "Do you want to apply this configuration? (yes/no): " + Style.RESET_ALL).strip().lower()
        if confirm in ['y', 'yes']:
            print(Fore.GREEN + "[✓] Applying configuration..." + Style.RESET_ALL)
            # Print and send the Store Parameter command as an example
            print(Fore.BLUE + "[CMD]  00000A320001" + Style.RESET_ALL)
            send_can_command(sock, '00000A320001')
            # TODO: Add actual configuration application logic here

            inout_map = {'None': '0', 'Out': '1', 'In': '2'}
            s1 = inout_map.get(str(config['InOut'].get('S1', 'None')).capitalize(), '0')
            s2 = inout_map.get(str(config['InOut'].get('S2', 'None')).capitalize(), '0')
            s3 = inout_map.get(str(config['InOut'].get('S3', 'None')).capitalize(), '0')
            s4 = inout_map.get(str(config['InOut'].get('S4', 'None')).capitalize(), '0')
            cmd_inout = f"00000A01{s1}{s2}{s3}{s4}"
            print(Fore.BLUE + f"[CMD]  {cmd_inout}" + Style.RESET_ALL)
            send_can_command(sock, cmd_inout)

            # Tote Flow command
            tote_flow_map = {'WCS': '0', 'Straight': '1', 'Left': '2', 'Right': '3', 'I/O': '4'}
            tote_flow = config.get('ToteFlow', {})
            tf_s1 = tote_flow_map.get(str(tote_flow.get('S1', 'WCS')).capitalize(), '0')
            tf_s2 = tote_flow_map.get(str(tote_flow.get('S2', 'WCS')).capitalize(), '0')
            tf_s3 = tote_flow_map.get(str(tote_flow.get('S3', 'WCS')).capitalize(), '0')
            tf_s4 = tote_flow_map.get(str(tote_flow.get('S4', 'WCS')).capitalize(), '0')
            tf_digits = f"{tf_s1}{tf_s2}{tf_s3}{tf_s4}"
            cmd_tote_flow = f"00000A02{tf_digits}"
            print(Fore.BLUE + f"[CMD]  {cmd_tote_flow} (Tote Flow S1-S4)" + Style.RESET_ALL)
            send_can_command(sock, cmd_tote_flow)
            time.sleep(0.2)
            # Extract and send Ethernet Retry Count command
            eth_retry_count = int(config.get('EthernetRetryCount', 1))
            if not (1 <= eth_retry_count <= 255):
                print(Fore.YELLOW + f"[!] Invalid EthernetRetryCount '{eth_retry_count}', defaulting to 1." + Style.RESET_ALL)
                eth_retry_count = 1
            cmd_eth_retry = f"00000A03{eth_retry_count:04d}"
            time.sleep(0.2)
            print(Fore.BLUE + f"[CMD]  {cmd_eth_retry} (Ethernet Retry Count)" + Style.RESET_ALL)
            send_can_command(sock, cmd_eth_retry)
            time.sleep(0.2)
            # Extract and send Conveyor Mode command
            conveyor_mode_map = {'Singulated': '1', 'Slug': '2', 'Disable': '3'}
            conveyor_mode_value = str(config.get('ConveyorMode', 'Singulated')).capitalize()
            conveyor_mode_digit = conveyor_mode_map.get(conveyor_mode_value, '1')
            cmd_conveyor_mode = f"00000A04{conveyor_mode_digit.zfill(4)}"
            time.sleep(0.2)
            print(Fore.BLUE + f"[CMD]  {cmd_conveyor_mode} (Conveyor Mode: {conveyor_mode_value})" + Style.RESET_ALL)
            send_can_command(sock, cmd_conveyor_mode)
            time.sleep(0.2)
            # Extract and send CAN ID commands
            can_id_config = config.get('CAN_ID', {})
            can_id_cmds = [
                ('S2', '00000A05', 'Roller Clockwise'),
                ('S4', '00000A06', 'Roller Anticlockwise'),
                ('S1', '00000A07', 'Belt Clockwise'),
                ('S3', '00000A08', 'Belt Anticlockwise'),
                ('DivertXMotorControl', '00000A09', 'Motor Control')
            ]
            for key, opcode, desc in can_id_cmds:
                can_id = int(can_id_config.get(key, 0))
                if not (1 <= can_id <= 255):
                    print(Fore.YELLOW + f"[!] Invalid CAN ID for {desc} ({key}): '{can_id}', skipping." + Style.RESET_ALL)
                    continue
                cmd = f"{opcode}{can_id:04X}"  # 4-digit uppercase hex
                time.sleep(0.2)
                print(Fore.BLUE + f"[CMD]  {cmd} ({desc} /{key})" + Style.RESET_ALL)
                send_can_command(sock, cmd)
            time.sleep(0.2)
            # Extract and send Barcode Scanner Server Port commands
            barcode_ports = config.get('BarcodePorts', {})
            barcode_cmds = [
                ('Barcode1', '00000A0A', 'Barcode Scanner 1'),
                ('Barcode2', '00000A0B', 'Barcode Scanner 2'),
                ('Barcode3', '00000A0C', 'Barcode Scanner 3'),
                ('Barcode4', '00000A0D', 'Barcode Scanner 4'),
            ]
            for key, opcode, desc in barcode_cmds:
                port_val = barcode_ports.get(key)
                if port_val is None:
                    print(Fore.YELLOW + f"[!] No port value for {desc} ({key}), skipping." + Style.RESET_ALL)
                    continue
                try:
                    port_digit = int(port_val)
                except Exception:
                    print(Fore.YELLOW + f"[!] Invalid port value for {desc} ({key}): '{port_val}', skipping." + Style.RESET_ALL)
                    continue
                if not (1 <= port_digit <= 4):
                    print(Fore.YELLOW + f"[!] Port value for {desc} ({key}) out of range: '{port_digit}', skipping." + Style.RESET_ALL)
                    continue
                cmd = f"{opcode}{port_digit:04d}"
                time.sleep(0.2)
                print(Fore.BLUE + f"[CMD]  {cmd} ({desc} /{key})" + Style.RESET_ALL)
                send_can_command(sock, cmd)
            time.sleep(0.2)
            # Extract and send Parallel Transfer command
            parallel_transfer = config.get('ParallelTransfer', {})
            pt_map = {'Enable': '1', 'Disable': '0'}
            pt_s1 = pt_map.get(str(parallel_transfer.get('S1', 'Disable')).capitalize(), '0')
            pt_s2 = pt_map.get(str(parallel_transfer.get('S2', 'Disable')).capitalize(), '0')
            pt_s3 = pt_map.get(str(parallel_transfer.get('S3', 'Disable')).capitalize(), '0')
            pt_s4 = pt_map.get(str(parallel_transfer.get('S4', 'Disable')).capitalize(), '0')
            pt_digits = f"{pt_s1}{pt_s2}{pt_s3}{pt_s4}"
            cmd_parallel_transfer = f"00000A0E{pt_digits}"
            time.sleep(0.2)
            print(Fore.BLUE + f"[CMD]  {cmd_parallel_transfer} (Parallel Transfer S1-S4)" + Style.RESET_ALL)
            send_can_command(sock, cmd_parallel_transfer)
            time.sleep(0.2)
            # Extract and send Tote Rejection Flow command
            tote_rejection_flow = config.get('ToteRejectionFlow', {})
            trf_map = {'WCS': '0', 'Straight': '1', 'Left': '2', 'Right': '3'}
            trf_s1 = trf_map.get(str(tote_rejection_flow.get('S1', 'WCS')).capitalize(), '0')
            trf_s2 = trf_map.get(str(tote_rejection_flow.get('S2', 'WCS')).capitalize(), '0')
            trf_s3 = trf_map.get(str(tote_rejection_flow.get('S3', 'WCS')).capitalize(), '0')
            trf_s4 = trf_map.get(str(tote_rejection_flow.get('S4', 'WCS')).capitalize(), '0')
            trf_digits = f"{trf_s1}{trf_s2}{trf_s3}{trf_s4}"
            cmd_trf = f"00000A0F{trf_digits}"
            time.sleep(0.2)
            print(Fore.BLUE + f"[CMD]  {cmd_trf} (Tote Rejection Flow S1-S4)" + Style.RESET_ALL)
            send_can_command(sock, cmd_trf)
            time.sleep(0.2)
            # Extract and send Motherboard IP command
            mb_ip = config.get('DivertX', {}).get('IP')
            if mb_ip:
                try:
                    ip_parts = [int(part) for part in mb_ip.strip().split('.')]
                    if len(ip_parts) == 4 and all(0 <= p <= 255 for p in ip_parts):
                        hex_ip = ''.join(f'{p:02x}' for p in ip_parts)
                        cmd_mbip = f"00000A11{hex_ip}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_mbip} (Motherboard IP {mb_ip})" + Style.RESET_ALL)
                        time.sleep(0.2)
                        send_can_command(sock, cmd_mbip)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid DivertX.IP value: '{mb_ip}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing DivertX.IP: '{mb_ip}', skipping." + Style.RESET_ALL)

            # Extract and send Subnet Mask command
            subnet_mask = config.get('DivertX', {}).get('Subnet')
            if subnet_mask:
                try:
                    subnet_parts = [int(part) for part in subnet_mask.strip().split('.')]
                    if len(subnet_parts) == 4 and all(0 <= p <= 255 for p in subnet_parts):
                        hex_subnet = ''.join(f'{p:02x}' for p in subnet_parts)
                        cmd_subnet = f"00000A12{hex_subnet}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_subnet} (Subnet Mask {subnet_mask})" + Style.RESET_ALL)
                        time.sleep(0.2)
                        send_can_command(sock, cmd_subnet)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid DivertX.Subnet value: '{subnet_mask}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing DivertX.Subnet: '{subnet_mask}', skipping." + Style.RESET_ALL)
            # Extract and send Gateway command
            gateway = config.get('DivertX', {}).get('Gateway')
            if gateway:
                try:
                    gateway_parts = [int(part) for part in gateway.strip().split('.')]
                    if len(gateway_parts) == 4 and all(0 <= p <= 255 for p in gateway_parts):
                        hex_gateway = ''.join(f'{p:02x}' for p in gateway_parts)
                        cmd_gateway = f"00000A13{hex_gateway}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_gateway} (Gateway {gateway})" + Style.RESET_ALL)
                        time.sleep(0.2)
                        send_can_command(sock, cmd_gateway)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid DivertX.Gateway value: '{gateway}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing DivertX.Gateway: '{gateway}', skipping." + Style.RESET_ALL)
            # Extract and send Destination IP command
            dest_ip = config.get('Destination', {}).get('IP')
            if dest_ip:
                try:
                    dest_ip_parts = [int(part) for part in dest_ip.strip().split('.')]
                    if len(dest_ip_parts) == 4 and all(0 <= p <= 255 for p in dest_ip_parts):
                        hex_dest_ip = ''.join(f'{p:02x}' for p in dest_ip_parts)
                        cmd_dest_ip = f"00000A14{hex_dest_ip}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_dest_ip} (Destination IP {dest_ip})" + Style.RESET_ALL)
                        time.sleep(0.2)
                        send_can_command(sock, cmd_dest_ip)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid Destination.IP value: '{dest_ip}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing Destination.IP: '{dest_ip}', skipping." + Style.RESET_ALL)
            # Extract and send Destination Port command
            dest_port = config.get('Destination', {}).get('Port')
            if dest_port is not None:
                try:
                    port_int = int(dest_port)
                    if 0 <= port_int <= 65535:
                        hex_port = f'{port_int:04x}'
                        cmd_dest_port = f"00000A15{hex_port}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_dest_port} (Destination Port {dest_port})" + Style.RESET_ALL)
                        time.sleep(0.2)
                        send_can_command(sock, cmd_dest_port)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid Destination.Port value: '{dest_port}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing Destination.Port: '{dest_port}', skipping." + Style.RESET_ALL)
            # Extract and send CAN Gateway commands
            can_gateways = config.get('CANGateways', {})
            gateway_map = {'Enable': '1', 'Disable': '0'}
            gateway_cmds = [
                ('S2', '00000A18', 'Roller Clockwise'),
                ('S4', '00000A19', 'Roller Anticlockwise'),
                ('S1', '00000A1A', 'Belt Clockwise'),
                ('S3', '00000A1B', 'Belt Anticlockwise'),
                ('DivertXMotorControl', '00000A1C', 'Pop CAN'),
                ('Barcode1', '00000A1D', 'Barcode-1'),
                ('Barcode2', '00000A1E', 'Barcode-2'),
                ('Barcode3', '00000A1F', 'Barcode-3'),
                ('Barcode4', '00000A20', 'Barcode-4'),
            ]
            for key, opcode, desc in gateway_cmds:
                val = gateway_map.get(str(can_gateways.get(key, 'Disable')).capitalize(), '0')
                payload = '0001' if val == '1' else '0000'
                cmd = f"{opcode}{payload}"
                time.sleep(0.2)
                print(Fore.BLUE + f"[CMD]  {cmd} (Gateway {desc} /{key}: {'Enable' if val == '1' else 'Disable'})" + Style.RESET_ALL)
                send_can_command(sock, cmd)
                time.sleep(0.2)
            # Extract and send PopUpType command
            pop_type_map = {
                'Ninety Degree': '1',
                'Diverter Left': '2',
                'Diverter Right': '3'
            }
            pop_type_val = str(config.get('PopUpType', '')).strip()
            pop_type_digit = pop_type_map.get(pop_type_val)
            if pop_type_digit:
                cmd_pop_type = f"00000A21{'000'+pop_type_digit}"
                time.sleep(0.2)
                print(Fore.BLUE + f"[CMD]  {cmd_pop_type} (PopUpType: {pop_type_val})" + Style.RESET_ALL)
                send_can_command(sock, cmd_pop_type)
                time.sleep(0.2)
            else:
                if pop_type_val:
                    print(Fore.YELLOW + f"[!] Invalid PopUpType value: '{pop_type_val}', skipping." + Style.RESET_ALL)
            # Extract and send Debug Device IP command
            debug_ip = config.get('Debug', {}).get('DeviceIP')
            if debug_ip:
                try:
                    debug_ip_parts = [int(part) for part in debug_ip.strip().split('.')]
                    if len(debug_ip_parts) == 4 and all(0 <= p <= 255 for p in debug_ip_parts):
                        hex_debug_ip = ''.join(f'{p:02x}' for p in debug_ip_parts)
                        cmd_debug_ip = f"00000A23{hex_debug_ip}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_debug_ip} (Debug Device IP {debug_ip})" + Style.RESET_ALL)
                        send_can_command(sock, cmd_debug_ip)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid Debug.DeviceIP value: '{debug_ip}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing Debug.DeviceIP: '{debug_ip}', skipping." + Style.RESET_ALL)
            # Extract and send Debug Device Port command
            debug_port = config.get('Debug', {}).get('DevicePort')
            if debug_port is not None:
                try:
                    debug_port_int = int(debug_port)
                    if 0 <= debug_port_int <= 65535:
                        hex_debug_port = f'{debug_port_int:04x}'
                        cmd_debug_port = f"00000A24{hex_debug_port}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_debug_port} (Debug Device Port {debug_port})" + Style.RESET_ALL)
                        send_can_command(sock, cmd_debug_port)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid Debug.DevicePort value: '{debug_port}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing Debug.DevicePort: '{debug_port}', skipping." + Style.RESET_ALL)
            # Extract and send ReverseCommand CAN commands
            reverse_cmds = [
                ('S2', '00000A25', 'Roller Clockwise'),
                ('S4', '00000A26', 'Roller Anticlockwise'),
                ('S1', '00000A27', 'Belt Clockwise'),
                ('S3', '00000A28', 'Belt Anticlockwise'),
            ]
            reverse_map = {'Enable': '1', 'Disable': '0'}
            reverse_config = config.get('ReverseCommand', {})
            for key, opcode, desc in reverse_cmds:
                val = reverse_map.get(str(reverse_config.get(key, 'Disable')).capitalize(), '0')
                payload = '0001' if val == '1' else '0000'
                cmd = f"{opcode}{payload}"
                time.sleep(0.5)
                print(Fore.BLUE + f"[CMD]  {cmd} (Reverse {desc} /{key}: {'Enable' if val == '1' else 'Disable'})" + Style.RESET_ALL)
                send_can_command(sock, cmd)
                time.sleep(0.5)
            # Extract and send Slug Free Delay Time CAN commands
            slug_delay_cmds = [
                ('S2', '00000A29', 'Roller Clockwise'),
                ('S4', '00000A2A', 'Roller Anticlockwise'),
                ('S1', '00000A2B', 'Belt Clockwise'),
                ('S3', '00000A2C', 'Belt Anticlockwise'),
            ]
            slug_delay_config = config.get('SlugFreeDelayTime', {})
            for key, opcode, desc in slug_delay_cmds:
                raw_val = str(slug_delay_config.get(key, '0 ms')).strip().lower()
                try:
                    ms_val = int(raw_val.replace('ms','').strip())
                    if 0 <= ms_val <= 65535:
                        hex_delay = f'{ms_val:04x}'
                        cmd = f"{opcode}{hex_delay}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd} (Slug Free Delay {desc} /{key}: {ms_val} ms)" + Style.RESET_ALL)
                        send_can_command(sock, cmd)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] SlugFreeDelayTime for {desc} /{key} out of range: '{ms_val}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing SlugFreeDelayTime for {desc} /{key}: '{raw_val}', skipping." + Style.RESET_ALL)
            # Extract and send ToteRetryTime command
            tote_retry_raw = str(config.get('ToteRetryTime', '0 ms')).strip().lower()
            try:
                tote_retry_ms = int(tote_retry_raw.replace('ms','').strip())
                if 0 <= tote_retry_ms <= 65535:
                    hex_retry = f'{tote_retry_ms:04x}'
                    cmd_tote_retry = f"00000A2D{hex_retry}"
                    time.sleep(0.2)
                    print(Fore.BLUE + f"[CMD]  {cmd_tote_retry} (Tote Retry Time: {tote_retry_ms} ms)" + Style.RESET_ALL)
                    send_can_command(sock, cmd_tote_retry)
                    time.sleep(0.2)
                else:
                    print(Fore.YELLOW + f"[!] ToteRetryTime out of range: '{tote_retry_ms}', skipping." + Style.RESET_ALL)
            except Exception:
                print(Fore.YELLOW + f"[!] Error parsing ToteRetryTime: '{tote_retry_raw}', skipping." + Style.RESET_ALL)
            # Extract and send ToteCentreTimeout CAN commands
            tote_centre_cmds = [
                ('S2', '00000A2E', 'Roller Clockwise'),
                ('S4', '00000A2F', 'Roller Anticlockwise'),
                ('S1', '00000A30', 'Belt Clockwise'),
                ('S3', '00000A31', 'Belt Anticlockwise'),
            ]
            tote_centre_config = config.get('ToteCentreTimeout', {})
            for key, opcode, desc in tote_centre_cmds:
                raw_val = str(tote_centre_config.get(key, '0 ms')).strip().lower()
                try:
                    ms_val = int(raw_val.replace('ms','').strip())
                    if 0 <= ms_val <= 65535:
                        hex_timeout = f'{ms_val:04x}'
                        cmd = f"{opcode}{hex_timeout}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd} (Tote Centre Timeout {desc} /{key}: {ms_val} ms)" + Style.RESET_ALL)
                        send_can_command(sock, cmd)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] ToteCentreTimeout for {desc} /{key} out of range: '{ms_val}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing ToteCentreTimeout for {desc} /{key}: '{raw_val}', skipping." + Style.RESET_ALL)
            # Extract and send PLCLoadPresenceFeedbackUpdateTime command
            plc_load_presence_raw = str(config.get('PLCLoadPresenceFeedbackUpdateTime', '0 ms')).strip().lower()
            try:
                plc_load_presence_ms = int(plc_load_presence_raw.replace('ms','').strip())
                if 0 <= plc_load_presence_ms <= 65535:
                    hex_presence = f'{plc_load_presence_ms:04x}'
                    cmd_plc_presence = f"00000A33{hex_presence}"
                    time.sleep(0.2)
                    print(Fore.BLUE + f"[CMD]  {cmd_plc_presence} (PLC Load Presence Feedback Update Time: {plc_load_presence_ms} ms)" + Style.RESET_ALL)
                    send_can_command(sock, cmd_plc_presence)
                    time.sleep(0.2)
                else:
                    print(Fore.YELLOW + f"[!] PLCLoadPresenceFeedbackUpdateTime out of range: '{plc_load_presence_ms}', skipping." + Style.RESET_ALL)
            except Exception:
                print(Fore.YELLOW + f"[!] Error parsing PLCLoadPresenceFeedbackUpdateTime: '{plc_load_presence_raw}', skipping." + Style.RESET_ALL)
            
            # Extract and send MQTT Broker IP command
            mqtt_broker_ip = config.get('MQTTBroker', {}).get('IP')
            if mqtt_broker_ip:
                try:
                    ip_parts = [int(part) for part in mqtt_broker_ip.strip().split('.')]
                    if len(ip_parts) == 4 and all(0 <= p <= 255 for p in ip_parts):
                        hex_ip = ''.join(f'{p:02x}' for p in ip_parts)
                        cmd_mqtt_ip = f"00000A37{hex_ip}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_mqtt_ip} (MQTT Broker IP {mqtt_broker_ip})" + Style.RESET_ALL)
                        send_can_command(sock, cmd_mqtt_ip)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid MQTTBroker.IP value: '{mqtt_broker_ip}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing MQTTBroker.IP: '{mqtt_broker_ip}', skipping." + Style.RESET_ALL)
            
            # Extract and send MQTT Broker Port command
            mqtt_broker_port = config.get('MQTTBroker', {}).get('Port')
            if mqtt_broker_port is not None:
                try:
                    port_int = int(mqtt_broker_port)
                    if 1 <= port_int <= 65535:
                        hex_port = f'{port_int:04x}'
                        cmd_mqtt_port = f"00000A39{hex_port}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_mqtt_port} (MQTT Broker Port {mqtt_broker_port})" + Style.RESET_ALL)
                        send_can_command(sock, cmd_mqtt_port)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid MQTTBroker.Port value: '{mqtt_broker_port}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing MQTTBroker.Port: '{mqtt_broker_port}', skipping." + Style.RESET_ALL)
            
            # Extract and send MQTT Request Topic command
            mqtt_request_topic = config.get('MQTTBroker', {}).get('RequestTopic')
            if mqtt_request_topic:
                try:
                    cmd_request_topic = f"00000A3A{mqtt_request_topic}"
                    time.sleep(0.2)
                    print(Fore.BLUE + f"[CMD]  {cmd_request_topic} (MQTT Request Topic: {mqtt_request_topic})" + Style.RESET_ALL)
                    send_can_command(sock, cmd_request_topic)
                    time.sleep(0.2)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error sending MQTT Request Topic: '{mqtt_request_topic}', skipping." + Style.RESET_ALL)
            
            # Extract and send MQTT Response Topic command
            mqtt_response_topic = config.get('MQTTBroker', {}).get('ResponseTopic')
            if mqtt_response_topic:
                try:
                    cmd_response_topic = f"00000A3B{mqtt_response_topic}"
                    time.sleep(0.2)
                    print(Fore.BLUE + f"[CMD]  {cmd_response_topic} (MQTT Response Topic: {mqtt_response_topic})" + Style.RESET_ALL)
                    send_can_command(sock, cmd_response_topic)
                    time.sleep(0.2)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error sending MQTT Response Topic: '{mqtt_response_topic}', skipping." + Style.RESET_ALL)
            
            # Extract and send Enable Tote Tracking command
            tote_tracking = config.get('ToteTracking', {}).get('Mode')
            if tote_tracking is not None:
                try:
                    tracking_mode = int(tote_tracking)
                    if 0 <= tracking_mode <= 2:
                        mode_hex = f'{tracking_mode:04x}'
                        mode_desc = {0: 'Disable', 1: 'CAN', 2: 'Ethernet'}.get(tracking_mode, 'Unknown')
                        cmd_tote_tracking = f"00000A38{mode_hex}"
                        time.sleep(0.2)
                        print(Fore.BLUE + f"[CMD]  {cmd_tote_tracking} (Tote Tracking: {mode_desc})" + Style.RESET_ALL)
                        send_can_command(sock, cmd_tote_tracking)
                        time.sleep(0.2)
                    else:
                        print(Fore.YELLOW + f"[!] Invalid ToteTracking.Mode value: '{tote_tracking}', skipping." + Style.RESET_ALL)
                except Exception:
                    print(Fore.YELLOW + f"[!] Error parsing ToteTracking.Mode: '{tote_tracking}', skipping." + Style.RESET_ALL)
            
            return True
        elif confirm in ['n', 'no']:
            print(Fore.YELLOW + "[!] Configuration application cancelled." + Style.RESET_ALL)
            return False
        else:
            print(Fore.RED + "[x] Please enter 'yes' or 'no'." + Style.RESET_ALL)

def main():
    ip = input(Fore.CYAN + "Enter server IP: " + Style.RESET_ALL).strip()
    while True:
        try:
            port = int(input(Fore.CYAN + "Enter server port: " + Style.RESET_ALL).strip())
            break
        except ValueError:
            print(Fore.RED + "[x] Invalid port. Must be a number." + Style.RESET_ALL)

    sock = connect_to_server(ip, port)
    if not sock:
        return

    # Command handlers for cmd_type from 0x01 to 0x24
    cmd_handlers = {
        CMD_CAN_IN_OUT_CONFIG: get_in_out_params,
        CMD_TOTE_DEFAULT_OUT_CONFIG: get_tote_flow_params,
        CMD_WCS_RETRY_COUNTS_CONFIG: lambda: get_validated_input(
            "Enter ethernet retry count (0 : 5): ",
            valid_range=range(0, 6)
        ),
        CMD_CONVEYOR_MODE_CONFIG: lambda: get_validated_input(
            "Enter conveyor mode (1: Singulated, 2: Slug, 3: Disable): ",
            valid_range=range(1, 4)
        ),
        CMD_S1_CAN_ID_CONFIG: lambda: get_validated_input(
            "Enter S1 CAN ID (1 : 80) : ",
            valid_range=range(1, 81)
        ),
        CMD_S2_CAN_ID_CONFIG: lambda: get_validated_input(
            "Enter S2 CAN ID (1 : 80) : ",
            valid_range=range(1, 81)
        ),
        CMD_S3_CAN_ID_CONFIG: lambda: get_validated_input(
            "Enter S3 CAN ID (1 : 80) : ",
            valid_range=range(1, 81)
        ),
        CMD_S4_CAN_ID_CONFIG: lambda: get_validated_input(
            "Enter S4 CAN ID (1 : 80) : ",
            valid_range=range(1, 81)
        ),
        CMD_DIVERT_X_MOTOR_CONTROL_CAN_ID_CONFIG: lambda: get_validated_input(
            "Enter Divert-X Motor Control CAN ID (1 : 255) : ",
            valid_range=range(1, 255)
        ),
        CMD_BARCODE_1_PORT_CONFIG: lambda: get_validated_input(
            "Enter Barcode 1 Port (1 : 65535) : ",
            valid_range=range(1, 65536)
        ),
        CMD_BARCODE_2_PORT_CONFIG: lambda: get_validated_input(
            "Enter Barcode 2 Port (1 : 65535) : ",
            valid_range=range(1, 65536)
        ),
        CMD_BARCODE_3_PORT_CONFIG: lambda: get_validated_input(
            "Enter Barcode 3 Port (1 : 65535) : ",
            valid_range=range(1, 65536)
        ),
        CMD_BARCODE_4_PORT_CONFIG: lambda: get_validated_input(
            "Enter Barcode 4 Port (1 : 65535) : ",
            valid_range=range(1, 65536)
        ),
        CMD_PARALLEL_TRANSFER_CONFIG: get_parallel_transfer_params,
        CMD_TOTE_REJECTION_FLOW_CONFIG: get_tote_flow_params,
        CMD_URL_CONFIG: lambda: input("Enter URL: ").strip(),
        CMD_DIVERT_X_IP_CONFIG: get_network_params,
        CMD_DIVERT_X_SUBNET_CONFIG: get_network_params,
        CMD_DIVERT_X_GATEWAY_CONFIG: get_network_params,
        CMD_DEST_IP_CONFIG: get_network_params,
        CMD_DEST_PORT_CONFIG: lambda: get_validated_input(
            "Enter destination port (1 : 65535): ",
            valid_range=range(1, 65536)
        ),
        CMD_ETH_MASTER_CONFIG: lambda: get_validated_input(
            "Enter ethernet master (0: No Master, 1: WCS, 2: PLC): ",
            valid_range=range(0, 3)
        ),
        CMD_RESET_POP_UP: lambda: get_validated_input(
            "Enter reset pop up (1: Reset): ",
            valid_range=[1]
        ),
        CMD_S1_CAN_GATEWAY: lambda: get_validated_input(
            "Enter S1 CAN Gateway (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_S2_CAN_GATEWAY: lambda: get_validated_input(
            "Enter S2 CAN Gateway (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_S3_CAN_GATEWAY: lambda: get_validated_input(
            "Enter S3 CAN Gateway (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_S4_CAN_GATEWAY: lambda: get_validated_input(
            "Enter S4 CAN Gateway (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_DIVERT_X_MOTOR_CONTROL_GATEWAY: lambda: get_validated_input(
            "Enter Divert-X Motor Control Gateway (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_BARCODE_1_GATEWAY: lambda: get_validated_input(
            "Enter Barcode 1 Gateway (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_BARCODE_2_GATEWAY: lambda: get_validated_input(
            "Enter Barcode 2 Gateway (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_BARCODE_3_GATEWAY: lambda: get_validated_input(
            "Enter Barcode 3 Gateway (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_BARCODE_4_GATEWAY: lambda: get_validated_input(
            "Enter Barcode 4 Gateway (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_POP_TYPE_CONFIG: lambda: get_validated_input(
            "Enter Pop Up Type (1: Ninety Degree, 2: Diverter Left, 3: Diverter Right, 4: Gateway): ",
            valid_range=range(0, 5)
        ),
        CMD_DEBUG_MODE_CONFIG: lambda: get_validated_input(
            "Enter Debug Mode (0: Disable, 1: UART, 3: Ethernet): ",
            valid_range=[0, 1, 3]
        ),
        CMD_DEBUG_DEVICE_IP_CONFIG: get_network_params,
        CMD_DEBUG_DEVICE_PORT_CONFIG: lambda: get_validated_input(
            "Enter Debug Device Port (1 : 65535): ",
            valid_range=range(1, 65536)
        ),
        CMD_S1_REVERSE_CMD: lambda: get_validated_input(
            "Enter S1 Reverse Command (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_S2_REVERSE_CMD: lambda: get_validated_input(
            "Enter S2 Reverse Command (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_S3_REVERSE_CMD: lambda: get_validated_input(
            "Enter S3 Reverse Command (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_S4_REVERSE_CMD: lambda: get_validated_input(
            "Enter S4 Reverse Command (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_S1_SLUG_FREE_DELAY_TIME: lambda: get_validated_input(
            "Enter S1 Slug Free Delay Time (0 : 65535): ",
            valid_range=range(0, 65536)
        ),
        CMD_S2_SLUG_FREE_DELAY_TIME: lambda: get_validated_input(
            "Enter S2 Slug Free Delay Time (0 : 65535): ",
            valid_range=range(0, 65536)
        ),
        CMD_S3_SLUG_FREE_DELAY_TIME: lambda: get_validated_input(
            "Enter S3 Slug Free Delay Time (0 : 65535): ",
            valid_range=range(0, 65536)
        ),
        CMD_S4_SLUG_FREE_DELAY_TIME: lambda: get_validated_input(
            "Enter S4 Slug Free Delay Time (0 : 65535): ",
            valid_range=range(0, 65536)
        ),
        CMD_TOTE_RETRY_TIME: lambda: get_validated_input(
            "Enter Tote Retry Time (0 : 65535): ",
            valid_range=range(0, 65536)
        ),
        CMD_S1_TOTE_CENTRE_TIMEOUT: lambda: get_validated_input(
            "Enter S1 Tote Centre Timeout (0 : 65535): ",
            valid_range=range(0, 65536)
        ),
        CMD_S2_TOTE_CENTRE_TIMEOUT: lambda: get_validated_input(
            "Enter S2 Tote Centre Timeout (0 : 65535): ",
            valid_range=range(0, 65536)
        ),
        CMD_S3_TOTE_CENTRE_TIMEOUT: lambda: get_validated_input(
            "Enter S3 Tote Centre Timeout (0 : 65535): ",
            valid_range=range(0, 65536)
        ),
        CMD_S4_TOTE_CENTRE_TIMEOUT: lambda: get_validated_input(
            "Enter S4 Tote Centre Timeout (0 : 65535): ",
            valid_range=range(0, 6553*6)
        ),
        CMD_STORE_PARAMETER: lambda: get_validated_input(
            "Enter Store Parameter (0: Disable, 1: Enable): ",
            valid_range=range(0, 2)
        ),
        CMD_PLC_LOAD_PRESENCE_FEEDBACK_UPDATE_TIME: lambda: get_validated_input(
            "Enter PLC Load Presence Feedback Update Time (0 : 65535): ",
            valid_range=range(0, 65536)
        ),
        CMD_SET_MQTT_BROKER_IP: get_network_params,
        CMD_SET_MQTT_BROKER_PORT: lambda: get_validated_input(
            "Enter MQTT Broker Port (1 : 65535): ",
            valid_range=range(1, 65536)
        ),
        CMD_SET_REQUEST_TOPIC: lambda: input("Enter MQTT Request Topic: ").strip(),
        CMD_SET_RESPONSE_TOPIC: lambda: input("Enter MQTT Response Topic: ").strip(),
        CMD_ENABLE_TOTE_TRACKING: lambda: get_validated_input(
            "Enter Tote Tracking Mode (0: Disable, 1: CAN, 2: Ethernet): ",
            valid_range=range(0, 3)
        )  
    }

    cmd_descriptions = {
        CMD_CAN_IN_OUT_CONFIG: "In/Out",
        CMD_TOTE_DEFAULT_OUT_CONFIG: "Tote Flow",
        CMD_WCS_RETRY_COUNTS_CONFIG: "Ethernet Retry Count",
        CMD_CONVEYOR_MODE_CONFIG: "Conveyor Mode",
        CMD_S1_CAN_ID_CONFIG: "S1 CAN ID",
        CMD_S2_CAN_ID_CONFIG: "S2 CAN ID",
        CMD_S3_CAN_ID_CONFIG: "S3 CAN ID",
        CMD_S4_CAN_ID_CONFIG: "S4 CAN ID",
        CMD_DIVERT_X_MOTOR_CONTROL_CAN_ID_CONFIG: "Divert-X Motor Control CAN ID",
        CMD_BARCODE_1_PORT_CONFIG: "Barcode 1 Port",
        CMD_BARCODE_2_PORT_CONFIG: "Barcode 2 Port",
        CMD_BARCODE_3_PORT_CONFIG: "Barcode 3 Port",
        CMD_BARCODE_4_PORT_CONFIG: "Barcode 4 Port",
        CMD_PARALLEL_TRANSFER_CONFIG: "Parallel Transfer",
        CMD_TOTE_REJECTION_FLOW_CONFIG: "Tote Rejection Flow",
        CMD_URL_CONFIG: "URL",
        CMD_DIVERT_X_IP_CONFIG: "Divert-X IP",
        CMD_DIVERT_X_SUBNET_CONFIG: "Divert-X Subnet",
        CMD_DIVERT_X_GATEWAY_CONFIG: "Divert-X Gateway",
        CMD_DEST_IP_CONFIG: "Destination IP",
        CMD_DEST_PORT_CONFIG: "Destination Port",
        CMD_ETH_MASTER_CONFIG: "Ethernet Master",
        CMD_RESET_POP_UP: "Reset Pop-Up",
        CMD_S1_CAN_GATEWAY: "S1 CAN Gateway",
        CMD_S2_CAN_GATEWAY: "S2 CAN Gateway",
        CMD_S3_CAN_GATEWAY: "S3 CAN Gateway",
        CMD_S4_CAN_GATEWAY: "S4 CAN Gateway",
        CMD_DIVERT_X_MOTOR_CONTROL_GATEWAY: "Divert-X Motor Control Gateway",
        CMD_BARCODE_1_GATEWAY: "Barcode 1 Gateway",
        CMD_BARCODE_2_GATEWAY: "Barcode 2 Gateway",
        CMD_BARCODE_3_GATEWAY: "Barcode 3 Gateway",
        CMD_BARCODE_4_GATEWAY: "Barcode 4 Gateway",
        CMD_POP_TYPE_CONFIG: "Pop-Up Type",
        CMD_DEBUG_MODE_CONFIG: "Debug Mode",
        CMD_DEBUG_DEVICE_IP_CONFIG: "Debug Device IP",
        CMD_DEBUG_DEVICE_PORT_CONFIG: "Debug Device Port",
        CMD_S1_REVERSE_CMD: "S1 Reverse Command",
        CMD_S2_REVERSE_CMD: "S2 Reverse Command",
        CMD_S3_REVERSE_CMD: "S3 Reverse Command",
        CMD_S4_REVERSE_CMD: "S4 Reverse Command",
        CMD_S1_SLUG_FREE_DELAY_TIME: "S1 Slug Free Delay Time",
        CMD_S2_SLUG_FREE_DELAY_TIME: "S2 Slug Free Delay Time",
        CMD_S3_SLUG_FREE_DELAY_TIME: "S3 Slug Free Delay Time",
        CMD_S4_SLUG_FREE_DELAY_TIME: "S4 Slug Free Delay Time",
        CMD_TOTE_RETRY_TIME: "Tote Retry Time",
        CMD_S1_TOTE_CENTRE_TIMEOUT: "S1 Tote Centre Timeout",
        CMD_S2_TOTE_CENTRE_TIMEOUT: "S2 Tote Centre Timeout",
        CMD_S3_TOTE_CENTRE_TIMEOUT: "S3 Tote Centre Timeout",
        CMD_S4_TOTE_CENTRE_TIMEOUT: "S4 Tote Centre Timeout",
        CMD_STORE_PARAMETER: "Store Parameter",
        CMD_PLC_LOAD_PRESENCE_FEEDBACK_UPDATE_TIME: "PLC Load Presence Feedback Update Time",
        CMD_SET_MQTT_BROKER_IP: "Set MQTT Broker IP",
        CMD_SET_MQTT_BROKER_PORT: "Set MQTT Broker Port",
        CMD_SET_REQUEST_TOPIC: "Set Request Topic",
        CMD_SET_RESPONSE_TOPIC: "Set Response Topic",
        CMD_ENABLE_TOTE_TRACKING: "Enable Tote Tracking",
    }

    # === Motor Parameter Handlers ===
    motor_param_handlers = {
        CMD_MOTOR_RPM: lambda: get_validated_input("Enter Motor RPM (50–395): ", range(50, 396)),
        CMD_MOTOR_ACCELERATION: lambda: get_validated_input("Enter Acceleration (0–10000): ", range(0, 10001)),
        CMD_MOTOR_DECELERATION: lambda: get_validated_input("Enter Deceleration (0–10000): ", range(0, 10001)),
        CMD_MOTOR_DIRECTION: lambda: get_validated_input("Enter Direction (0: Clockwise, 1: Anticlockwise): ", [0, 2]),
        CMD_STOP_TIME: lambda: get_validated_input("Enter Stop Time (ms, 0–60000): ", range(0, 60001)),
        CMD_EMPTY_STOP_TIME: lambda: get_validated_input("Enter Empty Stop Time (ms, 0–60000): ", range(0, 60001)),
        CMD_RESET_DEVICE: lambda: get_validated_input("Reset Device (1: Reset): ", range(0, 2)),
        CMD_MOTOR_OC: lambda: get_validated_input("Enter Overcurrent Threshold (1000–15000): ", range(1000, 15001)),
        CMD_MOTOR_SUDDEN_STOP: lambda: get_validated_input("Enter Sudden Stop Command (0: Disable - 1: Enable): ", range(0, 2)),
        CMD_MOTOR_UV: lambda: get_validated_input("Enter Undervoltage Threshold (3–22): ", range(3, 23)),
        CMD_MOTOR_OV: lambda: get_validated_input("Enter Overvoltage Threshold (22-30): ", range(22, 31)),
        CMD_MOTOR_TICKS: lambda: get_validated_input("Enter Ticks (0–65500): ", range(0, 65501)),
        CMD_STORE_PARAMS: lambda: get_validated_input("Store Parameters (0: Disable - 1: Enable): ", range(0, 2)),
    }

    motor_param_descriptions = {
        CMD_MOTOR_RPM: "Motor RPM",
        CMD_MOTOR_ACCELERATION: "Acceleration",
        CMD_MOTOR_DECELERATION: "Deceleration",
        CMD_STOP_TIME: "Stop Time",
        CMD_EMPTY_STOP_TIME: "Empty Stop Time",
        CMD_RESET_DEVICE: "Reset Device",
        CMD_MOTOR_OC: "Motor Overcurrent",
        CMD_MOTOR_SUDDEN_STOP: "Motor Sudden Stop",
        CMD_MOTOR_UV: "Motor Undervoltage",
        CMD_MOTOR_OV: "Motor Overvoltage",
        CMD_MOTOR_TICKS: "Motor Ticks",
        CMD_STORE_PARAMS: "Store Parameters",    
    }

    conveyor_param_descriptions = {
        CMD_SET_RPM : "Motor RPM",
        CMD_SET_ACCELERATION : "Acceleration",
        CMD_SET_DECELERATION : "Deceleration",
        CMD_SET_MOTOR_DIRECTION : "Motor Direction",
        CMD_SET_TOTAL_CARDS : "Total Cards",
        CMD_SET_CONVEYOR_MODE : "Conveyor Mode",
        CMD_SET_STOP_TIME: "Stop Time",
        CMD_SET_EMPTY_STOP_TIME: "Empty Stop Time",
        CMD_SET_ERROR_DESTINATION_ADDRESS: "Error Destination Address",
        CMD_SET_UNIQUE_ID: "Unique ID",
        CMD_SET_ADDRESSING_MODE: "Addressing Mode",
        CMD_RESET_DEVICE: "Reset Device",
        CMD_SET_MOTOR_ON_TH: "Motor On Threshold",
        CMD_SET_DEBUG_MODE: "Debug Mode",
        CMD_SET_SUDDEN_STOP: "Sudden Stop",
        CMD_SET_LOW_VOLTAGE_TH: "Low Voltage Threshold",
        CMD_SET_HIGH_VOLTAGE_TH: "High Voltage Threshold",
        CMD_SET_CRATE_JAM_TIME: "Crate Jam Time",
        CMD_SET_MOTOR_TICKS_TH: "Motor Ticks Threshold",
        CMD_SET_MERGER_MODE: "Merger Mode",
        CMD_SET_GRAVITY_MODE: "Gravity Mode",
        CMD_SET_CAN_RETRY_TIME: "CAN Retry Time",
        CMD_SET_SLUG_CRATE_JAM_TICKS: "Slug Crate Jam Ticks",
        CMD_SET_SLUG_NEAR_BOX_TICKS: "Slug Near Box Ticks",
        CMD_SET_BOX_PASS_TIME_TH: "Box Pass Time Threshold",
        CMD_SET_CURRENT_PRINT: "Current Print",
        CMD_SET_VOLTAGE_PRINT: "Voltage Print",
        CMD_SET_RPM_PRINT: "RPM Print",
        CMD_SET_CROSSOVER_MODE: "Crossover Mode", 
        CMD_SET_REVERSE_MODE: "Reverse Mode",
        CMD_SET_SENSOR_MODE: "Sensor Mode",
        CMD_SET_STORE_PARAMETERS: "Store Parameters",
        CMD_SET_LOG_LEVEL: "Log Level",
        CMD_SET_MODBUS_MODE: "Modbus Mode",
        CMD_SET_BAUDRATE: "Baudrate",
        CMD_SET_PLC_MOTOR_CONTROL_STOP_TIME: "PLC Motor Control Stop Time",
        CMD_SET_DELAY_SLUG_FREE_TIME: "Delay Slug Free Time",
        CMD_SET_ERROR_SIGNAL_MODE: "Error Signal Mode",
        CMD_SET_RESET_SIGNAL_MODE: "Reset Signal Mode", 
    }

    conveyor_param_descriptions_check = {
        CMD_CHECK_RPM: "Motor RPM",
        CMD_CHECK_ACCELERATION: "Acceleration",
        CMD_CHECK_DECELERATION: "Deceleration",
        CMD_CHECK_MOTOR_DIRECTION: "Motor Direction",
        CMD_CHECK_TOTAL_CARDS: "Total Cards",
        CMD_CHECK_CONVEYOR_MODE: "Conveyor Mode",
        CMD_CHECK_STOP_TIME: "Stop Time",
        CMD_CHECK_EMPTY_STOP_TIME: "Empty Stop Time",
        CMD_CHECK_ERROR_DESTINATION_ADDRESS: "Error Destination Address",
        CMD_CHECK_MOTOR_ON_TH: "Motor On Threshold",
        CMD_CHECK_DEBUG_MODE: "Debug Mode",
        CMD_CHECK_SUDDEN_STOP: "Sudden Stop",
        CMD_CHECK_LOW_VOLTAGE_TH: "Low Voltage Threshold",
        CMD_CHECK_HIGH_VOLTAGE_TH: "High Voltage Threshold",
        CMD_CHECK_CRATE_JAM_TIME: "Crate Jam Time",
        CMD_CHECK_MOTOR_TICKS_TH: "Motor Ticks Threshold",
        CMD_CHECK_MERGER_MODE: "Merger Mode",
        CMD_CHECK_GRAVITY_MODE: "Gravity Mode",
        CMD_CHECK_CAN_RETRY_TIME: "CAN Retry Time",
        CMD_CHECK_SLUG_CRATE_JAM_TICKS: "Slug Crate Jam Ticks",
        CMD_CHECK_SLUG_NEAR_BOX_TICKS: "Slug Near Box Ticks",
        CMD_CHECK_BOX_PASS_TIME_TH: "Box Pass Time Threshold",
        CMD_CHECK_CROSSOVER_MODE: "Crossover Mode", 
        CMD_CHECK_REVERSE_MODE: "Reverse Mode",
        CMD_CHECK_SENSOR_MODE: "Sensor Mode",
        CMD_CHECK_STORE_PARAMETERS: "Store Parameters",
        CMD_CHECK_FIRMWARE_VERSION: "Firmware Version",
        CMD_CHECK_LOG_LEVEL: "Log Level",
        CMD_CHECK_MODBUS_MODE: "Modbus Mode",
        CMD_CHECK_BAUDRATE: "Baudrate",
        CMD_CHECK_PLC_MOTOR_CONTROL_STOP_TIME: "PLC Motor Control Stop Time",
        CMD_CHECK_DELAY_SLUG_FREE_TIME: "Delay Slug Free Time",
        CMD_CHECK_ERROR_SIGNAL_MODE: "Error Signal Mode",
        CMD_CHECK_RESET_SIGNAL_MODE: "Reset Signal Mode"
    }


    conveyor_param_handlers = {
        CMD_SET_RPM: lambda: get_validated_input("Enter Motor RPM (50–395): ", range(50, 396)),
        CMD_SET_ACCELERATION: lambda: get_validated_input("Enter Acceleration (250–10000): ", range(250, 10001)),
        CMD_SET_DECELERATION: lambda: get_validated_input("Enter Deceleration (250–10000): ", range(250, 10001)),
        CMD_SET_MOTOR_DIRECTION: lambda: get_validated_input("Enter Direction (0: Clockwise, 1: Anticlockwise): ", [0, 2]),
        CMD_SET_STOP_TIME: lambda: get_validated_input("Enter Stop Time (0–60000): ", range(0, 60001)),
        CMD_SET_EMPTY_STOP_TIME: lambda: get_validated_input("Enter Empty Stop Time (0–60000): ", range(0, 60001)),
        CMD_SET_ERROR_DESTINATION_ADDRESS: lambda: get_validated_input("Enter Error Destination Address (0–255): ", range(0, 256)),
        CMD_SET_UNIQUE_ID: lambda: get_validated_input("Enter Unique ID (0–255): ", range(0, 256)),
        CMD_SET_ADDRESSING_MODE: lambda: get_validated_input("Enter Addressing Mode (0: Disable, 1: Enable): ", [0, 1]),
        CMD_RESET_DEVICE: lambda: get_validated_input("Reset Device (1: Reset): ", range(0, 2)),
        CMD_SET_TOTAL_CARDS: lambda: get_validated_input("Enter Total Cards (0–255): ", range(0, 256)),
        CMD_SET_CONVEYOR_MODE: lambda: get_validated_input("Enter Conveyor Mode (1: Singulated, 2: Slug, 3: Disable): ", range(1, 4)),
        CMD_SET_MOTOR_ON_TH: lambda: get_validated_input("Enter Motor On Threshold (0–10000): ", range(0, 10001)),
        CMD_SET_DEBUG_MODE: lambda: get_validated_input("Enter Debug Mode (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_SUDDEN_STOP: lambda: get_validated_input("Enter Sudden Stop Command (0: Disable - 1: Enable): ", range(0, 2)),
        CMD_SET_LOW_VOLTAGE_TH: lambda: get_validated_input("Enter Low Voltage Threshold (3–22): ", range(3, 23)),
        CMD_SET_HIGH_VOLTAGE_TH: lambda: get_validated_input("Enter High Voltage Threshold (22-30): ", range(22, 31)),
        CMD_SET_CRATE_JAM_TIME: lambda: get_validated_input("Enter Crate Jam Time (0–60000): ", range(0, 60001)),
        CMD_SET_MOTOR_TICKS_TH: lambda: get_validated_input("Enter Motor Ticks Threshold (0–65500): ", range(0, 65501)),
        CMD_SET_MERGER_MODE: lambda: get_validated_input("Enter Merger Mode (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_GRAVITY_MODE: lambda: get_validated_input("Enter Gravity Mode (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_CAN_RETRY_TIME: lambda: get_validated_input("Enter CAN Retry Time (0–65535): ", range(0, 65536)),
        CMD_SET_SLUG_CRATE_JAM_TICKS: lambda: get_validated_input("Enter Slug Crate Jam Ticks (0–65500): ", range(0, 65501)),
        CMD_SET_SLUG_NEAR_BOX_TICKS: lambda: get_validated_input("Enter Slug Near Box Ticks (0–65500): ", range(0, 65501)),
        CMD_SET_BOX_PASS_TIME_TH: lambda: get_validated_input("Enter Box Pass Time Threshold (0–65500): ", range(0, 65501)),
        CMD_SET_CURRENT_PRINT: lambda: get_validated_input("Enter Current Print (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_VOLTAGE_PRINT: lambda: get_validated_input("Enter Voltage Print (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_RPM_PRINT: lambda: get_validated_input("Enter RPM Print (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_CROSSOVER_MODE: lambda: get_validated_input("Enter Crossover Mode (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_REVERSE_MODE: lambda: get_validated_input("Enter Reverse Mode (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_SENSOR_MODE: lambda: get_validated_input("Enter Sensor Mode (0: Dark, 1: Light): ", [0, 1]),
        CMD_SET_STORE_PARAMETERS: lambda: get_validated_input("Store Parameters (0: Disable - 1: Enable): ", range(0, 2)),
        CMD_SET_LOG_LEVEL: lambda: get_validated_input("Enter Log Level (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_MODBUS_MODE: lambda: get_validated_input("Enter Modbus Mode (0: Disable, 1: Enable): ", [0, 1]),
        CMD_SET_BAUDRATE: lambda: get_validated_input("Enter Baudrate (0: 9600, 1: 115200): ", [0, 1]),
        CMD_SET_PLC_MOTOR_CONTROL_STOP_TIME: lambda: get_validated_input("Enter PLC Motor Control Stop Time (0–65535): ", range(0, 65536)),
        CMD_SET_DELAY_SLUG_FREE_TIME: lambda: get_validated_input("Enter Delay Slug Free Time (0–65535): ", range(0, 65536)),
        CMD_SET_ERROR_SIGNAL_MODE: lambda: get_validated_input("Enter Error Signal Mode (0: Stable, 1: Pulsating): ", [0, 1]),
        CMD_SET_RESET_SIGNAL_MODE: lambda: get_validated_input("Enter Reset Signal Mode (0: Stable, 1: Pulsating): ", [0, 1]),
    }

    try:
        while True:
            print(Fore.YELLOW + "\nAvailable Commands:" + Style.RESET_ALL)
            for key, val in SELECTIONS.items():
                print(Fore.GREEN + f"{key}. {val}" + Style.RESET_ALL)

            try:
                selection = int(input(Fore.CYAN + "Choose an option: " + Style.RESET_ALL))
                
                # Handle the new configuration from file option
                if selection == SELECTION_CONFIGURE_WITH_FILE:
                    config = load_configuration_file()
                    if config:
                        print(Fore.BLUE + "[✓] Configuration loaded successfully!" + Style.RESET_ALL)
                        # Apply the loaded configuration
                        print(Fore.YELLOW + "\n[!] Applying configuration to the device..." + Style.RESET_ALL)
                        if apply_config(sock, config):
                            print(Fore.GREEN + "[✓] Configuration applied successfully!" + Style.RESET_ALL)
                            time.sleep(0.2)
                            print(Fore.MAGENTA + "[SYS]  Resetting..." + Style.RESET_ALL)
                            send_can_command(sock, '00000a170001')
                        else:
                            print(Fore.RED + "[x] Failed to apply configuration" + Style.RESET_ALL)
                    continue
            except ValueError:
                print(Fore.RED + "[x] Invalid selection. Choose a number." + Style.RESET_ALL)
                continue

            if selection == SELECTION_SET_SINGLE_PARAM:
                decesion_type = CMD_TYPE_SET_POP_UP_CONFIG
                print(Fore.YELLOW + "\n[?] Available Config Commands:" + Style.RESET_ALL)
                print(Fore.GREEN + "1. In/Out" + Style.RESET_ALL)
                print(Fore.GREEN + "2. Tote Flow" + Style.RESET_ALL)
                print(Fore.GREEN + "3. Ethernet Retry Count" + Style.RESET_ALL)
                print(Fore.GREEN + "4. Conveyor Mode" + Style.RESET_ALL)
                print(Fore.GREEN + "5. S1 CAN ID" + Style.RESET_ALL)
                print(Fore.GREEN + "6. S2 CAN ID" + Style.RESET_ALL)
                print(Fore.GREEN + "7. S3 CAN ID" + Style.RESET_ALL)
                print(Fore.GREEN + "8. S4 CAN ID" + Style.RESET_ALL)
                print(Fore.GREEN + "9. Divert-X Motor Control CAN ID" + Style.RESET_ALL)
                print(Fore.GREEN + "10. Barcode 1 Port" + Style.RESET_ALL)
                print(Fore.GREEN + "11. Barcode 2 Port" + Style.RESET_ALL)
                print(Fore.GREEN + "12. Barcode 3 Port" + Style.RESET_ALL)
                print(Fore.GREEN + "13. Barcode 4 Port" + Style.RESET_ALL)
                print(Fore.GREEN + "14. Parallel Transfer" + Style.RESET_ALL)
                print(Fore.GREEN + "15. Tote Rejection Flow" + Style.RESET_ALL)
                print(Fore.GREEN + "16. URL" + Style.RESET_ALL)
                print(Fore.GREEN + "17. Divert-X IP" + Style.RESET_ALL)
                print(Fore.GREEN + "18. Divert-X Subnet" + Style.RESET_ALL)
                print(Fore.GREEN + "19. Divert-X Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "20. Destination IP" + Style.RESET_ALL)
                print(Fore.GREEN + "21. Destination Port" + Style.RESET_ALL)
                print(Fore.GREEN + "22. Ethernet Master" + Style.RESET_ALL)
                print(Fore.GREEN + "23. Reset Pop Up" + Style.RESET_ALL)
                print(Fore.GREEN + "24. S1 CAN Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "25. S2 CAN Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "26. S3 CAN Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "27. S4 CAN Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "28. Divert-X Motor Control Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "29. Barcode 1 Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "30. Barcode 2 Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "31. Barcode 3 Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "32. Barcode 4 Gateway" + Style.RESET_ALL)
                print(Fore.GREEN + "33. Pop Up Type" + Style.RESET_ALL)
                print(Fore.GREEN + "34. Debug Mode" + Style.RESET_ALL)
                print(Fore.GREEN + "35. Debug Device IP" + Style.RESET_ALL)
                print(Fore.GREEN + "36. Debug Device Port" + Style.RESET_ALL)
                print(Fore.GREEN + "37. S1 Reverse Command" + Style.RESET_ALL)
                print(Fore.GREEN + "38. S2 Reverse Command" + Style.RESET_ALL)
                print(Fore.GREEN + "39. S3 Reverse Command" + Style.RESET_ALL)
                print(Fore.GREEN + "40. S4 Reverse Command" + Style.RESET_ALL)
                print(Fore.GREEN + "41. S1 Slug Free Delay Time" + Style.RESET_ALL)
                print(Fore.GREEN + "42. S2 Slug Free Delay Time" + Style.RESET_ALL)
                print(Fore.GREEN + "43. S3 Slug Free Delay Time" + Style.RESET_ALL)
                print(Fore.GREEN + "44. S4 Slug Free Delay Time" + Style.RESET_ALL)
                print(Fore.GREEN + "45. Tote Retry Time" + Style.RESET_ALL)
                print(Fore.GREEN + "46. S1 Tote Centre Timeout" + Style.RESET_ALL)
                print(Fore.GREEN + "47. S2 Tote Centre Timeout" + Style.RESET_ALL)
                print(Fore.GREEN + "48. S3 Tote Centre Timeout" + Style.RESET_ALL)
                print(Fore.GREEN + "49. S4 Tote Centre Timeout" + Style.RESET_ALL)
                print(Fore.GREEN + "50. Store Parameter" + Style.RESET_ALL)
                print(Fore.GREEN + "51. PLC Load Presence Feedback Update Time" + Style.RESET_ALL)
                print(Fore.GREEN + "55. Set MQTT Broker IP" + Style.RESET_ALL)
                print(Fore.GREEN + "57. Set MQTT Broker Port" + Style.RESET_ALL)
                print(Fore.GREEN + "58. Set REquest Topic" + Style.RESET_ALL)
                print(Fore.GREEN + "59. Set Responce Topic" + Style.RESET_ALL)
                print(Fore.GREEN + "56. Enable Tote Tracking" + Style.RESET_ALL)

                cmd_type = int(input(Fore.CYAN + "Enter Config Command (e.g., 1 for In/Out): " + Style.RESET_ALL))
                param_list = None

                if cmd_type in cmd_handlers:
                    param_list = cmd_handlers[cmd_type]()
                else:
                    print(Fore.RED + "[x] Invalid command type. Command not sent." + Style.RESET_ALL)
                    continue

                if param_list is not None:
                    command = generate_command_with_flexibility(0, 0, param_list, cmd_type, decesion_type)
                    if cmd_type == 50:
                        print(Fore.BLUE + f"[CMD] Sending Store Parameter command: {command}" + Style.RESET_ALL)
                    send_can_command(sock, command)
                else:
                    print(Fore.RED + "[x] Invalid parameters. Command not sent." + Style.RESET_ALL)

            elif selection == SELECTION_SET_ALL_PARAM:
                decesion_type = CMD_TYPE_SET_POP_UP_CONFIG
                print(Fore.YELLOW + "\n[?] Setting all parameters..." + Style.RESET_ALL)

                # Map command types to descriptive names
                cmd_descriptions = {
                    CMD_CAN_IN_OUT_CONFIG: "In/Out",
                    CMD_TOTE_DEFAULT_OUT_CONFIG: "Tote Flow",
                    CMD_WCS_RETRY_COUNTS_CONFIG: "Ethernet Retry Count",
                    CMD_CONVEYOR_MODE_CONFIG: "Conveyor Mode",
                    CMD_S1_CAN_ID_CONFIG: "S1 CAN ID",
                    CMD_S2_CAN_ID_CONFIG: "S2 CAN ID",
                    CMD_S3_CAN_ID_CONFIG: "S3 CAN ID",
                    CMD_S4_CAN_ID_CONFIG: "S4 CAN ID",
                    CMD_DIVERT_X_MOTOR_CONTROL_CAN_ID_CONFIG: "Divert-X Motor Control CAN ID",
                    CMD_BARCODE_1_PORT_CONFIG: "Barcode 1 Port",
                    CMD_BARCODE_2_PORT_CONFIG: "Barcode 2 Port",
                    CMD_BARCODE_3_PORT_CONFIG: "Barcode 3 Port",
                    CMD_BARCODE_4_PORT_CONFIG: "Barcode 4 Port",
                    CMD_PARALLEL_TRANSFER_CONFIG: "Parallel Transfer",
                    CMD_TOTE_REJECTION_FLOW_CONFIG: "Tote Rejection Flow",
                    CMD_URL_CONFIG: "URL",
                    CMD_DIVERT_X_IP_CONFIG: "Divert-X IP",
                    CMD_DIVERT_X_SUBNET_CONFIG: "Divert-X Subnet",
                    CMD_DIVERT_X_GATEWAY_CONFIG: "Divert-X Gateway",
                    CMD_DEST_IP_CONFIG: "Destination IP",
                    CMD_DEST_PORT_CONFIG: "Destination Port",
                    CMD_ETH_MASTER_CONFIG: "Ethernet Master",
                    CMD_RESET_POP_UP: "Reset Pop-Up",
                    CMD_S1_CAN_GATEWAY: "S1 CAN Gateway",
                    CMD_S2_CAN_GATEWAY: "S2 CAN Gateway",
                    CMD_S3_CAN_GATEWAY: "S3 CAN Gateway",
                    CMD_S4_CAN_GATEWAY: "S4 CAN Gateway",
                    CMD_DIVERT_X_MOTOR_CONTROL_GATEWAY: "Divert-X Motor Control Gateway",
                    CMD_BARCODE_1_GATEWAY: "Barcode 1 Gateway",
                    CMD_BARCODE_2_GATEWAY: "Barcode 2 Gateway",
                    CMD_BARCODE_3_GATEWAY: "Barcode 3 Gateway",
                    CMD_BARCODE_4_GATEWAY: "Barcode 4 Gateway",
                    CMD_POP_TYPE_CONFIG: "Pop-Up Type",
                    CMD_DEBUG_MODE_CONFIG: "Debug Mode",
                    CMD_DEBUG_DEVICE_IP_CONFIG: "Debug Device IP",
                    CMD_DEBUG_DEVICE_PORT_CONFIG: "Debug Device Port",
                    CMD_S1_REVERSE_CMD: "S1 Reverse Command",
                    CMD_S2_REVERSE_CMD: "S2 Reverse Command",
                    CMD_S3_REVERSE_CMD: "S3 Reverse Command",
                    CMD_S4_REVERSE_CMD: "S4 Reverse Command",
                    CMD_S1_SLUG_FREE_DELAY_TIME: "S1 Slug Free Delay Time",
                    CMD_S2_SLUG_FREE_DELAY_TIME: "S2 Slug Free Delay Time",
                    CMD_S3_SLUG_FREE_DELAY_TIME: "S3 Slug Free Delay Time",
                    CMD_S4_SLUG_FREE_DELAY_TIME: "S4 Slug Free Delay Time",
                    CMD_TOTE_RETRY_TIME: "Tote Retry Time",
                    CMD_S1_TOTE_CENTRE_TIMEOUT: "S1 Tote Centre Timeout",
                    CMD_S2_TOTE_CENTRE_TIMEOUT: "S2 Tote Centre Timeout",
                    CMD_S3_TOTE_CENTRE_TIMEOUT: "S3 Tote Centre Timeout",
                    CMD_S4_TOTE_CENTRE_TIMEOUT: "S4 Tote Centre Timeout",
                    CMD_STORE_PARAMETER: "Store Parameter",
                    CMD_PLC_LOAD_PRESENCE_FEEDBACK_UPDATE_TIME: "PLC Load Presence Feedback Update Time",
                    CMD_SET_MQTT_BROKER_IP: "Set MQTT Broker IP",
                    CMD_SET_MQTT_BROKER_PORT: "Set MQTT Broker Port",
                    CMD_SET_REQUEST_TOPIC: "Set Request Topic",
                    CMD_SET_RESPONSE_TOPIC: "Set Response Topic",
                    CMD_ENABLE_TOTE_TRACKING: "Enable Tote Tracking",
                }

                for cmd_type, handler in cmd_handlers.items():
                    if cmd_type != CMD_RESET_POP_UP:
                        try:
                            # Get the description for the command type
                            description = cmd_descriptions.get(cmd_type, f"Unknown Command Type {cmd_type:02X}")

                            # Ask the user if they want to configure this command type
                            skip = input(Fore.CYAN + f"\n[?] Do you want to configure {description}? (y/n): " + Style.RESET_ALL).strip().lower()
                            if skip == 'n' or skip == 'no':
                                print(Fore.YELLOW + f"[!] Skipping {description}." + Style.RESET_ALL)
                                continue  # Skip this command type

                            print(Fore.GREEN + f"[?] Configuring {description}..." + Style.RESET_ALL)
                            param_list = handler()  # Call the handler function for the command
                            if param_list is not None:
                                command = generate_command_with_flexibility(0, 0, param_list, cmd_type, decesion_type)
                                send_can_command(sock, command)
                            else:
                                print(Fore.RED + f"[x] Skipping {description} due to invalid input." + Style.RESET_ALL)
                        except Exception as e:
                            print(Fore.RED + f"[x] Error while processing {description}: {e}" + Style.RESET_ALL)
            elif selection == SELECTION_CHECK_SINGLE_PARAM:
                decesion_type = CMD_TYPE_CHECK_POP_UP_CONFIG
                print(Fore.YELLOW + "\n[?] Available Commands:" + Style.RESET_ALL)
                for cmd_type, description in cmd_descriptions.items():
                    if cmd_type != CMD_RESET_POP_UP:
                        print(Fore.GREEN + f"{cmd_type:02d}. {description}" + Style.RESET_ALL)
                if cmd_type != CMD_RESET_POP_UP:
                    try:
                        cmd_type = int(input(Fore.CYAN + "Enter Command (e.g., 1 for In/Out): " + Style.RESET_ALL))
                        if cmd_type not in cmd_handlers:
                            print(Fore.RED + "[x] Invalid command type. Command not sent." + Style.RESET_ALL)
                            return

                        # Generate and send the command
                        command = generate_command_with_flexibility(0, 0, None, cmd_type, decesion_type)
                        send_can_command(sock, command)

                        # Wait for a response
                        sock.settimeout(5)  # Set timeout to 5 seconds
                        response = sock.recv(1024).decode("utf-8").strip()

                        # Parse the response
                        try:
                            response_data = json.loads(response)
                            ip = response_data.get("IP", "Unknown IP")
                            system_code = response_data.get("SYSTEM_CODE", "Unknown SYSTEM_CODE")
                            parse_system_code(system_code)
                        except json.JSONDecodeError:
                            print(Fore.RED + "[x] Failed to parse JSON response." + Style.RESET_ALL)

                    except socket.timeout:
                        print(Fore.RED + "[x] No response received. The server might be busy or unresponsive." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"[x] Error while receiving response: {e}" + Style.RESET_ALL)

            elif selection == SELECTION_CHECK_ALL_PARAM:
                decesion_type = CMD_TYPE_CHECK_POP_UP_CONFIG
                print(Fore.YELLOW + "\n[?] Checking all parameters..." + Style.RESET_ALL)

                for cmd_type, description in cmd_descriptions.items():
                    try:
                        if cmd_type != CMD_RESET_POP_UP:
                            print(Fore.GREEN + f"[?] Checking {description}..." + Style.RESET_ALL)

                            # Generate and send the command
                            command = generate_command_with_flexibility(0, 0, None, cmd_type, decesion_type)
                            send_can_command(sock, command)

                            # Wait for a response
                            sock.settimeout(5)  # Set timeout to 5 seconds
                            response = sock.recv(1024).decode("utf-8").strip()

                            # Parse the response
                            try:
                                response_data = json.loads(response)
                                ip = response_data.get("IP", "Unknown IP")
                                system_code = response_data.get("SYSTEM_CODE", "Unknown SYSTEM_CODE")
                                parse_system_code(system_code)
                            except json.JSONDecodeError:
                                print(Fore.RED + f"[x] Failed to parse JSON response for {description}." + Style.RESET_ALL)

                    except socket.timeout:
                        print(Fore.RED + f"[x] No response received for {description}. The server might be busy or unresponsive." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"[x] Error while processing {description}: {e}" + Style.RESET_ALL)
            elif selection == SELECTION_SET_DIVERT_X_HEALTH_CHECK:
                decesion_type = CMD_TYPE_HEALTH_CHECK
                print(Fore.YELLOW + "\n[?] Divert-X Health Check..." + Style.RESET_ALL)
                    
                # Map command types to descriptive names
                cmd_health_check_descriptions = {
                    CMD_CHECK_DIVERT_X_ERROR: "Divert-X Error"
                }

                for cmd_type, description in cmd_health_check_descriptions.items():
                    try:
                        print(Fore.GREEN + f"[?] Checking {description}..." + Style.RESET_ALL)

                        # Generate and send the command
                        print(Fore.GREEN + f"[?] Checking 1... {cmd_type}" + Style.RESET_ALL)

                        command = generate_command_with_flexibility(0, 0, None, cmd_type, decesion_type)
                        print(Fore.GREEN + f"[?] Checking 2..." + Style.RESET_ALL)
                        send_can_command(sock, command)
                        

                        # Wait for a response
                        sock.settimeout(5)  # Set timeout to 5 seconds
                        response = sock.recv(1024).decode("utf-8").strip()
                        print(Fore.GREEN + f"[?] Received response: {response}" + Style.RESET_ALL)
                        # Parse the response
                        try:
                            response_data = json.loads(response)
                            ip = response_data.get("IP", "Unknown IP")
                            system_code = response_data.get("SYSTEM_CODE", "Unknown SYSTEM_CODE")
                            parse_system_code(system_code)
                        except json.JSONDecodeError:
                            print(Fore.RED + f"[x] Failed to parse JSON response for {description}." + Style.RESET_ALL)

                    except socket.timeout:
                        print(Fore.RED + f"[x] No response received for {description}. The server might be busy or unresponsive." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"[x] Error while processing {description}: {e}" + Style.RESET_ALL)


            elif selection == SELECTION_SET_DIVERT_X_MOTOR_PARAM_SINGLE:
                decesion_type = CMD_TYPE_SET_CONFIG
                motor_type = get_motor_type()
                print(Fore.GREEN + f"Selected Motor Type: {motor_type}" + Style.RESET_ALL)

                print(Fore.YELLOW + "\n[?] Available Config Commands:" + Style.RESET_ALL)
                for cmd_type, description in motor_param_descriptions.items():
                    print(Fore.GREEN + f"{cmd_type}. {description}" + Style.RESET_ALL)
                try:
                    
                    conveyor_side = 5;  # Default value for Divert-X Motor side
                   
                    cmd_type = int(input(Fore.CYAN + "Enter Config Command: " + Style.RESET_ALL))
                    if cmd_type not in motor_param_handlers:
                        print(Fore.RED + "[x] Invalid motor command type." + Style.RESET_ALL)
                        continue
                    param = motor_param_handlers[cmd_type]()
                    if param is not None:
                        command = generate_command_with_flexibility(conveyor_side, motor_type, param, cmd_type, decesion_type)
                        send_can_command(sock, command)
                    else:
                        print(Fore.RED + "[x] Invalid input. Command not sent." + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)

            elif selection == SELECTION_SET_DIVERT_X_MOTOR_PARAM_ALL:
                decesion_type = CMD_TYPE_SET_CONFIG
                print(Fore.YELLOW + "\n[?] Setting all motor parameters..." + Style.RESET_ALL)

                motor_type = get_motor_type()
                print(Fore.GREEN + f"Selected Motor Type: {motor_type}" + Style.RESET_ALL)

                conveyor_side = 5  # Default value for Divert-X Motor side

                for cmd_type, description in motor_param_descriptions.items():
                    if cmd_type != CMD_RESET_DEVICE:
                        # Ask the user if they want to configure this parameter
                        user_input = input(Fore.CYAN + f"\n[?] Do you want to configure '{description}'? (y/n): " + Style.RESET_ALL).strip().lower()
                        
                        if user_input in ['n', 'no']:
                            print(Fore.YELLOW + f"[!] Skipping {description}." + Style.RESET_ALL)
                            continue

                        print(Fore.GREEN + f"[?] Configuring {description}..." + Style.RESET_ALL)
                        
                        try:
                            param = motor_param_handlers[cmd_type]()  # Get parameter value from handler
                            if param is not None:
                                command = generate_command_with_flexibility(conveyor_side, motor_type, param, cmd_type, decesion_type)
                                send_can_command(sock, command)
                            else:
                                print(Fore.RED + f"[x] Skipping {description} due to invalid input." + Style.RESET_ALL)
                        except Exception as e:
                            print(Fore.RED + f"[x] Error while setting {description}: {e}" + Style.RESET_ALL)
            elif selection == SELECTION_CHECK_DIVERT_X_MOTOR_PARAM_SINGLE:
                decesion_type = CMD_TYPE_CHECK_CONFIG
                motor_type = get_motor_type()
                print(Fore.GREEN + f"Selected Motor Type: {motor_type}" + Style.RESET_ALL)

                conveyor_side = 5;  # Default value for Divert-X Motor side
                print(Fore.YELLOW + "\n[?] Available Motor Check Commands:" + Style.RESET_ALL)
                for cmd_type, description in motor_param_descriptions.items():
                    print(Fore.GREEN + f"{cmd_type:02d}. {description}" + Style.RESET_ALL)
                try:
                    cmd_type = int(input(Fore.CYAN + "Enter Motor Check Command: " + Style.RESET_ALL))
                    if cmd_type != CMD_RESET_DEVICE:
                        if cmd_type not in motor_param_descriptions:
                            print(Fore.RED + "[x] Invalid command type." + Style.RESET_ALL)
                            continue
                        command = generate_command_with_flexibility(conveyor_side, motor_type, None, cmd_type, decesion_type)
                        send_can_command(sock, command)
                        sock.settimeout(5)
                        response = sock.recv(1024).decode("utf-8").strip()
                        try:
                            response_data = json.loads(response)
                            system_code = response_data.get("SYSTEM_CODE", "Unknown")
                            parse_system_code(system_code)
                        except json.JSONDecodeError:
                            print(Fore.RED + "[x] Failed to parse JSON response." + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)

            elif selection == SELECTION_CHECK_DIVERT_X_MOTOR_PARAM_ALL:
                decesion_type = CMD_TYPE_CHECK_CONFIG

                motor_type = get_motor_type()
                print(Fore.GREEN + f"Selected Motor Type: {motor_type}" + Style.RESET_ALL)

                conveyor_side = 5;  # Default value for Divert-X Motor side
                print(Fore.YELLOW + "\n[?] Checking all motor parameters..." + Style.RESET_ALL)
                for cmd_type, description in motor_param_descriptions.items():
                    if cmd_type != CMD_RESET_DEVICE:
                        try:
                            print(Fore.GREEN + f"[?] Checking {description}..." + Style.RESET_ALL)
                            command = generate_command_with_flexibility(conveyor_side, motor_type, None, cmd_type, decesion_type)
                            send_can_command(sock, command)
                            sock.settimeout(5)
                            response = sock.recv(1024).decode("utf-8").strip()
                            try:
                                response_data = json.loads(response)
                                system_code = response_data.get("SYSTEM_CODE", "Unknown")
                                parse_system_code(system_code)
                            except json.JSONDecodeError:
                                print(Fore.RED + f"[x] Failed to parse JSON for {description}" + Style.RESET_ALL)
                        except Exception as e:
                            print(Fore.RED + f"[x] Error while checking {description}: {e}" + Style.RESET_ALL)
            elif selection == SELECTION_SET_CONVEYOR_CARD_PARAM_SINGLE:
                decesion_type = CMD_TYPE_SET_CONFIG
                print(Fore.YELLOW + "\n[?] Available Config Commands:" + Style.RESET_ALL)
                for cmd_type, description in conveyor_param_descriptions.items():
                    print(Fore.GREEN + f"{int(cmd_type):02d}. {description}" + Style.RESET_ALL)

                try:
                    cmd_type = int(input(Fore.CYAN + "Enter Config Command: " + Style.RESET_ALL))
                    if cmd_type not in conveyor_param_descriptions:
                        print(Fore.RED + "[x] Invalid command type." + Style.RESET_ALL)
                        continue
                    param = conveyor_param_handlers[cmd_type]()

                    conveyor_side = get_validated_input("Enter Conveyor Side (1: S1, 2: S2, 3: S3, 4:S4): ", range(0, 5))

                    card_id = get_validated_input("Enter Card ID (Note: 255 for all cards): ", range(1, 256))
                    command = generate_command_with_flexibility(conveyor_side, card_id, param, cmd_type, decesion_type)
                    send_can_command(sock, command)
                except Exception as e:
                    print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)
            elif selection == SELECTION_SET_CONVEYOR_CARD_PARAM_ALL:
                decesion_type = CMD_TYPE_SET_CONFIG
                print(Fore.YELLOW + "\n[?] Setting all conveyor card parameters..." + Style.RESET_ALL)

                conveyor_side = get_validated_input("Enter Conveyor Side (1: S1, 2: S2, 3: S3, 4:S4): ", range(0, 5))

                card_id = get_validated_input("Enter Card ID (Note: 255 for all cards): ", range(1, 256))

                for cmd_type, description in conveyor_param_descriptions.items():
                    if cmd_type != CMD_RESET_DEVICE and cmd_type != CMD_UNIQUE_ADDRESS and cmd_type != CMD_ADDRESSING_MODE:
                        try:
                            print(Fore.GREEN + f"[?] Setting {description}..." + Style.RESET_ALL)
                            param = conveyor_param_handlers[cmd_type]()
                            command = generate_command_with_flexibility(conveyor_side, card_id, param, cmd_type, decesion_type)
                            send_can_command(sock, command)
                        except Exception as e:
                            print(Fore.RED + f"[x] Error while setting {description}: {e}" + Style.RESET_ALL)
            elif selection == SELECTION_CHECK_CONVEYOR_CARD_PARAM_SINGLE:
                decesion_type = CMD_TYPE_CHECK_CONFIG
                print(Fore.YELLOW + "\n[?] Available Check Commands:" + Style.RESET_ALL)
                for cmd_type, description in conveyor_param_descriptions_check.items():
                    print(Fore.GREEN + f"{cmd_type:02d}. {description}" + Style.RESET_ALL)
                try:
                    cmd_type = int(input(Fore.CYAN + "Enter Check Command: " + Style.RESET_ALL))
                    if cmd_type not in conveyor_param_descriptions_check:
                        print(Fore.RED + "[x] Invalid command type." + Style.RESET_ALL)
                        continue
                    conveyor_side = get_validated_input("Enter Conveyor Side (1: S1, 2: S2, 3: S3, 4:S4): ", range(0, 5))

                    card_id = get_validated_input("Enter Card ID (Range: 1 - 100): ", range(1, 101))

                    command = generate_command_with_flexibility(conveyor_side, card_id, None, cmd_type, decesion_type)
                    send_can_command(sock, command)
                    sock.settimeout(5)  # Set timeout to 5 seconds
                    response = sock.recv(1024).decode("utf-8").strip()
                    try:
                        response_data = json.loads(response)
                        system_code = response_data.get("SYSTEM_CODE", "Unknown")
                        parse_system_code(system_code)
                    except json.JSONDecodeError:
                        print(Fore.RED + "[x] Failed to parse JSON response." + Style.RESET_ALL)

                except Exception as e:
                    print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)
            elif selection == SELECTION_CHECK_CONVEYOR_CARD_PARAM_ALL:
                decesion_type = CMD_TYPE_CHECK_CONFIG
                print(Fore.YELLOW + "\n[?] Checking all conveyor card parameters..." + Style.RESET_ALL)

                conveyor_side = get_validated_input("Enter Conveyor Side (1: S1, 2: S2, 3: S3, 4:S4): ", range(0, 5))

                card_id = get_validated_input("Enter Card ID (Range: 1 - 100): ", range(1, 101))

                for cmd_type, description in conveyor_param_descriptions_check.items():
                    try:
                        print(Fore.GREEN + f"[?] Checking {description}..." + Style.RESET_ALL)
                        command = generate_command_with_flexibility(conveyor_side, card_id, None, cmd_type, decesion_type)
                        send_can_command(sock, command)
                        sock.settimeout(5)  # Set timeout to 5 seconds
                        response = sock.recv(1024).decode("utf-8").strip()
                        try:
                            response_data = json.loads(response)
                            system_code = response_data.get("SYSTEM_CODE", "Unknown")
                            parse_system_code(system_code)
                        except json.JSONDecodeError:
                            print(Fore.RED + "[x] Failed to parse JSON response." + Style.RESET_ALL)

                    except Exception as e:
                        print(Fore.RED + f"[x] Error while checking {description}: {e}" + Style.RESET_ALL)
            elif selection == SELECTION_EXIT:
                print(Fore.GREEN + "[✔] Exiting." + Style.RESET_ALL)
                break
            elif selection == SELECTION_CONFIGURE_MOTOR_WITH_FILE:
                print(Fore.YELLOW + "\n[?] Select Motor Parameters Configuration File..." + Style.RESET_ALL)
                config = load_configuration_file()
                if not config:
                    print(Fore.RED + "[x] No configuration loaded or file invalid. Aborting." + Style.RESET_ALL)
                    continue
                if 'MotorParameters' not in config or not config['MotorParameters']:
                    print(Fore.RED + "[x] 'MotorParameters' key not found or empty in the selected configuration file. Cannot proceed." + Style.RESET_ALL)
                    continue
                print(Fore.GREEN + "[✓] Applying Motor Parameters from selected config file..." + Style.RESET_ALL)
                apply_motor_config(sock, config)
            else:
                print(Fore.RED + "[x] Unknown option. Try again." + Style.RESET_ALL)

    except KeyboardInterrupt:
        print(Fore.RED + "\n[x] Interrupted by user." + Style.RESET_ALL)
    finally:
        sock.close()
        print(Fore.GREEN + "[✓] Connection closed." + Style.RESET_ALL)


if __name__ == "__main__":
    main()