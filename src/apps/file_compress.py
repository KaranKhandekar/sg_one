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
        
        # Initialize last selected locations
        self.last_file_location = os.path.expanduser("~")
        self.last_folder_location = os.path.expanduser("~")
        self.last_save_location = os.path.expanduser("~")
        self.last_batch_parent_location = os.path.expanduser("~")  # New variable for batch zip parent folder
        
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
        
        # Create format checkboxes
        self.zip_var = tk.BooleanVar(value=True)
        self.sevenz_var = tk.BooleanVar(value=False)
        
        zip_checkbox = ctk.CTkCheckBox(
            format_frame,
            text="ZIP",
            variable=self.zip_var,
            font=ctk.CTkFont(size=14),
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            fg_color="#00F5C4",
            hover_color="#00D4A8"
        )
        zip_checkbox.pack(side=tk.LEFT, padx=10)
        
        sevenz_checkbox = ctk.CTkCheckBox(
            format_frame,
            text="7Z",
            variable=self.sevenz_var,
            font=ctk.CTkFont(size=14),
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            fg_color="#00F5C4",
            hover_color="#00D4A8"
        )
        sevenz_checkbox.pack(side=tk.LEFT, padx=10)
        
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
        select_folder_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Batch Zip button
        batch_zip_btn = ctk.CTkButton(
            selection_frame,
            text="Batch Zip",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            command=self.handle_batch_zip,
            fg_color="#00F5C4",
            text_color="#000000",
            hover_color="#00D4A8",
            corner_radius=10
        )
        batch_zip_btn.pack(fill=tk.X)
        
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
                filetypes=[("All files", "*.*")],
                initialdir=self.last_file_location
            )
            if paths:
                # Remember the parent directory of the first selected file
                self.last_file_location = os.path.dirname(os.path.dirname(paths[0]))
                self.add_log(f"Selected {len(paths)} file(s)")
                self.handle_compression(paths)
            else:
                self.add_log("File selection cancelled")
        else:  # folder
            self.add_log("Opening folder selection dialog...")
            path = filedialog.askdirectory(
                title="Select Folder to Compress",
                initialdir=self.last_folder_location
            )
            if path:
                # Remember the parent directory of the selected folder
                self.last_folder_location = os.path.dirname(path)
                self.add_log(f"Selected folder: {os.path.basename(path)}")
                self.handle_compression([path])
            else:
                self.add_log("Folder selection cancelled")
    
    def handle_compression(self, paths):
        if not paths:
            return
            
        # Determine base name for the archive
        if len(paths) == 1:
            base_name = os.path.basename(paths[0])
        else:
            base_name = "compressed_files"
            
        # Get the directory of the first selected item
        base_dir = os.path.dirname(paths[0])
            
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
        
        # Compress files in selected formats
        success_messages = []
        error_messages = []
        
        if self.zip_var.get():
            output_path = os.path.join(base_dir, f"{base_name}.zip")
            self.add_log(f"Starting compression in ZIP format...")
            success, message = CompressionUtils.compress_to_zip(paths, output_path)
            if success:
                success_messages.append(f"ZIP: {message}")
            else:
                error_messages.append(f"ZIP: {message}")
                
        if self.sevenz_var.get():
            output_path = os.path.join(base_dir, f"{base_name}.7z")
            self.add_log(f"Starting compression in 7Z format...")
            success, message = CompressionUtils.compress_to_7z(paths, output_path)
            if success:
                success_messages.append(f"7Z: {message}")
            else:
                error_messages.append(f"7Z: {message}")
            
        # Hide progress
        self.progress.stop()
        self.progress.pack_forget()
        
        # Show results
        if success_messages:
            self.add_log("Success: " + "\n".join(success_messages))
            messagebox.showinfo("Success", "\n".join(success_messages))
        if error_messages:
            self.add_log("Error: " + "\n".join(error_messages))
            messagebox.showerror("Error", "\n".join(error_messages))
    
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
    
    def handle_batch_zip(self):
        """Handle batch compression of multiple folders"""
        self.add_log("Select parent folder containing folders to compress...")
        
        # Open directory selection dialog
        parent_folder = filedialog.askdirectory(
            title="Select Parent Folder",
            initialdir=self.last_batch_parent_location  # Use the batch parent location
        )
        
        if not parent_folder:
            self.add_log("Folder selection cancelled")
            return
            
        # Remember the parent directory for both regular and batch operations
        self.last_folder_location = parent_folder
        self.last_batch_parent_location = parent_folder  # Remember for next batch operation
        
        # Get all immediate subdirectories
        folder_paths = []
        for item in os.listdir(parent_folder):
            item_path = os.path.join(parent_folder, item)
            if os.path.isdir(item_path):
                folder_paths.append(item_path)
        
        if not folder_paths:
            self.add_log("No folders found in the selected directory")
            messagebox.showwarning("Warning", "No folders found in the selected directory!")
            return
            
        self.add_log(f"Found {len(folder_paths)} folders for batch compression")
        
        # Show progress
        self.progress.pack(pady=20)
        self.progress.start()
        
        success_messages = []
        error_messages = []
        
        # Process each folder
        for i, folder_path in enumerate(folder_paths):
            self.progress.set(i / len(folder_paths))
            self.root.update()
            
            folder_name = os.path.basename(folder_path)
            
            # Log files being excluded
            for root, dirs, files in os.walk(folder_path):
                excluded_files = [f for f in files if CompressionUtils.should_exclude_file(f)]
                if excluded_files:
                    self.add_log(f"Excluding system files from {os.path.basename(root)}: {', '.join(excluded_files)}")
            
            # Compress in selected formats
            if self.zip_var.get():
                output_path = os.path.join(parent_folder, f"{folder_name}.zip")
                self.add_log(f"Compressing {folder_name} to ZIP...")
                success, message = CompressionUtils.compress_to_zip([folder_path], output_path)
                if success:
                    success_messages.append(f"ZIP: {folder_name} - {message}")
                else:
                    error_messages.append(f"ZIP: {folder_name} - {message}")
                    
            if self.sevenz_var.get():
                output_path = os.path.join(parent_folder, f"{folder_name}.7z")
                self.add_log(f"Compressing {folder_name} to 7Z...")
                success, message = CompressionUtils.compress_to_7z([folder_path], output_path)
                if success:
                    success_messages.append(f"7Z: {folder_name} - {message}")
                else:
                    error_messages.append(f"7Z: {folder_name} - {message}")
        
        # Hide progress
        self.progress.stop()
        self.progress.pack_forget()
        
        # Show results
        if success_messages:
            self.add_log("Success: " + "\n".join(success_messages))
            messagebox.showinfo("Success", "\n".join(success_messages))
        if error_messages:
            self.add_log("Error: " + "\n".join(error_messages))
            messagebox.showerror("Error", "\n".join(error_messages)) 