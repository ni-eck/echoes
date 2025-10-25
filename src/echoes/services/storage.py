"""Service for data storage."""

import tempfile
import os
from pathlib import Path
import hashlib
from datetime import datetime

# Create a temp directory for Echoes storage
ECHOES_TEMP_DIR = Path(tempfile.gettempdir()) / "echoes"
ECHOES_TEMP_DIR.mkdir(exist_ok=True)

def save_text(filename: str, content: str) -> str:
    """
    Save text content to a file in the Echoes temp directory.
    
    Args:
        filename: Name of the file (e.g., "story.txt", "audio.mp3")
        content: Text content to save
    
    Returns:
        Full file path where content was saved
    """
    # Generate unique filename using hash and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    base_name, ext = os.path.splitext(filename)
    unique_filename = f"{base_name}_{timestamp}_{content_hash}{ext}"
    
    file_path = ECHOES_TEMP_DIR / unique_filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return str(file_path)

def public_url(path: str) -> str:
    """
    Convert a file path to a mock public URL.
    
    In production, this would upload to cloud storage and return a real URL.
    For now, returns a fake /static/... URL.
    
    Args:
        path: File path to convert
    
    Returns:
        Mock public URL string
    """
    filename = Path(path).name
    return f"/static/{filename}"