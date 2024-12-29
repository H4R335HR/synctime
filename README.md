# synctime
## NTP Time Sync and Adjust Script

This Python script fetches the current time from an NTP (Network Time Protocol) server, adjusts it to a specified timezone, and optionally adds a custom time offset before setting the system time. 

### Why this script exists?
- If you dont want to install ntp clients 

### Features:
- Fetches time from an NTP server (default: `time.google.com`).
- Adjusts the time to a specific timezone (default: `+05:30`).
- Adds a custom offset (in seconds) to the adjusted time (default: `5 seconds`).
- Sets the adjusted time to the system clock.

### Requirements:
- Python 3.x
- `sudo` access to set the system time.
- A Unix-like OS (Linux or macOS) for `date` and `hwclock` commands.

### Usage:

```bash
sudo python3 ntp_time_sync.py [OPTIONS]
```

### Options:

- `--server <NTP_SERVER>`:  
  **(Optional)** Specify the NTP server to fetch the time from. Default is `time.google.com`.  
  Example: `--server time.google.com`.

- `--offset <OFFSET>`:  
  **(Optional)** Set the timezone offset in `±HH:MM` format. Default is `+05:30`.  
  Example: `--offset +02:00` or `--offset -03:30`.

- `--custom-offset <SECONDS>`:  
  **(Optional)** Set a custom offset in seconds to add to the adjusted time. Default is `5`.  
  Example: `--custom-offset 30` to add 30 seconds.

### Default Behavior:
By default, the script:
- Fetches the time from `time.google.com`.
- Adjusts the time by the timezone offset `+05:30` (India Standard Time).
- Adds `5 seconds` to the adjusted time.

### Example Commands:

1. **Default behavior** (fetch time from Google's NTP server, adjust to `+05:30` timezone, and add 5 seconds):
   ```bash
   sudo python3 ntp_time_sync.py
   ```

2. **Custom NTP server and timezone offset** (fetch time from `ntp.example.com`, adjust to `+02:00` timezone, and add 30 seconds):
   ```bash
   sudo python3 ntp_time_sync.py --server ntp.example.com --offset +02:00 --custom-offset 30
   ```

3. **Custom NTP server** (fetch time from `ntp.example.com`, adjust to `+03:30` timezone, and add 10 seconds):
   ```bash
   sudo python3 ntp_time_sync.py --server ntp.example.com --offset +03:30 --custom-offset 10
   ```

4. **Custom offset only** (fetch time from the default NTP server `time.google.com`, adjust to `+05:30` timezone, and add 120 seconds):
   ```bash
   sudo python3 ntp_time_sync.py --custom-offset 120
   ```

### How it Works:

1. The script fetches the current time from an NTP server. By default, it uses `time.google.com` on port 123.
2. The script then adjusts the time based on the specified timezone offset (in seconds).
3. If specified, a custom offset (in seconds) is added to the adjusted time.
4. The system time is then updated with the final adjusted time using the `date` and `hwclock` commands.

### Example Output:

```bash
Fetching time from time.google.com...
NTP time (UTC): 2024-12-29 08:15:00
Adjusted time (local): 2024-12-29 13:45:00
Time after adding 5 seconds: 2024-12-29 13:45:05
System time successfully set to: 2024-12-29 13:45:05
```

### Notes:
- The script requires `sudo` to change the system time, so make sure you have the necessary permissions to run the script with elevated privileges.
- It uses the `date` command to set the system time, which is available on most Unix-like systems (Linux/macOS).
- Make sure your system allows setting the hardware clock using the `hwclock` command (usually requires `sudo`).

### License:
This script is open-source and released under the [MIT License](LICENSE).

---

### Saving and Running the Script:

1. Save the script as `ntp_time_sync.py`.
2. To make the script executable:
   ```bash
   chmod +x ntp_time_sync.py
   ```
3. Run the script with the desired options.

--- 
