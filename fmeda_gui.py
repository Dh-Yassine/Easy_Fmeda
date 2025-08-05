import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from FMEDA import Project, SafetyFunction, Component, FailureMode
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import time
import math
import pandas as pd
from tkinter import filedialog
import os

class SlideFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.visible = False
        self.target_width = 0
        
    def slide_in(self, target_width=250, duration=300):
        self.target_width = target_width
        self.visible = True
        self.animate_width(0, target_width, duration)
        
    def slide_out(self, duration=300):
        self.visible = False
        self.animate_width(self.target_width, 0, duration)
        
    def animate_width(self, start_width, end_width, duration):
        steps = 20
        step_time = duration / steps
        
        def update_step(step):
            if step < steps:
                progress = step / steps
                eased_progress = 1 - math.cos(progress * math.pi / 2)
                current_width = start_width + (end_width - start_width) * eased_progress
                self.configure(width=int(current_width))
                self.after(int(step_time), lambda: update_step(step + 1))
                
        update_step(0)

class ModernScrolledFrame(ScrolledFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure_scrollbar_style()
        
    def configure_scrollbar_style(self):
        style = ttk.Style()
        style.configure("Modern.Vertical.TScrollbar",
                       gripcount=0,
                       background="#3f51b5",
                       troughcolor="#f5f5f5",
                       borderwidth=0,
                       arrowcolor="#ffffff",
                       darkcolor="#3f51b5",
                       lightcolor="#3f51b5",
                       width=12)

class FMEDAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FMEDA Analysis Tool - Professional Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 600)
        
        self.predefined_failure_modes = {
            "Resistor": [
                {"description": "Open circuit", "fit_rate": 10.0, "system_effect": "Loss of function"},
                {"description": "Short circuit", "fit_rate": 5.0, "system_effect": "Overcurrent/overheating"}
            ],
            "Capacitor": [
                {"description": "Open circuit", "fit_rate": 15.0, "system_effect": "Loss of filtering/decoupling"},
                {"description": "Short circuit", "fit_rate": 8.0, "system_effect": "Overcurrent/overheating"}
            ],
            "Inductor": [
                {"description": "Open circuit", "fit_rate": 12.0, "system_effect": "Loss of filtering"},
                {"description": "Short circuit", "fit_rate": 6.0, "system_effect": "Overcurrent/overheating"}
            ],
            "Diodes": [
                {"description": "Open circuit", "fit_rate": 20.0, "system_effect": "Loss of rectification/protection"},
                {"description": "Short circuit", "fit_rate": 10.0, "system_effect": "Overcurrent/overheating"}
            ],
            "Transistor/transistor like": [
                {"description": "Pin open circuit", "fit_rate": 25.0, "system_effect": "Loss of switching/amplification"},
                {"description": "Pin to pin short circuit", "fit_rate": 15.0, "system_effect": "Malfunction"},
                {"description": "Pin to GND short circuit", "fit_rate": 12.0, "system_effect": "Loss of function"},
                {"description": "Pin to VCC short circuit", "fit_rate": 12.0, "system_effect": "Overcurrent/overheating"}
            ],
            "IC": [
                {"description": "Pin open circuit", "fit_rate": 30.0, "system_effect": "Loss of function"},
                {"description": "Pin to pin short circuit", "fit_rate": 20.0, "system_effect": "Malfunction"},
                {"description": "Pin to GND short circuit", "fit_rate": 15.0, "system_effect": "Loss of function"},
                {"description": "Pin to VCC short circuit", "fit_rate": 15.0, "system_effect": "Overcurrent/overheating"}
            ],
            "Relays, contactors": [
                {"description": "Stuck close", "fit_rate": 35.0, "system_effect": "Continuous operation"},
                {"description": "Stuck open", "fit_rate": 35.0, "system_effect": "Loss of switching"}
            ],
            "Transformer": [
                {"description": "Pin open circuit", "fit_rate": 18.0, "system_effect": "Loss of isolation/transformation"},
                {"description": "Pin to pin short circuit", "fit_rate": 12.0, "system_effect": "Malfunction"},
                {"description": "Pin to GND short circuit", "fit_rate": 10.0, "system_effect": "Loss of isolation"},
                {"description": "Pin to VCC short circuit", "fit_rate": 10.0, "system_effect": "Overcurrent/overheating"}
            ],
            "Thermistor": [
                {"description": "Open circuit", "fit_rate": 22.0, "system_effect": "Loss of temperature sensing"},
                {"description": "Short circuit", "fit_rate": 11.0, "system_effect": "False temperature reading"},
                {"description": "Resistance drift", "fit_rate": 8.0, "system_effect": "Inaccurate temperature reading"}
            ],
            "Crystals": [
                {"description": "Open circuit", "fit_rate": 28.0, "system_effect": "Loss of clock signal"},
                {"description": "Short circuit", "fit_rate": 14.0, "system_effect": "Clock malfunction"},
                {"description": "Frequency drift", "fit_rate": 10.0, "system_effect": "Inaccurate timing"}
            ],
            "Other": []
        }
        
        self.colors = {
            'primary': '#1a237e',
            'secondary': '#283593',
            'accent': '#3f51b5',
            'success': '#2e7d32',
            'warning': '#f57c00',
            'danger': '#d32f2f',
            'light': '#f5f5f5',
            'dark': '#1a237e',
            'sidebar': '#1a237e',
            'sidebar_hover': '#283593',
            'sidebar_active': '#3f51b5',
            'content': '#ffffff',
            'hover': '#3949ab',
            'text': '#212121',
            'text_light': '#757575',
            'text_white': '#ffffff',
            'border': '#e0e0e0',
            'shadow': '#00000020'
        }
        
        self.setup_theme()
        
        self.project = Project("FMEDA Project")
        self.lifetime = 0
        self.current_page = "assumptions"
        
        self.create_main_layout()
        
        self.create_modern_sidebar()
        
        self.disable_all_navigation_except_home()
        
        self.create_top_navigation()
        
        self.create_content_area()
        
        self.root.after(100, self.show_home_screen)
        
        self.root.bind('<Configure>', self.on_window_resize)

    def setup_theme(self):
        style = ttk.Style()
        
        style.configure("Modern.TButton", 
                       font=('Segoe UI', 11, 'bold'),
                       padding=(25, 15),
                       borderwidth=0,
                       focuscolor='none',
                       background=self.colors['accent'],
                       foreground=self.colors['text_white'])
        
        style.configure("Sidebar.TButton",
                       font=('Segoe UI', 12, 'bold'),
                       padding=(30, 18),
                       borderwidth=0,
                       focuscolor='none',
                       background=self.colors['sidebar'],
                       foreground=self.colors['text_white'],
                       width=22)
                   
        style.configure("Sidebar.Active.TButton",
                       font=('Segoe UI', 12, 'bold'),
                       padding=(30, 18),
                       borderwidth=0,
                       focuscolor='none',
                       background=self.colors['sidebar_active'],
                       foreground=self.colors['text_white'],
                       width=22)
    
        style.map("Sidebar.TButton",
                 background=[('active', self.colors['sidebar_hover'])],
                 foreground=[('active', self.colors['text_white'])])
             
        style.map("Sidebar.Active.TButton",
                 background=[('active', self.colors['sidebar_hover'])],
                 foreground=[('active', self.colors['text_white'])])
        
        style.configure("TopNav.TButton",
                       font=('Segoe UI', 10, 'bold'),
                       padding=(18, 10),
                       borderwidth=0,
                       focuscolor='none',
                       background=self.colors['accent'],
                       foreground=self.colors['text_white'])
        
        style.configure("Sidebar.TFrame", 
                       background=self.colors['sidebar'],
                       relief='flat')
        style.configure("Content.TFrame", 
                       background=self.colors['content'],
                       relief='flat')
        style.configure("TopNav.TFrame", 
                       background=self.colors['light'],
                       relief='flat')
        
        style.configure("Title.TLabel", 
                       font=('Segoe UI', 28, 'bold'),
                       background=self.colors['sidebar'],
                       foreground=self.colors['text_white'])
        
        style.configure("Subtitle.TLabel",
                       font=('Segoe UI', 14),
                       background=self.colors['sidebar'],
                       foreground=self.colors['text_white'])
        
        style.configure("SectionTitle.TLabel",
                       font=('Segoe UI', 18, 'bold'),
                       foreground=self.colors['primary'])
        
        style.configure("Modern.TLabelframe",
                       padding=25,
                       borderwidth=2,
                       relief='solid',
                       background=self.colors['content'])
        
        style.configure("Modern.TLabelframe.Label",
                       font=('Segoe UI', 14, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['content'])
        
        style.configure("Modern.TTreeview",
                       background=self.colors['content'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['content'],
                       font=('Segoe UI', 11),
                       rowheight=35)
        
        style.configure("Modern.TTreeview.Heading",
                       font=('Segoe UI', 12, 'bold'),
                       background=self.colors['light'],
                       foreground=self.colors['primary'],
                       padding=(10, 8))
        
        style.configure("Modern.Vertical.TScrollbar",
                       gripcount=0,
                       background=self.colors['accent'],
                       troughcolor=self.colors['light'],
                       borderwidth=0,
                       arrowcolor=self.colors['text_white'],
                       darkcolor=self.colors['accent'],
                       lightcolor=self.colors['accent'],
                       width=12)
        
        style.configure("Modern.TEntry",
                       font=('Segoe UI', 11),
                       padding=(10, 8),
                       borderwidth=2,
                       relief='solid',
                       fieldbackground=self.colors['content'])
        
        style.configure("Modern.TCombobox",
                       font=('Segoe UI', 11),
                       padding=(10, 8),
                       borderwidth=2,
                       relief='solid',
                       fieldbackground=self.colors['content'])
        
        style.configure("Modern.TCheckbutton",
                       font=('Segoe UI', 11),
                       background=self.colors['content'],
                       foreground=self.colors['text'])
        
    def create_main_layout(self):
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=BOTH, expand=True)
        
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
    def create_modern_sidebar(self):
        self.sidebar = ttk.Frame(self.main_container, style="Sidebar.TFrame", width=320)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=0, pady=0)
        self.sidebar.grid_propagate(False)
        
        self.create_sidebar_header()
        
        self.create_navigation_buttons()
        
        self.create_sidebar_footer()
        
    def create_sidebar_header(self):
        header_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        header_frame.pack(fill=X, pady=40, padx=25)
        
        self.title_label = ttk.Label(header_frame, 
                                    text=self.project.name if hasattr(self, 'project') else "FMEDA", 
                                    style="Title.TLabel")
        self.title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Analysis Tool", 
                                  style="Subtitle.TLabel")
        subtitle_label.pack(anchor='w', pady=(8, 0))
        
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill=X, pady=25)
        
    def create_navigation_buttons(self):
        nav_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        nav_frame.pack(fill=BOTH, expand=True, padx=25)
        
        nav_items = [
            ("🏠 Home", "home", self.show_home_screen),
            ("📋 Analysis Assumptions", "assumptions", self.show_assumptions),
            ("⚡ Safety Functions", "safety_functions", self.show_safety_functions),
            ("🔧 Components", "components", self.show_components),
            ("📊 FMEDA Analysis", "fmeda", self.show_fmeda),
            ("📈 Results", "results", self.show_results)
        ]
        
        self.nav_buttons = {}
        
        for text, key, command in nav_items:
            btn = ttk.Button(nav_frame, 
                           text=text, 
                           command=command, 
                           style='Sidebar.TButton')
            btn.pack(fill=X, pady=6)
            self.nav_buttons[key] = btn
            
    def create_sidebar_footer(self):
        footer_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        footer_frame.pack(side=BOTTOM, fill=X, pady=25, padx=25)
        
        footer_label = ttk.Label(footer_frame, 
                               text="© Dhouibi FMEDA Tool\nProfessional Edition", 
                               style="Subtitle.TLabel",
                               justify='center')
        footer_label.pack()
        
    def create_top_navigation(self):
        self.top_nav = ttk.Frame(self.main_container, style="TopNav.TFrame", height=70)
        self.top_nav.grid(row=0, column=1, sticky='ew', padx=0, pady=0)
        self.top_nav.grid_propagate(False)
        
        left_frame = ttk.Frame(self.top_nav, style="TopNav.TFrame")
        left_frame.pack(side=LEFT, fill=Y, padx=25, pady=20)
        
        self.breadcrumb_label = ttk.Label(left_frame, 
                                        text="Analysis Assumptions", 
                                        font=('Segoe UI', 16, 'bold'),
                                        foreground=self.colors['primary'])
        self.breadcrumb_label.pack(side=LEFT)
        
        right_frame = ttk.Frame(self.top_nav, style="TopNav.TFrame")
        right_frame.pack(side=RIGHT, fill=Y, padx=25, pady=15)
        
        action_buttons = [
            ("💾 Save Project", 'success.TButton', self.save_project),
            ("📥 Import Project", 'info.TButton', self.import_project),
            ("❓ Help", 'warning.TButton', self.show_help_page)
        ]

        for text, style, command in action_buttons:
            btn = ttk.Button(right_frame,
                           text=text,
                           style=style,
                           command=command)
            btn.pack(side=RIGHT, padx=8)
            
    def create_content_area(self):
        self.content_container = ModernScrolledFrame(self.main_container, autohide=True)
        self.content_container.grid(row=1, column=1, sticky='nsew', padx=15, pady=15)
        
        self.content_frame = ttk.Frame(self.content_container, style="Content.TFrame")
        self.content_frame.pack(fill=BOTH, expand=True, padx=25, pady=25)
        
    def update_breadcrumb(self, text):
        self.breadcrumb_label.configure(text=text)
        
    def update_active_nav(self, active_key):
        for key, btn in self.nav_buttons.items():
            btn.configure(style='Sidebar.TButton')
            
        if active_key in self.nav_buttons:
            self.nav_buttons[active_key].configure(style='Sidebar.Active.TButton')
            
    def on_window_resize(self, event):
        if event.widget == self.root:
            width = self.root.winfo_width()
            
            if width < 1400:
                self.sidebar.configure(width=280)
            elif width < 1600:
                self.sidebar.configure(width=300)
            else:
                self.sidebar.configure(width=320)
                
    def show_success_message(self, message):
        success_label = ttk.Label(self.main_container, 
                                  text=f"✅ {message}", 
                                  font=('Segoe UI', 12, 'bold'),
                                  foreground='white',
                                  background=self.colors['success'],
                                  padding=10)
        
        success_label.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)
        
        self.root.after(3000, success_label.destroy)
                
    def show_assumptions(self):
        self.clear_content()
        self.update_breadcrumb("Analysis Assumptions")
        self.update_active_nav("assumptions")
        
        main_frame = ttk.LabelFrame(self.content_frame, 
                                  text="🏠 Analysis Assumptions", 
                                  style="Modern.TLabelframe")
        main_frame.pack(fill=BOTH, expand=True)
        
        content_grid = ttk.Frame(main_frame)
        content_grid.pack(fill=BOTH, expand=True, padx=30, pady=30)
        content_grid.grid_columnconfigure(1, weight=1)
        
        lifetime_frame = ttk.Frame(content_grid)
        lifetime_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=20)
        lifetime_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(lifetime_frame, 
                 text="System Lifetime (hours):", 
                 font=('Segoe UI', 12, 'bold')).grid(row=0, column=0, sticky='w', pady=10)
        
        lifetime_entry = ttk.Entry(lifetime_frame, 
                                 font=('Segoe UI', 11),
                                 width=20)
        lifetime_entry.grid(row=0, column=1, sticky='ew', padx=(20, 0), pady=10)
        
        current_frame = ttk.Frame(content_grid)
        current_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=20)
        
        if self.lifetime > 0:
            ttk.Label(current_frame, 
                     text=f"Current Lifetime: {self.lifetime:,.0f} hours", 
                     font=('Segoe UI', 11),
                     foreground=self.colors['success']).pack(anchor='w')
        
        def save_lifetime():
            try:
                new_lifetime = float(lifetime_entry.get())
                if new_lifetime <= 0:
                    messagebox.showerror("Error", "Lifetime must be a positive number")
                    return
                    
                self.lifetime = new_lifetime
                self.project.lifetime = self.lifetime
                
                self.enable_all_navigation()
                
                self.show_success_message(f"Lifetime set to {self.lifetime:,.0f} hours")
                
                self.show_assumptions()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        button_frame = ttk.Frame(content_grid)
        button_frame.grid(row=2, column=0, columnspan=2, pady=30)
        
        save_btn = ttk.Button(button_frame, 
                                text="💾 Save Lifetime", 
                                command=save_lifetime, 
                                style='success.TButton')
        save_btn.pack()
        
    def show_safety_functions(self):
        self.clear_content()
        self.update_breadcrumb("Safety Functions")
        self.update_active_nav("safety_functions")

        main_frame = ttk.LabelFrame(self.content_frame,
                                  text="⚡ Safety Functions Management",
                                  style="Modern.TLabelframe")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=BOTH, expand=True, pady=10, padx=10)

        columns = ("SF-ID", "Description", "Target Integrity Level", "Components")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                          height=12, style="Modern.Treeview")

        tree.heading("SF-ID", text="SF-ID")
        tree.heading("Description", text="Description")
        tree.heading("Target Integrity Level", text="Target Integrity Level")
        tree.heading("Components", text="Components")

        tree.column("SF-ID", width=100, anchor='center')
        tree.column("Description", width=300, anchor='w')
        tree.column("Target Integrity Level", width=150, anchor='center')
        tree.column("Components", width=100, anchor='center')

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview, style="Modern.Vertical.TScrollbar")
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for sf in self.project.SF_list:
            component_count = len(sf.related_components)
            tree.insert("", END, iid=sf.id, values=(sf.id, sf.description, sf.target_integrity_level, component_count))

        def on_sf_double_click(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                show_edit_sf_form()
        tree.bind('<Double-1>', on_sf_double_click)

        def show_add_sf_form():
            add_window = ttk.Toplevel(self.root)
            add_window.title("Add Safety Function")
            add_window.geometry("700x600")
            add_window.minsize(600, 500)
            add_window.transient(self.root)
            add_window.grab_set()
            add_window.configure(bg=self.colors['content'])

            scrolled = ModernScrolledFrame(add_window, autohide=True)
            scrolled.pack(fill=BOTH, expand=True)
            form_container = ttk.Frame(scrolled, padding=40, style="Content.TFrame")
            form_container.pack(fill=BOTH, expand=True)
            form_container.grid_columnconfigure(1, weight=1)

            title_frame = ttk.Frame(form_container, style="Content.TFrame")
            title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky='ew')
            
            ttk.Label(title_frame, 
                     text="➕ Add New Safety Function",
                     font=('Segoe UI', 18, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").pack(anchor='w')
            
            ttk.Label(title_frame, 
                     text="Define a new safety function for your system",
                     font=('Segoe UI', 11),
                     foreground=self.colors['text_light'],
                     style="Content.TLabel").pack(anchor='w', pady=(5, 0))

            validator = FormValidator()

            ttk.Label(form_container, 
                     text="Safety Function ID:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=1, column=0, sticky='w', pady=15, padx=(0, 20))
            sf_id_entry = ttk.Entry(form_container, font=('Segoe UI', 12))
            sf_id_entry.grid(row=1, column=1, sticky='ew', padx=(0, 0), pady=15)
            validator.add_validator(sf_id_entry, validate_not_empty, "Safety Function ID cannot be empty", form_container, 1, 1)

            ttk.Label(form_container, 
                     text="Description:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=2, column=0, sticky='w', pady=15, padx=(0, 20))
            description_entry = ttk.Entry(form_container, font=('Segoe UI', 12))
            description_entry.grid(row=2, column=1, sticky='ew', padx=(0, 0), pady=15)
            validator.add_validator(description_entry, validate_not_empty, "Description cannot be empty", form_container, 2, 1)

            ttk.Label(form_container, 
                     text="Target Integrity Level:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=3, column=0, sticky='w', pady=15, padx=(0, 20))
            til_combo = ttk.Combobox(form_container, 
                                   values=["ASIL A", "ASIL B", "ASIL C", "ASIL D"], 
                                   font=('Segoe UI', 12),
                                   state="readonly")
            til_combo.grid(row=3, column=1, sticky='ew', padx=(0, 0), pady=15)
            til_combo.set("ASIL A")

            def save_sf():
                if not validator.validate_all():
                    messagebox.showerror("Validation Error", "Please fix the validation errors before saving.", parent=add_window)
                    return
                
                sf_id = sf_id_entry.get().strip()
                if any(sf.id == sf_id for sf in self.project.SF_list):
                    messagebox.showerror("Error", "Safety Function ID already exists", parent=add_window)
                    return

                sf = SafetyFunction(sf_id)
                sf.description = description_entry.get().strip()
                sf.target_integrity_level = til_combo.get()
                self.project.add_SF(sf)

                tree.insert("", END, iid=sf_id, values=(sf.id, sf.description, sf.target_integrity_level, 0))

                self.enable_all_navigation()
                
                self.show_success_message(f"Safety Function '{sf_id}' added successfully")
                add_window.destroy()

            button_container = ttk.Frame(form_container, style="Content.TFrame")
            button_container.grid(row=4, column=0, columnspan=2, pady=(40, 0), sticky='ew')
            
            HoverButton(button_container, 
                       text="💾 Save Safety Function", 
                       command=save_sf, 
                       style="success.TButton", 
                       width=20).pack(side=LEFT, padx=(0, 15))
            
            HoverButton(button_container, 
                       text="❌ Cancel", 
                       command=add_window.destroy, 
                       style="danger.TButton", 
                       width=15).pack(side=LEFT, padx=(0, 0))
        
        def show_edit_sf_form():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a safety function to edit.")
                return

            sf_id = selected[0]
            sf_to_edit = next((sf for sf in self.project.SF_list if sf.id == sf_id), None)
            if not sf_to_edit:
                return

            edit_window = ttk.Toplevel(self.root)
            edit_window.title("Edit Safety Function")
            edit_window.geometry("700x600")
            edit_window.minsize(600, 500)
            edit_window.transient(self.root)
            edit_window.grab_set()
            edit_window.configure(bg=self.colors['content'])

            scrolled = ModernScrolledFrame(edit_window, autohide=True)
            scrolled.pack(fill=BOTH, expand=True)
            form_container = ttk.Frame(scrolled, padding=40, style="Content.TFrame")
            form_container.pack(fill=BOTH, expand=True)
            form_container.grid_columnconfigure(1, weight=1)

            title_frame = ttk.Frame(form_container, style="Content.TFrame")
            title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky='ew')
            
            ttk.Label(title_frame, 
                     text="✏️ Edit Safety Function",
                     font=('Segoe UI', 18, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").pack(anchor='w')
            
            ttk.Label(title_frame, 
                     text=f"Modify safety function: {sf_to_edit.id}",
                     font=('Segoe UI', 11),
                     foreground=self.colors['text_light'],
                     style="Content.TLabel").pack(anchor='w', pady=(5, 0))

            ttk.Label(form_container, 
                     text="Safety Function ID:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=1, column=0, sticky='w', pady=15, padx=(0, 20))
            ttk.Label(form_container, 
                     text=sf_to_edit.id, 
                     font=('Segoe UI', 12),
                     foreground=self.colors['text'],
                     style="Content.TLabel").grid(row=1, column=1, sticky='w', padx=(0, 0), pady=15)

            ttk.Label(form_container, 
                     text="Description:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=2, column=0, sticky='w', pady=15, padx=(0, 20))
            desc_entry = ttk.Entry(form_container, font=('Segoe UI', 12))
            desc_entry.insert(0, sf_to_edit.description)
            desc_entry.grid(row=2, column=1, sticky='ew', padx=(0, 0), pady=15)

            ttk.Label(form_container, 
                     text="Target Integrity Level:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=3, column=0, sticky='w', pady=15, padx=(0, 20))
            til_combo = ttk.Combobox(form_container, 
                                   values=["ASIL A", "ASIL B", "ASIL C", "ASIL D"], 
                                   font=('Segoe UI', 12),
                                   state="readonly")
            til_combo.set(sf_to_edit.target_integrity_level)
            til_combo.grid(row=3, column=1, sticky='ew', padx=(0, 0), pady=15)

            ttk.Label(form_container, 
                     text="Related Components:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=4, column=0, sticky='w', pady=15, padx=(0, 20))
            
            comp_count = len(sf_to_edit.related_components)
            comp_text = f"{comp_count} component{'s' if comp_count != 1 else ''} linked"
            ttk.Label(form_container, 
                     text=comp_text, 
                     font=('Segoe UI', 12),
                     foreground=self.colors['text_light'],
                     style="Content.TLabel").grid(row=4, column=1, sticky='w', padx=(0, 0), pady=15)

            def save_changes():
                new_desc = desc_entry.get().strip()
                new_til = til_combo.get()

                if not new_desc:
                    messagebox.showerror("Error", "Description cannot be empty.", parent=edit_window)
                    return

                sf_to_edit.description = new_desc
                sf_to_edit.target_integrity_level = new_til

                tree.item(sf_id, values=(sf_id, new_desc, new_til, len(sf_to_edit.related_components)))
                self.show_success_message("Safety function updated successfully!")
                edit_window.destroy()

            button_container = ttk.Frame(form_container, style="Content.TFrame")
            button_container.grid(row=5, column=0, columnspan=2, pady=(40, 0), sticky='ew')
            
            HoverButton(button_container, 
                       text="💾 Save Changes", 
                       command=save_changes, 
                       style="success.TButton", 
                       width=18).pack(side=LEFT, padx=(0, 15))
            
            HoverButton(button_container, 
                       text="❌ Cancel", 
                       command=edit_window.destroy, 
                       style="danger.TButton", 
                       width=15).pack(side=LEFT, padx=(0, 0))
        
        def remove_sf():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a safety function to remove.")
                return

            sf_id = selected[0]
            sf_to_remove = next((sf for sf in self.project.SF_list if sf.id == sf_id), None)

            if sf_to_remove:
                self.project.SF_list.remove(sf_to_remove)
                
                for comp in self.project.bom:
                    if sf_to_remove in comp.related_Sfs:
                        comp.related_Sfs.remove(sf_to_remove)

                tree.delete(selected[0])
                self.enable_all_navigation()
                self.show_success_message("Safety function removed successfully!")
        
        button_frame = ttk.Frame(main_frame, style="Content.TFrame")
        button_frame.pack(fill=X, pady=20, padx=20)

        add_btn = ttk.Button(button_frame, text="➕ Add SF",
                           command=show_add_sf_form, style='success.TButton')
        add_btn.pack(side=LEFT, padx=5, pady=10)

        edit_btn = ttk.Button(button_frame, text="✏️ Edit SF",
                              command=show_edit_sf_form, style='warning.TButton')
        edit_btn.pack(side=LEFT, padx=5, pady=10)

        remove_btn = ttk.Button(button_frame, text="❌ Remove SF",
                                command=remove_sf, style='danger.TButton')
        remove_btn.pack(side=LEFT, padx=5, pady=10)
        
        import_sf_btn = ttk.Button(button_frame, text="📥 Import SF",
                                 command=self.import_sf,
                                 style='info.TButton')
        import_sf_btn.pack(side=LEFT, padx=5, pady=10)

    def import_sf(self):
        from tkinter import filedialog
        import pandas as pd
        file_path = filedialog.askopenfilename(
            title='Import Safety Functions CSV',
            filetypes=[('CSV Files', '*.csv')]
        )
        if not file_path:
            return
        try:
            df = pd.read_csv(file_path)
            required_cols = {'id', 'description', 'target_integrity_level'}
            if not required_cols.issubset(df.columns):
                messagebox.showerror("Error", f"CSV must contain columns: {', '.join(required_cols)}")
                return
            for _, row in df.iterrows():
                sf_id = str(row['id']).strip()
                if any(str(sf.id) == sf_id for sf in self.project.SF_list):
                    continue  # Skip duplicates
                sf = SafetyFunction(sf_id)
                sf.description = str(row['description']).strip()
                sf.target_integrity_level = str(row['target_integrity_level']).strip()
                self.project.add_SF(sf)
            self.show_success_message("Safety Functions imported successfully!")
            self.show_safety_functions()  # Refresh table
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Safety Functions: {e}")

    def show_components(self):
        self.clear_content()
        self.update_breadcrumb("Components")
        self.update_active_nav("components")
        
        main_frame = ttk.LabelFrame(self.content_frame, 
                                  text="🔧 Components Management", 
                                  style="Modern.TLabelframe")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=BOTH, expand=True, pady=10, padx=10)
        
        columns = ("ID", "Type", "Failure Rate (FIT)", "Related SF", "Failure Modes")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                          height=10, style="Modern.Treeview")
        
        for col in columns:
            tree.heading(col, text=col)
            
        tree.column("ID", width=80, anchor='center')
        tree.column("Type", width=150, anchor='w')
        tree.column("Failure Rate (FIT)", width=120, anchor='center')
        tree.column("Related SF", width=100, anchor='center')
        tree.column("Failure Modes", width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview, style="Modern.Vertical.TScrollbar")
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        for comp in self.project.bom:
            related_sf = ", ".join([sf.id for sf in comp.related_Sfs]) if comp.related_Sfs else "None"
            fm_count = len(comp.failure_modes)
            tree.insert("", END, iid=comp.id, values=(comp.id, comp.type, comp.failure_rate, related_sf, fm_count))
        
        def on_component_double_click(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                show_edit_component_form()
        tree.bind('<Double-1>', on_component_double_click)
        
        def show_add_component_form():
            add_window = ttk.Toplevel(self.root)
            add_window.title("Add Component")
            add_window.geometry("700x900")
            add_window.minsize(600, 700)
            add_window.transient(self.root)
            add_window.grab_set()
            add_window.configure(bg=self.colors['content'])

            scrolled = ModernScrolledFrame(add_window, autohide=True)
            scrolled.pack(fill=BOTH, expand=True)
            form_container = ttk.Frame(scrolled, padding=40, style="Content.TFrame")
            form_container.pack(fill=BOTH, expand=True)
            form_container.grid_columnconfigure(1, weight=1)

            title_frame = ttk.Frame(form_container, style="Content.TFrame")
            title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky='ew')
            
            ttk.Label(title_frame, 
                     text="🔧 Add New Component",
                     font=('Segoe UI', 18, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").pack(anchor='w')
            
            ttk.Label(title_frame, 
                     text="Define a new hardware component for your system",
                     font=('Segoe UI', 11),
                     foreground=self.colors['text_light'],
                     style="Content.TLabel").pack(anchor='w', pady=(5, 0))

            basic_frame = ttk.LabelFrame(form_container, text="Basic Information", 
                                       style="Modern.TLabelframe", padding=15)
            basic_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20))
            basic_frame.grid_columnconfigure(1, weight=1)

            ttk.Label(basic_frame, 
                     text="Component ID:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=0, column=0, sticky='w', pady=10, padx=(0, 20))
            id_entry = ttk.Entry(basic_frame, font=('Segoe UI', 12))
            id_entry.grid(row=0, column=1, sticky='ew', pady=10)

            ttk.Label(basic_frame, 
                     text="Component Type:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=1, column=0, sticky='w', pady=10, padx=(0, 20))
            component_types = list(self.predefined_failure_modes.keys())
            type_combo = ttk.Combobox(basic_frame, 
                                    values=component_types, 
                                    font=('Segoe UI', 12),
                                    state="readonly")
            type_combo.grid(row=1, column=1, sticky='ew', pady=10)
            
            ttk.Label(basic_frame, 
                     text="FIT Rate Total:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=2, column=0, sticky='w', pady=10, padx=(0, 20))
            fit_entry = ttk.Entry(basic_frame, font=('Segoe UI', 12))
            fit_entry.grid(row=2, column=1, sticky='ew', pady=10)
            
            auto_populate_var = tk.BooleanVar(value=True)
            auto_check = ttk.Checkbutton(basic_frame, 
                                       text="Auto-populate failure modes based on type",
                                       variable=auto_populate_var,
                                       style='Modern.TCheckbutton')
            auto_check.grid(row=3, column=0, columnspan=2, sticky='w', pady=10)

            sf_frame = ttk.LabelFrame(form_container, text="Related Safety Functions", 
                                    style="Modern.TLabelframe", padding=15)
            sf_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 20))
            sf_frame.grid_columnconfigure(0, weight=1)
            
            ttk.Label(sf_frame, 
                     text="Select the safety functions this component is related to:", 
                     font=('Segoe UI', 11),
                     foreground=self.colors['text'],
                     style="Content.TLabel").grid(row=0, column=0, sticky='w', pady=(0, 10))
            
            sf_ids = [sf.id for sf in self.project.SF_list]
            sf_listbox = tk.Listbox(sf_frame, 
                                  selectmode='multiple', 
                                  exportselection=False, 
                                  height=6, 
                                  font=('Segoe UI', 11))
            for sfid in sf_ids:
                sf_listbox.insert(END, sfid)
            sf_listbox.grid(row=1, column=0, sticky='ew', pady=(0, 10))

            fm_preview_frame = ttk.LabelFrame(form_container, text="Failure Modes (auto-populate)", style="Modern.TLabelframe", padding=15)
            fm_preview_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(0, 20))
            fm_preview_frame.grid_columnconfigure(0, weight=1)

            fm_check_vars = [[]]  # mutable container for closure
            fm_checkboxes = []
            select_all_var = tk.BooleanVar(value=True)

            def update_fm_checkboxes():
                for cb in fm_checkboxes:
                    cb.destroy()
                fm_check_vars[0].clear()
                fm_checkboxes.clear()
                comp_type = type_combo.get().strip()
                try:
                    fit_rate = float(fit_entry.get())
                except ValueError:
                    fit_rate = 0
                existing_fm_descs = set()  # No existing FMs for a new component
                if comp_type in self.predefined_failure_modes and fit_rate > 0:
                    for i, fm_data in enumerate(self.predefined_failure_modes[comp_type]):
                        percent = fm_data["fit_rate"]
                        actual_fit = fit_rate * (percent / 100)
                        checked = fm_data["description"] in existing_fm_descs
                        var = tk.BooleanVar(value=checked)
                        cb = ttk.Checkbutton(fm_preview_frame, text=f"{fm_data['description']} ({percent}% = {actual_fit:.2f} FIT)", variable=var, style='Modern.TCheckbutton')
                        cb.pack(anchor='w', padx=10, pady=2)
                        fm_check_vars[0].append(var)
                        fm_checkboxes.append(cb)
                else:
                    lbl = ttk.Label(fm_preview_frame, text="No predefined failure modes or FIT rate not set.", font=('Segoe UI', 11))
                    lbl.pack(anchor='w', padx=10, pady=2)
                    fm_checkboxes.append(lbl)

            def on_select_all():
                for var in fm_check_vars[0]:
                    var.set(select_all_var.get())

            select_all_cb = ttk.Checkbutton(fm_preview_frame, text="Select All", variable=select_all_var, command=on_select_all, style='Modern.TCheckbutton')
            select_all_cb.pack(anchor='w', padx=5, pady=(0, 5))

            def auto_populate_failure_modes():
                update_fm_checkboxes()

            type_combo.bind('<<ComboboxSelected>>', lambda e: auto_populate_failure_modes())
            fit_entry.bind('<KeyRelease>', lambda e: auto_populate_failure_modes())

            auto_populate_failure_modes()

            def save_component():
                try:
                    comp_id = int(id_entry.get())
                    comp_type = type_combo.get().strip()
                    fit_rate = float(fit_entry.get())
                    if not comp_type:
                        messagebox.showerror("Error", "Please select a component type", parent=add_window)
                        return
                    if any(c.id == comp_id for c in self.project.bom):
                        messagebox.showerror("Error", "Component ID already exists", parent=add_window)
                        return
                    comp = Component(comp_id)
                    comp.type = comp_type
                    comp.failure_rate = fit_rate
                    if auto_populate_var.get() and comp_type in self.predefined_failure_modes and fit_rate > 0:
                        predefined_fms = self.predefined_failure_modes[comp_type]
                        for i, fm_data in enumerate(predefined_fms):
                            if i < len(fm_check_vars[0]) and fm_check_vars[0][i].get():
                                fm = FailureMode()
                                fm.description = fm_data["description"]
                                percent = fm_data["fit_rate"]
                                fm.Failure_rate_total = fit_rate * (percent / 100)
                                fm.system_level_effect = fm_data["system_effect"]
                                fm.is_SPF = 1
                                fm.set_spf_mechanism("None", 0.0)
                                comp.add_FM(fm)
                    selected_indices = sf_listbox.curselection()
                    selected_sf_ids = [sf_ids[i] for i in selected_indices]
                    for sfid in selected_sf_ids:
                        sf_obj = next((sf for sf in self.project.SF_list if sf.id == sfid), None)
                        if sf_obj:
                            comp.related_Sfs.append(sf_obj)
                            sf_obj.add_component(comp)
                    self.project.bom.append(comp)
                    related_sf_str = ", ".join(selected_sf_ids) if selected_sf_ids else "None"
                    fm_count = len(comp.failure_modes)
                    tree.insert("", END, iid=comp_id, values=(comp_id, comp_type, fit_rate, related_sf_str, fm_count))
                    success_msg = f"Component '{comp_id}' added successfully"
                    if auto_populate_var.get() and comp_type in self.predefined_failure_modes:
                        fm_count = len(self.predefined_failure_modes[comp_type])
                        success_msg += f" with {fm_count} predefined failure modes"
                    self.show_success_message(success_msg)
                    add_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid values for ID and FIT rate", parent=add_window)

            button_frame = ttk.Frame(form_container, style="Content.TFrame")
            button_frame.grid(row=4, column=0, columnspan=2, pady=(30, 0), sticky='ew')
            
            HoverButton(button_frame, 
                       text="💾 Save Component", 
                       command=save_component, 
                       style="success.TButton", 
                       width=18).pack(side=LEFT, padx=(0, 15))
            
            HoverButton(button_frame, 
                       text="❌ Cancel", 
                       command=add_window.destroy, 
                       style="danger.TButton", 
                       width=15).pack(side=LEFT, padx=(0, 0))

        def show_edit_component_form():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a component to edit.")
                return

            try:
                selected_item = selected[0]
                comp_to_edit = None
                for comp in self.project.bom:
                    if str(comp.id) == str(selected_item):
                        comp_to_edit = comp
                        break
                if not comp_to_edit:
                    messagebox.showerror("Error", f"Component with ID {selected_item} not found.")
                    return
            except Exception as e:
                messagebox.showerror("Error", f"Error finding component: {str(e)}")
                return

            edit_window = ttk.Toplevel(self.root)
            edit_window.title("Edit Component")
            edit_window.geometry("700x900")
            edit_window.minsize(600, 700)
            edit_window.transient(self.root)
            edit_window.grab_set()
            edit_window.configure(bg=self.colors['content'])

            scrolled = ModernScrolledFrame(edit_window, autohide=True)
            scrolled.pack(fill=BOTH, expand=True)
            form_container = ttk.Frame(scrolled, padding=40, style="Content.TFrame")
            form_container.pack(fill=BOTH, expand=True)
            form_container.grid_columnconfigure(1, weight=1)

            title_frame = ttk.Frame(form_container, style="Content.TFrame")
            title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky='ew')
            ttk.Label(title_frame, 
                     text="✏️ Edit Component",
                     font=('Segoe UI', 18, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").pack(anchor='w')
            ttk.Label(title_frame, 
                     text=f"Modify component: {comp_to_edit.id}",
                     font=('Segoe UI', 11),
                     foreground=self.colors['text_light'],
                     style="Content.TLabel").pack(anchor='w', pady=(5, 0))

            basic_frame = ttk.LabelFrame(form_container, text="Basic Information", 
                                       style="Modern.TLabelframe", padding=15)
            basic_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20))
            basic_frame.grid_columnconfigure(1, weight=1)

            ttk.Label(basic_frame, 
                     text="Component ID:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=0, column=0, sticky='w', pady=10, padx=(0, 20))
            ttk.Label(basic_frame, 
                     text=str(comp_to_edit.id), 
                     font=('Segoe UI', 12),
                     foreground=self.colors['text'],
                     style="Content.TLabel").grid(row=0, column=1, sticky='w', pady=10)
            ttk.Label(basic_frame, 
                     text="Component Type:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=1, column=0, sticky='w', pady=10, padx=(0, 20))
            component_types = list(self.predefined_failure_modes.keys())
            type_combo = ttk.Combobox(basic_frame, 
                                    values=component_types, 
                                    font=('Segoe UI', 12),
                                    state="readonly")
            type_combo.set(comp_to_edit.type)
            type_combo.grid(row=1, column=1, sticky='ew', pady=10)
            ttk.Label(basic_frame, 
                     text="FIT Rate Total:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=2, column=0, sticky='w', pady=10, padx=(0, 20))
            fit_entry = ttk.Entry(basic_frame, font=('Segoe UI', 12))
            fit_entry.insert(0, str(comp_to_edit.failure_rate))
            fit_entry.grid(row=2, column=1, sticky='ew', pady=10)
            ttk.Label(basic_frame, 
                     text="Failure Modes:", 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").grid(row=3, column=0, sticky='w', pady=10, padx=(0, 20))
            ttk.Label(basic_frame, 
                     text=f"{len(comp_to_edit.failure_modes)} failure mode{'s' if len(comp_to_edit.failure_modes) != 1 else ''} defined", 
                     font=('Segoe UI', 12),
                     foreground=self.colors['text_light'],
                     style="Content.TLabel").grid(row=3, column=1, sticky='w', pady=10)

            sf_frame = ttk.LabelFrame(form_container, text="Related Safety Functions", 
                                    style="Modern.TLabelframe", padding=15)
            sf_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 20))
            sf_frame.grid_columnconfigure(0, weight=1)
            ttk.Label(sf_frame, 
                     text="Select the safety functions this component is related to:", 
                     font=('Segoe UI', 11),
                     foreground=self.colors['text'],
                     style="Content.TLabel").grid(row=0, column=0, sticky='w', pady=(0, 10))
            sf_ids = [sf.id for sf in self.project.SF_list]
            sf_listbox = tk.Listbox(sf_frame, 
                                  selectmode='multiple', 
                                  exportselection=False, 
                                  height=6, 
                                  font=('Segoe UI', 11))
            for sfid in sf_ids:
                sf_listbox.insert(END, sfid)
            for idx, sfid in enumerate(sf_ids):
                if any(sf.id == sfid for sf in comp_to_edit.related_Sfs):
                    sf_listbox.selection_set(idx)
            sf_listbox.grid(row=1, column=0, sticky='ew', pady=(0, 10))

            fm_preview_frame = ttk.LabelFrame(form_container, text="Failure Modes (auto-populate)", style="Modern.TLabelframe", padding=15)
            fm_preview_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(0, 20))
            fm_preview_frame.grid_columnconfigure(0, weight=1)
            fm_check_vars = [[]]  # mutable container for closure
            fm_checkboxes = []
            select_all_var = tk.BooleanVar(value=True)
            def update_fm_checkboxes():
                for cb in fm_checkboxes:
                    cb.destroy()
                fm_check_vars[0].clear()
                fm_checkboxes.clear()
                comp_type = type_combo.get().strip()
                try:
                    fit_rate = float(fit_entry.get())
                except ValueError:
                    fit_rate = 0
                existing_fm_descs = set(fm.description for fm in comp_to_edit.failure_modes)
                if comp_type in self.predefined_failure_modes and fit_rate > 0:
                    for i, fm_data in enumerate(self.predefined_failure_modes[comp_type]):
                        percent = fm_data["fit_rate"]
                        actual_fit = fit_rate * (percent / 100)
                        checked = fm_data["description"] in existing_fm_descs
                        var = tk.BooleanVar(value=checked)
                        cb = ttk.Checkbutton(fm_preview_frame, text=f"{fm_data['description']} ({percent}% = {actual_fit:.2f} FIT)", variable=var, style='Modern.TCheckbutton')
                        cb.pack(anchor='w', padx=10, pady=2)
                        fm_check_vars[0].append(var)
                        fm_checkboxes.append(cb)
                else:
                    lbl = ttk.Label(fm_preview_frame, text="No predefined failure modes or FIT rate not set.", font=('Segoe UI', 11))
                    lbl.pack(anchor='w', padx=10, pady=2)
                    fm_checkboxes.append(lbl)
            def on_select_all():
                for var in fm_check_vars[0]:
                    var.set(select_all_var.get())
            select_all_cb = ttk.Checkbutton(fm_preview_frame, text="Select All", variable=select_all_var, command=on_select_all, style='Modern.TCheckbutton')
            select_all_cb.pack(anchor='w', padx=5, pady=(0, 5))
            def auto_populate_failure_modes():
                update_fm_checkboxes()
            type_combo.bind('<<ComboboxSelected>>', lambda e: auto_populate_failure_modes())
            fit_entry.bind('<KeyRelease>', lambda e: auto_populate_failure_modes())
            auto_populate_failure_modes()

            def save_changes():
                try:
                    new_type = type_combo.get().strip()
                    new_fit = float(fit_entry.get())
                    selected_indices = sf_listbox.curselection()
                    selected_sf_ids = [sf_ids[i] for i in selected_indices]
                    if not new_type:
                        messagebox.showerror("Error", "Component type cannot be empty.", parent=edit_window)
                        return
                    comp_to_edit.type = new_type
                    comp_to_edit.failure_rate = new_fit
                    for sf in comp_to_edit.related_Sfs:
                        if comp_to_edit in sf.related_components:
                            sf.related_components.remove(comp_to_edit)
                    comp_to_edit.related_Sfs.clear()
                    for sfid in selected_sf_ids:
                        sf_obj = next((sf for sf in self.project.SF_list if sf.id == sfid), None)
                        if sf_obj:
                            comp_to_edit.related_Sfs.append(sf_obj)
                            if comp_to_edit not in sf_obj.related_components:
                                sf_obj.add_component(comp_to_edit)
                    comp_type = type_combo.get().strip()
                    fit_rate = float(fit_entry.get())
                    if comp_type in self.predefined_failure_modes and fit_rate > 0:
                        predefined_fms = self.predefined_failure_modes[comp_type]
                        comp_to_edit.failure_modes = [fm for fm in comp_to_edit.failure_modes if fm.description not in [fm_data["description"] for fm_data in predefined_fms]]
                        for i, fm_data in enumerate(predefined_fms):
                            if i < len(fm_check_vars[0]) and fm_check_vars[0][i].get():
                                fm = FailureMode()
                                fm.description = fm_data["description"]
                                percent = fm_data["fit_rate"]
                                fm.Failure_rate_total = fit_rate * (percent / 100)
                                fm.system_level_effect = fm_data["system_effect"]
                                fm.is_SPF = 1
                                fm.set_spf_mechanism("None", 0.0)
                                comp_to_edit.add_FM(fm)
                    related_sf_str = ", ".join(selected_sf_ids) if selected_sf_ids else "None"
                    tree.item(selected_item, values=(comp_to_edit.id, new_type, new_fit, related_sf_str, len(comp_to_edit.failure_modes)))
                    self.show_success_message("Component updated successfully!")
                    edit_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Invalid FIT rate.", parent=edit_window)
            button_frame = ttk.Frame(form_container, style="Content.TFrame")
            button_frame.grid(row=4, column=0, columnspan=2, pady=(30, 0), sticky='ew')
            HoverButton(button_frame, 
                       text="💾 Save Changes", 
                       command=save_changes, 
                       style="success.TButton", 
                       width=18).pack(side=LEFT, padx=(0, 15))
            HoverButton(button_frame, 
                       text="❌ Cancel", 
                       command=edit_window.destroy, 
                       style="danger.TButton", 
                       width=15).pack(side=LEFT, padx=(0, 0))

        def remove_component():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a component to remove.")
                return

            if not messagebox.askyesno("Confirm", "Are you sure you want to remove this component?"):
                return
            
            comp_id = int(selected[0])
            comp_to_remove = next((c for c in self.project.bom if c.id == comp_id), None)

            if comp_to_remove:
                self.project.bom.remove(comp_to_remove)
                for sf in comp_to_remove.related_Sfs:
                    sf.related_components.remove(comp_to_remove)
                
                tree.delete(selected[0])
                self.show_success_message("Component removed successfully!")

        button_frame = ttk.Frame(main_frame, style="Content.TFrame")
        button_frame.pack(fill=X, pady=20, padx=20)
        
        add_btn = ttk.Button(button_frame, text="➕ Add Component",
                           command=show_add_component_form, style='success.TButton')
        add_btn.pack(side=LEFT, padx=10)
        
        edit_btn = ttk.Button(button_frame, text="✏️ Edit Component",
                            command=show_edit_component_form, style='warning.TButton')
        edit_btn.pack(side=LEFT, padx=10)
        
        remove_btn = ttk.Button(button_frame, text="❌ Remove Component",
                              command=remove_component, style='danger.TButton')
        remove_btn.pack(side=LEFT, padx=10)
        
        fm_btn = ttk.Button(button_frame, text="🔍 Component Failure Modes", 
                          command=lambda: self.show_failure_modes_page(selected_component_id=tree.selection()[0] if tree.selection() else None), style='info.TButton')
        fm_btn.pack(side=LEFT, padx=10)

        import_btn = ttk.Button(button_frame, text="📥 Import BOM",
                              command=self.import_bom,
                              style='info.TButton')
        import_btn.pack(side=LEFT, padx=10)

    def import_bom(self):
        from tkinter import filedialog
        import pandas as pd
        file_path = filedialog.askopenfilename(
            title='Import BOM CSV',
            filetypes=[('CSV Files', '*.csv')]
        )
        if not file_path:
            return
        try:
            df = pd.read_csv(file_path)
            required_cols = {'id', 'type', 'failure_rate'}
            if not required_cols.issubset(df.columns):
                messagebox.showerror("Error", f"CSV must contain columns: {', '.join(required_cols)}")
                return
            for _, row in df.iterrows():
                comp_id = str(row['id']).strip()
                if any(str(c.id) == comp_id for c in self.project.bom):
                    continue  # Skip duplicates
                comp = Component(comp_id)
                comp.type = str(row['type']).strip()
                try:
                    comp.failure_rate = float(row['failure_rate'])
                except Exception:
                    comp.failure_rate = 0
                if 'related_sf_ids' in row and pd.notna(row['related_sf_ids']):
                    sf_ids = [s.strip() for s in str(row['related_sf_ids']).split(',') if s.strip()]
                    for sfid in sf_ids:
                        sf_obj = next((sf for sf in self.project.SF_list if str(sf.id) == sfid), None)
                        if sf_obj:
                            comp.related_Sfs.append(sf_obj)
                            sf_obj.add_component(comp)
                self.project.bom.append(comp)
            self.show_success_message("BOM imported successfully!")
            self.show_components()  # Refresh table
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import BOM: {e}")

    def show_failure_modes_page(self, selected_component_id=None):
        fm_window = ttk.Toplevel(self.root)
        fm_window.title("Component Failure Modes")
        fm_window.geometry("1200x800")
        fm_window.transient(self.root)
        fm_window.grab_set()
        
        main_frame = ttk.LabelFrame(fm_window, 
                                  text="🔍 Component Failure Modes", 
                                  style="Modern.TLabelframe")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=BOTH, expand=True, pady=10)
        
        columns = ("Failure Mode", "Description", "FIT Rate", "System Level Effect",
                  "Is SPF?", "SPF Safety Mechanism", "SPF DC%",
                  "Is MPF?", "MPF Safety Mechanism", "MPF DC%")
        
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                          style="Modern.Treeview", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.fm_data = []
        
        if selected_component_id is not None:
            try:
                comp = next(c for c in self.project.bom if str(c.id) == str(selected_component_id))
                comps = [comp]
            except StopIteration:
                comps = []
        else:
            comps = self.project.bom
        for comp in comps:
            for fm in comp.failure_modes:
                item = tree.insert("", END, values=(
                    f"FM-{comp.id}-{len(comp.failure_modes)}",
                    fm.description,
                    f"{fm.Failure_rate_total:.2f}",
                    fm.system_level_effect,
                    "Yes" if fm.is_SPF else "No",
                    fm.SPF_safety_mechanism,
                    f"{fm.SPF_diagnostic_coverage:.1f}%" if fm.is_SPF else "N/A",
                    "Yes" if fm.is_MPF else "No",
                    fm.MPF_safety_mechanism,
                    f"{fm.MPF_diagnostic_coverage:.1f}%" if fm.is_MPF else "N/A"
                ))
                self.fm_data.append((item, comp, fm))
        
        def on_fm_double_click(event):
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                show_edit_fm_form()
        tree.bind('<Double-1>', on_fm_double_click)
        
        def show_add_fm_form():
            add_window = ttk.Toplevel(fm_window)
            add_window.title("Add Failure Mode")
            add_window.geometry("900x700")
            add_window.minsize(800, 600)
            add_window.transient(fm_window)
            add_window.grab_set()
            add_window.configure(bg=self.colors['content'])
            
            scrolled = ModernScrolledFrame(add_window, autohide=True)
            scrolled.pack(fill=BOTH, expand=True)
            form = ttk.Frame(scrolled, style="Content.TFrame", padding=30)
            form.pack(fill=BOTH, expand=True)
            
            title_frame = ttk.Frame(form, style="Content.TFrame")
            title_frame.pack(fill=X, pady=(0, 20))
            ttk.Label(title_frame, 
                     text="➕ Add New Failure Mode",
                     font=('Segoe UI', 16, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").pack(anchor='w')
            
            comp_frame = ttk.LabelFrame(form, text="Component Selection", 
                                      style="Modern.TLabelframe", padding=15)
            comp_frame.pack(fill=X, pady=(0, 20))
            
            ttk.Label(comp_frame, 
                     text="Select Component:", 
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w', pady=(0, 5))
            comp_combo = ttk.Combobox(comp_frame, 
                                    values=[f"{c.id} - {c.type}" for c in self.project.bom],
                                    font=('Segoe UI', 11))
            comp_combo.pack(fill=X, pady=(0, 5))
            if selected_component_id is not None:
                comp_ids = [str(c.id) for c in self.project.bom]
                try:
                    idx = comp_ids.index(str(selected_component_id))
                    comp_combo.current(idx)
                    comp_combo.configure(state="disabled")
                except ValueError:
                    pass
            
            basic_frame = ttk.LabelFrame(form, text="Basic Information", 
                                       style="Modern.TLabelframe", padding=15)
            basic_frame.pack(fill=X, pady=(0, 20))
            
            ttk.Label(basic_frame, 
                     text="Description:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            desc_entry = ttk.Entry(basic_frame, font=('Segoe UI', 11))
            desc_entry.pack(fill=X, pady=(0, 15))
            
            ttk.Label(basic_frame, 
                     text="FIT Rate:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            fit_entry = ttk.Entry(basic_frame, font=('Segoe UI', 11))
            fit_entry.pack(fill=X, pady=(0, 15))
            
            ttk.Label(basic_frame, 
                     text="System Level Effect:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            effect_entry = ttk.Entry(basic_frame, font=('Segoe UI', 11))
            effect_entry.pack(fill=X, pady=(0, 15))
            
            spf_frame = ttk.LabelFrame(form, text="SPF Details", 
                                     style="Modern.TLabelframe", padding=15)
            spf_frame.pack(fill=X, pady=(0, 20))
            
            is_spf_var = tk.BooleanVar()
            ttk.Checkbutton(spf_frame, 
                          text="Is SPF?",
                          variable=is_spf_var,
                          style='Modern.TCheckbutton').pack(anchor='w', pady=(0, 10))
            
            ttk.Label(spf_frame, 
                     text="SPF Safety Mechanism:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            spf_mech_entry = ttk.Entry(spf_frame, font=('Segoe UI', 11))
            spf_mech_entry.pack(fill=X, pady=(0, 15))
            
            ttk.Label(spf_frame, 
                     text="SPF DC (%):",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            spf_dc_entry = ttk.Entry(spf_frame, font=('Segoe UI', 11))
            spf_dc_entry.pack(fill=X, pady=(0, 15))
            
            mpf_frame = ttk.LabelFrame(form, text="MPF Details", 
                                     style="Modern.TLabelframe", padding=15)
            mpf_frame.pack(fill=X, pady=(0, 20))
            
            is_mpf_var = tk.BooleanVar()
            ttk.Checkbutton(mpf_frame, 
                          text="Is MPF?",
                          variable=is_mpf_var,
                          style='Modern.TCheckbutton').pack(anchor='w', pady=(0, 10))
            
            ttk.Label(mpf_frame, 
                     text="MPF Safety Mechanism:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            mpf_mech_entry = ttk.Entry(mpf_frame, font=('Segoe UI', 11))
            mpf_mech_entry.pack(fill=X, pady=(0, 15))
            
            ttk.Label(mpf_frame, 
                     text="MPF DC (%):",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            mpf_dc_entry = ttk.Entry(mpf_frame, font=('Segoe UI', 11))
            mpf_dc_entry.pack(fill=X, pady=(0, 15))
            
            def save_failure_mode():
                try:
                    comp_id = self._normalize_id(comp_combo.get().split(' - ')[0])
                    component = next(c for c in self.project.bom if self._normalize_id(c.id) == comp_id)
                    
                    new_description = desc_entry.get().strip()
                    if not new_description:
                        messagebox.showerror("Error", "Description cannot be empty.")
                        return

                    for existing_fm in component.failure_modes:
                        if existing_fm.description == new_description:
                            messagebox.showerror("Error", f"Failure mode with description '{new_description}' already exists for this component.")
                            return

                    fm = FailureMode()
                    fm.description = new_description
                    fm.Failure_rate_total = float(fit_entry.get())
                    fm.system_level_effect = effect_entry.get()
                    fm.is_SPF = 1 if is_spf_var.get() else 0
                    fm.is_MPF = 1 if is_mpf_var.get() else 0
                    
                    if fm.is_SPF:
                        fm.set_spf_mechanism(spf_mech_entry.get(), float(spf_dc_entry.get()))
                    
                    if fm.is_MPF:
                        fm.set_mpf_mechanism(mpf_mech_entry.get(), float(mpf_dc_entry.get()))
                    
                    component.add_FM(fm)
                    
                    item = tree.insert("", END, values=(
                        f"FM-{component.id}-{len(component.failure_modes)}",
                        fm.description,
                        f"{fm.Failure_rate_total:.2f}",
                        fm.system_level_effect,
                        "Yes" if fm.is_SPF else "No",
                        fm.SPF_safety_mechanism,
                        f"{fm.SPF_diagnostic_coverage:.1f}%" if fm.is_SPF else "N/A",
                        "Yes" if fm.is_MPF else "No",
                        fm.MPF_safety_mechanism,
                        f"{fm.MPF_diagnostic_coverage:.1f}%" if fm.is_MPF else "N/A"
                    ))
                    self.fm_data.append((item, component, fm))
                    
                    self.show_success_message("Failure Mode added successfully")
                    add_window.destroy()
                    
                except (ValueError, IndexError) as e:
                    messagebox.showerror("Error", "Please fill all fields with valid values")
            
            button_container = ttk.Frame(add_window, style="Content.TFrame")
            button_container.pack(side=BOTTOM, fill=X, padx=30, pady=20)
            
            ttk.Button(button_container, 
                      text="💾 Save",
                      command=save_failure_mode,
                      style='success.TButton',
                      width=15).pack(side=LEFT, padx=5)
            
            ttk.Button(button_container, 
                      text="❌ Cancel",
                      command=add_window.destroy,
                      style='danger.TButton',
                      width=15).pack(side=LEFT, padx=5)
        
        def show_edit_fm_form():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a failure mode to edit")
                return
            
            item = selected[0]
            item_data = next((data for data in self.fm_data if data[0] == item), None)
            if not item_data:
                return
            
            _, component, fm = item_data
            
            edit_window = ttk.Toplevel(fm_window)
            edit_window.title("Edit Failure Mode")
            edit_window.geometry("900x700")
            edit_window.minsize(800, 600)
            edit_window.transient(fm_window)
            edit_window.grab_set()
            edit_window.configure(bg=self.colors['content'])
            
            scrolled = ModernScrolledFrame(edit_window, autohide=True)
            scrolled.pack(fill=BOTH, expand=True)
            form = ttk.Frame(scrolled, style="Content.TFrame", padding=30)
            form.pack(fill=BOTH, expand=True)
            
            title_frame = ttk.Frame(form, style="Content.TFrame")
            title_frame.pack(fill=X, pady=(0, 20))
            ttk.Label(title_frame, 
                     text="✏️ Edit Failure Mode",
                     font=('Segoe UI', 16, 'bold'),
                     foreground=self.colors['primary'],
                     style="Content.TLabel").pack(anchor='w')
            
            comp_frame = ttk.LabelFrame(form, text="Component Information", 
                                      style="Modern.TLabelframe", padding=15)
            comp_frame.pack(fill=X, pady=(0, 20))
            
            ttk.Label(comp_frame, 
                     text=f"Component: {component.id} - {component.type}",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            
            basic_frame = ttk.LabelFrame(form, text="Basic Information", 
                                       style="Modern.TLabelframe", padding=15)
            basic_frame.pack(fill=X, pady=(0, 20))
            
            ttk.Label(basic_frame, 
                     text="Description:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            desc_entry = ttk.Entry(basic_frame, font=('Segoe UI', 11))
            desc_entry.pack(fill=X, pady=(0, 15))
            
            ttk.Label(basic_frame, 
                     text="FIT Rate:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            fit_entry = ttk.Entry(basic_frame, font=('Segoe UI', 11))
            fit_entry.pack(fill=X, pady=(0, 15))
            
            ttk.Label(basic_frame, 
                     text="System Level Effect:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            effect_entry = ttk.Entry(basic_frame, font=('Segoe UI', 11))
            effect_entry.pack(fill=X, pady=(0, 15))
            
            spf_frame = ttk.LabelFrame(form, text="SPF Details", 
                                     style="Modern.TLabelframe", padding=15)
            spf_frame.pack(fill=X, pady=(0, 20))
            
            is_spf_var = tk.BooleanVar(value=bool(fm.is_SPF))
            ttk.Checkbutton(spf_frame, 
                          text="Is SPF?",
                          variable=is_spf_var,
                          style='Modern.TCheckbutton').pack(anchor='w', pady=(0, 10))
            
            ttk.Label(spf_frame, 
                     text="SPF Safety Mechanism:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            spf_mech_entry = ttk.Entry(spf_frame, font=('Segoe UI', 11))
            spf_mech_entry.pack(fill=X, pady=(0, 15))
            
            ttk.Label(spf_frame, 
                     text="SPF DC (%):",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            spf_dc_entry = ttk.Entry(spf_frame, font=('Segoe UI', 11))
            spf_dc_entry.pack(fill=X, pady=(0, 15))
            
            mpf_frame = ttk.LabelFrame(form, text="MPF Details", 
                                     style="Modern.TLabelframe", padding=15)
            mpf_frame.pack(fill=X, pady=(0, 20))
            
            is_mpf_var = tk.BooleanVar(value=bool(fm.is_MPF))
            ttk.Checkbutton(mpf_frame, 
                          text="Is MPF?",
                          variable=is_mpf_var,
                          style='Modern.TCheckbutton').pack(anchor='w', pady=(0, 10))
            
            ttk.Label(mpf_frame, 
                     text="MPF Safety Mechanism:",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            mpf_mech_entry = ttk.Entry(mpf_frame, font=('Segoe UI', 11))
            mpf_mech_entry.pack(fill=X, pady=(0, 15))
            
            ttk.Label(mpf_frame, 
                     text="MPF DC (%):",
                     font=('Segoe UI', 11, 'bold'),
                     foreground=self.colors['primary']).pack(anchor='w')
            mpf_dc_entry = ttk.Entry(mpf_frame, font=('Segoe UI', 11))
            mpf_dc_entry.pack(fill=X, pady=(0, 15))
            
            def save_changes():
                try:
                    fm.description = desc_entry.get()
                    fm.Failure_rate_total = float(fit_entry.get())
                    fm.system_level_effect = effect_entry.get()
                    fm.is_SPF = 1 if is_spf_var.get() else 0
                    fm.is_MPF = 1 if is_mpf_var.get() else 0
                    
                    if fm.is_SPF:
                        fm.set_spf_mechanism(spf_mech_entry.get(), float(spf_dc_entry.get()))
                    else:
                        fm.SPF_safety_mechanism = "none"
                        fm.SPF_diagnostic_coverage = 0
                    
                    if fm.is_MPF:
                        fm.set_mpf_mechanism(mpf_mech_entry.get(), float(mpf_dc_entry.get()))
                    else:
                        fm.MPF_safety_mechanism = "none"
                        fm.MPF_diagnostic_coverage = 0
                    
                    tree.item(item, values=(
                        f"FM-{component.id}-{len(component.failure_modes)}",
                        fm.description,
                        f"{fm.Failure_rate_total:.2f}",
                        fm.system_level_effect,
                        "Yes" if fm.is_SPF else "No",
                        fm.SPF_safety_mechanism,
                        f"{fm.SPF_diagnostic_coverage:.1f}%" if fm.is_SPF else "N/A",
                        "Yes" if fm.is_MPF else "No",
                        fm.MPF_safety_mechanism,
                        f"{fm.MPF_diagnostic_coverage:.1f}%" if fm.is_MPF else "N/A"
                    ))
                    
                    self.show_success_message("Failure Mode updated successfully")
                    edit_window.destroy()
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numeric values")
            
            button_container = ttk.Frame(edit_window, style="Content.TFrame")
            button_container.pack(side=BOTTOM, fill=X, padx=30, pady=20)
            
            ttk.Button(button_container, 
                      text="💾 Save Changes",
                      command=save_changes,
                      style='success.TButton',
                      width=15).pack(side=LEFT, padx=5)
            
            ttk.Button(button_container, 
                      text="❌ Cancel",
                      command=edit_window.destroy,
                      style='danger.TButton',
                      width=15).pack(side=LEFT, padx=5)
            
        def remove_failure_mode():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a failure mode to remove")
                return

            if not messagebox.askyesno("Confirm", "Are you sure you want to remove this failure mode?"):
                return
            
            item = selected[0]
            item_data = next((data for data in self.fm_data if data[0] == item), None)
            
            if not item_data:
                return
                
            _, component, fm = item_data
            
            component.failure_modes.remove(fm)
            
            self.fm_data.remove(item_data)
            
            tree.delete(item)
            
            self.show_success_message("Failure Mode removed successfully")

        button_frame = ttk.Frame(main_frame, style="Content.TFrame")
        button_frame.pack(fill=X, pady=20)
        
        edit_btn = ttk.Button(button_frame, 
                            text="✏️ Edit FM",
                            command=show_edit_fm_form,
                            style='warning.TButton',
                            width=15)
        edit_btn.pack(side=LEFT, padx=10)
        
        add_btn = ttk.Button(button_frame, 
                           text="➕ Add FM",
                           command=show_add_fm_form,
                           style='success.TButton',
                           width=15)
        add_btn.pack(side=LEFT, padx=10)
        
        remove_btn = ttk.Button(button_frame, 
                              text="❌ Remove FM",
                              command=remove_failure_mode,
                              style='danger.TButton',
                              width=15)
        remove_btn.pack(side=LEFT, padx=10)
        
        ok_btn = ttk.Button(button_frame, 
                          text="✅ OK",
                          command=fm_window.destroy,
                          style='info.TButton',
                          width=15)
        ok_btn.pack(side=LEFT, padx=10)

    def show_fmeda(self):
        self.clear_content()
        self.update_breadcrumb("FMEDA Analysis")
        self.update_active_nav("fmeda")

        frame = ttk.LabelFrame(self.content_frame, text="📊 FMEDA Analysis",
                               style="Modern.TLabelframe")
        frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        if not self.lifetime:
            ttk.Label(frame, text="⚠ Please set lifetime in Analysis Assumptions first",
                      font=('Segoe UI', 11), foreground="red").pack(pady=20)
            return

        self.project.evaluate_metrics(self.lifetime)

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill=BOTH, expand=True)

        columns = ("SF-ID", "RF (FIT)", "MPFL (FIT)", "MPFD (FIT)",
                   "MPHF", "SPFM (%)", "LFM (%)")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Modern.Treeview", height=10)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for sf in self.project.SF_list:
            mphf_val = sf.MPHF
            if mphf_val == 0:
                mphf_str = "0.000000"
            elif abs(mphf_val) < 0.0001:  # Use scientific notation for small numbers
                parts = f"{mphf_val:.2e}".split('e')
                mantissa = parts[0]
                exponent = int(parts[1])
                mphf_str = f"{mantissa}*10^{exponent}"
            else:
                mphf_str = f"{mphf_val:.6f}"

            tree.insert("", END, values=(
                sf.id, f"{sf.RF:.2f}", f"{sf.MPFL:.2f}", f"{sf.MPFD:.2f}",
                mphf_str, f"{sf.SPFM*100:.2f}", f"{sf.LFM*100:.2f}"
            ))

    def show_results(self):
        self.clear_content()
        self.update_breadcrumb("Results")
        self.update_active_nav("results")

        frame = ttk.LabelFrame(self.content_frame, text="📈 Analysis Results",
                               style="Modern.TLabelframe")
        frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        if not self.lifetime:
            ttk.Label(frame, text="⚠ Please set lifetime in Analysis Assumptions first",
                      font=('Segoe UI', 11), foreground="red").pack(pady=20)
            return

        summary_frame = ttk.LabelFrame(frame, text="📌 Summary", style="Modern.TLabelframe")
        summary_frame.pack(fill=X, padx=10, pady=10)

        grid_frame = ttk.Frame(summary_frame)
        grid_frame.pack(fill=X, padx=20, pady=10)

        metrics = [
            ("Total Components:", len(self.project.bom)),
            ("Total Safety Functions:", len(self.project.SF_list)),
            ("Total Failure Modes:", sum(len(c.failure_modes) for c in self.project.bom)),
            ("Lifetime (hours):", self.lifetime)
        ]

        for i, (label, value) in enumerate(metrics):
            ttk.Label(grid_frame, text=label, font=('Segoe UI', 10, 'bold')).grid(row=i, column=0, sticky='w', pady=5)
            ttk.Label(grid_frame, text=str(value), font=('Segoe UI', 10)).grid(row=i, column=1, sticky='w', padx=10)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def save_project(self):
        save_dialog = ttk.Toplevel(self.root)
        save_dialog.title("Save Project")
        save_dialog.geometry("700x600")
        save_dialog.minsize(450, 350)
        save_dialog.transient(self.root)
        save_dialog.grab_set()
        save_dialog.configure(bg=self.colors['content'])

        scrolled = ModernScrolledFrame(save_dialog, autohide=True)
        scrolled.pack(fill=BOTH, expand=True)
        main_frame = ttk.Frame(scrolled, padding=30, style="Content.TFrame")
        main_frame.pack(fill=BOTH, expand=True)

        title_frame = ttk.Frame(main_frame, style="Content.TFrame")
        title_frame.pack(fill=X, pady=(0, 25))
        
        ttk.Label(title_frame, 
                 text="💾 Save Project",
                 font=('Segoe UI', 18, 'bold'),
                 foreground=self.colors['primary'],
                 style="Content.TLabel").pack(anchor='w')
        
        ttk.Label(title_frame, 
                 text="Save your FMEDA project to a CSV file",
                 font=('Segoe UI', 11),
                 foreground=self.colors['text_light'],
                 style="Content.TLabel").pack(anchor='w', pady=(5, 0))

        info_frame = ttk.LabelFrame(main_frame, text="Project Information", 
                                  style="Modern.TLabelframe", padding=20)
        info_frame.pack(fill=X, pady=(0, 25))

        ttk.Label(info_frame, 
                 text="Project Name:", 
                 font=('Segoe UI', 12, 'bold'),
                 foreground=self.colors['primary'],
                 style="Content.TLabel").pack(anchor='w', pady=(0, 8))
        
        project_name_entry = ttk.Entry(info_frame, font=('Segoe UI', 12))
        project_name_entry.insert(0, self.project.name)
        project_name_entry.pack(fill=X, pady=(0, 15))

        summary_frame = ttk.Frame(info_frame, style="Content.TFrame")
        summary_frame.pack(fill=X)
        
        metrics = [
            ("Components:", len(self.project.bom)),
            ("Safety Functions:", len(self.project.SF_list)),
            ("Failure Modes:", sum(len(c.failure_modes) for c in self.project.bom)),
            ("Lifetime:", f"{self.lifetime} hours")
        ]

        for i, (label, value) in enumerate(metrics):
            row_frame = ttk.Frame(summary_frame, style="Content.TFrame")
            row_frame.pack(fill=X, pady=2)
            
            ttk.Label(row_frame, 
                     text=label, 
                     font=('Segoe UI', 10, 'bold'),
                     foreground=self.colors['text'],
                     style="Content.TLabel").pack(side=LEFT)
            
            ttk.Label(row_frame, 
                     text=str(value), 
                     font=('Segoe UI', 10),
                     foreground=self.colors['text_light'],
                     style="Content.TLabel").pack(side=RIGHT)

        def execute_save():
            project_name = project_name_entry.get().strip()
            if not project_name:
                messagebox.showwarning("Warning", "Project name cannot be empty.", parent=save_dialog)
                return
            save_dialog.destroy()
            self._execute_save_logic_single_csv(project_name)

        button_frame = ttk.Frame(main_frame, style="Content.TFrame")
        button_frame.pack(fill=X, pady=(20, 0))
        
        HoverButton(button_frame, 
                   text="💾 Save Project", 
                   command=execute_save, 
                   style="success.TButton", 
                   width=18).pack(side=LEFT, padx=(0, 15))
        
        HoverButton(button_frame, 
                   text="❌ Cancel", 
                   command=save_dialog.destroy, 
                   style="danger.TButton", 
                   width=15).pack(side=LEFT, padx=(0, 0))

    def _execute_save_logic_single_csv(self, project_name):
        from tkinter import filedialog
        self.project.name = project_name
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV Files', '*.csv')],
            initialfile=project_name + '.csv',
            title='Save FMEDA Project As...')
        if not file_path:
            return
        try:
            rows = []
            rows.append({'section': 'project', 'name': self.project.name, 'lifetime': self.project.lifetime})
            for sf in self.project.SF_list:
                rows.append({'section': 'sf', 'id': sf.id, 'description': sf.description, 'target_integrity_level': sf.target_integrity_level})
            for comp in self.project.bom:
                rows.append({'section': 'component', 'id': comp.id, 'type': comp.type, 'failure_rate': comp.failure_rate, 'related_sf_ids': ",".join([sf.id for sf in comp.related_Sfs])})
            for comp in self.project.bom:
                for fm in comp.failure_modes:
                    rows.append({'section': 'fm', 'component_id': comp.id, 'description': fm.description, 'Failure_rate_total': fm.Failure_rate_total, 'system_level_effect': fm.system_level_effect, 'is_SPF': fm.is_SPF, 'SPF_safety_mechanism': fm.SPF_safety_mechanism, 'SPF_diagnostic_coverage': fm.SPF_diagnostic_coverage, 'is_MPF': fm.is_MPF, 'MPF_safety_mechanism': fm.MPF_safety_mechanism, 'MPF_diagnostic_coverage': fm.MPF_diagnostic_coverage})
            df = pd.DataFrame(rows)
            df.to_csv(file_path, index=False)
            self.show_success_message(f"Project '{project_name}' saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save project: {e}")

    def import_project(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title='Open FMEDA Project',
            filetypes=[('CSV Files', '*.csv')]
        )
        if not file_path:
            return
        self._load_project_from_single_csv(file_path)

    def _load_project_from_single_csv(self, file_path):
        try:
            df = pd.read_csv(file_path, dtype=str)  # Force all columns to string
            new_project = Project("Loaded Project")
            project_row = df[df['section'] == 'project'].iloc[0]
            new_project.name = project_row['name']
            new_project.lifetime = float(project_row['lifetime']) if pd.notna(project_row['lifetime']) else 0
            self.lifetime = new_project.lifetime
            sf_map = {}
            for _, row in df[df['section'] == 'sf'].iterrows():
                sf_id = self._normalize_id(row['id'])
                sf = SafetyFunction(sf_id)
                sf.description = row['description'] if pd.notna(row['description']) else ''
                sf.target_integrity_level = row['target_integrity_level'] if pd.notna(row['target_integrity_level']) else ''
                new_project.add_SF(sf)
                sf_map[sf.id] = sf
            comp_map = {}
            for _, row in df[df['section'] == 'component'].iterrows():
                comp_id = self._normalize_id(row['id'])
                comp = Component(comp_id)
                comp.type = row['type'] if pd.notna(row['type']) else ''
                comp.failure_rate = float(row['failure_rate']) if pd.notna(row['failure_rate']) else 0
                comp_map[comp.id] = comp
                new_project.bom.append(comp)
            for _, row in df[df['section'] == 'fm'].iterrows():
                comp_id = self._normalize_id(row['component_id'])
                if comp_id in comp_map:
                    comp = comp_map[comp_id]
                    fm = FailureMode()
                    fm.description = row['description'] if pd.notna(row['description']) else ''
                    fm.Failure_rate_total = float(row['Failure_rate_total']) if pd.notna(row['Failure_rate_total']) else 0
                    fm.system_level_effect = row['system_level_effect'] if pd.notna(row['system_level_effect']) else ''
                    fm.is_SPF = int(float(row['is_SPF'])) if pd.notna(row['is_SPF']) else 0
                    fm.is_MPF = int(float(row['is_MPF'])) if pd.notna(row['is_MPF']) else 0
                    fm.set_spf_mechanism(row['SPF_safety_mechanism'] if pd.notna(row['SPF_safety_mechanism']) else '', float(row['SPF_diagnostic_coverage']) if pd.notna(row['SPF_diagnostic_coverage']) else 0)
                    fm.set_mpf_mechanism(row['MPF_safety_mechanism'] if pd.notna(row['MPF_safety_mechanism']) else '', float(row['MPF_diagnostic_coverage']) if pd.notna(row['MPF_diagnostic_coverage']) else 0)
                    comp.add_FM(fm)
            for sf in new_project.SF_list:
                sf.related_components = []
            for comp in new_project.bom:
                comp.related_Sfs = []
            for _, row in df[df['section'] == 'component'].iterrows():
                comp_id = self._normalize_id(row['id'])
                comp = comp_map[comp_id]
                if pd.notna(row['related_sf_ids']):
                    sf_ids = [self._normalize_id(s) for s in str(row['related_sf_ids']).split(',') if self._normalize_id(s)]
                    for sf_id in sf_ids:
                        if sf_id in sf_map:
                            sf = sf_map[sf_id]
                            if comp not in sf.related_components:
                                sf.related_components.append(comp)
                            if sf not in comp.related_Sfs:
                                comp.related_Sfs.append(sf)
            self.project = new_project
            self.project.evaluate_metrics(self.lifetime)
            self.enable_all_navigation()
            self.refresh_all_views()
            self.show_success_message("Project imported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import project: {e}")

    def refresh_all_views(self):
        self.title_label.config(text=self.project.name)
        self.show_assumptions()

    def show_help_page(self):
        help_window = ttk.Toplevel(self.root)
        help_window.title("FMEDA Tool - Help & Information")
        help_window.geometry("900x700")
        help_window.transient(self.root)
        help_window.configure(bg=self.colors['content'])

        scroll_frame = ModernScrolledFrame(help_window, autohide=True)
        scroll_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        content = ttk.Frame(scroll_frame, style="Content.TFrame", padding=30)
        content.pack(fill=X, expand=True)

        def add_heading(parent, text):
            ttk.Label(parent, text=text, style="SectionTitle.TLabel").pack(anchor='w', pady=(20, 10))

        def add_text(parent, text, is_bold=False):
            font = ('Segoe UI', 10, 'bold' if is_bold else 'normal')
            label = ttk.Label(parent, text=text, wraplength=750, justify=LEFT, font=font, style="Content.TLabel")
            label.pack(anchor='w', pady=2)

        add_heading(content, "How to Use the FMEDA Tool")
        add_text(content, 
            "This tool guides you through the process of a Failure Modes, Effects, and Diagnostics Analysis (FMEDA). "
            "The intended workflow is to follow the sections in the sidebar from top to bottom:")
        add_text(content, "1. Analysis Assumptions: Start by defining the project's lifetime in hours.")
        add_text(content, "2. Safety Functions: Define the safety functions of your system.")
        add_text(content, "3. Components: Add all hardware components and link them to the relevant safety functions.")
        add_text(content, "4. Failure Modes: For each component, define its failure modes, their FIT rates, and how they are handled by safety mechanisms.")
        add_text(content, "5. FMEDA Analysis: The tool calculates key safety metrics based on your inputs.")
        add_text(content, "6. Results: View a summary of the analysis.")

        add_heading(content, "FMEDA Metrics Explained")
        add_text(content, "The following metrics are calculated for each Safety Function:", True)
        
        add_text(content, "\nSPFM (Single-Point Fault Metric)", True)
        add_text(content, 
            "Indicates the system's robustness against single faults that can directly violate a safety goal. It is calculated as: "
            "1 - (Σλ_SPF + Σλ_RF) / Σλ_total. A higher percentage is better.")

        add_text(content, "\nLFM (Latent Fault Metric)", True)
        add_text(content,
            "Indicates the system's robustness against latent multi-point faults that could remain undetected. It is calculated as: "
            "1 - Σλ_MPF,L / (Σλ_total - (Σλ_SPF + Σλ_RF)). A higher percentage is better.")

        add_text(content, "\nMPHF (Probabilistic Metric for Hardware Failure)", True)
        add_text(content,
            "Represents the overall failure rate of the safety function, considering residual faults and latent multi-point faults. This value should be below the target defined by the ASIL level.")

        add_text(content, "\nRF (Residual Fault)", True)
        add_text(content, "The portion of a single-point fault's failure rate that is not covered by any safety mechanism.")

        add_text(content, "\nMPFL (Multiple-Point Fault, Latent)", True)
        add_text(content, "The portion of a multi-point fault's failure rate that is not detected by a safety mechanism and is not perceived by the driver.")
        
        add_text(content, "\nMPFD (Multiple-Point Fault, Detected)", True)
        add_text(content, "The portion of a multi-point fault's failure rate that is detected by a safety mechanism.")

    def show_home_screen(self):
        self.clear_content()
        self.update_breadcrumb("Home")
        self.update_active_nav("home")
        
        welcome_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        welcome_frame.pack(fill=BOTH, expand=True, padx=40, pady=40)
        
        header_frame = ttk.Frame(welcome_frame, style="Content.TFrame")
        header_frame.pack(fill=X, pady=(0, 40))
        
        ttk.Label(header_frame, 
                 text="Welcome to FMEDA Analysis Tool", 
                 font=('Segoe UI', 28, 'bold'),
                 foreground=self.colors['primary'],
                 style="Content.TLabel").pack(anchor='center')
        
        ttk.Label(header_frame, 
                 text="Professional Edition", 
                 font=('Segoe UI', 16),
                 foreground=self.colors['text_light'],
                 style="Content.TLabel").pack(anchor='center', pady=(5, 0))
        
        desc_frame = ttk.Frame(welcome_frame, style="Content.TFrame")
        desc_frame.pack(fill=X, pady=(0, 50))
        
        ttk.Label(desc_frame, 
                 text="Failure Modes, Effects, and Diagnostics Analysis Tool", 
                 font=('Segoe UI', 14),
                 foreground=self.colors['text'],
                 style="Content.TLabel").pack(anchor='center')
        
        ttk.Label(desc_frame, 
                 text="Create, manage, and analyze safety functions, components, and failure modes", 
                 font=('Segoe UI', 12),
                 foreground=self.colors['text_light'],
                 style="Content.TLabel").pack(anchor='center', pady=(10, 0))
        
        actions_frame = ttk.Frame(welcome_frame, style="Content.TFrame")
        actions_frame.pack(fill=X, pady=(0, 40))
        
        buttons_frame = ttk.Frame(actions_frame, style="Content.TFrame")
        buttons_frame.pack(anchor='center')
        
        new_project_frame = ttk.Frame(buttons_frame, style="Content.TFrame")
        new_project_frame.pack(side=LEFT, padx=20)
        
        new_btn = HoverButton(new_project_frame, 
                            text="🆕 New Project", 
                            command=self.start_new_project,
                            style='success.TButton',
                            width=20)
        new_btn.pack(pady=10)
        
        ttk.Label(new_project_frame, 
                 text="Start a fresh FMEDA analysis", 
                 font=('Segoe UI', 10),
                 foreground=self.colors['text_light'],
                 style="Content.TLabel").pack()
        
        load_project_frame = ttk.Frame(buttons_frame, style="Content.TFrame")
        load_project_frame.pack(side=LEFT, padx=20)
        
        load_btn = HoverButton(load_project_frame, 
                             text="📂 Load Project", 
                             command=self.import_project,
                             style='info.TButton',
                             width=20)
        load_btn.pack(pady=10)
        
        ttk.Label(load_project_frame, 
                 text="Open an existing project", 
                 font=('Segoe UI', 10),
                 foreground=self.colors['text_light'],
                 style="Content.TLabel").pack()
        
        guide_frame = ttk.LabelFrame(welcome_frame, 
                                   text="🚀 Quick Start Guide", 
                                   style="Modern.TLabelframe")
        guide_frame.pack(fill=X, pady=(20, 0))
        
        steps = [
            "1. Set the system lifetime in Analysis Assumptions",
            "2. Define your Safety Functions and their target integrity levels", 
            "3. Add Components and link them to Safety Functions",
            "4. Define Failure Modes for each component",
            "5. Run FMEDA Analysis to calculate safety metrics",
            "6. Review Results and export your findings"
        ]
        
        for step in steps:
            ttk.Label(guide_frame, 
                     text=step, 
                     font=('Segoe UI', 11),
                     foreground=self.colors['text'],
                     style="Content.TLabel").pack(anchor='w', padx=20, pady=5)
    
    def start_new_project(self):
        self.project = Project("FMEDA Project")
        self.lifetime = 0
        self.enable_all_navigation()
        self.show_assumptions()

    def _normalize_id(self, idval):
        s = str(idval).strip() if idval is not None and str(idval).strip() != '' else ''
        if s.endswith('.0'):
            s = s[:-2]
        return s

    def enable_all_navigation(self):
        for key, btn in self.nav_buttons.items():
            btn.configure(state='normal')
            if key == self.current_page:
                btn.configure(style='Sidebar.Active.TButton')
            else:
                btn.configure(style='Sidebar.TButton')

    def disable_all_navigation_except_home(self):
        for key, btn in self.nav_buttons.items():
            if key == 'home':
                btn.configure(state='normal')
            else:
                btn.configure(state='disabled')

class HoverButton(ttk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.original_style = kwargs.get('style', 'TButton')
        self.hover_style = self._get_hover_style(self.original_style)
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
        
    def _get_hover_style(self, original_style):
        if 'success' in original_style:
            return 'success.TButton'
        elif 'warning' in original_style:
            return 'warning.TButton'
        elif 'danger' in original_style:
            return 'danger.TButton'
        elif 'info' in original_style:
            return 'info.TButton'
        else:
            return 'primary.TButton'
    
    def _on_enter(self, event):
        self.configure(style=self.hover_style)
        
    def _on_leave(self, event):
        self.configure(style=self.original_style)
        
    def _on_click(self, event):
        self.configure(style=self.hover_style)
        self.after(100, lambda: self.configure(style=self.original_style))

class FormValidator:
    def __init__(self):
        self.validators = {}
        self.error_labels = {}
        
    def add_validator(self, entry_widget, validation_func, error_message, parent_frame, row, col):
        self.validators[entry_widget] = {
            'func': validation_func,
            'message': error_message,
            'parent': parent_frame,
            'row': row,
            'col': col
        }
        
        entry_widget.bind('<KeyRelease>', self._validate_field)
        entry_widget.bind('<FocusOut>', self._validate_field)
        
        error_label = ttk.Label(parent_frame, 
                               text=error_message, 
                               font=('Segoe UI', 9),
                               foreground='red',
                               style="Content.TLabel")
        error_label.grid(row=row+1, column=col, sticky='w', padx=(5, 0))
        error_label.grid_remove()
        
        self.error_labels[entry_widget] = error_label
        
    def _validate_field(self, event):
        widget = event.widget
        if widget not in self.validators:
            return
            
        validator_info = self.validators[widget]
        error_label = self.error_labels[widget]
        
        is_valid = validator_info['func'](widget.get())
        
        if is_valid:
            error_label.grid_remove()
            widget.configure(style='TEntry')
        else:
            error_label.grid()
            widget.configure(style='danger.TEntry')
            
    def validate_all(self):
        all_valid = True
        for widget, validator_info in self.validators.items():
            is_valid = validator_info['func'](widget.get())
            if not is_valid:
                all_valid = False
                error_label = self.error_labels[widget]
                error_label.grid()
                widget.configure(style='danger.TEntry')
        return all_valid
        
    def clear_errors(self):
        for error_label in self.error_labels.values():
            error_label.grid_remove()
        for widget in self.validators.keys():
            widget.configure(style='TEntry')

def validate_not_empty(value):
    return value.strip() != ""

def validate_positive_number(value):
    try:
        num = float(value)
        return num > 0
    except ValueError:
        return False

def validate_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def validate_percentage(value):
    try:
        num = float(value)
        return 0 <= num <= 100
    except ValueError:
        return False

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = FMEDAGUI(root)
    root.mainloop()
 