import socket
import struct
import time
import subprocess
import os
import argparse

# Fetches the current time from an NTP server and returns it as a Unix timestamp.
# The default server is "time.google.com" on port 123. Converts the NTP timestamp 
# (seconds since 1900) to Unix time (seconds since 1970).
def get_ntp_time(ntp_server="time.google.com", port=123):
    try:
        ntp_data = b'\x1b' + 47 * b'\0'
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.settimeout(5)
            client.sendto(ntp_data, (ntp_server, port))
            ntp_response, _ = client.recvfrom(1024)
        
        ntp_time = struct.unpack('!12I', ntp_response)[10]
        ntp_time -= 2208988800  # Convert NTP epoch to Unix epoch
        return ntp_time
    except Exception as e:
        print(f"Error fetching time from {ntp_server}: {e}")
        return None

def set_system_time(unix_time):
    try:
        # Convert to a human-readable date string
        local_time = time.gmtime(unix_time)  # Convert to UTC
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        
        # Use 'date' command to set system time
        subprocess.run(["sudo", "date", "--set", formatted_time], check=True)
        
        # Synchronize hardware clock
        subprocess.run(["sudo", "hwclock", "--systohc"], check=True)
        
        print(f"System time successfully set to: {formatted_time}")
    except Exception as e:
        print(f"Error setting system time: {e}")

def main():
    parser = argparse.ArgumentParser(description="Fetch and set system time using NTP server with custom timezone offset.")
    
    # Default values as per your request
    parser.add_argument("-s", "--server", type=str, default="time.google.com", help="NTP server to fetch time from (default: time.google.com)")
    parser.add_argument("-t", "--tz-offset", type=str, default="+05:30", help="Timezone offset in ±HH:MM format (default: +05:30)")
    parser.add_argument("-o", "--custom-offset", type=int, default=5, help="Custom offset to add to the adjusted time (in seconds, default: 5)")

    args = parser.parse_args()

    # Parse offset (e.g., +05:30 -> 19800 seconds)
    try:
        offset_sign = 1 if args.tz_offset.startswith('+') else -1
        offset_parts = args.tz_offset[1:].split(':')
        offset_seconds = offset_sign * (int(offset_parts[0]) * 3600 + int(offset_parts[1]) * 60)
    except Exception:
        print("Invalid offset format. Use ±HH:MM (e.g., +05:30 or -03:00).")
        exit(1)

    # Ensure the script is run with sudo
    if os.geteuid() != 0:
        print("Please run with sudo.")
        exit(1)

    print(f"Fetching time from {args.server}...")
    ntp_time = get_ntp_time(args.server)
    
    if ntp_time:
        # Print the raw NTP time in UTC format
        print(f"NTP time (UTC): {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ntp_time))}")
        
        # Adjust for timezone offset
        ntp_time += offset_seconds
        print(f"Adjusted time (local): {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ntp_time))}")
        
        # Add the custom offset to the adjusted time (default is 5 seconds)
        ntp_time += args.custom_offset
        print(f"Time after adding {args.custom_offset} seconds: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ntp_time))}")
        
        # Set system time
        set_system_time(ntp_time)

if __name__ == "__main__":
    main()

