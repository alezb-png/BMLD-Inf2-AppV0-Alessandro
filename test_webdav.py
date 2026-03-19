#!/usr/bin/env python3
"""
Test script to diagnose WebDAV connection issues.
Run this before running the Streamlit app.
"""

import fsspec
import sys

# Read credentials from secrets.toml
import tomllib
with open('.streamlit/secrets.toml', 'rb') as f:
    secrets = tomllib.load(f)
    webdav_config = secrets['webdav']

print("=" * 60)
print("WebDAV Connection Test")
print("=" * 60)
print(f"Base URL: {webdav_config['base_url']}")
print(f"Username: {webdav_config['username']}")
print()

try:
    # Test 1: Connect to WebDAV
    print("Test 1: Connecting to WebDAV...")
    fs = fsspec.filesystem(
        'webdav',
        base_url=webdav_config['base_url'],
        auth=(webdav_config['username'], webdav_config['password'])
    )
    print("  ✓ Connection successful!")
    print()
    
    # Test 2: List root directory
    print("Test 2: Listing root directory...")
    try:
        items = fs.ls('/')
        print(f"  ✓ Found {len(items)} items in root:")
        for item in items[:10]:  # Show first 10
            print(f"    - {item}")
        if len(items) > 10:
            print(f"    ... and {len(items) - 10} more")
    except Exception as e:
        print(f"  ⚠ Could not list root: {e}")
    print()
    
    # Test 3: Check if BMLD_App_DB folder exists
    print("Test 3: Checking if 'BMLD_App_DB' folder exists...")
    folder_path = '/BMLD_App_DB'
    if fs.exists(folder_path):
        print(f"  ✓ Folder exists at {folder_path}")
    else:
        print(f"  ✗ Folder NOT found at {folder_path}")
    print()
    
    # Test 4: Try to create BMLD_App_DB folder
    print("Test 4: Attempting to create 'BMLD_App_DB' folder...")
    try:
        if not fs.exists(folder_path):
            fs.makedirs(folder_path, exist_ok=True)
            print(f"  ✓ Successfully created {folder_path}")
        else:
            print(f"  ℹ Folder already exists")
    except Exception as e:
        print(f"  ✗ Failed to create folder: {e}")
        print(f"  Error type: {type(e).__name__}")
    print()
    
    # Test 5: Try to create user folder
    print("Test 5: Attempting to create user data folder...")
    user_folder = '/BMLD_App_DB/user_data_test'
    try:
        if not fs.exists(user_folder):
            fs.makedirs(user_folder, exist_ok=True)
            print(f"  ✓ Successfully created {user_folder}")
        else:
            print(f"  ℹ Folder already exists")
    except Exception as e:
        print(f"  ✗ Failed to create user folder: {e}")
    print()
    
    print("=" * 60)
    print("✓ All tests completed! Check results above.")
    print("=" * 60)
    
except Exception as e:
    print(f"✗ Fatal error: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
