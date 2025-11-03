#!/usr/bin/env python3
"""
Android Device Scanner
Recursively scans an Android phone connected via USB (MTP mode) and generates
a CSV file containing MD5 hashes and file paths of all files.
"""

import os
import hashlib
import csv
import sys
from pathlib import Path
from datetime import datetime
import argparse


def calculate_md5(file_path):
    """
    Calculate MD5 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        MD5 hash as hexadecimal string, or None if error occurs
    """
    md5_hash = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(8192), b''):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except (PermissionError, OSError) as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return None


def scan_directory(root_path, output_csv, verbose=False):
    """
    Recursively scan directory and write file information to CSV.
    
    Args:
        root_path: Root directory to start scanning
        output_csv: Path to output CSV file
        verbose: Print progress if True
    """
    file_count = 0
    error_count = 0
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header
        csv_writer.writerow(['File Path', 'MD5 Hash', 'File Size (bytes)', 'Status'])
        
        print(f"Scanning: {root_path}")
        print(f"Output will be written to: {output_csv}")
        print("-" * 80)
        
        for root, dirs, files in os.walk(root_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                try:
                    # Get file size
                    file_size = os.path.getsize(file_path)
                    
                    # Calculate MD5 hash
                    md5_hash = calculate_md5(file_path)
                    
                    if md5_hash:
                        status = "Success"
                        file_count += 1
                        if verbose:
                            print(f"[{file_count}] {file_path}")
                    else:
                        status = "Error - Could not read file"
                        error_count += 1
                        md5_hash = "N/A"
                    
                    # Write to CSV
                    csv_writer.writerow([file_path, md5_hash, file_size, status])
                    
                except Exception as e:
                    error_count += 1
                    print(f"Error processing {file_path}: {e}", file=sys.stderr)
                    csv_writer.writerow([file_path, "N/A", "N/A", f"Error - {str(e)}"])
    
    print("-" * 80)
    print(f"Scan complete!")
    print(f"Total files processed: {file_count}")
    print(f"Errors encountered: {error_count}")
    print(f"Results saved to: {output_csv}")


def find_android_mount_point():
    """
    Try to find the Android device mount point.
    
    Returns:
        Path to Android device or None if not found
    """
    # Common mount points for MTP devices on Ubuntu
    possible_paths = [
        "/run/user/{uid}/gvfs",
        os.path.expanduser("~/.gvfs"),
        "/media/{user}"
    ]
    
    uid = os.getuid()
    username = os.environ.get('USER', '')
    
    # Check gvfs mounts (most common for MTP)
    gvfs_path = f"/run/user/{uid}/gvfs"
    if os.path.exists(gvfs_path):
        for entry in os.listdir(gvfs_path):
            if 'mtp' in entry.lower():
                full_path = os.path.join(gvfs_path, entry)
                return full_path
    
    # Check legacy gvfs location
    legacy_gvfs = os.path.expanduser("~/.gvfs")
    if os.path.exists(legacy_gvfs):
        for entry in os.listdir(legacy_gvfs):
            if 'mtp' in entry.lower():
                full_path = os.path.join(legacy_gvfs, entry)
                return full_path
    
    # Check /media
    media_path = f"/media/{username}"
    if os.path.exists(media_path):
        for entry in os.listdir(media_path):
            full_path = os.path.join(media_path, entry)
            if os.path.ismount(full_path):
                return full_path
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description='Scan Android device and generate CSV with MD5 hashes of all files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Auto-detect Android device and scan
  python3 scan_android_device.py
  
  # Specify device path manually
  python3 scan_android_device.py -p /run/user/1000/gvfs/mtp:host=SAMSUNG_SAMSUNG_Android_XXXXX
  
  # Specify output file
  python3 scan_android_device.py -o my_phone_scan.csv
  
  # Verbose mode
  python3 scan_android_device.py -v
        '''
    )
    
    parser.add_argument(
        '-p', '--path',
        help='Path to Android device mount point (auto-detected if not specified)',
        default=None
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output CSV filename (default: android_scan_TIMESTAMP.csv)',
        default=None
    )
    
    parser.add_argument(
        '-v', '--verbose',
        help='Print each file being processed',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    # Determine device path
    if args.path:
        device_path = args.path
    else:
        print("Attempting to auto-detect Android device...")
        device_path = find_android_mount_point()
        
        if not device_path:
            print("\nError: Could not auto-detect Android device.")
            print("\nPlease ensure:")
            print("1. Your Android phone is connected via USB")
            print("2. You have selected 'File Transfer' (MTP) mode on your phone")
            print("3. You have opened the device in your file manager (Nautilus/Files)")
            print("\nOr specify the device path manually using -p option.")
            print("\nTo find the path manually, check:")
            print(f"  - /run/user/{os.getuid()}/gvfs/")
            print(f"  - {os.path.expanduser('~/.gvfs/')}")
            sys.exit(1)
        
        print(f"Found Android device at: {device_path}")
    
    # Check if path exists
    if not os.path.exists(device_path):
        print(f"Error: Path does not exist: {device_path}")
        sys.exit(1)
    
    # Generate output filename
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"android_scan_{timestamp}.csv"
    
    # Make output path absolute
    output_file = os.path.abspath(output_file)
    
    # Perform the scan
    try:
        scan_directory(device_path, output_file, args.verbose)
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
