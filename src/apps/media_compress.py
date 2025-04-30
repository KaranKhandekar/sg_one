import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
import subprocess

class MediaCompressApp(ctk.CTkFrame):
    def __init__(self, root, home_screen):
        super().__init__(root, fg_color="#1a1a1a")
        self.home_screen = home_screen
        
        # Create header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill=tk.X, pady=20)
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            command=self.go_back,
            width=100
        )
        back_btn.pack(side=tk.LEFT, padx=20)
        
        # Title
        ctk.CTkLabel(
            header_frame,
            text="MediaCompressX",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        ).pack(side=tk.LEFT, padx=20)
        
        # Create main content
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Media type selection
        media_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        media_frame.pack(fill=tk.X, pady=10)
        
        ctk.CTkLabel(
            media_frame,
            text="Media Type:",
            font=ctk.CTkFont(size=16),
            text_color="#ffffff"
        ).pack(side=tk.LEFT, padx=5)
        
        self.media_var = tk.StringVar(value="Image")
        media_combo = ctk.CTkComboBox(
            media_frame,
            values=["Image", "Video", "Audio"],
            variable=self.media_var,
            state="readonly",
            width=100
        )
        media_combo.pack(side=tk.LEFT, padx=5)
        
        # Quality selection
        quality_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        quality_frame.pack(fill=tk.X, pady=10)
        
        ctk.CTkLabel(
            quality_frame,
            text="Quality:",
            font=ctk.CTkFont(size=16),
            text_color="#ffffff"
        ).pack(side=tk.LEFT, padx=5)
        
        self.quality_var = tk.StringVar(value="Medium")
        quality_combo = ctk.CTkComboBox(
            quality_frame,
            values=["Low", "Medium", "High"],
            variable=self.quality_var,
            state="readonly",
            width=100
        )
        quality_combo.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # Compress button
        compress_btn = ctk.CTkButton(
            buttons_frame,
            text="Compress Media",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.compress_media
        )
        compress_btn.pack(fill=tk.X, pady=10)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.set(0)
    
    def go_back(self):
        self.pack_forget()
        self.home_screen.show_home()
    
    def compress_media(self):
        media_type = self.media_var.get().lower()
        quality = self.quality_var.get().lower()
        
        if media_type == "image":
            self.compress_image(quality)
        elif media_type == "video":
            self.compress_video(quality)
        elif media_type == "audio":
            self.compress_audio(quality)
    
    def compress_image(self, quality):
        # Get input image
        input_path = filedialog.askopenfilename(
            title="Select Image to Compress",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if not input_path:
            return
            
        # Get output path
        output_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("WebP files", "*.webp"),
                ("All files", "*.*")
            ]
        )
        
        if not output_path:
            return
            
        # Show progress
        self.progress.pack(pady=20)
        self.progress.start()
        
        try:
            # Open image
            img = Image.open(input_path)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGB')
            
            # Set quality based on selection
            quality_map = {
                'low': 30,
                'medium': 60,
                'high': 85
            }
            
            # Save with compression
            img.save(output_path, quality=quality_map[quality], optimize=True)
            
            # Show success
            messagebox.showinfo(
                "Success",
                f"Image compressed successfully!\nSaved to: {output_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compress image: {str(e)}")
        finally:
            # Hide progress
            self.progress.stop()
            self.progress.pack_forget()
    
    def compress_video(self, quality):
        messagebox.showinfo(
            "Coming Soon",
            "Video compression feature will be available in the next update!"
        )
    
    def compress_audio(self, quality):
        messagebox.showinfo(
            "Coming Soon",
            "Audio compression feature will be available in the next update!"
        ) 