import tkinter as tk
import customtkinter as ctk

class SplitImageApp(ctk.CTkFrame):
    def __init__(self, root, dashboard):
        super().__init__(root, fg_color="#1E1E1E")
        self.root = root
        self.dashboard = dashboard

        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Card-like content frame
        content_frame = ctk.CTkFrame(main_container, fg_color="#252525", corner_radius=15)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Title
        ctk.CTkLabel(
            content_frame,
            text="SG One Split Image",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00F5C4"
        ).pack(pady=(30, 10))

        # Placeholder
        ctk.CTkLabel(
            content_frame,
            text="Split Image Module Coming Soon",
            font=ctk.CTkFont(size=16),
            text_color="#FFFFFF"
        ).pack(pady=20) 