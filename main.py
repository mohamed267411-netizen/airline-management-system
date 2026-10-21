"""
SkyWing Modern Aviation Suite
==============================
A high-end, modern desktop application for flight inquiry, schedule tracking,
loyalty rewards, and airline management.

Palette: Deep Aviation Obsidian & Vibrant Sky
  - Primary Dark:       #0F172A (Deep Slate)
  - Card / Surface:     #1E293B (Elevated Surface)
  - Border / Muted:     #334155 (Subtle Stroke)
  - Vibrant Cyan/Sky:   #38BDF8 (Primary Accent)
  - Sky Deep:           #0284C7 (Hover / Button)
  - Emerald:            #10B981 (Success / On-time)
  - Amber:              #F59E0B (Special Deals)
  - Text Primary:       #F8FAFC (Pure Light)
  - Text Secondary:     #94A3B8 (Cool Slate)
"""

import math
import random
import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager

# Design Tokens
COLOR_BG = "#0B132B"          # Main Window Background
COLOR_SURFACE = "#1C2541"     # Cards, Panels & Sidebar
COLOR_SURFACE_ALT = "#243256" # Elevated Cards
COLOR_BORDER = "#3A506B"      # Borders
COLOR_ACCENT = "#48CAE4"      # Cyan Accent / Active Pills
COLOR_ACCENT_HOVER = "#0096C7"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_MUTED = "#94A3B8"

FONT_NAME = "Segoe UI"
FONT_TITLE_HERO = (FONT_NAME, 20, "bold")
FONT_TITLE_SECTION = (FONT_NAME, 15, "bold")
FONT_SUBTITLE = (FONT_NAME, 12, "bold")
FONT_BODY = (FONT_NAME, 10)
FONT_BODY_BOLD = (FONT_NAME, 10, "bold")


class ModernAirlineApp(tk.Tk):
    """Main Application Shell with modern sidebar and multi-view navigation."""

    def __init__(self):
        super().__init__()
        self.title("SkyWing Aviation - Global Operations Suite")
        self.geometry("980x640")
        self.minsize(940, 600)
        self.configure(bg=COLOR_BG)

        self.db = DatabaseManager()
        self.current_user = None
        self.is_admin = False

        self._configure_styles()
        self.center_window(self, 980, 640)

        # Main dynamic shell
        self.shell = tk.Frame(self, bg=COLOR_BG)
        self.shell.pack(fill="both", expand=True)

        self.show_auth_view()

    def center_window(self, win, width, height):
        win.update_idletasks()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = max(0, (sw - width) // 2)
        y = max(0, (sh - height) // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Table Styles
        style.configure(
            "FlightBoard.Treeview",
            background=COLOR_SURFACE,
            foreground=COLOR_TEXT_LIGHT,
            rowheight=36,
            font=(FONT_NAME, 10),
            fieldbackground=COLOR_SURFACE,
            borderwidth=0
        )
        style.configure(
            "FlightBoard.Treeview.Heading",
            background="#121D38",
            foreground=COLOR_ACCENT,
            font=(FONT_NAME, 11, "bold"),
            relief="flat",
            padding=8
        )
        style.map(
            "FlightBoard.Treeview",
            background=[("selected", COLOR_SURFACE_ALT)],
            foreground=[("selected", COLOR_ACCENT)]
        )

        # Custom Scrollbar
        style.configure(
            "Custom.Vertical.TScrollbar",
            background=COLOR_SURFACE_ALT,
            troughcolor=COLOR_BG,
            arrowcolor=COLOR_TEXT_LIGHT,
            borderwidth=0
        )

    def clear_shell(self):
        for widget in self.shell.winfo_children():
            widget.destroy()

    def show_auth_view(self):
        self.clear_shell()
        AuthView(self.shell, self)

    def show_main_workspace(self, username: str):
        self.current_user = username
        self.clear_shell()
        MainWorkspace(self.shell, self)


# ==============================================================================
# AUTHENTICATION VIEW (Modern Split Screen)
# ==============================================================================
class AuthView(tk.Frame):
    """High-contrast split-screen login and sign up."""

    def __init__(self, parent, controller: ModernAirlineApp):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.is_register_mode = False
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        # Left Visual Banner
        left_banner = tk.Frame(self, bg=COLOR_SURFACE, width=380)
        left_banner.pack(side="left", fill="y")
        left_banner.pack_propagate(False)

        # Brand visuals
        badge = tk.Frame(left_banner, bg=COLOR_SURFACE_ALT, padx=12, pady=6)
        badge.pack(anchor="w", padx=35, pady=(50, 20))
        tk.Label(
            badge, text="ENTERPRISE AVIATION", font=(FONT_NAME, 9, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_ACCENT
        ).pack()

        tk.Label(
            left_banner, text="✈ SkyWing", font=(FONT_NAME, 26, "bold"),
            bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT
        ).pack(anchor="w", padx=35)

        tk.Label(
            left_banner, text="Airlines Global Suite", font=(FONT_NAME, 14),
            bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED
        ).pack(anchor="w", padx=35, pady=(2, 25))

        desc = (
            "Experience seamless flight tracking,\n"
            "dynamic ticket fare estimation,\n"
            "real-time fleet management, and\n"
            "exclusive promotional rewards."
        )
        tk.Label(
            left_banner, text=desc, font=(FONT_NAME, 11),
            bg=COLOR_SURFACE, fg="#B0C4DE", justify="left", anchor="w"
        ).pack(anchor="w", padx=35, pady=(0, 40))

        # Bottom quote badge
        q_frame = tk.Frame(left_banner, bg="#131B33", padx=20, pady=15, highlightbackground=COLOR_BORDER, highlightthickness=1)
        q_frame.pack(side="bottom", fill="x", padx=30, pady=30)
        tk.Label(
            q_frame, text="“The sky has no limits, only horizons.”",
            font=(FONT_NAME, 10, "italic"), bg="#131B33", fg=COLOR_ACCENT
        ).pack()

        # Right Auth Form Panel
        self.right_panel = tk.Frame(self, bg=COLOR_BG)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=50, pady=40)

        self._render_form()

    def _render_form(self):
        for w in self.right_panel.winfo_children():
            w.destroy()

        card = tk.Frame(self.right_panel, bg=COLOR_SURFACE, padx=35, pady=35, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420)

        if not self.is_register_mode:
            # ================= LOGIN FORM =================
            tk.Label(
                card, text="Welcome Back", font=FONT_TITLE_HERO,
                bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT
            ).pack(anchor="w")
            tk.Label(
                card, text="Enter your flight ID and credentials to continue.",
                font=FONT_BODY, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED
            ).pack(anchor="w", pady=(2, 25))

            # ID
            tk.Label(card, text="USER ID", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.id_entry = tk.Entry(
                card, font=(FONT_NAME, 12), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.id_entry.pack(fill="x", ipady=7, pady=(4, 15))

            # Password
            tk.Label(card, text="PASSWORD", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.pwd_entry = tk.Entry(
                card, font=(FONT_NAME, 12), show="*", bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.pwd_entry.pack(fill="x", ipady=7, pady=(4, 25))

            # Sign In Button
            btn = tk.Button(
                card, text="AUTHENTICATE & ENTER →", font=(FONT_NAME, 11, "bold"),
                bg=COLOR_ACCENT, fg=COLOR_BG, activebackground=COLOR_ACCENT_HOVER, activeforeground=COLOR_TEXT_LIGHT,
                relief="flat", cursor="hand2", command=self._handle_login
            )
            btn.pack(fill="x", ipady=8, pady=(0, 15))

            # Toggle to Register
            toggle_link = tk.Label(
                card, text="Need a new traveler account? Register here",
                font=(FONT_NAME, 10, "underline"), bg=COLOR_SURFACE, fg=COLOR_ACCENT, cursor="hand2"
            )
            toggle_link.pack()
            toggle_link.bind("<Button-1>", lambda e: self._toggle_mode())

            self.pwd_entry.bind("<Return>", lambda e: self._handle_login())

        else:
            # ================= REGISTER FORM =================
            tk.Label(
                card, text="Create Account", font=FONT_TITLE_HERO,
                bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT
            ).pack(anchor="w")
            tk.Label(
                card, text="Register as a traveler to access ticket portals.",
                font=FONT_BODY, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED
            ).pack(anchor="w", pady=(2, 20))

            # Name
            tk.Label(card, text="FULL NAME", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.reg_name = tk.Entry(
                card, font=(FONT_NAME, 11), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.reg_name.pack(fill="x", ipady=6, pady=(3, 12))

            # ID
            tk.Label(card, text="USER ID (NUMBERS)", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.reg_id = tk.Entry(
                card, font=(FONT_NAME, 11), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.reg_id.pack(fill="x", ipady=6, pady=(3, 12))

            # Password
            tk.Label(card, text="PASSWORD", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.reg_pwd = tk.Entry(
                card, font=(FONT_NAME, 11), show="*", bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.reg_pwd.pack(fill="x", ipady=6, pady=(3, 20))

            # Submit
            btn = tk.Button(
                card, text="CREATE ACCOUNT", font=(FONT_NAME, 11, "bold"),
                bg=COLOR_SUCCESS, fg=COLOR_TEXT_LIGHT, activebackground="#059669",
                relief="flat", cursor="hand2", command=self._handle_register
            )
            btn.pack(fill="x", ipady=8, pady=(0, 12))

            back_link = tk.Label(
                card, text="Already registered? Back to Login",
                font=(FONT_NAME, 10, "underline"), bg=COLOR_SURFACE, fg=COLOR_ACCENT, cursor="hand2"
            )
            back_link.pack()
            back_link.bind("<Button-1>", lambda e: self._toggle_mode())

    def _toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        self._render_form()

    def _handle_login(self):
        uid = self.id_entry.get().strip()
        pwd = self.pwd_entry.get().strip()
        if not uid or not pwd:
            messagebox.showwarning("Notice", "Please enter both User ID and Password.")
            return

        username = self.controller.db.authenticate_user(uid, pwd)
        if username:
            self.controller.show_main_workspace(username)
        else:
            messagebox.showerror("Auth Error", "Invalid ID or Password. Please try again.")
            self.pwd_entry.delete(0, tk.END)

    def _handle_register(self):
        name = self.reg_name.get().strip()
        uid = self.reg_id.get().strip()
        pwd = self.reg_pwd.get().strip()

        if not name or not uid or not pwd:
            messagebox.showwarning("Notice", "Please fill in all registration fields.")
            return

        success = self.controller.db.add_user(uid, name, pwd)
        if success:
            messagebox.showinfo("Success", f"User {name} registered successfully!")
            self.is_register_mode = False
            self._render_form()
        else:
            messagebox.showerror("Conflict", f"User ID '{uid}' is already registered.")


# ==============================================================================
# MAIN WORKSPACE (Single-Window Sidebar Hub)
# ==============================================================================
class MainWorkspace(tk.Frame):
    """Full-featured modern desktop dashboard with dynamic content swapping."""

    def __init__(self, parent, controller: ModernAirlineApp):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.pack(fill="both", expand=True)

        self._build_sidebar()
        self._build_content_area()

        # Start on Flights Overview
        self.switch_tab("flights")

    def _build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=COLOR_SURFACE, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand header
        brand_frame = tk.Frame(self.sidebar, bg=COLOR_SURFACE, padx=20, pady=25)
        brand_frame.pack(fill="x")

        tk.Label(
            brand_frame, text="✈ SkyWing", font=(FONT_NAME, 16, "bold"),
            bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT
        ).pack(anchor="w")

        tk.Label(
            brand_frame, text="Aviation Console", font=(FONT_NAME, 9),
            bg=COLOR_SURFACE, fg=COLOR_ACCENT
        ).pack(anchor="w")

        # Nav Buttons Container
        self.nav_frame = tk.Frame(self.sidebar, bg=COLOR_SURFACE, pady=10)
        self.nav_frame.pack(fill="both", expand=True)

        self.nav_buttons = {}
        tabs = [
            ("flights", "🛫  Flight Board"),
            ("tickets", "🎟  Price Estimator"),
            ("offers",  "🎡  Lucky Wheel"),
        ]

        for tab_id, label in tabs:
            btn = tk.Button(
                self.nav_frame, text=label, font=(FONT_NAME, 11),
                bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, activebackground=COLOR_SURFACE_ALT,
                activeforeground=COLOR_TEXT_LIGHT, relief="flat", anchor="w",
                padx=20, pady=10, cursor="hand2",
                command=lambda tid=tab_id: self.switch_tab(tid)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[tab_id] = btn

        # Bottom Profile & Logout
        bottom_profile = tk.Frame(self.sidebar, bg="#131B33", padx=15, pady=15)
        bottom_profile.pack(side="bottom", fill="x")

        tk.Label(
            bottom_profile, text=f"👤 {self.controller.current_user}",
            font=(FONT_NAME, 10, "bold"), bg="#131B33", fg=COLOR_TEXT_LIGHT, anchor="w"
        ).pack(fill="x")

        role_text = "Admin Mode 🔓" if self.controller.is_admin else "Traveler Access"
        self.role_lbl = tk.Label(
            bottom_profile, text=role_text, font=(FONT_NAME, 9),
            bg="#131B33", fg=COLOR_ACCENT if self.controller.is_admin else COLOR_TEXT_MUTED, anchor="w"
        )
        self.role_lbl.pack(fill="x", pady=(2, 8))

        logout_btn = tk.Button(
            bottom_profile, text="Sign Out", font=(FONT_NAME, 9, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MUTED, activebackground=COLOR_DANGER,
            activeforeground=COLOR_TEXT_LIGHT, relief="flat", cursor="hand2",
            command=self.controller.show_auth_view
        )
        logout_btn.pack(fill="x", ipady=3)

    def _build_content_area(self):
        self.main_content = tk.Frame(self, bg=COLOR_BG, padx=30, pady=25)
        self.main_content.pack(side="right", fill="both", expand=True)

    def switch_tab(self, tab_id: str):
        # Update active nav indicator
        for tid, btn in self.nav_buttons.items():
            if tid == tab_id:
                btn.config(bg=COLOR_SURFACE_ALT, fg=COLOR_ACCENT, font=(FONT_NAME, 11, "bold"))
            else:
                btn.config(bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, font=(FONT_NAME, 11))

        # Clear active panel
        for widget in self.main_content.winfo_children():
            widget.destroy()

        if tab_id == "flights":
            FlightBoardPanel(self.main_content, self)
        elif tab_id == "tickets":
            TicketPricingPanel(self.main_content, self)
        elif tab_id == "offers":
            LuckyWheelPanel(self.main_content, self)

    def refresh_role_label(self):
        if self.controller.is_admin:
            self.role_lbl.config(text="Admin Mode 🔓", fg=COLOR_ACCENT)
        else:
            self.role_lbl.config(text="Traveler Access", fg=COLOR_TEXT_MUTED)


# ==============================================================================
# TAB 1: FLIGHT BOARD & ADMIN CONTROL PANEL
# ==============================================================================
class FlightBoardPanel(tk.Frame):
    """Modern live Flight Schedule Table with integrated Admin toggle and Search."""

    ADMIN_PASSWORD = "123456789"

    def __init__(self, parent, workspace: MainWorkspace):
        super().__init__(parent, bg=COLOR_BG)
        self.workspace = workspace
        self.controller = workspace.controller
        self.pack(fill="both", expand=True)
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        # Top Header Bar
        header = tk.Frame(self, bg=COLOR_BG)
        header.pack(fill="x", pady=(0, 15))

        title_box = tk.Frame(header, bg=COLOR_BG)
        title_box.pack(side="left")

        tk.Label(
            title_box, text="Live Flight Board", font=FONT_TITLE_HERO,
            bg=COLOR_BG, fg=COLOR_TEXT_LIGHT
        ).pack(anchor="w")

        tk.Label(
            title_box, text="Real-time scheduled airline operations and departures.",
            font=FONT_BODY, bg=COLOR_BG, fg=COLOR_TEXT_MUTED
        ).pack(anchor="w")

        # Admin Toggle Button on Header
        self.admin_btn = tk.Button(
            header,
            text="🔓 Admin Controls" if self.controller.is_admin else "🔒 Unlock Admin",
            font=(FONT_NAME, 10, "bold"),
            bg=COLOR_ACCENT if self.controller.is_admin else COLOR_SURFACE_ALT,
            fg=COLOR_BG if self.controller.is_admin else COLOR_TEXT_LIGHT,
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self._toggle_admin_dialog
        )
        self.admin_btn.pack(side="right")

        # Search Bar + Quick Stats
        filter_bar = tk.Frame(self, bg=COLOR_SURFACE, padx=15, pady=10, highlightbackground=COLOR_BORDER, highlightthickness=1)
        filter_bar.pack(fill="x", pady=(0, 15))

        tk.Label(filter_bar, text="🔍 Search:", font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._filter_table())
        search_ent = tk.Entry(
            filter_bar, textvariable=self.search_var, font=(FONT_NAME, 10),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT, insertbackground=COLOR_ACCENT,
            relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1, width=25
        )
        search_ent.pack(side="left", ipady=3)

        self.count_badge = tk.Label(
            filter_bar, text="0 Flights Available", font=(FONT_NAME, 9, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_ACCENT, padx=10, pady=3
        )
        self.count_badge.pack(side="right")

        # Table Container
        table_frame = tk.Frame(self, bg=COLOR_SURFACE, highlightbackground=COLOR_BORDER, highlightthickness=1)
        table_frame.pack(fill="both", expand=True)

        columns = ("ID", "Destination", "The Date", "Time", "Flight Number", "Status")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings",
            style="FlightBoard.Treeview", selectmode="browse"
        )

        col_widths = {"ID": 50, "Destination": 160, "The Date": 110, "Time": 100, "Flight Number": 130, "Status": 110}
        for col, width in col_widths.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview, style="Custom.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Admin Control Panel (Visible only when unlocked)
        self.admin_panel = tk.Frame(self, bg=COLOR_SURFACE, padx=15, pady=12, highlightbackground=COLOR_BORDER, highlightthickness=1)
        if self.controller.is_admin:
            self._render_admin_panel()

    def _render_admin_panel(self):
        self.admin_panel.pack(fill="x", pady=(15, 0))

        tk.Label(
            self.admin_panel, text="Admin Action: Add New Flight",
            font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_ACCENT
        ).grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 6))

        # Inputs
        labels = ["Destination", "The Date", "Time", "Flight No."]
        self.admin_entries = {}
        for idx, text in enumerate(labels):
            tk.Label(self.admin_panel, text=text, font=(FONT_NAME, 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).grid(row=1, column=idx, sticky="w", padx=4)
            ent = tk.Entry(
                self.admin_panel, font=(FONT_NAME, 10), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1, width=14
            )
            ent.grid(row=2, column=idx, sticky="ew", padx=4, pady=(2, 0))
            self.admin_entries[text] = ent

        # Add Button
        add_btn = tk.Button(
            self.admin_panel, text="+ ADD FLIGHT", font=(FONT_NAME, 10, "bold"),
            bg=COLOR_SUCCESS, fg=COLOR_TEXT_LIGHT, relief="flat", cursor="hand2", padx=10,
            command=self._add_flight_record
        )
        add_btn.grid(row=2, column=4, padx=8, pady=(2, 0))

        # Delete Button
        del_btn = tk.Button(
            self.admin_panel, text="🗑 DELETE SELECTED", font=(FONT_NAME, 9, "bold"),
            bg=COLOR_DANGER, fg=COLOR_TEXT_LIGHT, relief="flat", cursor="hand2", padx=8,
            command=self._delete_selected_flight
        )
        del_btn.grid(row=2, column=5, padx=8, pady=(2, 0))

    def _toggle_admin_dialog(self):
        if self.controller.is_admin:
            self.controller.is_admin = False
            self.admin_btn.config(text="🔒 Unlock Admin", bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT)
            self.admin_panel.pack_forget()
            self.workspace.refresh_role_label()
            messagebox.showinfo("Admin", "Logged out of Admin mode.")
            return

        # Modal Dialog
        win = tk.Toplevel(self)
        win.title("Admin Access")
        win.geometry("320x170")
        win.resizable(False, False)
        win.configure(bg=COLOR_BG)
        self.controller.center_window(win, 320, 170)
        win.grab_set()

        card = tk.Frame(win, bg=COLOR_SURFACE, padx=20, pady=20, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(card, text="Enter Admin Security PIN", font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT).pack(pady=(0, 8))
        pwd_in = tk.Entry(
            card, show="*", font=(FONT_NAME, 12), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT,
            insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1, justify="center"
        )
        pwd_in.pack(fill="x", ipady=4, pady=(0, 12))
        pwd_in.focus()

        def submit():
            if pwd_in.get().strip() == self.ADMIN_PASSWORD:
                self.controller.is_admin = True
                self.admin_btn.config(text="🔓 Admin Controls", bg=COLOR_ACCENT, fg=COLOR_BG)
                self._render_admin_panel()
                self.workspace.refresh_role_label()
                win.destroy()
                messagebox.showinfo("Admin", "مرحبا بعودتك! Admin access granted.")
            else:
                messagebox.showerror("Access Denied", "Incorrect Admin Password.")
                pwd_in.delete(0, tk.END)

        tk.Button(card, text="Verify PIN", font=(FONT_NAME, 10, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG, relief="flat", cursor="hand2", command=submit).pack(fill="x", ipady=4)
        pwd_in.bind("<Return>", lambda e: submit())

    def load_data(self):
        self.raw_flights = self.controller.db.get_all_flights()
        self._populate_table(self.raw_flights)

    def _populate_table(self, flight_list):
        for item in self.tree.get_children():
            self.tree.delete(item)

        statuses = ["ON TIME", "SCHEDULED", "BOARDING"]
        for f in flight_list:
            # f: (id, destination, date, time, flight_number)
            status = statuses[f[0] % len(statuses)]
            self.tree.insert("", "end", values=(f[0], f[1], f[2], f[3], f[4], status))

        self.count_badge.config(text=f"{len(flight_list)} Flights Available")

    def _filter_table(self):
        q = self.search_var.get().strip().lower()
        if not q:
            self._populate_table(self.raw_flights)
            return

        filtered = [
            f for f in self.raw_flights
            if q in str(f[1]).lower() or q in str(f[4]).lower() or q in str(f[2]).lower()
        ]
        self._populate_table(filtered)

    def _add_flight_record(self):
        dest = self.admin_entries["Destination"].get().strip()
        date = self.admin_entries["The Date"].get().strip()
        time_ = self.admin_entries["Time"].get().strip()
        num = self.admin_entries["Flight No."].get().strip()

        if dest and date and time_ and num:
            success = self.controller.db.add_flight(dest, date, time_, num)
            if success:
                messagebox.showinfo("Success", f"Flight {num} to {dest} added!")
                for ent in self.admin_entries.values():
                    ent.delete(0, tk.END)
                self.load_data()
            else:
                messagebox.showerror("Error", "Could not save flight to database.")
        else:
            messagebox.showwarning("Warning", "Please fill in all flight parameters.")

    def _delete_selected_flight(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Notice", "Select a flight row to delete.")
            return

        vals = self.tree.item(sel[0], "values")
        flight_id = vals[0]
        flight_no = vals[4]

        if messagebox.askyesno("Confirm", f"Are you sure you want to delete Flight {flight_no}?"):
            self.controller.db.delete_flight(flight_id)
            self.load_data()


# ==============================================================================
# TAB 2: TICKET FARE ESTIMATOR
# ==============================================================================
class TicketPricingPanel(tk.Frame):
    """Modern interactive Fare & Category Calculator."""

    PRICING = {
        "Cairo (CAI)": {"eco": 15282, "business": 22300, "first-class": 30000},
        "Paris (CDG)": {"eco": 18700, "business": 25600, "first-class": 34000},
        "New York (JFK)": {"eco": 25000, "business": 35000, "first-class": 45000},
        "London (LHR)": {"eco": 20000, "business": 28000, "first-class": 37000},
        "Rome (FCO)": {"eco": 17500, "business": 24000, "first-class": 32000},
        "Riyadh (RUH)": {"eco": 14500, "business": 21000, "first-class": 29000},
        "Dubai (DXB)": {"eco": 16200, "business": 23800, "first-class": 31500},
    }

    def __init__(self, parent, workspace: MainWorkspace):
        super().__init__(parent, bg=COLOR_BG)
        self.workspace = workspace
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        # Header
        tk.Label(self, text="Ticket Price Inquiry", font=FONT_TITLE_HERO, bg=COLOR_BG, fg=COLOR_TEXT_LIGHT).pack(anchor="w")
        tk.Label(self, text="Instant estimated fares across destinations and cabin classes.", font=FONT_BODY, bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(2, 25))

        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(fill="both", expand=True)

        # Left Config Card
        card = tk.Frame(container, bg=COLOR_SURFACE, padx=30, pady=30, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=(0, 15))

        tk.Label(card, text="FLIGHT PARAMETERS", font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_ACCENT).pack(anchor="w", pady=(0, 15))

        # Destination Dropdown
        tk.Label(card, text="Select Destination", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
        self.dest_var = tk.StringVar(value=list(self.PRICING.keys())[0])
        dest_drop = tk.OptionMenu(card, self.dest_var, *self.PRICING.keys(), command=lambda e: self._calculate())
        dest_drop.configure(
            font=(FONT_NAME, 11), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT,
            activebackground=COLOR_SURFACE, activeforeground=COLOR_ACCENT,
            relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDER
        )
        dest_drop["menu"].config(bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT, font=(FONT_NAME, 10))
        dest_drop.pack(fill="x", ipady=5, pady=(4, 15))

        # Class Radios
        tk.Label(card, text="Cabin Class", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(5, 5))
        self.class_var = tk.StringVar(value="eco")
        classes = [("Economy Class", "eco"), ("Business Class", "business"), ("First Class VIP", "first-class")]
        for title, val in classes:
            rb = tk.Radiobutton(
                card, text=title, variable=self.class_var, value=val,
                font=(FONT_NAME, 10), bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT,
                selectcolor=COLOR_SURFACE_ALT, activebackground=COLOR_SURFACE,
                activeforeground=COLOR_ACCENT, command=self._calculate
            )
            rb.pack(anchor="w", pady=3)

        # Right Summary Card
        self.summary_card = tk.Frame(container, bg=COLOR_SURFACE, padx=30, pady=30, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.summary_card.pack(side="right", fill="both", expand=True, padx=(15, 0))

        tk.Label(self.summary_card, text="ESTIMATED FARE SUMMARY", font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_ACCENT).pack(anchor="w")

        self.price_display = tk.Label(
            self.summary_card, text="0 EGP", font=(FONT_NAME, 26, "bold"),
            bg=COLOR_SURFACE, fg=COLOR_TEXT_LIGHT
        )
        self.price_display.pack(anchor="w", pady=(20, 2))

        self.usd_display = tk.Label(
            self.summary_card, text="~$0 USD", font=(FONT_NAME, 12),
            bg=COLOR_SURFACE, fg=COLOR_SUCCESS
        )
        self.usd_display.pack(anchor="w", pady=(0, 20))

        details = [
            "✔ Includes baggage allowance (2x 23kg)",
            "✔ In-flight meal and Wi-Fi complimentary",
            "✔ Flexible date rescheduling permitted"
        ]
        for d in details:
            tk.Label(self.summary_card, text=d, font=(FONT_NAME, 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=2)

        self._calculate()

    def _calculate(self):
        dest = self.dest_var.get()
        cls = self.class_var.get()
        if dest in self.PRICING and cls in self.PRICING[dest]:
            price = self.PRICING[dest][cls]
            usd = price / 50
            self.price_display.config(text=f"{price:,.0f} EGP")
            self.usd_display.config(text=f"~${usd:,.0f} USD (approx. exchange)")


# ==============================================================================
# TAB 3: PROMOTIONAL LUCKY WHEEL
# ==============================================================================
class LuckyWheelPanel(tk.Frame):
    """Sleek Promotional Wheel of Fortune with trigonometry physics."""

    OFFERS = ["10% DISCOUNT", "20% DISCOUNT", "30% DISCOUNT", "50% MEGA SALE", "40% DISCOUNT", "BETTER LUCK!"]
    SEGMENT_COLORS = ["#0077B6", "#023E8A", "#0096C7", "#03045E", "#48CAE4", "#1E293B"]

    def __init__(self, parent, workspace: MainWorkspace):
        super().__init__(parent, bg=COLOR_BG)
        self.workspace = workspace
        self.pack(fill="both", expand=True)

        self.current_angle = 0
        self.total_angle = 0
        self.is_spinning = False

        self._build_ui()
        self.draw_wheel()

    def _build_ui(self):
        # Header
        tk.Label(self, text="Promotional Wheel of Fortune", font=FONT_TITLE_HERO, bg=COLOR_BG, fg=COLOR_TEXT_LIGHT).pack(anchor="w")
        tk.Label(self, text="Spin daily to win exclusive flight vouchers and seat upgrade discounts.", font=FONT_BODY, bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(2, 10))

        content = tk.Frame(self, bg=COLOR_BG)
        content.pack(fill="both", expand=True)

        # Left Canvas
        self.canvas = tk.Canvas(content, width=440, height=440, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(side="left", padx=(0, 20))

        # Right Controls & Prize Board
        right_box = tk.Frame(content, bg=COLOR_SURFACE, padx=25, pady=30, highlightbackground=COLOR_BORDER, highlightthickness=1)
        right_box.pack(side="right", fill="both", expand=True)

        tk.Label(right_box, text="REWARDS CONSOLE", font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_ACCENT).pack(anchor="w")

        self.spin_btn = tk.Button(
            right_box, text="🎡 SPIN THE WHEEL", font=(FONT_NAME, 12, "bold"),
            bg=COLOR_ACCENT, fg=COLOR_BG, activebackground=COLOR_ACCENT_HOVER, activeforeground=COLOR_TEXT_LIGHT,
            relief="flat", cursor="hand2", command=self.spin_wheel
        )
        self.spin_btn.pack(fill="x", ipady=10, pady=(20, 15))

        self.status_lbl = tk.Label(
            right_box, text="Click 'SPIN' to begin your flight reward draw.",
            font=FONT_BODY, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, justify="left"
        )
        self.status_lbl.pack(anchor="w")

        # Prize Card
        self.prize_card = tk.Frame(right_box, bg=COLOR_SURFACE_ALT, padx=15, pady=15, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.prize_card.pack(fill="x", pady=20)

        self.prize_badge = tk.Label(
            self.prize_card, text="Awaiting Spin...", font=(FONT_NAME, 13, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_LIGHT
        )
        self.prize_badge.pack(pady=4)

        self.promo_code_lbl = tk.Label(
            self.prize_card, text="", font=(FONT_NAME, 11, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_SUCCESS
        )
        self.promo_code_lbl.pack()

    def draw_wheel(self):
        self.canvas.delete("all")
        cx, cy, radius = 220, 220, 190
        num = len(self.OFFERS)
        step = 360 / num

        for i in range(num):
            start = self.current_angle + i * step
            color = self.SEGMENT_COLORS[i % len(self.SEGMENT_COLORS)]

            self.canvas.create_arc(
                cx - radius, cy - radius, cx + radius, cy + radius,
                start=start, extent=step, fill=color, outline="#334155", width=2
            )

            mid = start + (step / 2)
            rad = math.radians(mid)
            tx = cx + (radius * 0.65) * math.cos(rad)
            ty = cy - (radius * 0.65) * math.sin(rad)

            self.canvas.create_text(
                tx, ty, text=self.OFFERS[i], fill=COLOR_TEXT_LIGHT, font=(FONT_NAME, 9, "bold")
            )

        # Center Gold Hub
        self.canvas.create_oval(cx - 24, cy - 24, cx + 24, cy + 24, fill=COLOR_SURFACE_ALT, outline=COLOR_ACCENT, width=3)
        self.canvas.create_text(cx, cy, text="✈", fill=COLOR_ACCENT, font=(FONT_NAME, 14, "bold"))

        # Top Indicator Arrow
        self.canvas.create_polygon(
            cx - 14, cy - radius - 10,
            cx + 14, cy - radius - 10,
            cx, cy - radius + 14,
            fill="#EF4444", outline="#B91C1C", width=1
        )

    def spin_wheel(self):
        if self.is_spinning:
            return
        self.is_spinning = True
        self.spin_btn.config(state="disabled", bg=COLOR_SURFACE_ALT)
        self.status_lbl.config(text="Spinning the turbines... Good luck!")
        self.total_angle = random.randint(720, 1200)
        self.animate_spin()

    def animate_spin(self):
        if self.total_angle > 0:
            step = max(5, int(self.total_angle * 0.05))
            self.total_angle -= step
            self.current_angle = (self.current_angle + step) % 360
            self.draw_wheel()
            self.after(20, self.animate_spin)
        else:
            self.is_spinning = False
            self.spin_btn.config(state="normal", bg=COLOR_ACCENT)
            num = len(self.OFFERS)
            step = 360 / num
            winning_idx = int((90 - self.current_angle) % 360 // step) % num
            prize = self.OFFERS[winning_idx]

            self.prize_badge.config(text=f"🎉 Result: {prize}")
            if "DISCOUNT" in prize or "SALE" in prize:
                code = f"SKYWING-{random.randint(1000, 9999)}"
                self.promo_code_lbl.config(text=f"Promo Voucher: {code}")
                self.status_lbl.config(text="Congratulations! Voucher code ready for checkout.")
            else:
                self.promo_code_lbl.config(text="Try again tomorrow!")
                self.status_lbl.config(text="Thank you for playing SkyWing Rewards.")


# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    app = ModernAirlineApp()
    app.mainloop()
