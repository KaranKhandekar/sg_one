import os
import sys
import shutil
import PyInstaller.__main__

def clean_build_dirs():
    """Clean build and dist directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"Cleaned {dir_name} directory")
            except OSError as e:
                print(f"Warning: Could not clean {dir_name} directory: {e}")
                # Try to remove files individually
                for root, dirs, files in os.walk(dir_name, topdown=False):
                    for name in files:
                        try:
                            os.remove(os.path.join(root, name))
                        except OSError:
                            pass
                    for name in dirs:
                        try:
                            os.rmdir(os.path.join(root, name))
                        except OSError:
                            pass
                try:
                    os.rmdir(dir_name)
                    print(f"Cleaned {dir_name} directory after retry")
                except OSError:
                    print(f"Warning: Could not remove {dir_name} directory, continuing anyway")

def create_macos_app():
    """Create macOS app bundle with proper structure"""
    # PyInstaller arguments for macOS
    args = [
        'src/main.py',  # Main script
        '--name=SG_One',  # Name of the executable
        '--windowed',  # No console window
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace existing build
        '--target-architecture=arm64',  # Target Apple Silicon
        '--icon=src/assets/logo.icns',  # macOS icon file
        '--add-data=src/assets:assets',  # Include assets
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=customtkinter',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=moviepy',
        '--osx-bundle-identifier=com.saksglobal.sgone',  # Bundle identifier
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    # Move the app to the correct location
    if os.path.exists('dist/SG_One.app'):
        print("App bundle created successfully!")
    else:
        print("Error: App bundle creation failed!")

def create_windows_exe():
    """Create Windows executable"""
    args = [
        'src/main.py',
        '--name=SG_One',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--icon=src/assets/logo.ico',
        '--add-data=src/assets;assets',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=customtkinter',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=moviepy',
        '--uac-admin',
    ]
    
    PyInstaller.__main__.run(args)

def main():
    print("Starting build process...")
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build based on platform
    if sys.platform == 'darwin':
        print("Building macOS app bundle for Apple Silicon...")
        create_macos_app()
    elif sys.platform == 'win32':
        print("Building Windows executable...")
        create_windows_exe()
    else:
        print("Unsupported platform!")
        return
    
    print("\nBuild completed successfully!")
    print("You can find the application in the 'dist' directory.")

if __name__ == "__main__":
    main() 