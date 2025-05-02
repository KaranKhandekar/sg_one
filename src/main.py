import sys
import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import time
from apps.file_compress import FileCompressApp
from apps.media_compress import MediaCompressApp

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
        for btn in [self.home_btn, self.file_compress_btn, self.media_compress_btn]:
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
        
        # Create home view content
        welcome_frame = ctk.CTkFrame(self.content_frame, fg_color="#252525", corner_radius=15)
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
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
It provides two main applications:

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
  - Video compression (Coming Soon)
  - Audio compression (Coming Soon)

Choose an application from the sidebar to get started!
        """
        
        ctk.CTkLabel(
            welcome_frame,
            text=description,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            justify="left"
        ).pack(pady=20, padx=40)
    
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
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.show_home_view()

def main():
    root = ctk.CTk()
    
    # Show splash screen
    splash = SplashScreen(root)
    root.mainloop()
    
    # Create new root window for dashboard
    root = ctk.CTk()
    app = DashboardScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main() 