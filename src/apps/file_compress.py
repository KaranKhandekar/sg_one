import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import customtkinter as ctk
from utils import CompressionUtils, ExtractionUtils, get_archive_type
from datetime import datetime

class FileCompressApp(ctk.CTkFrame):
    def __init__(self, root, dashboard):
        super().__init__(root, fg_color="#1E1E1E")
        self.root = root
        self.dashboard = dashboard
        
        # Create main container to hold content and log
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create main content with card-like appearance
        content_frame = ctk.CTkFrame(main_container, fg_color="#252525", corner_radius=15)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=0)
        
        # Title
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill=tk.X, pady=20, padx=30)
        
        ctk.CTkLabel(
            title_frame,
            text="SG One SnapZip",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00F5C4"
        ).pack(side=tk.LEFT)
        
        # Format selection with modern style
        format_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        format_frame.pack(fill=tk.X, pady=20, padx=30)
        
        ctk.CTkLabel(
            format_frame,
            text="Format:",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF"
        ).pack(side=tk.LEFT, padx=5)
        
        self.format_var = tk.StringVar(value="ZIP")
        format_combo = ctk.CTkComboBox(
            format_frame,
            values=["ZIP", "7Z"],
            variable=self.format_var,
            state="readonly",
            width=120,
            font=ctk.CTkFont(size=14),
            fg_color="#333333",
            button_color="#404040",
            button_hover_color="#505050",
            border_color="#00F5C4",
            dropdown_fg_color="#333333"
        )
        format_combo.pack(side=tk.LEFT, padx=5)
        
        # Buttons with modern style
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Create a frame for file and folder selection buttons
        selection_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        selection_frame.pack(fill=tk.X, pady=10)
        
        # Select Files button
        select_files_btn = ctk.CTkButton(
            selection_frame,
            text="Select Files",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            command=lambda: self.handle_compression_selection("files"),
            fg_color="#00F5C4",
            text_color="#000000",
            hover_color="#00D4A8",
            corner_radius=10
        )
        select_files_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Select Folder button
        select_folder_btn = ctk.CTkButton(
            selection_frame,
            text="Select Folder",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            command=lambda: self.handle_compression_selection("folder"),
            fg_color="#00F5C4",
            text_color="#000000",
            hover_color="#00D4A8",
            corner_radius=10
        )
        select_folder_btn.pack(fill=tk.X)
        
        # Extract button
        extract_btn = ctk.CTkButton(
            buttons_frame,
            text="Extract Archive",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            command=self.extract_files,
            fg_color="#333333",
            hover_color="#404040",
            corner_radius=10
        )
        extract_btn.pack(fill=tk.X, pady=10)
        
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
        
        # Create log panel
        log_frame = ctk.CTkFrame(main_container, fg_color="#252525", corner_radius=15, width=300)
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
    
    def handle_compression_selection(self, selection_type):
        if selection_type == "files":
            self.add_log("Opening file selection dialog...")
            paths = filedialog.askopenfilenames(
                title="Select Files to Compress",
                filetypes=[("All files", "*.*")]
            )
            if paths:
                self.add_log(f"Selected {len(paths)} file(s)")
                self.handle_compression(paths)
            else:
                self.add_log("File selection cancelled")
        else:  # folder
            self.add_log("Opening folder selection dialog...")
            path = filedialog.askdirectory(
                title="Select Folder to Compress"
            )
            if path:
                self.add_log(f"Selected folder: {os.path.basename(path)}")
                self.handle_compression([path])
            else:
                self.add_log("Folder selection cancelled")
    
    def handle_compression(self, paths):
        if not paths:
            return
            
        self.add_log("Opening save dialog...")
        # Get output path
        output_path = filedialog.asksaveasfilename(
            defaultextension=f".{self.format_var.get().lower()}",
            filetypes=[
                (f"{self.format_var.get()} files", f"*.{self.format_var.get().lower()}"),
                ("All files", "*.*")
            ]
        )
        
        if not output_path:
            self.add_log("Save location selection cancelled")
            return
            
        # Show progress
        self.progress.pack(pady=20)
        self.progress.start()
        
        # Log files being excluded
        for path in paths:
            if os.path.isfile(path):
                if CompressionUtils.should_exclude_file(path):
                    self.add_log(f"Excluding system file: {os.path.basename(path)}")
            else:
                # Check directory contents
                for root, dirs, files in os.walk(path):
                    excluded_files = [f for f in files if CompressionUtils.should_exclude_file(f)]
                    if excluded_files:
                        self.add_log(f"Excluding system files from {os.path.basename(root)}: {', '.join(excluded_files)}")
        
        # Compress files
        format_type = self.format_var.get().lower()
        self.add_log(f"Starting compression in {format_type.upper()} format...")
        
        if format_type == 'zip':
            success, message = CompressionUtils.compress_to_zip(paths, output_path)
        else:  # 7z
            success, message = CompressionUtils.compress_to_7z(paths, output_path)
            
        # Hide progress
        self.progress.stop()
        self.progress.pack_forget()
        
        # Show result
        if success:
            self.add_log(f"Success: {message}")
            messagebox.showinfo("Success", message)
        else:
            self.add_log(f"Error: {message}")
            messagebox.showerror("Error", message)
    
    def extract_files(self):
        self.add_log("Opening archive selection dialog...")
        archive_path = filedialog.askopenfilename(
            title="Select Archive to Extract",
            filetypes=[
                ("Archive files", "*.zip *.7z"),
                ("All files", "*.*")
            ]
        )
        
        if not archive_path:
            self.add_log("Archive selection cancelled")
            return
            
        self.add_log("Opening extraction directory selection...")
        # Get extraction directory
        extract_dir = filedialog.askdirectory(
            title="Select Extraction Directory"
        )
        
        if not extract_dir:
            self.add_log("Extraction directory selection cancelled")
            return
            
        # Show progress
        self.progress.pack(pady=20)
        self.progress.start()
        
        # Extract archive
        archive_type = get_archive_type(archive_path)
        self.add_log(f"Starting extraction of {archive_type.upper()} archive...")
        
        if archive_type == 'zip':
            success, message = ExtractionUtils.extract_zip(archive_path, extract_dir)
        elif archive_type == '7z':
            success, message = ExtractionUtils.extract_7z(archive_path, extract_dir)
        else:
            success, message = False, "Unsupported archive format"
            
        # Hide progress
        self.progress.stop()
        self.progress.pack_forget()
        
        # Show result
        if success:
            self.add_log(f"Success: {message}")
            messagebox.showinfo("Success", message)
        else:
            self.add_log(f"Error: {message}")
            messagebox.showerror("Error", message) 