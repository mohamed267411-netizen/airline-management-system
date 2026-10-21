"""
SkyWing Modern Aviation Suite
==============================
A high-end, cheerful light-mode desktop application for flight inquiry, schedule tracking,
loyalty rewards, and airline management.

Palette: Fresh & Cheerful Sky Aviation (Light Mode)
  - Window Background:       #F0F5FA (Fresh Airy Cloud Blue)
  - Card / Surface:          #FFFFFF (Pure White)
  - Elevated / Inputs:       #EBF3FA (Soft Sky Accent Surface)
  - Borders:                 #D0E0EE (Clean Slate Border)
  - Primary Cheerful Sky:    #0284C7 (Vibrant Sky Blue)
  - Sky Hover:               #0369A1 (Deeper Aviation Blue)
  - Success:                 #10B981 (Fresh Emerald)
  - Warning / Gold:          #F59E0B (Warm Sun Amber)
  - Danger:                  #EF4444 (Bright Coral Red)
  - Text Primary:            #0F172A (Deep Navy / High Contrast)
  - Text Muted:              #64748B (Readable Cool Slate)
  - Text White:              #FFFFFF (Pure White for Colored Buttons)
"""

import math
import random
import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager

# Design Tokens (Fresh Cheerful Aviation Light Palette)
COLOR_BG = "#F0F5FA"          # Clean airy sky background
COLOR_SURFACE = "#FFFFFF"     # White cards, panels & sidebar
COLOR_SURFACE_ALT = "#EBF3FA" # Soft sky-tinted inputs & active pills
COLOR_BORDER = "#D0E0EE"      # Clean soft border
COLOR_ACCENT = "#0284C7"      # Cheerful vibrant Sky Blue
COLOR_ACCENT_HOVER = "#0369A1"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"
COLOR_TEXT_MAIN = "#0F172A"   # Crisp readable dark navy
COLOR_TEXT_MUTED = "#64748B"  # Muted subtitle slate
COLOR_TEXT_WHITE = "#FFFFFF"  # White for primary buttons

FONT_NAME = "Segoe UI"
FONT_TITLE_HERO = (FONT_NAME, 18, "bold")
FONT_TITLE_SECTION = (FONT_NAME, 14, "bold")
FONT_SUBTITLE = (FONT_NAME, 11, "bold")
FONT_BODY = (FONT_NAME, 10)
FONT_BODY_BOLD = (FONT_NAME, 10, "bold")


class ModernAirlineApp(tk.Tk):
    """Main Application Shell with fixed stable window size and cheerful light styling."""

    WINDOW_WIDTH = 1020
    WINDOW_HEIGHT = 680

    def __init__(self):
        super().__init__()
        self.title("SkyWing Aviation - Global Operations Suite")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.resizable(False, False)  # Fixed stable window size
        self.configure(bg=COLOR_BG)

        self.db = DatabaseManager()
        self.current_user = None
        self.is_admin = False

        self._configure_styles()
        self.center_window(self, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

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

        # Cheerful Light Table Styles
        style.configure(
            "FlightBoard.Treeview",
            background=COLOR_SURFACE,
            foreground=COLOR_TEXT_MAIN,
            rowheight=32,
            font=(FONT_NAME, 10),
            fieldbackground=COLOR_SURFACE,
            borderwidth=0
        )
        style.configure(
            "FlightBoard.Treeview.Heading",
            background="#E0EDF8",
            foreground=COLOR_ACCENT,
            font=(FONT_NAME, 10, "bold"),
            relief="flat",
            padding=6
        )
        style.map(
            "FlightBoard.Treeview",
            background=[("selected", COLOR_SURFACE_ALT)],
            foreground=[("selected", COLOR_ACCENT)]
        )

        style.configure(
            "Custom.Vertical.TScrollbar",
            background=COLOR_SURFACE_ALT,
            troughcolor=COLOR_BG,
            arrowcolor=COLOR_ACCENT,
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
# AUTHENTICATION VIEW (Modern Cheerful Split Screen)
# ==============================================================================
class AuthView(tk.Frame):
    """Vibrant cheerful split-screen login and sign up."""

    def __init__(self, parent, controller: ModernAirlineApp):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.is_register_mode = False
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        # Left Visual Banner (Bright Cheerful Aviation Blue)
        left_banner = tk.Frame(self, bg=COLOR_ACCENT, width=380)
        left_banner.pack(side="left", fill="y")
        left_banner.pack_propagate(False)

        badge = tk.Frame(left_banner, bg=COLOR_ACCENT_HOVER, padx=12, pady=6)
        badge.pack(anchor="w", padx=35, pady=(55, 20))
        tk.Label(
            badge, text="GLOBAL AVIATION PORTAL", font=(FONT_NAME, 9, "bold"),
            bg=COLOR_ACCENT_HOVER, fg=COLOR_TEXT_WHITE
        ).pack()

        tk.Label(
            left_banner, text="✈ SkyWing", font=(FONT_NAME, 28, "bold"),
            bg=COLOR_ACCENT, fg=COLOR_TEXT_WHITE
        ).pack(anchor="w", padx=35)

        tk.Label(
            left_banner, text="Airlines & Flight Operations", font=(FONT_NAME, 13),
            bg=COLOR_ACCENT, fg="#E0F2FE"
        ).pack(anchor="w", padx=35, pady=(2, 25))

        desc = (
            "Experience seamless flight tracking,\n"
            "dynamic ticket fare estimation,\n"
            "real-time fleet management, and\n"
            "exclusive promotional rewards."
        )
        tk.Label(
            left_banner, text=desc, font=(FONT_NAME, 11),
            bg=COLOR_ACCENT, fg="#F0F9FF", justify="left", anchor="w"
        ).pack(anchor="w", padx=35, pady=(0, 40))

        q_frame = tk.Frame(left_banner, bg="#0275B1", padx=20, pady=15, highlightbackground="#38BDF8", highlightthickness=1)
        q_frame.pack(side="bottom", fill="x", padx=30, pady=35)
        tk.Label(
            q_frame, text="“The sky has no limits, only horizons.”",
            font=(FONT_NAME, 10, "italic"), bg="#0275B1", fg=COLOR_TEXT_WHITE
        ).pack()

        # Right Form Area (Crisp White Card on Soft Sky Backdrop)
        self.right_panel = tk.Frame(self, bg=COLOR_BG)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=40, pady=40)

        self._render_form()

    def _render_form(self):
        for w in self.right_panel.winfo_children():
            w.destroy()

        card = tk.Frame(self.right_panel, bg=COLOR_SURFACE, padx=35, pady=35, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420)

        if not self.is_register_mode:
            # Login
            tk.Label(card, text="Welcome Back", font=FONT_TITLE_HERO, bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN).pack(anchor="w")
            tk.Label(card, text="Enter your flight ID and credentials to continue.", font=FONT_BODY, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(2, 25))

            tk.Label(card, text="USER ID", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.id_entry = tk.Entry(
                card, font=(FONT_NAME, 11), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.id_entry.pack(fill="x", ipady=6, pady=(4, 15))

            tk.Label(card, text="PASSWORD", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.pwd_entry = tk.Entry(
                card, font=(FONT_NAME, 11), show="*", bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.pwd_entry.pack(fill="x", ipady=6, pady=(4, 25))

            btn = tk.Button(
                card, text="AUTHENTICATE & ENTER →", font=(FONT_NAME, 11, "bold"),
                bg=COLOR_ACCENT, fg=COLOR_TEXT_WHITE, activebackground=COLOR_ACCENT_HOVER, activeforeground=COLOR_TEXT_WHITE,
                relief="flat", cursor="hand2", command=self._handle_login
            )
            btn.pack(fill="x", ipady=8, pady=(0, 15))

            toggle_link = tk.Label(
                card, text="Need a new traveler account? Register here",
                font=(FONT_NAME, 10, "underline"), bg=COLOR_SURFACE, fg=COLOR_ACCENT, cursor="hand2"
            )
            toggle_link.pack()
            toggle_link.bind("<Button-1>", lambda e: self._toggle_mode())

            self.pwd_entry.bind("<Return>", lambda e: self._handle_login())

        else:
            # Register
            tk.Label(card, text="Create Account", font=FONT_TITLE_HERO, bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN).pack(anchor="w")
            tk.Label(card, text="Register as a traveler to access ticket portals.", font=FONT_BODY, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(2, 20))

            tk.Label(card, text="FULL NAME", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.reg_name = tk.Entry(
                card, font=(FONT_NAME, 11), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.reg_name.pack(fill="x", ipady=5, pady=(3, 12))

            tk.Label(card, text="USER ID (NUMBERS)", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.reg_id = tk.Entry(
                card, font=(FONT_NAME, 11), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.reg_id.pack(fill="x", ipady=5, pady=(3, 12))

            tk.Label(card, text="PASSWORD", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            self.reg_pwd = tk.Entry(
                card, font=(FONT_NAME, 11), show="*", bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            self.reg_pwd.pack(fill="x", ipady=5, pady=(3, 20))

            btn = tk.Button(
                card, text="CREATE ACCOUNT", font=(FONT_NAME, 11, "bold"),
                bg=COLOR_SUCCESS, fg=COLOR_TEXT_WHITE, activebackground="#059669",
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
# MAIN WORKSPACE (Cheerful White Sidebar & Clean Sky Console)
# ==============================================================================
class MainWorkspace(tk.Frame):
    """Full-featured modern desktop dashboard with cheerful light styling."""

    def __init__(self, parent, controller: ModernAirlineApp):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.pack(fill="both", expand=True)

        self._build_sidebar()
        self._build_content_area()

        self.switch_tab("flights")

    def _build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=COLOR_SURFACE, width=220, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand_frame = tk.Frame(self.sidebar, bg=COLOR_SURFACE, padx=20, pady=25)
        brand_frame.pack(fill="x")

        tk.Label(
            brand_frame, text="✈ SkyWing", font=(FONT_NAME, 17, "bold"),
            bg=COLOR_SURFACE, fg=COLOR_ACCENT
        ).pack(anchor="w")

        tk.Label(
            brand_frame, text="Aviation Operations", font=(FONT_NAME, 9),
            bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED
        ).pack(anchor="w")

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
                activeforeground=COLOR_ACCENT, relief="flat", anchor="w",
                padx=20, pady=11, cursor="hand2",
                command=lambda tid=tab_id: self.switch_tab(tid)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[tab_id] = btn

        # Bottom Profile (Light Sky Pill)
        bottom_profile = tk.Frame(self.sidebar, bg=COLOR_SURFACE_ALT, padx=15, pady=15, highlightbackground=COLOR_BORDER, highlightthickness=1)
        bottom_profile.pack(side="bottom", fill="x", padx=10, pady=10)

        tk.Label(
            bottom_profile, text=f"👤 {self.controller.current_user}",
            font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN, anchor="w"
        ).pack(fill="x")

        role_text = "Admin Mode 🔓" if self.controller.is_admin else "Traveler Access"
        self.role_lbl = tk.Label(
            bottom_profile, text=role_text, font=(FONT_NAME, 9),
            bg=COLOR_SURFACE_ALT, fg=COLOR_ACCENT if self.controller.is_admin else COLOR_TEXT_MUTED, anchor="w"
        )
        self.role_lbl.pack(fill="x", pady=(2, 8))

        logout_btn = tk.Button(
            bottom_profile, text="Sign Out", font=(FONT_NAME, 9, "bold"),
            bg=COLOR_SURFACE, fg=COLOR_DANGER, activebackground=COLOR_DANGER,
            activeforeground=COLOR_TEXT_WHITE, relief="flat", cursor="hand2",
            highlightbackground=COLOR_BORDER, highlightthickness=1,
            command=self.controller.show_auth_view
        )
        logout_btn.pack(fill="x", ipady=3)

    def _build_content_area(self):
        self.main_content = tk.Frame(self, bg=COLOR_BG, padx=25, pady=20)
        self.main_content.pack(side="right", fill="both", expand=True)

    def switch_tab(self, tab_id: str):
        for tid, btn in self.nav_buttons.items():
            if tid == tab_id:
                btn.config(bg=COLOR_SURFACE_ALT, fg=COLOR_ACCENT, font=(FONT_NAME, 11, "bold"))
            else:
                btn.config(bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, font=(FONT_NAME, 11))

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
# TAB 1: FLIGHT BOARD & ADMIN CONTROL PANEL (Cheerful Light Theme)
# ==============================================================================
class FlightBoardPanel(tk.Frame):
    """Live Flight Schedule Table with integrated Admin toggle and Search."""

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
        header.pack(fill="x", pady=(0, 10))

        title_box = tk.Frame(header, bg=COLOR_BG)
        title_box.pack(side="left")

        tk.Label(
            title_box, text="Live Flight Board", font=FONT_TITLE_HERO,
            bg=COLOR_BG, fg=COLOR_TEXT_MAIN
        ).pack(anchor="w")

        tk.Label(
            title_box, text="Real-time scheduled airline operations and departures.",
            font=(FONT_NAME, 9), bg=COLOR_BG, fg=COLOR_TEXT_MUTED
        ).pack(anchor="w")

        self.admin_btn = tk.Button(
            header,
            text="🔓 Admin Controls" if self.controller.is_admin else "🔒 Unlock Admin",
            font=(FONT_NAME, 9, "bold"),
            bg=COLOR_ACCENT if self.controller.is_admin else COLOR_SURFACE,
            fg=COLOR_TEXT_WHITE if self.controller.is_admin else COLOR_TEXT_MAIN,
            relief="flat", cursor="hand2", padx=10, pady=5,
            highlightbackground=COLOR_BORDER, highlightthickness=1,
            command=self._toggle_admin_dialog
        )
        self.admin_btn.pack(side="right")

        # Search Bar + Quick Stats
        filter_bar = tk.Frame(self, bg=COLOR_SURFACE, padx=12, pady=7, highlightbackground=COLOR_BORDER, highlightthickness=1)
        filter_bar.pack(fill="x", pady=(0, 10))

        tk.Label(filter_bar, text="🔍 Search Flights:", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._filter_table())
        search_ent = tk.Entry(
            filter_bar, textvariable=self.search_var, font=(FONT_NAME, 10),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN, insertbackground=COLOR_ACCENT,
            relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1, width=28
        )
        search_ent.pack(side="left", ipady=3)

        self.count_badge = tk.Label(
            filter_bar, text="0 Flights Available", font=(FONT_NAME, 9, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_ACCENT, padx=10, pady=2
        )
        self.count_badge.pack(side="right")

        # Table Container
        self.table_frame = tk.Frame(self, bg=COLOR_SURFACE, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.table_frame.pack(fill="x", pady=(0, 10))

        columns = ("ID", "Destination", "The Date", "Time", "Flight Number", "Status")
        self.tree = ttk.Treeview(
            self.table_frame, columns=columns, show="headings",
            style="FlightBoard.Treeview", selectmode="browse",
            height=7
        )

        col_widths = {"ID": 50, "Destination": 150, "The Date": 110, "Time": 100, "Flight Number": 120, "Status": 110}
        for col, width in col_widths.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview, style="Custom.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Admin Control Panel
        self.admin_panel = tk.Frame(self, bg=COLOR_SURFACE, padx=15, pady=10, highlightbackground=COLOR_BORDER, highlightthickness=1)
        if self.controller.is_admin:
            self._render_admin_panel()

    def _render_admin_panel(self):
        for w in self.admin_panel.winfo_children():
            w.destroy()

        self.admin_panel.pack(fill="x", pady=(0, 5))

        top_row = tk.Frame(self.admin_panel, bg=COLOR_SURFACE)
        top_row.pack(fill="x", pady=(0, 6))

        tk.Label(
            top_row, text="ADMIN CONTROLS: ADD NEW FLIGHT RECORD",
            font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_ACCENT
        ).pack(side="left")

        del_btn = tk.Button(
            top_row, text="🗑 DELETE SELECTED FLIGHT", font=(FONT_NAME, 9, "bold"),
            bg=COLOR_DANGER, fg=COLOR_TEXT_WHITE, relief="flat", cursor="hand2", padx=8, pady=2,
            command=self._delete_selected_flight
        )
        del_btn.pack(side="right")

        form_row = tk.Frame(self.admin_panel, bg=COLOR_SURFACE)
        form_row.pack(fill="x")

        labels = ["Destination", "The Date", "Time", "Flight No."]
        self.admin_entries = {}
        for idx, text in enumerate(labels):
            box = tk.Frame(form_row, bg=COLOR_SURFACE)
            box.pack(side="left", fill="x", expand=True, padx=4)

            tk.Label(box, text=text, font=(FONT_NAME, 8, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
            ent = tk.Entry(
                box, font=(FONT_NAME, 10), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN,
                insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1
            )
            ent.pack(fill="x", ipady=3, pady=(2, 0))
            self.admin_entries[text] = ent

        add_box = tk.Frame(form_row, bg=COLOR_SURFACE)
        add_box.pack(side="left", padx=(6, 0))
        tk.Label(add_box, text=" ", font=(FONT_NAME, 8), bg=COLOR_SURFACE).pack()
        add_btn = tk.Button(
            add_box, text="+ ADD FLIGHT", font=(FONT_NAME, 10, "bold"),
            bg=COLOR_SUCCESS, fg=COLOR_TEXT_WHITE, relief="flat", cursor="hand2", padx=12, pady=4,
            command=self._add_flight_record
        )
        add_btn.pack()

    def _toggle_admin_dialog(self):
        if self.controller.is_admin:
            self.controller.is_admin = False
            self.admin_btn.config(text="🔒 Unlock Admin", bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN)
            self.admin_panel.pack_forget()
            self.workspace.refresh_role_label()
            messagebox.showinfo("Admin", "Logged out of Admin mode.")
            return

        win = tk.Toplevel(self)
        win.title("Admin Access")
        win.geometry("320x170")
        win.resizable(False, False)
        win.configure(bg=COLOR_BG)
        self.controller.center_window(win, 320, 170)
        win.grab_set()

        card = tk.Frame(win, bg=COLOR_SURFACE, padx=20, pady=20, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(card, text="Enter Admin Security PIN", font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN).pack(pady=(0, 8))
        pwd_in = tk.Entry(
            card, show="*", font=(FONT_NAME, 12), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN,
            insertbackground=COLOR_ACCENT, relief="flat", highlightbackground=COLOR_BORDER, highlightthickness=1, justify="center"
        )
        pwd_in.pack(fill="x", ipady=4, pady=(0, 12))
        pwd_in.focus()

        def submit():
            if pwd_in.get().strip() == self.ADMIN_PASSWORD:
                self.controller.is_admin = True
                self.admin_btn.config(text="🔓 Admin Controls", bg=COLOR_ACCENT, fg=COLOR_TEXT_WHITE)
                self._render_admin_panel()
                self.workspace.refresh_role_label()
                win.destroy()
                messagebox.showinfo("Admin", "مرحبا بعودتك! Admin access granted.")
            else:
                messagebox.showerror("Access Denied", "Incorrect Admin Password.")
                pwd_in.delete(0, tk.END)

        tk.Button(card, text="Verify PIN", font=(FONT_NAME, 10, "bold"), bg=COLOR_ACCENT, fg=COLOR_TEXT_WHITE, relief="flat", cursor="hand2", command=submit).pack(fill="x", ipady=4)
        pwd_in.bind("<Return>", lambda e: submit())

    def load_data(self):
        self.raw_flights = self.controller.db.get_all_flights()
        self._populate_table(self.raw_flights)

    def _populate_table(self, flight_list):
        for item in self.tree.get_children():
            self.tree.delete(item)

        statuses = ["ON TIME", "SCHEDULED", "BOARDING"]
        for f in flight_list:
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
            messagebox.showwarning("Notice", "Select a flight row in the table first.")
            return

        vals = self.tree.item(sel[0], "values")
        flight_id = vals[0]
        flight_no = vals[4]

        if messagebox.askyesno("Confirm", f"Are you sure you want to delete Flight {flight_no}?"):
            self.controller.db.delete_flight(flight_id)
            self.load_data()


# ==============================================================================
# TAB 2: TICKET FARE ESTIMATOR (Cheerful Light Theme)
# ==============================================================================
class TicketPricingPanel(tk.Frame):
    """
    Modern interactive Fare Estimator featuring:
      1. Departure / المكان (من أين؟)
      2. Destination / الوجهة (إلى أين؟)
      3. Cabin Class (درجة السفر)
      4. Trip Type (ذهاب فقط / ذهاب وعودة)
    """

    AIRPORTS = [
        "Cairo (CAI)",
        "Alexandria (HBE)",
        "Dubai (DXB)",
        "Riyadh (RUH)",
        "Paris (CDG)",
        "London (LHR)",
        "Rome (FCO)",
        "New York (JFK)"
    ]

    BASE_FARES = {
        ("Cairo (CAI)", "Paris (CDG)"): (18700, "4h 35m"),
        ("Cairo (CAI)", "London (LHR)"): (20000, "5h 15m"),
        ("Cairo (CAI)", "New York (JFK)"): (28500, "11h 45m"),
        ("Cairo (CAI)", "Rome (FCO)"): (17500, "3h 40m"),
        ("Cairo (CAI)", "Dubai (DXB)"): (16200, "3h 30m"),
        ("Cairo (CAI)", "Riyadh (RUH)"): (14500, "2h 45m"),
        ("Cairo (CAI)", "Alexandria (HBE)"): (3200, "0h 45m"),

        ("Dubai (DXB)", "London (LHR)"): (24000, "7h 30m"),
        ("Dubai (DXB)", "Paris (CDG)"): (23500, "7h 10m"),
        ("Dubai (DXB)", "New York (JFK)"): (36000, "14h 20m"),
        ("Dubai (DXB)", "Cairo (CAI)"): (16200, "3h 45m"),
        ("Dubai (DXB)", "Riyadh (RUH)"): (8500, "1h 50m"),

        ("Riyadh (RUH)", "Cairo (CAI)"): (14500, "2h 45m"),
        ("Riyadh (RUH)", "Dubai (DXB)"): (8500, "1h 50m"),
        ("Riyadh (RUH)", "London (LHR)"): (23000, "6h 50m"),
        ("Riyadh (RUH)", "Paris (CDG)"): (22500, "6h 35m"),
        ("Riyadh (RUH)", "New York (JFK)"): (35000, "13h 40m"),

        ("London (LHR)", "New York (JFK)"): (22000, "8h 05m"),
        ("London (LHR)", "Paris (CDG)"): (6500, "1h 20m"),
        ("London (LHR)", "Cairo (CAI)"): (20000, "5h 10m"),

        ("Paris (CDG)", "New York (JFK)"): (23000, "8h 25m"),
        ("Paris (CDG)", "Cairo (CAI)"): (18700, "4h 30m"),
        ("Paris (CDG)", "Rome (FCO)"): (5800, "2h 05m"),
    }

    def __init__(self, parent, workspace: MainWorkspace):
        super().__init__(parent, bg=COLOR_BG)
        self.workspace = workspace
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        # Header
        tk.Label(self, text="Flight Ticket Fare Estimator", font=FONT_TITLE_HERO, bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        tk.Label(self, text="حدد مكان الانطلاق والوجهة المطلوبة لحساب متوسط سعر التذكرة فورياً.", font=FONT_BODY, bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(2, 12))

        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(fill="both", expand=True)

        # Left Parameters Card
        card = tk.Frame(container, bg=COLOR_SURFACE, padx=22, pady=18, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(card, text="مسار الرحلة والخيارات", font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_ACCENT).pack(anchor="w", pady=(0, 8))

        # 1. المكان / نقطة الانطلاق (From)
        tk.Label(card, text="1. مكان الانطلاق (Departure - من)", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
        self.origin_var = tk.StringVar(value="Cairo (CAI)")
        origin_drop = tk.OptionMenu(card, self.origin_var, *self.AIRPORTS, command=lambda e: self._calculate())
        origin_drop.configure(
            font=(FONT_NAME, 10), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_SURFACE, activeforeground=COLOR_ACCENT,
            relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDER
        )
        origin_drop["menu"].config(bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN, font=(FONT_NAME, 10))
        origin_drop.pack(fill="x", ipady=3, pady=(2, 8))

        # 2. الوجهة / الوصول (To)
        tk.Label(card, text="2. الوجهة المطلوبة (Destination - إلى)", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
        self.dest_var = tk.StringVar(value="Paris (CDG)")
        dest_drop = tk.OptionMenu(card, self.dest_var, *self.AIRPORTS, command=lambda e: self._calculate())
        dest_drop.configure(
            font=(FONT_NAME, 10), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_SURFACE, activeforeground=COLOR_ACCENT,
            relief="flat", highlightthickness=1, highlightbackground=COLOR_BORDER
        )
        dest_drop["menu"].config(bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN, font=(FONT_NAME, 10))
        dest_drop.pack(fill="x", ipady=3, pady=(2, 8))

        # 3. نوع الرحلة
        tk.Label(card, text="3. نوع التذكرة", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
        trip_type_frame = tk.Frame(card, bg=COLOR_SURFACE)
        trip_type_frame.pack(fill="x", pady=(2, 8))
        self.trip_type = tk.StringVar(value="one_way")
        tk.Radiobutton(
            trip_type_frame, text="ذهاب فقط (One Way)", variable=self.trip_type, value="one_way",
            font=(FONT_NAME, 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN, selectcolor=COLOR_SURFACE_ALT,
            activebackground=COLOR_SURFACE, activeforeground=COLOR_ACCENT, command=self._calculate
        ).pack(side="left", padx=(0, 15))
        tk.Radiobutton(
            trip_type_frame, text="ذهاب وعودة (Round Trip)", variable=self.trip_type, value="round_trip",
            font=(FONT_NAME, 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN, selectcolor=COLOR_SURFACE_ALT,
            activebackground=COLOR_SURFACE, activeforeground=COLOR_ACCENT, command=self._calculate
        ).pack(side="left")

        # 4. درجة السفر
        tk.Label(card, text="4. درجة السفر (Cabin Class)", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")
        class_frame = tk.Frame(card, bg=COLOR_SURFACE)
        class_frame.pack(fill="x", pady=(2, 0))
        self.class_var = tk.StringVar(value="eco")
        classes = [("السياحية (Eco)", "eco"), ("رجال الأعمال (Business)", "business"), ("الأولى (First VIP)", "first-class")]
        for title, val in classes:
            rb = tk.Radiobutton(
                class_frame, text=title, variable=self.class_var, value=val,
                font=(FONT_NAME, 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN,
                selectcolor=COLOR_SURFACE_ALT, activebackground=COLOR_SURFACE,
                activeforeground=COLOR_ACCENT, command=self._calculate
            )
            rb.pack(anchor="w", pady=1)

        # Right Summary Card
        self.summary_card = tk.Frame(container, bg=COLOR_SURFACE, padx=22, pady=18, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.summary_card.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(self.summary_card, text="تفاصيل وحساب التذكرة", font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_ACCENT).pack(anchor="w")

        self.route_badge = tk.Label(
            self.summary_card, text="Cairo (CAI) ➔ Paris (CDG)", font=(FONT_NAME, 11, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_ACCENT, padx=10, pady=5
        )
        self.route_badge.pack(fill="x", pady=(10, 6))

        self.duration_lbl = tk.Label(
            self.summary_card, text="⏱ مدة الرحلة المتوقعة: 4h 35m مباشر",
            font=(FONT_NAME, 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED
        )
        self.duration_lbl.pack(anchor="w", pady=(0, 8))

        tk.Label(self.summary_card, text="السعر المقدر للتذكرة:", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w")

        self.price_display = tk.Label(
            self.summary_card, text="0 EGP", font=(FONT_NAME, 24, "bold"),
            bg=COLOR_SURFACE, fg=COLOR_TEXT_MAIN
        )
        self.price_display.pack(anchor="w", pady=(2, 2))

        self.usd_display = tk.Label(
            self.summary_card, text="~$0 USD", font=(FONT_NAME, 11),
            bg=COLOR_SURFACE, fg=COLOR_SUCCESS
        )
        self.usd_display.pack(anchor="w", pady=(0, 12))

        details = [
            "✔ شاملة وزن الأمتعة (2 حقيبة × 23 كجم)",
            "✔ وجبة طعام ساخنة وخدمة Wi-Fi أثناء الرحلة",
            "✔ إمكانية استرداد أو تغيير الموعد بمرونة",
            "✔ أسعار رسمية شاملة الضرائب والرسوم"
        ]
        for d in details:
            tk.Label(self.summary_card, text=d, font=(FONT_NAME, 9), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=1)

        self._calculate()

    def _calculate(self):
        origin = self.origin_var.get()
        dest = self.dest_var.get()
        cls = self.class_var.get()
        is_round_trip = (self.trip_type.get() == "round_trip")

        self.route_badge.config(text=f"{origin} ✈ ➔ {dest}")

        if origin == dest:
            self.duration_lbl.config(text="⚠️ مكان الانطلاق والوجهة متطابقان! اختر وجهتين مختلفتين.")
            self.price_display.config(text="-- EGP")
            self.usd_display.config(text="غير متاح")
            return

        key = (origin, dest)
        reverse_key = (dest, origin)

        if key in self.BASE_FARES:
            base_fare, duration = self.BASE_FARES[key]
        elif reverse_key in self.BASE_FARES:
            base_fare, duration = self.BASE_FARES[reverse_key]
        else:
            base_fare = 19500
            duration = "5h 30m"

        multiplier = 1.0
        if cls == "business":
            multiplier = 1.45
        elif cls == "first-class":
            multiplier = 1.95

        trip_mult = 1.85 if is_round_trip else 1.0

        total_price = base_fare * multiplier * trip_mult
        usd_price = total_price / 50

        type_text = "ذهاب وعودة" if is_round_trip else "ذهاب فقط"
        self.duration_lbl.config(text=f"⏱ مدة الرحلة التقريبية: {duration} ({type_text})")
        self.price_display.config(text=f"{total_price:,.0f} EGP")
        self.usd_display.config(text=f"~${usd_price:,.0f} USD (حسب سعر الصرف التقريبي)")


# ==============================================================================
# TAB 3: PROMOTIONAL LUCKY WHEEL (Cheerful Light Theme)
# ==============================================================================
class LuckyWheelPanel(tk.Frame):
    """Sleek Promotional Wheel of Fortune with cheerful light styling."""

    OFFERS = ["10% DISCOUNT", "20% DISCOUNT", "30% DISCOUNT", "50% MEGA SALE", "40% DISCOUNT", "BETTER LUCK!"]
    # Cheerful Sky & Aviation Segment Palette
    SEGMENT_COLORS = ["#0284C7", "#38BDF8", "#0284C7", "#38BDF8", "#0284C7", "#94A3B8"]

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
        tk.Label(self, text="Promotional Wheel of Fortune", font=FONT_TITLE_HERO, bg=COLOR_BG, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        tk.Label(self, text="Spin daily to win exclusive flight vouchers and seat upgrade discounts.", font=FONT_BODY, bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w", pady=(2, 10))

        content = tk.Frame(self, bg=COLOR_BG)
        content.pack(fill="both", expand=True)

        # Left Canvas
        self.canvas = tk.Canvas(content, width=370, height=370, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(side="left", padx=(0, 20))

        # Right Controls & Prize Board
        right_box = tk.Frame(content, bg=COLOR_SURFACE, padx=25, pady=20, highlightbackground=COLOR_BORDER, highlightthickness=1)
        right_box.pack(side="right", fill="both", expand=True)

        tk.Label(right_box, text="REWARDS CONSOLE", font=(FONT_NAME, 10, "bold"), bg=COLOR_SURFACE, fg=COLOR_ACCENT).pack(anchor="w")

        self.spin_btn = tk.Button(
            right_box, text="🎡 SPIN THE WHEEL", font=(FONT_NAME, 12, "bold"),
            bg=COLOR_ACCENT, fg=COLOR_TEXT_WHITE, activebackground=COLOR_ACCENT_HOVER, activeforeground=COLOR_TEXT_WHITE,
            relief="flat", cursor="hand2", command=self.spin_wheel
        )
        self.spin_btn.pack(fill="x", ipady=8, pady=(15, 12))

        self.status_lbl = tk.Label(
            right_box, text="Click 'SPIN' to begin your flight reward draw.",
            font=FONT_BODY, bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED, justify="left"
        )
        self.status_lbl.pack(anchor="w")

        # Prize Card
        self.prize_card = tk.Frame(right_box, bg=COLOR_SURFACE_ALT, padx=15, pady=15, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.prize_card.pack(fill="x", pady=(15, 10))

        tk.Label(self.prize_card, text="CURRENT RESULT", font=(FONT_NAME, 9, "bold"), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MUTED).pack(anchor="w")

        self.prize_badge = tk.Label(
            self.prize_card, text="Awaiting Spin...", font=(FONT_NAME, 14, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT_MAIN
        )
        self.prize_badge.pack(pady=(6, 4))

        self.promo_code_lbl = tk.Label(
            self.prize_card, text="Voucher: ----", font=(FONT_NAME, 12, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_ACCENT
        )
        self.promo_code_lbl.pack(pady=(0, 4))

        tk.Label(
            right_box, text="ℹ Discounts apply automatically to eligible bookings at checkout.",
            font=(FONT_NAME, 8), bg=COLOR_SURFACE, fg=COLOR_TEXT_MUTED
        ).pack(side="bottom", anchor="w", pady=(10, 0))

    def draw_wheel(self):
        self.canvas.delete("all")
        cx, cy, radius = 185, 185, 155
        num = len(self.OFFERS)
        step = 360 / num

        for i in range(num):
            start = self.current_angle + i * step
            color = self.SEGMENT_COLORS[i % len(self.SEGMENT_COLORS)]

            self.canvas.create_arc(
                cx - radius, cy - radius, cx + radius, cy + radius,
                start=start, extent=step, fill=color, outline="#FFFFFF", width=2
            )

            mid = start + (step / 2)
            rad = math.radians(mid)
            tx = cx + (radius * 0.64) * math.cos(rad)
            ty = cy - (radius * 0.64) * math.sin(rad)

            self.canvas.create_text(
                tx, ty, text=self.OFFERS[i], fill=COLOR_TEXT_WHITE, font=(FONT_NAME, 8, "bold")
            )

        # Center Hub
        self.canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill=COLOR_SURFACE, outline=COLOR_ACCENT, width=3)
        self.canvas.create_text(cx, cy, text="✈", fill=COLOR_ACCENT, font=(FONT_NAME, 12, "bold"))

        # Top Indicator Arrow
        self.canvas.create_polygon(
            cx - 12, cy - radius - 8,
            cx + 12, cy - radius - 8,
            cx, cy - radius + 12,
            fill="#EF4444", outline="#B91C1C", width=1
        )

    def spin_wheel(self):
        if self.is_spinning:
            return
        self.is_spinning = True
        self.spin_btn.config(state="disabled", bg=COLOR_BORDER)
        self.status_lbl.config(text="Spinning the turbines... Good luck!")
        self.prize_badge.config(text="Spinning in progress...")
        self.promo_code_lbl.config(text="Calculating prize...", fg=COLOR_WARNING)
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
                self.promo_code_lbl.config(text=f"Promo Code: {code}", fg=COLOR_SUCCESS)
                self.status_lbl.config(text="Congratulations! Voucher code ready for checkout.")
            else:
                self.promo_code_lbl.config(text="Better luck next flight!", fg=COLOR_TEXT_MUTED)
                self.status_lbl.config(text="Thank you for participating.")


# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    app = ModernAirlineApp()
    app.mainloop()
