#!/usr/bin/env python3
"""
Simple Image Upload Server
Allows drag-and-drop image uploads from any browser
"""

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import socket
from datetime import datetime
import json

UPLOAD_DIR = "/home/jason/projects/Elegant_Man/screenshots"
PORT = 8888

class UploadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve the upload page and handle list requests"""
        if self.path == '/list':
            # List uploaded files
            files = []
            if os.path.exists(UPLOAD_DIR):
                # Get files with modification time
                image_files = []
                for f in os.listdir(UPLOAD_DIR):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        filepath = os.path.join(UPLOAD_DIR, f)
                        mtime = os.path.getmtime(filepath)
                        image_files.append((f, mtime))
                
                # Sort by modification time (newest first)
                image_files.sort(key=lambda x: x[1], reverse=True)
                files = [f[0] for f in image_files]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())
            return
        
        # Default: serve the upload page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Image Upload for Claude Code</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .upload-area {{
            border: 3px dashed #4CAF50;
            border-radius: 10px;
            padding: 50px;
            text-align: center;
            background-color: white;
            transition: all 0.3s;
        }}
        .upload-area.dragover {{
            background-color: #e8f5e9;
            border-color: #2e7d32;
        }}
        .file-list {{
            margin-top: 30px;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
        }}
        .file-item {{
            padding: 10px;
            margin: 5px 0;
            background-color: #f0f0f0;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .file-item:hover {{
            background-color: #e0e0e0;
        }}
        .file-info {{
            flex: 1;
        }}
        .file-name {{
            font-weight: bold;
            color: #333;
        }}
        .file-command {{
            font-family: monospace;
            background-color: #2e7d32;
            color: white;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
        }}
        .no-images {{
            text-align: center;
            color: #999;
            padding: 20px;
        }}
        .success {{
            color: #4CAF50;
            font-weight: bold;
        }}
        button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        button:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <h1>Image Upload for Claude Code</h1>
    <div class="upload-area" id="uploadArea">
        <h2>Drag & Drop Images Here</h2>
        <p>or</p>
        <input type="file" id="fileInput" multiple accept="image/*" style="display: none;">
        <button onclick="document.getElementById('fileInput').click()">Choose Files</button>
    </div>
    <div id="status"></div>
    <div class="file-list">
        <h3>Available Images ({UPLOAD_DIR}):</h3>
        <div id="fileList">Loading...</div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const status = document.getElementById('status');
        const fileList = document.getElementById('fileList');
        
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {{
            uploadArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        }});
        
        // Highlight drop area
        ['dragenter', 'dragover'].forEach(eventName => {{
            uploadArea.addEventListener(eventName, highlight, false);
        }});
        
        ['dragleave', 'drop'].forEach(eventName => {{
            uploadArea.addEventListener(eventName, unhighlight, false);
        }});
        
        // Handle dropped files
        uploadArea.addEventListener('drop', handleDrop, false);
        fileInput.addEventListener('change', handleFiles, false);
        
        function preventDefaults(e) {{
            e.preventDefault();
            e.stopPropagation();
        }}
        
        function highlight(e) {{
            uploadArea.classList.add('dragover');
        }}
        
        function unhighlight(e) {{
            uploadArea.classList.remove('dragover');
        }}
        
        function handleDrop(e) {{
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles({{target: {{files: files}}}});
        }}
        
        function handleFiles(e) {{
            const files = [...e.target.files];
            files.forEach(uploadFile);
        }}
        
        function uploadFile(file) {{
            const formData = new FormData();
            formData.append('file', file);
            
            fetch('/upload', {{
                method: 'POST',
                body: formData
            }})
            .then(response => response.text())
            .then(data => {{
                status.innerHTML = '<p class="success">Uploaded: ' + file.name + '</p>';
                loadFileList();
            }})
            .catch(error => {{
                status.innerHTML = '<p style="color: red;">Error uploading ' + file.name + '</p>';
            }});
        }}
        
        function loadFileList() {{
            fetch('/list')
                .then(response => response.json())
                .then(files => {{
                    if (files.length === 0) {{
                        fileList.innerHTML = '<div class="no-images">No images uploaded yet. Drag & drop an image above to get started!</div>';
                    }} else {{
                        fileList.innerHTML = files.map(file => 
                            '<div class="file-item">' + 
                            '<div class="file-info">' +
                            '<span class="file-name">' + file + '</span>' +
                            '</div>' +
                            '<span class="file-command">ri "' + file + '"</span>' +
                            '</div>'
                        ).join('');
                    }}
                }})
                .catch(error => {{
                    console.error('Error loading files:', error);
                    fileList.innerHTML = '<div class="no-images">Error loading file list</div>';
                }});
        }}
        
        // Load file list on page load
        loadFileList();
        
        // Auto-refresh file list every 5 seconds
        setInterval(loadFileList, 5000);
    </script>
</body>
</html>
        """
        self.wfile.write(html.encode())
    
    def do_POST(self):
        """Handle file uploads"""
        if self.path == '/upload':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            file_item = form['file']
            if file_item.filename:
                # Create upload directory if it doesn't exist
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                
                # Save the file
                filename = os.path.basename(file_item.filename)
                filepath = os.path.join(UPLOAD_DIR, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(file_item.file.read())
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"File {filename} uploaded successfully".encode())
                
                print(f"\n✓ Image uploaded: {filename}")
                print(f"  Location: {filepath}")
                print(f"  Use 'ri {filename}' to have Claude read this image\n")
            else:
                self.send_response(400)
                self.end_headers()

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == "__main__":
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    server = HTTPServer(('0.0.0.0', PORT), UploadHandler)
    local_ip = get_local_ip()
    
    print(f"\n🖼️  Image Upload Server Started!")
    print(f"📁 Upload directory: {UPLOAD_DIR}")
    print(f"\n🌐 Access from your Windows machine:")
    print(f"   http://{local_ip}:{PORT}")
    print(f"   http://localhost:{PORT} (if on same machine)")
    print(f"\n📤 Drag & drop images or click to upload")
    print(f"🤖 After upload, use 'ri <filename>' to have Claude read the image")
    print(f"\nPress Ctrl+C to stop the server\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped")
        server.shutdown()