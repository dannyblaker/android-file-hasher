# Android Device Scanner

A Python script that recursively scans your Android phone connected via USB and generates a CSV file containing MD5 hashes, file paths, and file sizes for every file on the device.

[![A Danny Blaker project badge](https://github.com/dannyblaker/dannyblaker.github.io/blob/main/danny_blaker_project_badge.svg)](https://github.com/dannyblaker/)


## Features

- 🔍 Recursively scans entire Android device
- 🔐 Calculates MD5 hash for each file
- 📊 Generates CSV output with file paths, hashes, and sizes
- 🎯 Auto-detects Android device mount point
- ⚡ Handles large files efficiently (reads in chunks)
- 🛡️ Error handling for permission issues and unreadable files
- 📝 Verbose mode for detailed progress tracking

## Requirements

- Ubuntu Linux (or other Linux distributions with MTP support)
- Python 3.6 or higher (uses standard library only)
- Android phone with USB debugging or File Transfer (MTP) enabled
- `gvfs` and `gvfs-backends` for MTP support

## Installation

### 1. Install MTP Support (if not already installed)

```bash
sudo apt update
sudo apt install mtp-tools gvfs gvfs-backends
```

### 2. Make the script executable

```bash
chmod +x scan_android_device.py
```

## Usage

### Step 1: Connect Your Android Phone

1. Connect your Android phone to your computer via USB
2. On your phone, select **"File Transfer"** or **"Transfer files"** when prompted
3. Open your file manager (Nautilus/Files) and click on your device to mount it

### Step 2: Run the Scanner

#### Auto-detect device (recommended):

```bash
python3 scan_android_device.py
```

#### Specify device path manually:

```bash
python3 scan_android_device.py -p /run/user/1000/gvfs/mtp:host=SAMSUNG_SAMSUNG_Android_XXXXX
```

#### Specify output filename:

```bash
python3 scan_android_device.py -o my_phone_backup.csv
```

#### Verbose mode (see each file being processed):

```bash
python3 scan_android_device.py -v
```

#### Combine options:

```bash
python3 scan_android_device.py -o phone_scan.csv -v
```

## Command Line Options

```
-h, --help            Show help message and exit
-p PATH, --path PATH  Path to Android device mount point (auto-detected if not specified)
-o OUTPUT, --output OUTPUT
                      Output CSV filename (default: android_scan_TIMESTAMP.csv)
-v, --verbose         Print each file being processed
```

## Output Format

The script generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| File Path | Full path to the file on the Android device |
| MD5 Hash | MD5 hash of the file content (or "N/A" if error) |
| File Size (bytes) | Size of the file in bytes |
| Status | "Success" or error message |

### Example Output:

```csv
File Path,MD5 Hash,File Size (bytes),Status
/run/user/1000/gvfs/mtp:host=XXX/Internal storage/DCIM/Camera/IMG_001.jpg,a1b2c3d4e5f6...,2048576,Success
/run/user/1000/gvfs/mtp:host=XXX/Internal storage/Documents/file.pdf,9f8e7d6c5b4a...,512000,Success
```

## Troubleshooting

### Device not detected

If auto-detection fails:

1. Make sure your phone is in "File Transfer" mode
2. Open your file manager and click on the device to mount it
3. Manually find the mount point:
   ```bash
   ls /run/user/$(id -u)/gvfs/
   ```
4. Use the `-p` option to specify the path manually

### Permission errors

Some files may not be readable due to Android's permission system. The script will:
- Log these errors to stderr
- Mark them as errors in the CSV
- Continue scanning other files

### Large number of files

For devices with many files (10,000+), the scan may take a while. Use `-v` (verbose mode) to monitor progress.

### MTP connection issues

If you experience connection issues:

```bash
# Restart MTP services
killall gvfsd-mtp
# Unplug and replug your device
# Open file manager and access the device again
```

## Performance Notes

- The script reads files in 8KB chunks for memory efficiency
- Large files (videos, backups) may take longer to hash
- Typical scan time: 1-2 hours for devices with 50GB of data

## Use Cases

- 📱 Create a complete inventory of your phone's contents
- 🔄 Verify file integrity after transfers
- 🗂️ Track changes to files over time
- 💾 Document device contents before factory reset
- 🔍 Find duplicate files by comparing MD5 hashes

## Security Note

MD5 hashes are used for file identification and integrity checking. While MD5 is not cryptographically secure, it's sufficient for detecting accidental file corruption and identifying duplicate files.

## License

This script is provided as-is for personal use.
