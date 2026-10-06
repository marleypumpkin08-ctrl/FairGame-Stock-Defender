"""
UI module for FairGame Stock Defender.
Implements the main dashboard using CustomTkinter.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import asyncio
import time
import webbrowser
import sys
from typing import List, Dict, Optional
from datetime import datetime


class StockDefenderUI:
    """Main UI class for the Stock Defender application."""

    def __init__(self, scraper, config: dict):
        """
        Initialize the UI.

        Args:
            scraper: StockScraper instance
            config: Configuration dictionary
        """
        self.scraper = scraper
        self.config = config
        self.alert_history: List[str] = []
        self.current_version = config.get("version", "1.6.0")

        # Configure CustomTkinter theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Create main window
        self.root = ctk.CTk()
        self.root.title(f"FairGame Stock Defender (v{self.current_version})")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        # Build UI
        self._build_ui()

        # Start monitoring
        self._start_monitoring_thread()

    def _build_ui(self):
        """Build the complete UI layout."""
        # Main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Create three-column layout
        self._build_left_sidebar()
        self._build_main_content()
        self._build_right_sidebar()

    def _build_left_sidebar(self):
        """Build the left sidebar with watchlist and settings."""
        self.left_sidebar = ctk.CTkFrame(self.main_container, width=250)
        self.left_sidebar.pack(side="left", fill="y", padx=(0, 5))
        self.left_sidebar.pack_propagate(False)

        # Header
        header = ctk.CTkLabel(
            self.left_sidebar,
            text="Product Watchlist",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.pack(pady=(15, 10))

        # Watchlist count
        self.watchlist_count = ctk.CTkLabel(
            self.left_sidebar,
            text="(0)",
            font=ctk.CTkFont(size=14)
        )
        self.watchlist_count.pack(pady=(0, 15))

        # Scrollable watchlist frame
        self.watchlist_frame = ctk.CTkScrollableFrame(
            self.left_sidebar,
            label_text="",
            height=300
        )
        self.watchlist_frame.pack(fill="x", padx=10, pady=(0, 15))

        # Add product button
        self.add_product_btn = ctk.CTkButton(
            self.left_sidebar,
            text="+ Add Product",
            command=self._show_add_product_dialog,
            height=40
        )
        self.add_product_btn.pack(fill="x", padx=10, pady=(0, 20))

        # Alert Settings section
        settings_header = ctk.CTkLabel(
            self.left_sidebar,
            text="Alert Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        settings_header.pack(pady=(0, 10))

        # Sound alerts toggle
        self.sound_alerts_var = ctk.BooleanVar(value=self.config.get("alert_sound_enabled", True))
        self.sound_alerts_switch = ctk.CTkSwitch(
            self.left_sidebar,
            text="System Sound Alerts",
            variable=self.sound_alerts_var,
            command=self._toggle_sound_alerts
        )
        self.sound_alerts_switch.pack(fill="x", padx=10, pady=5)

        # Desktop notifications toggle
        self.desktop_notifications_var = ctk.BooleanVar(value=self.config.get("desktop_notifications_enabled", True))
        self.desktop_notifications_switch = ctk.CTkSwitch(
            self.left_sidebar,
            text="Desktop Notifications",
            variable=self.desktop_notifications_var,
            command=self._toggle_desktop_notifications
        )
        self.desktop_notifications_switch.pack(fill="x", padx=10, pady=5)

        # Navigation & Monitor Control section
        control_header = ctk.CTkLabel(
            self.left_sidebar,
            text="Monitor Control",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        control_header.pack(pady=(20, 10))

        # Start/Stop monitoring button
        self.monitor_btn = ctk.CTkButton(
            self.left_sidebar,
            text="Stop Monitoring",
            command=self._toggle_monitoring,
            height=40,
            fg_color="red"
        )
        self.monitor_btn.pack(fill="x", padx=10, pady=5)

    def _build_main_content(self):
        """Build the main content area with the tracker grid."""
        self.main_content = ctk.CTkFrame(self.main_container)
        self.main_content.pack(side="left", fill="both", expand=True, padx=5)

        # Header
        header = ctk.CTkLabel(
            self.main_content,
            text="The Live Tracker Grid",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header.pack(pady=(15, 10))

        # Create treeview for data grid
        self._create_tracker_grid()

    def _create_tracker_grid(self):
        """Create the data grid/treeview for tracking products."""
        # Use standard tkinter Treeview with CustomTkinter styling
        grid_frame = ctk.CTkFrame(self.main_content)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Treeview
        self.tree = ttk.Treeview(
            grid_frame,
            columns=("product", "store", "status", "last_check"),
            show="headings",
            height=15
        )

        # Define columns
        self.tree.heading("product", text="Product")
        self.tree.heading("store", text="Store")
        self.tree.heading("status", text="Status")
        self.tree.heading("last_check", text="Last Check")

        self.tree.column("product", width=300)
        self.tree.column("store", width=150)
        self.tree.column("status", width=150)
        self.tree.column("last_check", width=120)

        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            font=("Arial", 11)
        )
        style.configure(
            "Treeview.Heading",
            background="#1a1a1a",
            foreground="white",
            font=("Arial", 12, "bold")
        )
        style.map("Treeview", background=[("selected", "#006400")])

        # Scrollbar
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_right_sidebar(self):
        """Build the right sidebar with version info and logs."""
        self.right_sidebar = ctk.CTkFrame(self.main_container, width=280)
        self.right_sidebar.pack(side="right", fill="y", padx=(5, 0))
        self.right_sidebar.pack_propagate(False)

        # GitHub Version section
        version_header = ctk.CTkLabel(
            self.right_sidebar,
            text="GitHub Version",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        version_header.pack(pady=(15, 10))

        self.version_label = ctk.CTkLabel(
            self.right_sidebar,
            text=f"v{self.current_version} [Checking...]",
            font=ctk.CTkFont(size=12),
            text_color="yellow"
        )
        self.version_label.pack(pady=(0, 15))

        # Alert History Logs section
        logs_header = ctk.CTkLabel(
            self.right_sidebar,
            text="Alert History Logs",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        logs_header.pack(pady=(0, 10))

        # Scrollable logs frame
        self.logs_frame = ctk.CTkScrollableFrame(
            self.right_sidebar,
            label_text="",
            height=300
        )
        self.logs_frame.pack(fill="x", padx=10, pady=(0, 15))

        # Support Development section
        support_header = ctk.CTkLabel(
            self.right_sidebar,
            text="Support Development",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        support_header.pack(pady=(0, 10))

        support_text = ctk.CTkLabel(
            self.right_sidebar,
            text="Like this tool? Keep it\nfree with a donation.",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        support_text.pack(pady=(0, 10))

        self.donate_btn = ctk.CTkButton(
            self.right_sidebar,
            text="SUPPORT DEVELOPMENT (Ko-fi)",
            command=self._open_donation_link,
            height=45,
            fg_color="#FF5E5B",
            hover_color="#E04946"
        )
        self.donate_btn.pack(fill="x", padx=10, pady=(0, 20))

    def _show_add_product_dialog(self):
        """Show dialog to add a new product."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Product")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # Product name
        ctk.CTkLabel(dialog, text="Product Name:").pack(pady=(20, 5))
        name_entry = ctk.CTkEntry(dialog, width=400)
        name_entry.pack(pady=5)

        # Store
        ctk.CTkLabel(dialog, text="Store:").pack(pady=(15, 5))
        store_entry = ctk.CTkEntry(dialog, width=400)
        store_entry.pack(pady=5)

        # URL
        ctk.CTkLabel(dialog, text="Product URL:").pack(pady=(15, 5))
        url_entry = ctk.CTkEntry(dialog, width=400)
        url_entry.pack(pady=5)

        # Add button
        def add_product():
            name = name_entry.get().strip()
            store = store_entry.get().strip()
            url = url_entry.get().strip()

            if name and store and url:
                self.scraper.add_product(url, name, store)
                self._update_watchlist()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields")

        add_btn = ctk.CTkButton(
            dialog,
            text="Add Product",
            command=add_product,
            height=40
        )
        add_btn.pack(pady=20)

    def _update_watchlist(self):
        """Update the watchlist display."""
        # Clear existing widgets
        for widget in self.watchlist_frame.winfo_children():
            widget.destroy()

        products = self.scraper.get_all_products()

        # Update count
        self.watchlist_count.configure(text=f"({len(products)})")

        # Add product items
        for product in products:
            item_frame = ctk.CTkFrame(self.watchlist_frame, height=50)
            item_frame.pack(fill="x", pady=5, padx=5)

            name_label = ctk.CTkLabel(
                item_frame,
                text=product["name"],
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            name_label.pack(fill="x", padx=10, pady=(5, 0))

            store_label = ctk.CTkLabel(
                item_frame,
                text=product["store"],
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="w"
            )
            store_label.pack(fill="x", padx=10, pady=(0, 5))

            # Delete button
            delete_btn = ctk.CTkButton(
                item_frame,
                text="✕",
                width=30,
                height=30,
                command=lambda p=product: self._remove_product(p["url"])
            )
            delete_btn.pack(anchor="e", padx=5, pady=5)

    def _remove_product(self, url: str):
        """Remove a product from monitoring."""
        self.scraper.remove_product(url)
        self._update_watchlist()
        self._update_tracker_grid()

    def _update_tracker_grid(self):
        """Update the tracker grid with current product statuses."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        products = self.scraper.get_all_products()

        for product in products:
            status = product["status"]
            last_check = product.get("last_check", "Never")

            # Insert item
            item_id = self.tree.insert(
                "",
                "end",
                values=(product["name"], product["store"], status, last_check)
            )

            # Color code status
            if "IN STOCK" in status.upper():
                self.tree.tag_configure("in_stock", background="#006400", foreground="white")
                self.tree.item(item_id, tags=("in_stock",))
            elif "OUT OF STOCK" in status.upper():
                self.tree.tag_configure("out_of_stock", background="#8B0000", foreground="white")
                self.tree.item(item_id, tags=("out_of_stock",))
            elif "ERROR" in status.upper() or "TIMEOUT" in status.upper():
                self.tree.tag_configure("error", background="#8B4513", foreground="white")
                self.tree.item(item_id, tags=("error",))

    def _add_alert_log(self, message: str):
        """Add an entry to the alert history logs."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"

        self.alert_history.insert(0, log_entry)

        # Keep only last 50 logs
        if len(self.alert_history) > 50:
            self.alert_history = self.alert_history[:50]

        # Update logs display
        self._update_logs_display()

    def _update_logs_display(self):
        """Update the logs display frame."""
        # Clear existing widgets
        for widget in self.logs_frame.winfo_children():
            widget.destroy()

        # Add log entries
        for log in self.alert_history[:20]:  # Show last 20
            log_label = ctk.CTkLabel(
                self.logs_frame,
                text=log,
                font=ctk.CTkFont(size=10),
                anchor="w"
            )
            log_label.pack(fill="x", pady=2, padx=5)

    def _toggle_sound_alerts(self):
        """Toggle sound alerts setting."""
        self.config["alert_sound_enabled"] = self.sound_alerts_var.get()

    def _toggle_desktop_notifications(self):
        """Toggle desktop notifications setting."""
        self.config["desktop_notifications_enabled"] = self.desktop_notifications_var.get()

    def _toggle_monitoring(self):
        """Toggle monitoring on/off."""
        if self.scraper.is_running:
            self.scraper.stop_monitoring()
            self.monitor_btn.configure(text="Start Monitoring", fg_color="green")
        else:
            self._start_monitoring_thread()
            self.monitor_btn.configure(text="Stop Monitoring", fg_color="red")

    def _start_monitoring_thread(self):
        """Start the monitoring in a background thread."""
        def run_monitoring():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.scraper.start_monitoring())

        thread = threading.Thread(target=run_monitoring, daemon=True)
        thread.start()

    def _open_donation_link(self):
        """Open the donation link in the default browser."""
        donation_url = self.config.get("donation_url", "https://ko-fi.com")
        webbrowser.open(donation_url)

    def set_version_status(self, is_up_to_date: bool, latest_version: str = None):
        """
        Update the version status display.

        Args:
            is_up_to_date: Whether the current version is up to date
            latest_version: Latest version from GitHub
        """
        if is_up_to_date:
            self.version_label.configure(
                text=f"v{self.current_version} [Up to Date]",
                text_color="#00FF00"
            )
        else:
            self.version_label.configure(
                text=f"v{self.current_version} [Update: v{latest_version}]",
                text_color="#FFA500"
            )

    def handle_stock_alert(self, product: Dict):
        """
        Handle a stock alert from the scraper.

        Args:
            product: Product dictionary that triggered the alert
        """
        # Add to alert logs
        self._add_alert_log(f"{product['store']}: IN STOCK!")

        # Play sound if enabled
        if self.config.get("alert_sound_enabled", True):
            self._play_alert_sound()

        # Show desktop notification if enabled
        if self.config.get("desktop_notifications_enabled", True):
            self._show_desktop_notification(product)

        # Update grid
        self._update_tracker_grid()

    def _play_alert_sound(self):
        """Play an alert sound."""
        try:
            import winsound
            winsound.Beep(1000, 500)
            winsound.Beep(1500, 500)
        except:
            # Fallback for non-Windows systems
            print("\a" * 3)

    def _show_desktop_notification(self, product: Dict):
        """Show a desktop notification."""
        try:
            if sys.platform == "win32":
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(
                    "Stock Alert!",
                    f"{product['name']} is IN STOCK at {product['store']}!",
                    duration=10,
                    threaded=True
                )
            elif sys.platform == "darwin":
                # macOS notification
                import subprocess
                subprocess.run([
                    "osascript",
                    "-e",
                    f'display notification "{product['name']} is IN STOCK at {product['store']}!" with title "Stock Alert!"'
                ])
            else:
                # Linux notification (requires libnotify-bin)
                import subprocess
                subprocess.run([
                    "notify-send",
                    "Stock Alert!",
                    f"{product['name']} is IN STOCK at {product['store']}!"
                ])
        except Exception as e:
            # Fallback to messagebox
            messagebox.showinfo(
                "Stock Alert!",
                f"{product['name']} is IN STOCK at {product['store']}!"
            )

    def update_ui_periodically(self):
        """Periodically update the UI with latest data."""
        self._update_tracker_grid()

        # Schedule next update
        self.root.after(2000, self.update_ui_periodically)

    def run(self):
        """Start the UI main loop."""
        # Set up alert callback
        self.scraper.set_alert_callback(self.handle_stock_alert)

        # Start periodic UI updates
        self.update_ui_periodically()

        # Run main loop
        self.root.mainloop()
