# Image Upload Server for Claude Code

A simple, lightweight web-based image upload server designed to work seamlessly with Claude Code. This server allows you to easily transfer screenshots and images from any device to your Claude Code environment.

## Features

- 🖼️ Drag & drop image uploads
- 📱 Works from any device with a web browser
- 🔄 Auto-refreshing file list
- 📋 One-click copy commands for Claude Code
- 🚀 Zero dependencies (uses Python standard library)
- 💾 Automatic file organization

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/image-server.git
cd image-server
```

2. Make the script executable:
```bash
chmod +x image-upload-server.py
```

## Usage

### Starting the Server

```bash
./image-upload-server.py
```

Or with Python:
```bash
python3 image-upload-server.py
```

The server will start on port 8888 and display:
- Local network IP address
- Upload directory location
- Access URLs

### Uploading Images

1. Open your web browser and navigate to:
   - `http://YOUR_SERVER_IP:8888` (from another device)
   - `http://localhost:8888` (from the same machine)

2. Upload images by:
   - Dragging and dropping onto the upload area
   - Clicking "Choose Files" to browse

3. View uploaded images in the file list below

### Using with Claude Code

After uploading an image, use the displayed command in Claude Code:
```bash
ri "image-name.png"
```

This requires the `ri` (read image) command to be set up in your Claude Code environment.

## Configuration

You can modify these settings in the script:

- `UPLOAD_DIR`: Directory where images are stored (default: `/home/jason/projects/Elegant_Man/screenshots`)
- `PORT`: Server port (default: 8888)

## Running in Background

To run the server in the background:

```bash
nohup ./image-upload-server.py > /dev/null 2>&1 &
```

To stop the background server:
```bash
pkill -f image-upload-server.py
```

## Security Notes

- This server is designed for local network use only
- No authentication is implemented
- All uploaded files are publicly accessible
- Use only on trusted networks

## Requirements

- Python 3.6+
- No external dependencies required

## License

MIT License

## Contributing

Feel free to submit issues and enhancement requests!