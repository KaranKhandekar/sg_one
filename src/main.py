import sys
import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import time
from apps.file_compress import FileCompressApp
from apps.media_compress import MediaCompressApp
from apps.split_image import SplitImageApp
import tkinter.messagebox as messagebox

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate position to center the window
        window_width = 800
        window_height = 500
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main frame with modern dark theme
        self.frame = ctk.CTkFrame(self.root, fg_color="#1E1E1E")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Add logo or app name with modern style
        self.title_label = ctk.CTkLabel(
            self.frame,
            text="Welcome to SG One",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#00F5C4"  # Turquoise accent color
        )
        self.title_label.pack(pady=40)
        
        self.subtitle_label = ctk.CTkLabel(
            self.frame,
            text="The Creative Engine of Saks Global",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFFFFF"
        )
        self.subtitle_label.pack(pady=10)
        
        self.made_in_label = ctk.CTkLabel(
            self.frame,
            text="For Saks Global\nMade in India",
            font=ctk.CTkFont(size=14),
            text_color="#808080"  # Gray text
        )
        self.made_in_label.pack(pady=20)
        
        # Add version with modern style
        self.version_label = ctk.CTkLabel(
            self.frame,
            text="SG One V 1.0.0",
            font=ctk.CTkFont(size=12),
            text_color="#808080"  # Gray text
        )
        self.version_label.pack(pady=20)
        
        # Add loading bar with modern style
        self.progress = ctk.CTkProgressBar(
            self.frame,
            width=300,
            height=8,
            corner_radius=4,
            progress_color="#00F5C4",
            fg_color="#333333"
        )
        self.progress.pack(pady=20)
        self.progress.set(0)
        
        # Start loading animation
        self.loading_animation()
    
    def loading_animation(self):
        for i in range(101):
            self.progress.set(i/100)
            self.root.update()
            time.sleep(0.02)
        self.root.destroy()

class DashboardScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("SG One")
        self.root.geometry("1400x800")
        
        # Configure theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.root, fg_color="#1E1E1E")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self.sidebar = ctk.CTkFrame(self.main_container, fg_color="#252525", width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.sidebar.pack_propagate(False)  # Fix the width
        
        # App title in sidebar
        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(fill=tk.X, padx=20, pady=30)
        
        ctk.CTkLabel(
            title_frame,
            text="SG One",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00F5C4"
        ).pack()
        
        ctk.CTkLabel(
            title_frame,
            text="V 1.0.0",
            font=ctk.CTkFont(size=12),
            text_color="#808080"
        ).pack()
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.current_view = None
        self.active_button = None
        
        # Home button
        self.home_btn = self.create_nav_button(
            nav_frame,
            "🏠 Home",
            self.show_home_view
        )
        
        # SnapZip button
        self.file_compress_btn = self.create_nav_button(
            nav_frame,
            "📁 SnapZip",
            self.show_file_compress
        )
        
        # MediaPress button
        self.media_compress_btn = self.create_nav_button(
            nav_frame,
            "🎬 MediaPress",
            self.show_media_compress
        )
        
        # Split Image button
        self.split_image_btn = self.create_nav_button(
            nav_frame,
            "🖼️ Split Image",
            self.show_split_image
        )
        
        # Footer in sidebar
        footer_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
        
        ctk.CTkLabel(
            footer_frame,
            text="For Saks Global\nMade in India",
            font=ctk.CTkFont(size=12),
            text_color="#808080"
        ).pack()
        
        # Create main content area
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="#1E1E1E")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show home view by default
        self.show_home_view()
    
    def create_nav_button(self, parent, text, command):
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color="#FFFFFF",
            hover_color="#333333",
            anchor="w",
            height=40,
            corner_radius=8
        )
        btn.pack(fill=tk.X, pady=5)
        return btn
    
    def set_active_button(self, active_btn):
        # Reset all buttons
        for btn in [self.home_btn, self.file_compress_btn, self.media_compress_btn, self.split_image_btn]:
            btn.configure(
                fg_color="transparent",
                text_color="#FFFFFF"
            )
        
        # Highlight active button
        active_btn.configure(
            fg_color="#00F5C4",
            text_color="#000000"
        )
    
    def show_home_view(self):
        self.set_active_button(self.home_btn)
        self.clear_content()
        
        # Create scrollable frame for the entire content
        scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create home view content
        welcome_frame = ctk.CTkFrame(scrollable_frame, fg_color="#252525", corner_radius=15)
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Welcome message
        ctk.CTkLabel(
            welcome_frame,
            text="Welcome to SG One",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00F5C4"
        ).pack(pady=20)
        
        # Tagline
        ctk.CTkLabel(
            welcome_frame,
            text="The Creative Engine of Saks Global",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 30))
        
        # App description
        description = """
SG One is a powerful suite of creative tools designed for the Saks Global team.
It provides three main applications:

• Split Image
  - Split and organize images efficiently
  - Automatic background detection
  - Smart distribution to designers
  - Detailed activity logging
  - Excel report generation

• SnapZip
  - Compress multiple files and folders
  - Support for ZIP and 7Z formats
  - Easy extraction of archives
  - Secure and efficient compression
  - Automatic exclusion of system files:
    ∙ .DS_Store (macOS)
    ∙ Thumbs.db (Windows)
    ∙ desktop.ini (Windows)
  - Real-time activity logging

• MediaPress
  - Compress media files while maintaining quality
  - Support for various image formats
  - Video compression
  - Audio compression
  - Video to GIF conversion

Choose an application from the sidebar to get started!
        """
        
        ctk.CTkLabel(
            welcome_frame,
            text=description,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            justify="left"
        ).pack(pady=20, padx=40)
        
        # Separator line
        separator = ctk.CTkFrame(
            welcome_frame,
            height=2,
            fg_color="#333333"
        )
        separator.pack(fill=tk.X, padx=40, pady=20)
        
        # Support Contact
        contact_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        contact_frame.pack(fill=tk.X, padx=40, pady=(20, 10))
        
        ctk.CTkLabel(
            contact_frame,
            text="Support Contact",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00F5C4"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            contact_frame,
            text="coe@saks.com | karan.khandekar@saks.com",
            font=ctk.CTkFont(size=16),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(5, 0))
        
        # Special Thanks
        thanks_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        thanks_frame.pack(fill=tk.X, padx=40, pady=(20, 10))
        
        ctk.CTkLabel(
            thanks_frame,
            text="Special Thanks",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00F5C4"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            thanks_frame,
            text="Deepika Sharma and Gnanaprakash K",
            font=ctk.CTkFont(size=16),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(5, 0))
        
        # GitHub Link
        github_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        github_frame.pack(fill=tk.X, padx=40, pady=(20, 20))
        
        ctk.CTkLabel(
            github_frame,
            text="GitHub Repository",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00F5C4"
        ).pack(anchor="w", pady=(0, 10))
        
        github_btn = ctk.CTkButton(
            github_frame,
            text="Visit GitHub Repository",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: self.open_github(),
            fg_color="#00F5C4",
            hover_color="#00D4A8",
            text_color="#000000",
            height=45,
            corner_radius=8,
            width=250
        )
        github_btn.pack(anchor="w")
    
    def open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/KaranKhandekar/sg_one")
    
    def show_file_compress(self):
        self.set_active_button(self.file_compress_btn)
        self.clear_content()
        if self.current_view:
            self.current_view.destroy()
        self.current_view = FileCompressApp(self.content_frame, self)
        self.current_view.pack(fill=tk.BOTH, expand=True)
    
    def show_media_compress(self):
        self.set_active_button(self.media_compress_btn)
        self.clear_content()
        if self.current_view:
            self.current_view.destroy()
        self.current_view = MediaCompressApp(self.content_frame, self)
        self.current_view.pack(fill=tk.BOTH, expand=True)
        self.root.update()  # Force update the UI
    
    def show_split_image(self):
        print("Starting show_split_image...")  # Debug log
        self.set_active_button(self.split_image_btn)
        print("Button set active...")  # Debug log
        self.clear_content()
        print("Content cleared...")  # Debug log
        if self.current_view:
            print("Destroying current view...")  # Debug log
            self.current_view.destroy()
        try:
            print("Creating SplitImageApp...")  # Debug log
            self.current_view = SplitImageApp(self.content_frame, self)
            print("SplitImageApp created...")  # Debug log
            self.current_view.pack(fill=tk.BOTH, expand=True)
            print("SplitImageApp packed...")  # Debug log
            self.root.update()
            print("Root updated...")  # Debug log
            self.root.lift()
            print("Window lifted...")  # Debug log
        except Exception as e:
            print(f"Error in show_split_image: {str(e)}")  # Debug log
            messagebox.showerror("Error", f"Failed to load Split Image module: {str(e)}")
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.show_home_view()

def main():
    # Create root window
    root = ctk.CTk()
    
    # Show splash screen
    splash = SplashScreen(root)
    root.mainloop()
    
    # Create new root window for dashboard
    root = ctk.CTk()
    root.title("SG One")
    root.geometry("1400x800")
    
    # Configure theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create dashboard
    app = DashboardScreen(root)
    
    # Handle window close
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.quit()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 