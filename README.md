# Hollow Knight Save Tool

A Python tool for reading, modifying, and restoring Hollow Knight save files. This tool handles the encryption, decryption, and serialization of save data for both Hollow Knight and Hollow Knight: Silksong.

## Features

- **Decrypt save files**: Convert encrypted save files to readable JSON format
- **Encrypt save files**: Convert JSON data back to encrypted save file format
- **Restore backups**: Extract and restore save data from backup files
- **Support for both games**: Works with Hollow Knight and Hollow Knight: Silksong save files
- **Flexible encryption**: Can handle both encrypted and unencrypted data

## Install from source

```bash
git clone https://github.com/hotwords123/hollow-knight-save.git
cd hollow-knight-save

# Run the following command to install the tool globally
uv tool install .
# Or install it in editable mode for development
uv sync
```

## Usage

The tool provides three main commands: `decrypt`, `encrypt`, and `restore`.

### Command Line Interface

```bash
hollow-knight-save <command> <input-file> [options]
```

### Commands

#### 1. Decrypt Save Files

Convert an encrypted save file to readable JSON format:

```bash
hollow-knight-save decrypt "path/to/save/user.dat" -o decrypted.json
```

#### 2. Encrypt Save Files

Convert JSON data back to encrypted save file format:

```bash
hollow-knight-save encrypt "modified_save.json" -o "user.dat"
```

#### 3. Restore from Backup

Extract save data from a backup file and create a new save file:

```bash
hollow-knight-save restore "path/to/backup/restoreData.dat" -o "user.dat"
```

### Options

- `-o, --output`: Specify output file (if not provided, outputs to stdout)
- `-n, --no-encryption`: Disable encryption/decryption (for unencrypted save files)

### Examples

#### Basic decryption
```bash
# Decrypt a save file to view its contents
hollow-knight-save decrypt "C:\Users\YourName\AppData\LocalLow\Team Cherry\Hollow Knight\user1.dat" -o save_data.json
```

#### Modify and re-encrypt
```bash
# 1. Decrypt the save file
hollow-knight-save decrypt "user1.dat" -o save_data.json

# 2. Edit save_data.json with your preferred text editor

# 3. Encrypt it back
hollow-knight-save encrypt "save_data.json" -o "user1_modified.dat"
```

#### Restore from backup
```bash
# Restore from a Silksong backup file
hollow-knight-save restore "C:\Users\YourName\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\YourUserID\Restore_Points1\restoreData2.dat" -o user1.dat
```

## Save File Mechanics

This section explains the technical details of how Hollow Knight save files work and the conversion process between different formats.

### Save File Format Overview

Hollow Knight uses a multi-layered approach to store save data:

**Plain JSON** → **AES Encryption** → **Base64 Encoding** → **Binary Serialization** → **.dat file**

### Conversion Process

The conversion from readable JSON to encrypted .dat files follows these steps:

1. **JSON Data**: The save data starts as JSON containing game state information
2. **AES Encryption**: The JSON string is encrypted using AES-256-ECB with a hardcoded 32-byte key (`UKu52ePUBwetZ9wNX88o54dnfKRu0T1l`) and PKCS7 padding
3. **Base64 Encoding**: The encrypted bytes are encoded as a base64 string
4. **Binary Serialization**: The base64 string is wrapped in .NET `BinaryFormatter` format
5. **File Output**: The final binary data is written to a `.dat` file

The decryption process simply reverses these steps.

### Backup File Format (Restore Points)

Backup files (usually named `restoreData#.dat` or `NODELrestoreData#.dat`, where `#` is a number) contain additional metadata and follow this structure:

```json
{
  "data": "<base64-encoded encrypted save file bytes>",
  "date": "2025/09/19",
  "version": "1.0.28650",
  "number": 5,
  "identifier": "GAINED_WALLJUMP"
}
```

**Fields explained:**
- `data`: The actual save file content, encrypted and then base64-encoded (contains the main game data in a `saveGameData` field)
- `date`: When the backup was created (YYYY/MM/DD format)
- `version`: Game version when backup was made
- `number`: Sequential backup number
- `identifier`: Game event that triggered the backup (e.g., ability gained, act unlocked)

## Save File Locations

Google "Hollow Knight save file location" or "Hollow Knight Silksong save file location" for your platform to find where the game stores its save files.

## Disclaimer

This tool is for educational and personal use only. Always backup your save files before making modifications. The developers are not responsible for any data loss or corruption that may occur from using this tool.
