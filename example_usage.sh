#!/bin/bash
# Example usage script for Android Device Scanner

echo "=== Android Device Scanner - Example Usage ==="
echo ""

# Make the Python script executable
chmod +x scan_android_device.py

echo "1. Basic usage (auto-detect device):"
echo "   python3 scan_android_device.py"
echo ""

echo "2. With custom output filename:"
echo "   python3 scan_android_device.py -o my_phone_$(date +%Y%m%d).csv"
echo ""

echo "3. With verbose output:"
echo "   python3 scan_android_device.py -v"
echo ""

echo "4. Manually specify device path:"
echo "   First, find your device:"
echo "   ls /run/user/\$(id -u)/gvfs/"
echo ""
echo "   Then run with -p option:"
echo "   python3 scan_android_device.py -p /run/user/\$(id -u)/gvfs/mtp:host=YOUR_DEVICE_PATH"
echo ""

echo "5. Full example with all options:"
echo "   python3 scan_android_device.py -o phone_backup.csv -v"
echo ""

echo "=== To run now with auto-detection ==="
echo "Press Enter to start scanning, or Ctrl+C to cancel..."
read

python3 scan_android_device.py
