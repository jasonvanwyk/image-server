# Image Upload Server for Claude Code

A comprehensive image management system designed to work seamlessly with Claude Code and AI development workflows. This server allows you to easily transfer screenshots and images from any device to your development environment and provides intelligent command integration.

![image](https://github.com/user-attachments/assets/8cc84095-7fe6-4267-b51d-a6bec935d557)


## Features

- 🖼️ **Drag & Drop Upload**: Upload images from any browser
- 📱 **Cross-Device Access**: Works from Windows, Mac, mobile, or any device with a browser
- 🔄 **Auto-Refresh**: Real-time file list updates
- 🤖 **Claude Code Integration**: One-click commands for AI image analysis
- 🚀 **Zero Dependencies**: Uses only Python standard library
- 💾 **Smart Organization**: Automatic file management and organization
- 🔧 **Multi-Script Support**: Various image transfer methods (SSH, mounted shares, direct upload)
- ⚡ **Smart Commands**: Auto-server management with the `ri` command system

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/jasonvanwyk/image-server.git
cd image-server
chmod +x image-upload-server.py
```

### 2. Start the Server

```bash
python3 image-upload-server.py
```

### 3. Upload Images

Open `http://YOUR_SERVER_IP:8888` in any browser and drag/drop images.

### 4. Use with Claude Code

```bash
ri "your-image.png"
```

## Complete Installation & Setup

### Prerequisites

- Python 3.6+ 
- Linux/Unix environment
- Network access between devices

### Basic Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jasonvanwyk/image-server.git
   cd image-server
   ```

2. **Make scripts executable**:
   ```bash
   chmod +x image-upload-server.py
   ```

3. **Test the server**:
   ```bash
   python3 image-upload-server.py
   ```

### Advanced Setup with `ri` Command Integration

For full integration with development workflows, set up the complete `ri` command system:

#### 1. Download Support Scripts

You'll need these additional scripts for full functionality:

- `ri-smart.sh` - Main command interface with auto-server management
- `read-image.sh` - SSH-based Windows screenshot fetching  
- `read-image-simple.sh` - Manual transfer fallback
- `read-image-winscp.sh` - WinSCP-based transfers
- `mount-windows-share.sh` - Windows share mounting
- `image-server.service` - SystemD service file

#### 2. Setup Directory Structure

```bash
# Create central screenshots directory
mkdir -p /home/$USER/screenshots

# Update image-upload-server.py to use central location
# Edit UPLOAD_DIR = "/home/$USER/screenshots"
```

#### 3. Install ri Command System

```bash
# Make ri-smart.sh accessible globally
sudo ln -sf /path/to/ri-smart.sh /usr/local/bin/ri

# Or add to ~/.bashrc:
echo 'alias ri="/path/to/ri-smart.sh"' >> ~/.bashrc
source ~/.bashrc
```

#### 4. Configure for Your Environment

Edit the configuration variables in each script:

**ri-smart.sh**:
```bash
LOCAL_IMAGE_DIR="/home/$USER/screenshots"
IMAGE_SERVER_PORT=8888
IMAGE_SERVER_SCRIPT="/path/to/image-upload-server.py"
```

**For Windows Integration** (read-image.sh):
```bash
WINDOWS_USER="your-windows-username"
WINDOWS_HOST="192.168.x.x"  # Your Windows machine IP
WINDOWS_SCREENSHOT_DIR="/c/Users/YourName/Downloads"
```

#### 5. Optional: SystemD Service Setup

```bash
# Copy service file to systemd
sudo cp image-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable image-server
sudo systemctl start image-server
```

## Usage Guide

### Basic Commands

| Command | Description |
|---------|-------------|
| `ri` | List images and start server if needed |
| `ri filename.png` | Prepare specific image for Claude to read |
| `ri --server` | Start image upload server |
| `ri --stop` | Stop image upload server |
| `ri --status` | Check server status |
| `ri --help` | Show help information |

### Advanced Commands (with full setup)

| Command | Description |
|---------|-------------|
| `ri --latest` | Fetch latest screenshot from Windows |
| `ri --list` | List available images |
| Windows Integration | SSH-based screenshot fetching |

### Web Interface

1. **Access the server**: `http://YOUR_SERVER_IP:8888`
2. **Upload methods**:
   - Drag & drop images onto the upload area
   - Click "Choose Files" to browse and select
   - Mobile/tablet friendly interface
3. **File management**: View uploaded files with ready-to-use commands

### Windows Integration Options

#### Option 1: SSH Method (Recommended)
- Setup OpenSSH on Windows
- Use `ri --latest` to fetch screenshots automatically
- Requires Windows PowerShell setup (see `setup-windows-openssh.ps1`)

#### Option 2: Mounted Share
- Mount Windows shared folder
- Direct file access without SSH
- Use `mount-windows-share.sh` script

#### Option 3: Direct Upload
- Use web interface from Windows browser
- Drag/drop screenshots directly
- No additional setup required

### Usage
```
  ri                     - Start server and list images
  ri <filename>          - Prepare image for Claude to read
  ri --server            - Just start the image server
  ri --stop              - Stop the image server
  ri --status            - Check server status
  ri --help              - Show this help
```

## Configuration

### Environment Variables

```bash
# Override default settings
export LOCAL_IMAGE_DIR="/custom/path/screenshots"
export WINDOWS_HOST="192.168.1.100"
export IMAGE_SERVER_PORT="9999"
```

### Server Configuration

Edit `image-upload-server.py`:

```python
UPLOAD_DIR = "/home/user/screenshots"  # Change upload directory
PORT = 8888                            # Change server port
```

### Network Configuration

- **Default Port**: 8888
- **Bind Address**: 0.0.0.0 (all interfaces)
- **Upload Directory**: `/home/user/screenshots`

## Troubleshooting

### Common Issues

**Server won't start**:
```bash
# Check if port is in use
lsof -i:8888
# Kill existing process
pkill -f image-upload-server.py
```

**Permission denied**:
```bash
# Make sure scripts are executable
chmod +x *.sh *.py
# Check directory permissions
ls -la /home/$USER/screenshots
```

**Network access issues**:
```bash
# Check firewall
sudo ufw status
# Allow port if needed
sudo ufw allow 8888
```

**Windows SSH issues**:
- Ensure OpenSSH is installed and running
- Check Windows firewall settings
- Verify SSH key authentication

### Debug Mode

Run with verbose output:
```bash
python3 image-upload-server.py --debug
```

## Integration Examples

### With VS Code
```json
{
  "tasks": [
    {
      "label": "Start Image Server",
      "type": "shell",
      "command": "ri --server"
    }
  ]
}
```

### With Claude Code Projects
```bash
# In any project directory
ri screenshot.png  # Image is ready for Claude analysis
```

### Automation Scripts
```bash
#!/bin/bash
# Auto-capture and prepare for Claude
ri --latest
echo "Latest screenshot ready for analysis"
```

## API Reference

### HTTP Endpoints

- `GET /` - Web interface
- `GET /list` - JSON list of uploaded files
- `POST /upload` - File upload endpoint

### Response Formats

**File List** (`/list`):
```json
["image1.png", "image2.jpg", "screenshot.png"]
```

**Upload Response**:
```
File filename.png uploaded successfully
```

## Security Considerations

- **Local Network Only**: Server binds to all interfaces but intended for local network use
- **No Authentication**: Anyone with network access can upload/view files
- **File Validation**: Only image files are accepted
- **Directory Traversal**: Protected against path traversal attacks
- **Recommended**: Use on trusted networks only

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
git clone https://github.com/jasonvanwyk/image-server.git
cd image-server
# Make changes
python3 image-upload-server.py  # Test locally
```

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/jasonvanwyk/image-server/issues)
- **Documentation**: This README and inline code comments
- **Community**: Contributions and feature requests welcome

## Changelog

### v2.0.0 (Latest)
- Central screenshot directory (`/home/user/screenshots`)
- Improved ri command integration
- Enhanced Windows compatibility
- SystemD service support
- Comprehensive documentation

### v1.0.0
- Basic web upload functionality
- Claude Code integration
- Cross-platform support
