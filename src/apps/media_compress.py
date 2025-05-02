import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import customtkinter as ctk
from PIL import Image
import subprocess
from datetime import datetime
from moviepy.editor import VideoFileClip
import numpy as np
import warnings
import logging

# Configure logging
logging.getLogger('PIL').setLevel(logging.WARNING)
logging.getLogger('moviepy').setLevel(logging.WARNING)

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

class MediaCompressApp(ctk.CTkFrame):
    def __init__(self, root, dashboard):
        super().__init__(root, fg_color="#1E1E1E")
        self.root = root
        self.dashboard = dashboard
        
        # Disable Tkinter update checks
        self.root.after_cancel("update")
        self.root.after_cancel("check_dpi_scaling")
        
        # Bind focus events
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<Visibility>', self.on_visibility)
        
        # Create main container to hold content and log
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create main content with card-like appearance
        content_frame = ctk.CTkFrame(self.main_container, fg_color="#252525", corner_radius=15)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=0)
        
        # Title
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill=tk.X, pady=20, padx=30)
        
        ctk.CTkLabel(
            title_frame,
            text="SG One MediaPress",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00F5C4"
        ).pack(side=tk.LEFT)
        
        # Media type selection with radio buttons
        media_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        media_frame.pack(fill=tk.X, pady=20, padx=30)
        
        ctk.CTkLabel(
            media_frame,
            text="Media Type:",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF"
        ).pack(side=tk.LEFT, padx=5)
        
        self.media_var = tk.StringVar(value="image")
        
        image_radio = ctk.CTkRadioButton(
            media_frame,
            text="Image",
            variable=self.media_var,
            value="image",
            font=ctk.CTkFont(size=14),
            fg_color="#00F5C4",
            hover_color="#00D4A8"
        )
        image_radio.pack(side=tk.LEFT, padx=10)
        
        video_radio = ctk.CTkRadioButton(
            media_frame,
            text="Video",
            variable=self.media_var,
            value="video",
            font=ctk.CTkFont(size=14),
            fg_color="#00F5C4",
            hover_color="#00D4A8"
        )
        video_radio.pack(side=tk.LEFT, padx=10)
        
        audio_radio = ctk.CTkRadioButton(
            media_frame,
            text="Audio",
            variable=self.media_var,
            value="audio",
            font=ctk.CTkFont(size=14),
            fg_color="#00F5C4",
            hover_color="#00D4A8"
        )
        audio_radio.pack(side=tk.LEFT, padx=10)
        
        # Quality selection with checkboxes
        quality_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        quality_frame.pack(fill=tk.X, pady=20, padx=30)
        
        ctk.CTkLabel(
            quality_frame,
            text="Quality:",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF"
        ).pack(side=tk.LEFT, padx=5)
        
        self.low_quality_var = tk.BooleanVar(value=False)
        self.medium_quality_var = tk.BooleanVar(value=True)
        self.high_quality_var = tk.BooleanVar(value=False)
        
        low_checkbox = ctk.CTkCheckBox(
            quality_frame,
            text="Low",
            variable=self.low_quality_var,
            font=ctk.CTkFont(size=14),
            fg_color="#00F5C4",
            hover_color="#00D4A8"
        )
        low_checkbox.pack(side=tk.LEFT, padx=10)
        
        medium_checkbox = ctk.CTkCheckBox(
            quality_frame,
            text="Medium",
            variable=self.medium_quality_var,
            font=ctk.CTkFont(size=14),
            fg_color="#00F5C4",
            hover_color="#00D4A8"
        )
        medium_checkbox.pack(side=tk.LEFT, padx=10)
        
        high_checkbox = ctk.CTkCheckBox(
            quality_frame,
            text="High",
            variable=self.high_quality_var,
            font=ctk.CTkFont(size=14),
            fg_color="#00F5C4",
            hover_color="#00D4A8"
        )
        high_checkbox.pack(side=tk.LEFT, padx=10)
        
        # Buttons with modern style
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Compress button
        compress_btn = ctk.CTkButton(
            buttons_frame,
            text="Compress Media",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            command=self.compress_media,
            fg_color="#00F5C4",
            text_color="#000000",
            hover_color="#00D4A8",
            corner_radius=10
        )
        compress_btn.pack(fill=tk.X)
        
        # Progress bar with modern style
        self.progress = ctk.CTkProgressBar(
            content_frame,
            width=300,
            height=8,
            corner_radius=4,
            progress_color="#00F5C4",
            fg_color="#333333"
        )
        self.progress.set(0)
        
        # Separator line
        separator = ctk.CTkFrame(
            content_frame,
            height=1,
            fg_color="#333333"
        )
        separator.pack(fill=tk.X, pady=20, padx=30)
        
        # Video to GIF section
        gif_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        gif_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Video to GIF title
        gif_title_frame = ctk.CTkFrame(gif_frame, fg_color="transparent")
        gif_title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ctk.CTkLabel(
            gif_title_frame,
            text="Video to Animated GIF:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00F5C4"
        ).pack(side=tk.LEFT, padx=5)
        
        # FPS selection
        fps_frame = ctk.CTkFrame(gif_frame, fg_color="transparent")
        fps_frame.pack(fill=tk.X, pady=10)
        
        ctk.CTkLabel(
            fps_frame,
            text="FPS:",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF"
        ).pack(side=tk.LEFT, padx=5)
        
        self.fps_var = tk.StringVar(value="12.5")
        fps_options = ["12.5", "15", "20", "24", "30"]
        fps_combo = ctk.CTkComboBox(
            fps_frame,
            values=fps_options,
            variable=self.fps_var,
            font=ctk.CTkFont(size=14),
            width=100
        )
        fps_combo.pack(side=tk.LEFT, padx=10)
        
        # Size selection
        size_frame = ctk.CTkFrame(gif_frame, fg_color="transparent")
        size_frame.pack(fill=tk.X, pady=10)
        
        ctk.CTkLabel(
            size_frame,
            text="Size:",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF"
        ).pack(side=tk.LEFT, padx=5)
        
        self.size_var = tk.StringVar(value="Original")
        size_options = ["Original", "720p", "480p", "360p"]
        size_combo = ctk.CTkComboBox(
            size_frame,
            values=size_options,
            variable=self.size_var,
            font=ctk.CTkFont(size=14),
            width=100
        )
        size_combo.pack(side=tk.LEFT, padx=10)
        
        # Convert to GIF button
        convert_btn = ctk.CTkButton(
            gif_frame,
            text="Convert Video to Animated GIF",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.convert_to_gif,
            fg_color="#00F5C4",
            text_color="#000000",
            hover_color="#00D4A8",
            corner_radius=10
        )
        convert_btn.pack(fill=tk.X, pady=10)
        
        # Create log panel
        log_frame = ctk.CTkFrame(self.main_container, fg_color="#252525", corner_radius=15, width=300)
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0), pady=0)
        log_frame.pack_propagate(False)  # Fix the width
        
        # Log title
        log_title_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_title_frame.pack(fill=tk.X, pady=20, padx=20)
        
        ctk.CTkLabel(
            log_title_frame,
            text="Activity Log",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00F5C4"
        ).pack(side=tk.LEFT)
        
        # Create log text area
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Courier", 12),
            bg="#333333",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief="flat",
            height=20
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.log_text.configure(state='disabled')
    
    def add_log(self, message):
        """Add a message to the log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)  # Scroll to bottom
        self.log_text.configure(state='disabled')
    
    def on_focus_in(self, event):
        """Handle focus in event"""
        self.root.lift()
        self.root.focus_force()
        
    def on_visibility(self, event):
        """Handle visibility event"""
        if event.state == 'VisibilityUnobscured':
            self.root.lift()
            self.root.focus_force()
    
    def convert_to_gif(self):
        """Convert video to animated GIF with compression"""
        # Ensure window is in front
        self.root.lift()
        self.root.focus_force()
        
        self.add_log("Opening video selection dialog...")
        
        # Get input video
        input_path = filedialog.askopenfilename(
            title="Select Video to Convert",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv"),
                ("All files", "*.*")
            ]
        )
        
        if not input_path:
            self.add_log("Video selection cancelled")
            return
            
        # Get output path
        output_path = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif")],
            initialfile=os.path.splitext(os.path.basename(input_path))[0] + ".gif"
        )
        
        if not output_path:
            self.add_log("Output path selection cancelled")
            return
            
        # Show progress
        self.progress.pack(pady=20)
        self.progress.start()
        
        try:
            self.add_log(f"Loading video: {os.path.basename(input_path)}")
            video = VideoFileClip(input_path)
            
            # Get target size
            size = self.size_var.get()
            if size != "Original":
                if size == "720p":
                    target_size = (1280, 720)
                elif size == "480p":
                    target_size = (854, 480)
                else:  # 360p
                    target_size = (640, 360)
                
                # Calculate new size maintaining aspect ratio
                aspect_ratio = video.size[0] / video.size[1]
                if aspect_ratio > 1:  # Landscape
                    new_width = target_size[0]
                    new_height = int(new_width / aspect_ratio)
                else:  # Portrait
                    new_height = target_size[1]
                    new_width = int(new_height * aspect_ratio)
                
                self.add_log(f"Resizing video to {new_width}x{new_height}")
                video = video.resize((new_width, new_height))
            
            # Set FPS
            fps = float(self.fps_var.get())
            self.add_log(f"Setting FPS to {fps}")
            
            # Convert to GIF with animation
            self.add_log("Converting to animated GIF...")
            
            # Create a temporary file for the initial GIF
            temp_gif = output_path + ".temp.gif"
            
            # Write the GIF with moviepy using basic settings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Disable Tkinter update checks during conversion
                self.root.after_cancel("update")
                self.root.after_cancel("check_dpi_scaling")
                video.write_gif(
                    temp_gif,
                    fps=fps,
                    program='ffmpeg',
                    opt='optimizeplus',
                    fuzz=10,
                    loop=0
                )
            
            # Check file size and compress if needed
            file_size = os.path.getsize(temp_gif) / (1024 * 1024)  # Size in MB
            self.add_log(f"Initial GIF size: {file_size:.2f}MB")
            
            if file_size > 35:
                self.add_log("GIF size exceeds 35MB, applying additional compression...")
                # Load all frames from the temporary GIF
                frames = []
                with Image.open(temp_gif) as img:
                    # Get all frames
                    while True:
                        try:
                            frames.append(img.copy())
                            img.seek(img.tell() + 1)
                        except EOFError:
                            break
                
                # Save frames as an animated GIF with reduced colors
                if frames:
                    frames[0].save(
                        output_path,
                        save_all=True,
                        append_images=frames[1:],
                        optimize=False,  # Disable optimization to preserve animation
                        duration=int(1000/fps),  # Frame duration in milliseconds
                        loop=0,  # Infinite loop
                        quality=85  # Quality setting
                    )
                
                # Remove temporary file
                os.remove(temp_gif)
            else:
                # Move temporary file to final location
                os.rename(temp_gif, output_path)
            
            final_size = os.path.getsize(output_path) / (1024 * 1024)
            self.add_log(f"Final GIF size: {final_size:.2f}MB")
            
            self.add_log(f"Animated GIF created successfully! Saved to: {output_path}")
            messagebox.showinfo(
                "Success",
                f"Video converted to animated GIF successfully!\nSaved to: {output_path}"
            )
        except Exception as e:
            self.add_log(f"Error converting video to animated GIF: {str(e)}")
            messagebox.showerror("Error", f"Failed to convert video to animated GIF: {str(e)}")
        finally:
            # Hide progress
            self.progress.stop()
            self.progress.pack_forget()
            if 'video' in locals():
                video.close()
            # Clean up temporary file if it exists
            if 'temp_gif' in locals() and os.path.exists(temp_gif):
                try:
                    os.remove(temp_gif)
                except:
                    pass
    
    def compress_media(self):
        # Ensure window is in front
        self.root.lift()
        self.root.focus_force()
        
        media_type = self.media_var.get()
        self.add_log(f"Starting {media_type} compression...")
        
        if media_type == "image":
            self.compress_image()
        elif media_type == "video":
            self.compress_video()
        elif media_type == "audio":
            self.compress_audio()
    
    def compress_image(self):
        # Get input image
        input_path = filedialog.askopenfilename(
            title="Select Image to Compress",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if not input_path:
            self.add_log("Image selection cancelled")
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
            self.add_log("Output path selection cancelled")
            return
            
        # Show progress
        self.progress.pack(pady=20)
        self.progress.start()
        
        try:
            # Open image
            img = Image.open(input_path)
            self.add_log(f"Processing image: {os.path.basename(input_path)}")
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGB')
                self.add_log("Converting image to RGB format")
            
            # Set quality based on selection
            quality_map = {
                'low': 30,
                'medium': 60,
                'high': 85
            }
            
            # Save with compression
            quality = quality_map['medium']  # Default to medium if none selected
            if self.low_quality_var.get():
                quality = quality_map['low']
            elif self.high_quality_var.get():
                quality = quality_map['high']
                
            self.add_log(f"Compressing with quality: {quality}")
            img.save(output_path, quality=quality, optimize=True)
            
            # Show success
            self.add_log(f"Image compressed successfully! Saved to: {output_path}")
            messagebox.showinfo(
                "Success",
                f"Image compressed successfully!\nSaved to: {output_path}"
            )
        except Exception as e:
            self.add_log(f"Error compressing image: {str(e)}")
            messagebox.showerror("Error", f"Failed to compress image: {str(e)}")
        finally:
            # Hide progress
            self.progress.stop()
            self.progress.pack_forget()
    
    def compress_video(self):
        self.add_log("Video compression feature coming soon!")
        messagebox.showinfo(
            "Coming Soon",
            "Video compression feature will be available in the next update!"
        )
    
    def compress_audio(self):
        self.add_log("Audio compression feature coming soon!")
        messagebox.showinfo(
            "Coming Soon",
            "Audio compression feature will be available in the next update!"
        ) 