import os
import py7zr
import zipfile
import pyzipper
from typing import List, Tuple, Optional
from pathlib import Path

def get_all_files(path: str) -> List[str]:
    """
    Get all files in a directory recursively, excluding system files
    """
    all_files = []
    if os.path.isfile(path):
        if not CompressionUtils.should_exclude_file(path):
            all_files.append(path)
    else:
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if not CompressionUtils.should_exclude_file(file_path):
                    all_files.append(file_path)
    return all_files

class CompressionUtils:
    @staticmethod
    def should_exclude_file(filename: str) -> bool:
        """
        Check if the file should be excluded from compression
        """
        excluded_files = {
            '.DS_Store',  # macOS system file
            'Thumbs.db',  # Windows thumbnail cache
            'desktop.ini'  # Windows folder settings
        }
        return os.path.basename(filename) in excluded_files

    @staticmethod
    def compress_to_zip(paths: List[str], output_path: str, password: Optional[str] = None) -> Tuple[bool, str]:
        """
        Compress files and folders to ZIP format with optional encryption
        """
        try:
            # Get all files to compress
            all_files = []
            for path in paths:
                all_files.extend(get_all_files(path))
            
            if password:
                with pyzipper.AESZipFile(output_path,
                                       'w',
                                       compression=pyzipper.ZIP_LZMA,
                                       encryption=pyzipper.WZ_AES) as zf:
                    zf.setpassword(password.encode())
                    for file in all_files:
                        # Calculate relative path for the archive
                        rel_path = os.path.relpath(file, os.path.dirname(paths[0]))
                        zf.write(file, rel_path)
            else:
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for file in all_files:
                        # Calculate relative path for the archive
                        rel_path = os.path.relpath(file, os.path.dirname(paths[0]))
                        zf.write(file, rel_path)
            return True, "Compression successful"
        except Exception as e:
            return False, f"Compression failed: {str(e)}"

    @staticmethod
    def compress_to_7z(paths: List[str], output_path: str, password: Optional[str] = None) -> Tuple[bool, str]:
        """
        Compress files and folders to 7Z format with optional encryption
        """
        try:
            # Get all files to compress
            all_files = []
            for path in paths:
                all_files.extend(get_all_files(path))
            
            with py7zr.SevenZipFile(output_path, 'w', password=password) as sz:
                for file in all_files:
                    # Calculate relative path for the archive
                    rel_path = os.path.relpath(file, os.path.dirname(paths[0]))
                    sz.write(file, rel_path)
            return True, "Compression successful"
        except Exception as e:
            return False, f"Compression failed: {str(e)}"

class ExtractionUtils:
    @staticmethod
    def extract_zip(archive_path: str, extract_path: str, password: Optional[str] = None) -> Tuple[bool, str]:
        """
        Extract ZIP archive with optional password
        """
        try:
            try:
                # Try with pyzipper first (for encrypted files)
                with pyzipper.AESZipFile(archive_path, 'r') as zf:
                    if password:
                        zf.setpassword(password.encode())
                    zf.extractall(extract_path)
            except:
                # Fall back to regular zipfile for non-encrypted files
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    if password:
                        zf.setpassword(password.encode())
                    zf.extractall(extract_path)
            return True, "Extraction successful"
        except Exception as e:
            return False, f"Extraction failed: {str(e)}"

    @staticmethod
    def extract_7z(archive_path: str, extract_path: str, password: Optional[str] = None) -> Tuple[bool, str]:
        """
        Extract 7Z archive with optional password
        """
        try:
            with py7zr.SevenZipFile(archive_path, 'r', password=password) as sz:
                sz.extractall(extract_path)
            return True, "Extraction successful"
        except Exception as e:
            return False, f"Extraction failed: {str(e)}"

def get_archive_type(file_path: str) -> str:
    """
    Determine the archive type based on file extension
    """
    ext = Path(file_path).suffix.lower()
    if ext == '.zip':
        return 'zip'
    elif ext == '.7z':
        return '7z'
    else:
        return 'unknown' 