import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates


class DatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Management System")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f0f0")

        self.root.minsize(1200, 800)

        self.conn = None
        self.cursor = None
        self.current_user = None
        self.tables_data = {}  # Store treeviews by table name
        self.available_functions = []
        self.available_procedures = []
        self.function_params = {}  # Store function parameters
        self.procedure_params = {}  # Store procedure parameters

        self.create_login_screen()

    def create_login_screen(self):
        """Create styled login screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main login frame with gradient-like background
        login_frame = tk.Frame(self.root, bg="#2c3e50")
        login_frame.pack(expand=True, fill="both")

        # Title section
        title_frame = tk.Frame(login_frame, bg="#2c3e50", pady=30)
        title_frame.pack(fill="x")

        title = tk.Label(title_frame, text="🏥 Database Management System",
                         font=("Arial", 28, "bold"), fg="#ecf0f1", bg="#2c3e50")
        title.pack()

        subtitle = tk.Label(title_frame, text="Elderly Care Facility Management",
                            font=("Arial", 14), fg="#bdc3c7", bg="#2c3e50")
        subtitle.pack(pady=(5, 0))

        # Login form
        form_frame = tk.Frame(login_frame, bg="#34495e", padx=40, pady=40)
        form_frame.pack(pady=30)

        # User credentials
        tk.Label(form_frame, text="Username:", font=("Arial", 12, "bold"),
                 fg="#ecf0f1", bg="#34495e").pack(anchor="w", pady=(0, 5))
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12), width=35,
                                       relief="flat", bd=10)
        self.username_entry.pack(pady=(0, 15), ipady=5)

        tk.Label(form_frame, text="Password:", font=("Arial", 12, "bold"),
                 fg="#ecf0f1", bg="#34495e").pack(anchor="w", pady=(0, 5))
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), width=35,
                                       show="*", relief="flat", bd=10)
        self.password_entry.pack(pady=(0, 20), ipady=5)

        # Database connection settings
        db_frame = tk.LabelFrame(form_frame, text="Database Connection Settings",
                                 font=("Arial", 11, "bold"), fg="#ecf0f1", bg="#34495e")
        db_frame.pack(fill="x", pady=(0, 25))

        # Host and Database in one row
        row1 = tk.Frame(db_frame, bg="#34495e")
        row1.pack(fill="x", padx=10, pady=10)

        tk.Label(row1, text="Host:", fg="#ecf0f1", bg="#34495e", font=("Arial", 10)).pack(side="left")
        self.host_entry = tk.Entry(row1, width=15, font=("Arial", 10))
        self.host_entry.insert(0, "localhost")
        self.host_entry.pack(side="left", padx=(5, 20))

        tk.Label(row1, text="Database:", fg="#ecf0f1", bg="#34495e", font=("Arial", 10)).pack(side="left")
        self.db_entry = tk.Entry(row1, width=15, font=("Arial", 10))
        self.db_entry.insert(0, "mydatabase")
        self.db_entry.pack(side="left", padx=(5, 0))

        # Login button
        login_btn = tk.Button(form_frame, text="Connect to Database", font=("Arial", 14, "bold"),
                              bg="#3498db", fg="white", padx=40, pady=12, relief="flat",
                              command=self.login, cursor="hand2")
        login_btn.pack(pady=15)

        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())

    def login(self):
        """Handle login process"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        host = self.host_entry.get().strip()
        database = self.db_entry.get().strip()

        if not all([username, password, host, database]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            self.conn = psycopg2.connect(
                host=host,
                user=username,
                password=password,
                dbname=database,
                port=5432
            )
            self.cursor = self.conn.cursor()
            self.current_user = username

            # Load functions and procedures after connection
            self.load_functions_and_procedures()

            messagebox.showinfo("Success", f"Successfully connected to database: {database}")
            self.create_main_interface()

        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database:\n{str(e)}")

    def load_functions_and_procedures(self):
        """Load only specific functions and procedures from database with parameter information"""
        try:
            # Clear any previous transaction errors
            self.conn.rollback()

            # Define the specific functions we want to show (in order)
            allowed_functions = [
                'count_active_employees_by_position',
                'get_active_employees_by_position_simple',
                'get_equipment_residents_summary'
            ]

            # Define the specific procedures we want to show (in order)
            allowed_procedures = [
                'update_doctors_email_by_firstname',
                'update_resident_medication_status'
            ]

            # Load functions with parameters - filtered by name
            func_names_filter = "', '".join(allowed_functions)
            self.cursor.execute(f"""
                SELECT 
                    p.proname,
                    p.pronargs,
                    pg_get_function_arguments(p.oid) as args
                FROM pg_proc p
                LEFT JOIN pg_namespace n ON p.pronamespace = n.oid
                WHERE n.nspname = 'public' 
                AND p.prokind = 'f'
                AND p.proname IN ('{func_names_filter}')
                ORDER BY 
                    CASE p.proname
                        WHEN 'count_active_employees_by_position' THEN 1
                        WHEN 'get_active_employees_by_position_simple' THEN 2
                        WHEN 'get_equipment_residents_summary' THEN 3
                        ELSE 4
                    END;
            """)
            func_results = self.cursor.fetchall()

            self.available_functions = []
            self.function_params = {}

            for func_name, arg_count, args in func_results:
                if func_name in allowed_functions:
                    self.available_functions.append(func_name)
                    if args:
                        # Parse arguments string to extract parameter info
                        param_info = self.parse_function_arguments(args)
                        self.function_params[func_name] = param_info
                    else:
                        self.function_params[func_name] = []

            # Load procedures with parameters - filtered by name
            proc_names_filter = "', '".join(allowed_procedures)
            self.cursor.execute(f"""
                SELECT 
                    p.proname,
                    p.pronargs,
                    pg_get_function_arguments(p.oid) as args
                FROM pg_proc p
                LEFT JOIN pg_namespace n ON p.pronamespace = n.oid
                WHERE n.nspname = 'public' 
                AND p.prokind = 'p'
                AND p.proname IN ('{proc_names_filter}')
                ORDER BY 
                    CASE p.proname
                        WHEN 'update_doctors_email_by_firstname' THEN 1
                        WHEN 'update_resident_medication_status' THEN 2
                        ELSE 3
                    END;
            """)
            proc_results = self.cursor.fetchall()

            self.available_procedures = []
            self.procedure_params = {}

            for proc_name, arg_count, args in proc_results:
                if proc_name in allowed_procedures:
                    self.available_procedures.append(proc_name)
                    if args:
                        param_info = self.parse_function_arguments(args)
                        self.procedure_params[proc_name] = param_info
                    else:
                        self.procedure_params[proc_name] = []

            print(f"Loaded {len(self.available_functions)} functions and {len(self.available_procedures)} procedures")

        except Exception as e:
            # Rollback on error
            try:
                self.conn.rollback()
            except:
                pass
            messagebox.showerror("Load Error", f"Failed to load functions/procedures:\n{str(e)}")
            self.available_functions = []
            self.available_procedures = []

    def parse_function_arguments(self, args_string):
        """Parse function arguments string to extract parameter information"""
        if not args_string or args_string.strip() == '':
            return []

        params = []
        # Simple parsing - split by comma and extract name and type
        arg_parts = args_string.split(',')

        for arg in arg_parts:
            arg = arg.strip()
            if arg:
                # Try to extract parameter name and type
                if ' ' in arg:
                    parts = arg.split()
                    param_name = parts[0]
                    param_type = ' '.join(parts[1:])
                else:
                    param_name = arg
                    param_type = 'unknown'

                # Clean up common PostgreSQL type variations
                param_type = param_type.lower()
                if 'int' in param_type:
                    param_type = 'integer'
                elif 'varchar' in param_type or 'text' in param_type:
                    param_type = 'text'
                elif 'date' in param_type:
                    param_type = 'date'
                elif 'timestamp' in param_type:
                    param_type = 'timestamp'

                params.append({'name': param_name, 'type': param_type})

        return params

    def create_main_interface(self):
        """Create main interface"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Database menu
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Database", menu=db_menu)
        db_menu.add_command(label="Refresh Functions/Procedures", command=self.load_functions_and_procedures)
        db_menu.add_command(label="Show Database Info", command=self.show_database_info)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab styles
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'))

        # Main tables tabs
        self.create_residents_tab()
        self.create_doctors_tab()
        self.create_medications_tab()
        self.create_employee_tab()
        self.create_medical_equipment_tab()

        # Additional tables
        self.create_medical_treatments_tab()
        self.create_departments_tab()
        self.create_positions_tab()

        # Queries tab with all 8 queries
        self.create_queries_tab()

        # Separate Functions and Procedures tabs
        self.create_functions_tab()
        self.create_procedures_tab()

    def create_residents_tab(self):
        """Create residents tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏠 Residents")
        self.create_crud_tab(frame, "residents", "Residents")

    def create_doctors_tab(self):
        """Create doctors tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👨‍⚕️ Doctors")
        self.create_crud_tab(frame, "doctors", "Doctors")

    def create_medications_tab(self):
        """Create resident medications tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💊 Medications")
        self.create_crud_tab(frame, "residentmedications", "Resident Medications")

    def create_employee_tab(self):
        """Create employees tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👥 Employees")
        self.create_crud_tab(frame, "employee", "Employees")

    def create_medical_equipment_tab(self):
        """Create medical equipment tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏥 Equipment")
        self.create_crud_tab(frame, "medicalequipmentreceiving", "Medical Equipment")

    def create_medical_treatments_tab(self):
        """Create medical treatments tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💉 Treatments")
        self.create_crud_tab(frame, "medicaltreatments", "Medical Treatments")

    def create_departments_tab(self):
        """Create departments tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🏢 Departments")
        self.create_crud_tab(frame, "department", "Departments")

    def create_positions_tab(self):
        """Create positions tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💼 Positions")
        self.create_crud_tab(frame, "position", "Positions")

    def create_crud_tab(self, parent, table_name, hebrew_name):
        """Create detailed CRUD tab for each table"""
        main_frame = tk.Frame(parent, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_frame = tk.Frame(main_frame, bg="#ecf0f1")
        title_frame.pack(fill="x", pady=(0, 10))

        title_label = tk.Label(title_frame, text=f"{hebrew_name} Management",
                               font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title_label.pack(side="left")

        # Record count label
        count_label = tk.Label(title_frame, text="", font=("Arial", 12),
                               bg="#ecf0f1", fg="#7f8c8d")
        count_label.pack(side="right")

        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg="#ecf0f1")
        control_frame.pack(fill="x", pady=(0, 10))

        # CRUD buttons with better styling
        btn_frame = tk.Frame(control_frame, bg="#ecf0f1")
        btn_frame.pack(side="left")

        add_btn = tk.Button(btn_frame, text="➕ Add Record",
                            command=lambda: self.add_record(table_name),
                            bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                            padx=15, pady=5, relief="flat", cursor="hand2")
        add_btn.pack(side="left", padx=(0, 5))

        edit_btn = tk.Button(btn_frame, text="✏️ Edit Record",
                             command=lambda: self.edit_record(table_name),
                             bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                             padx=15, pady=5, relief="flat", cursor="hand2")
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(btn_frame, text="🗑️ Delete Record",
                               command=lambda: self.delete_record(table_name),
                               bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                               padx=15, pady=5, relief="flat", cursor="hand2")
        delete_btn.pack(side="left", padx=5)

        refresh_btn = tk.Button(btn_frame, text="🔄 Refresh",
                                command=lambda: self.refresh_table_data(table_name),
                                bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                                padx=15, pady=5, relief="flat", cursor="hand2")
        refresh_btn.pack(side="left", padx=5)

        # Export button
        export_btn = tk.Button(btn_frame, text="📄 Export",
                               command=lambda: self.export_table_data(table_name),
                               bg="#9b59b6", fg="white", font=("Arial", 10, "bold"),
                               padx=15, pady=5, relief="flat", cursor="hand2")
        export_btn.pack(side="left", padx=5)

        # Search frame
        search_frame = tk.Frame(control_frame, bg="#ecf0f1")
        search_frame.pack(side="right")

        search_label = tk.Label(search_frame, text="🔍 Search:",
                                bg="#ecf0f1", font=("Arial", 10, "bold"))
        search_label.pack(side="left", padx=(0, 5))

        search_entry = tk.Entry(search_frame, font=("Arial", 10), width=25)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", lambda event: self.filter_tree(table_name, search_entry.get()))

        # Clear search button
        clear_search_btn = tk.Button(search_frame, text="❌",
                                     command=lambda: [search_entry.delete(0, tk.END), self.filter_tree(table_name, "")],
                                     bg="#e74c3c", fg="white", font=("Arial", 8, "bold"),
                                     padx=5, pady=2, relief="flat", cursor="hand2")
        clear_search_btn.pack(side="left", padx=(5, 0))

        # Treeview frame with scrollbars
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)

        # Treeview
        tree = ttk.Treeview(tree_frame)
        tree.pack(side="left", fill="both", expand=True)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        v_scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=tree.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=h_scrollbar.set)

        # Status bar
        status_frame = tk.Frame(main_frame, bg="#ecf0f1")
        status_frame.pack(fill="x", pady=(5, 0))

        status_label = tk.Label(status_frame, text="Ready",
                                bg="#ecf0f1", fg="#7f8c8d", font=("Arial", 9))
        status_label.pack(side="left")

        # Row selection label
        selection_label = tk.Label(status_frame, text="No selection",
                                   bg="#ecf0f1", fg="#7f8c8d", font=("Arial", 9))
        selection_label.pack(side="right")

        # Bind tree selection
        tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_select(table_name, event))

        self.tables_data[table_name] = {
            "tree": tree,
            "status_label": status_label,
            "selection_label": selection_label,
            "count_label": count_label,
            "hebrew_name": hebrew_name
        }

        # Load table data
        self.load_table_data(table_name)

    def on_tree_select(self, table_name, event):
        """Handle tree selection"""
        tree = self.tables_data[table_name]["tree"]
        selection_label = self.tables_data[table_name]["selection_label"]

        selected = tree.focus()
        if selected:
            values = tree.item(selected)['values']
            if values:
                selection_label.config(text=f"Selected: {values[0] if values else 'None'}")
        else:
            selection_label.config(text="No selection")

    def load_table_data(self, table_name):
        """Load table data with improved error handling"""
        try:
            # Clear any previous transaction errors
            self.conn.rollback()

            tree = self.tables_data[table_name]["tree"]
            status_label = self.tables_data[table_name]["status_label"]
            count_label = self.tables_data[table_name]["count_label"]

            # Get column names and types
            self.cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            column_info = self.cursor.fetchall()
            columns = [info[0] for info in column_info]

            # Configure tree columns
            tree["columns"] = columns
            tree["show"] = "headings"

            for col in columns:
                tree.heading(col, text=col.replace('_', ' ').title(),
                             command=lambda _col=col: self.sort_tree(table_name, _col, False))
                tree.column(col, width=120, anchor="center")

            # Load data
            self.cursor.execute(f"SELECT * FROM {table_name}")
            data = self.cursor.fetchall()

            self.tables_data[table_name]["data"] = data
            self.tables_data[table_name]["columns"] = columns
            self.tables_data[table_name]["column_info"] = column_info

            self.refresh_tree(table_name)
            status_label.config(text=f"Loaded {len(data)} records")
            count_label.config(text=f"Total: {len(data)} records")

        except Exception as e:
            # Rollback on error
            try:
                self.conn.rollback()
            except:
                pass
            messagebox.showerror("Error", f"Failed to load table '{table_name}':\n{str(e)}")

    def refresh_table_data(self, table_name):
        """Refresh table data"""
        self.load_table_data(table_name)
        self.tables_data[table_name]["status_label"].config(text="Data refreshed")

    def refresh_tree(self, table_name):
        """Refresh tree view display"""
        tree = self.tables_data[table_name]["tree"]
        for item in tree.get_children():
            tree.delete(item)

        for row in self.tables_data[table_name]["data"]:
            # Handle None values
            display_row = [str(cell) if cell is not None else "" for cell in row]
            tree.insert("", "end", values=display_row)

    def filter_tree(self, table_name, query):
        """Filter table by search query"""
        tree = self.tables_data[table_name]["tree"]
        data = self.tables_data[table_name]["data"]

        if not query:
            filtered = data
        else:
            filtered = [row for row in data if
                        any(query.lower() in str(cell).lower() for cell in row if cell is not None)]

        tree.delete(*tree.get_children())
        for row in filtered:
            display_row = [str(cell) if cell is not None else "" for cell in row]
            tree.insert("", "end", values=display_row)

        self.tables_data[table_name]["status_label"].config(text=f"Found {len(filtered)} records")

    def sort_tree(self, table_name, col, reverse):
        """Sort table by column"""
        tree = self.tables_data[table_name]["tree"]
        data = [(tree.set(k, col), k) for k in tree.get_children("")]

        try:
            # Try to sort numerically first
            data.sort(key=lambda x: float(x[0]) if x[0] and x[0].replace('.', '').replace('-', '').isdigit() else float(
                'inf'),
                      reverse=reverse)
        except:
            # Fall back to string sorting
            data.sort(reverse=reverse)

        for idx, (val, k) in enumerate(data):
            tree.move(k, "", idx)

        tree.heading(col, command=lambda: self.sort_tree(table_name, col, not reverse))

    def add_record(self, table_name):
        """Add new record with validation"""
        columns = self.tables_data[table_name]["columns"]
        column_info = self.tables_data[table_name]["column_info"]
        hebrew_name = self.tables_data[table_name]["hebrew_name"]

        # Create input dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add new record - {hebrew_name}")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(self.root)

        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))

        # Main container
        container = tk.Frame(dialog, bg="#ecf0f1")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(container, text=f"Add new record - {hebrew_name}",
                               font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title_label.pack(pady=(0, 20))

        # Scroll frame for many fields
        canvas = tk.Canvas(container, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Input fields with type information
        entries = {}
        for i, (col, col_type, is_nullable) in enumerate(
                zip(columns, [info[1] for info in column_info], [info[2] for info in column_info])):
            field_frame = tk.Frame(scrollable_frame, bg="#ecf0f1")
            field_frame.pack(fill="x", pady=5)

            # Label with type info
            label_text = f"{col.replace('_', ' ').title()}:"
            if is_nullable == 'NO':
                label_text += " *"

            label = tk.Label(field_frame, text=label_text,
                             font=("Arial", 10, "bold"), bg="#ecf0f1", width=20, anchor="w")
            label.pack(side="left")

            # Type hint
            type_hint = tk.Label(field_frame, text=f"({col_type})",
                                 font=("Arial", 8), bg="#ecf0f1", fg="#7f8c8d")
            type_hint.pack(side="left", padx=(5, 0))

            entry = tk.Entry(field_frame, font=("Arial", 10), width=25)
            entry.pack(side="right", padx=(10, 0))
            entries[col] = entry

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Required fields note - positioned above buttons
        note_label = tk.Label(container, text="* Required fields",
                              font=("Arial", 9), bg="#ecf0f1", fg="#e74c3c")
        note_label.pack(pady=(20, 10))

        # Buttons frame - moved to bottom
        button_frame = tk.Frame(container, bg="#ecf0f1")
        button_frame.pack(side="bottom", fill="x", pady=(10, 0))

        def save_record():
            values = []
            for col in columns:
                val = entries[col].get().strip()
                if val == "":
                    val = None
                values.append(val)

            try:
                # Clear any previous transaction errors
                self.conn.rollback()

                placeholders = ','.join(['%s'] * len(columns))
                self.cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", values)
                self.conn.commit()

                # Refresh data
                self.load_table_data(table_name)
                messagebox.showinfo("Success", "Record added successfully")
                dialog.destroy()

            except Exception as e:
                # Rollback on error
                try:
                    self.conn.rollback()
                except:
                    pass
                messagebox.showerror("Error", f"Failed to add record:\n{str(e)}")

        save_btn = tk.Button(button_frame, text="💾 Save", command=save_record,
                             bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                             padx=30, pady=10, relief="flat", cursor="hand2")
        save_btn.pack(side="left", padx=(0, 10))

        cancel_btn = tk.Button(button_frame, text="❌ Cancel", command=dialog.destroy,
                               bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=10, relief="flat", cursor="hand2")
        cancel_btn.pack(side="left")

    def edit_record(self, table_name):
        """Edit existing record with validation"""
        tree = self.tables_data[table_name]["tree"]
        selected = tree.focus()

        if not selected:
            messagebox.showwarning("Select Record", "Please select a record to edit")
            return

        old_values = tree.item(selected)['values']
        columns = self.tables_data[table_name]["columns"]
        column_info = self.tables_data[table_name]["column_info"]
        hebrew_name = self.tables_data[table_name]["hebrew_name"]

        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Record - {hebrew_name}")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(self.root)

        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))

        # Main container
        container = tk.Frame(dialog, bg="#ecf0f1")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(container, text=f"Edit Record - {hebrew_name}",
                               font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title_label.pack(pady=(0, 20))

        # Scroll frame
        canvas = tk.Canvas(container, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Input fields with existing values
        entries = {}
        for i, (col, col_type, is_nullable) in enumerate(
                zip(columns, [info[1] for info in column_info], [info[2] for info in column_info])):
            field_frame = tk.Frame(scrollable_frame, bg="#ecf0f1")
            field_frame.pack(fill="x", pady=5)

            # Label with type info
            label_text = f"{col.replace('_', ' ').title()}:"
            if is_nullable == 'NO':
                label_text += " *"

            label = tk.Label(field_frame, text=label_text,
                             font=("Arial", 10, "bold"), bg="#ecf0f1", width=20, anchor="w")
            label.pack(side="left")

            # Type hint
            type_hint = tk.Label(field_frame, text=f"({col_type})",
                                 font=("Arial", 8), bg="#ecf0f1", fg="#7f8c8d")
            type_hint.pack(side="left", padx=(5, 0))

            entry = tk.Entry(field_frame, font=("Arial", 10), width=25)
            entry.pack(side="right", padx=(10, 0))

            # Pre-fill with existing value
            if i < len(old_values) and old_values[i] != "":
                entry.insert(0, str(old_values[i]))

            entries[col] = entry

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Required fields note - positioned above buttons
        note_label = tk.Label(container, text="* Required fields",
                              font=("Arial", 9), bg="#ecf0f1", fg="#e74c3c")
        note_label.pack(pady=(20, 10))

        # Buttons frame - moved to bottom
        button_frame = tk.Frame(container, bg="#ecf0f1")
        button_frame.pack(side="bottom", fill="x", pady=(10, 0))

        def update_record():
            new_values = []
            for col in columns:
                val = entries[col].get().strip()
                if val == "":
                    val = None
                new_values.append(val)

            try:
                # Clear any previous transaction errors
                self.conn.rollback()

                pk_col = columns[0]  # Assume first column is primary key
                assignments = ', '.join([f"{col} = %s" for col in columns])
                self.cursor.execute(
                    f"UPDATE {table_name} SET {assignments} WHERE {pk_col} = %s",
                    new_values + [old_values[0] if old_values else None]
                )
                self.conn.commit()

                # Refresh data
                self.load_table_data(table_name)
                messagebox.showinfo("Success", "Record updated successfully")
                dialog.destroy()

            except Exception as e:
                # Rollback on error
                try:
                    self.conn.rollback()
                except:
                    pass
                messagebox.showerror("Error", f"Failed to update record:\n{str(e)}")

        update_btn = tk.Button(button_frame, text="💾 Update", command=update_record,
                               bg="#f39c12", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=10, relief="flat", cursor="hand2")
        update_btn.pack(side="left", padx=(0, 10))

        cancel_btn = tk.Button(button_frame, text="❌ Cancel", command=dialog.destroy,
                               bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=10, relief="flat", cursor="hand2")
        cancel_btn.pack(side="left")

    def delete_record(self, table_name):
        """Delete record with confirmation"""
        tree = self.tables_data[table_name]["tree"]
        selected = tree.focus()

        if not selected:
            messagebox.showwarning("Select Record", "Please select a record to delete")
            return

        values = tree.item(selected)['values']
        columns = self.tables_data[table_name]["columns"]
        pk_col = columns[0]  # Assume first column is primary key
        hebrew_name = self.tables_data[table_name]["hebrew_name"]

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete this record?\n{pk_col}: {values[0]}"):
            try:
                # Clear any previous transaction errors
                self.conn.rollback()

                self.cursor.execute(f"DELETE FROM {table_name} WHERE {pk_col} = %s", [values[0]])
                self.conn.commit()

                # Refresh data
                self.load_table_data(table_name)
                messagebox.showinfo("Success", "Record deleted successfully")

            except Exception as e:
                # Rollback on error
                try:
                    self.conn.rollback()
                except:
                    pass
                messagebox.showerror("Error", f"Failed to delete record:\n{str(e)}")

    def export_table_data(self, table_name):
        """Export table data to file"""
        try:
            data = self.tables_data[table_name]["data"]
            columns = self.tables_data[table_name]["columns"]

            if not data:
                messagebox.showwarning("No Data", "No data to export")
                return

            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")],
                title=f"Export {table_name} data"
            )

            if filename:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(columns)
                    for row in data:
                        writer.writerow([str(cell) if cell is not None else "" for cell in row])

                messagebox.showinfo("Success", f"Data exported to {filename}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")

    def create_queries_tab(self):
        """Create queries tab with all 8 queries"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Queries & Reports")

        main_frame = tk.Frame(frame, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = tk.Label(main_frame, text="📊 Database Queries and Reports",
                               font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title_label.pack(pady=(0, 20))

        # Query selection frame
        query_frame = tk.LabelFrame(main_frame, text="Select Query to Run",
                                    font=("Arial", 12, "bold"), bg="#ecf0f1")
        query_frame.pack(fill="x", pady=(0, 20))

        self.query_var = tk.StringVar()
        # All 8 queries from your document
        queries = [
            "1. Residents with more than 4 devices",
            "2. Most rented equipment",
            "3. Currently rented equipment by type",
            "4. Doctors with most treatments",
            "5. Equipment usage by year and visits",
            "6. Medication count per resident",
            "7. Oldest resident details",
            "8. Patient visit history"
        ]

        query_dropdown = ttk.Combobox(query_frame, textvariable=self.query_var, values=queries,
                                      width=60, font=("Arial", 11), state="readonly")
        query_dropdown.pack(pady=15)

        # Query buttons
        button_frame = tk.Frame(query_frame, bg="#ecf0f1")
        button_frame.pack(pady=15)

        run_btn = tk.Button(button_frame, text="▶️ Run Query",
                            command=self.run_selected_query,
                            bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                            padx=25, pady=10, relief="flat", cursor="hand2")
        run_btn.pack(side="left", padx=(0, 15))

        clear_btn = tk.Button(button_frame, text="🗑️ Clear Results",
                              command=self.clear_query_results,
                              bg="#95a5a6", fg="white", font=("Arial", 12, "bold"),
                              padx=25, pady=10, relief="flat", cursor="hand2")
        clear_btn.pack(side="left")

        # Results area
        results_frame = tk.LabelFrame(main_frame, text="Query Results",
                                      font=("Arial", 12, "bold"), bg="#ecf0f1")
        results_frame.pack(fill="both", expand=True)

        # Text output
        text_frame = tk.Frame(results_frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.query_output = tk.Text(text_frame, height=12, wrap="none",
                                    font=("Courier", 10), bg="white")

        # Scrollbars for text
        text_v_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.query_output.yview)
        text_h_scroll = ttk.Scrollbar(text_frame, orient="horizontal", command=self.query_output.xview)

        self.query_output.configure(yscrollcommand=text_v_scroll.set, xscrollcommand=text_h_scroll.set)

        self.query_output.pack(side="left", fill="both", expand=True)
        text_v_scroll.pack(side="right", fill="y")
        text_h_scroll.pack(side="bottom", fill="x")

        # Graph area
        self.canvas_frame = tk.Frame(results_frame, bg="#ecf0f1")
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def create_functions_tab(self):
        """Create separate Functions tab with parameter support"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔧 Functions")

        main_frame = tk.Frame(frame, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = tk.Label(main_frame, text="🔧 Database Functions",
                               font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title_label.pack(pady=(0, 20))

        # Refresh button
        refresh_btn = tk.Button(main_frame, text="🔄 Refresh Functions",
                                command=self.refresh_functions,
                                bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                                padx=20, pady=8, relief="flat", cursor="hand2")
        refresh_btn.pack(pady=(0, 20))

        # Functions frame
        functions_frame = tk.LabelFrame(main_frame, text=f"Available Functions (3)",
                                        font=("Arial", 12, "bold"), bg="#ecf0f1")
        functions_frame.pack(fill="x", pady=(0, 20))

        # Functions listbox with scrollbar
        func_frame = tk.Frame(functions_frame)
        func_frame.pack(fill="x", padx=10, pady=10)

        self.functions_listbox = tk.Listbox(func_frame, height=8, font=("Arial", 10))
        func_scrollbar = ttk.Scrollbar(func_frame, orient="vertical", command=self.functions_listbox.yview)
        self.functions_listbox.configure(yscrollcommand=func_scrollbar.set)

        self.functions_listbox.pack(side="left", fill="both", expand=True)
        func_scrollbar.pack(side="right", fill="y")

        # Function buttons
        func_btn_frame = tk.Frame(functions_frame, bg="#ecf0f1")
        func_btn_frame.pack(pady=10)

        run_func_btn = tk.Button(func_btn_frame, text="▶️ Run Function",
                                 command=self.run_selected_function,
                                 bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                                 padx=20, pady=8, relief="flat", cursor="hand2")
        run_func_btn.pack(side="left", padx=(0, 10))

        clear_func_btn = tk.Button(func_btn_frame, text="🗑️ Clear Results",
                                   command=lambda: self.functions_output.delete("1.0", tk.END),
                                   bg="#95a5a6", fg="white", font=("Arial", 11, "bold"),
                                   padx=20, pady=8, relief="flat", cursor="hand2")
        clear_func_btn.pack(side="left")

        # Results area for functions
        results_frame = tk.LabelFrame(main_frame, text="Function Results",
                                      font=("Arial", 12, "bold"), bg="#ecf0f1")
        results_frame.pack(fill="both", expand=True)

        self.functions_output = tk.Text(results_frame, height=15, wrap="none",
                                        font=("Courier", 10), bg="white")

        # Scrollbars
        func_v_scroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.functions_output.yview)
        func_h_scroll = ttk.Scrollbar(results_frame, orient="horizontal", command=self.functions_output.xview)

        self.functions_output.configure(yscrollcommand=func_v_scroll.set, xscrollcommand=func_h_scroll.set)

        self.functions_output.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        func_v_scroll.pack(side="right", fill="y")
        func_h_scroll.pack(side="bottom", fill="x")

        # Populate the listbox
        self.refresh_functions()

    def create_procedures_tab(self):
        """Create separate Procedures tab with parameter support"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ Procedures")

        main_frame = tk.Frame(frame, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = tk.Label(main_frame, text="⚙️ Database Procedures",
                               font=("Arial", 16, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title_label.pack(pady=(0, 20))

        # Refresh button
        refresh_btn = tk.Button(main_frame, text="🔄 Refresh Procedures",
                                command=self.refresh_procedures,
                                bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                                padx=20, pady=8, relief="flat", cursor="hand2")
        refresh_btn.pack(pady=(0, 20))

        # Procedures frame
        procedures_frame = tk.LabelFrame(main_frame, text=f"Available Procedures (2)",
                                         font=("Arial", 12, "bold"), bg="#ecf0f1")
        procedures_frame.pack(fill="x", pady=(0, 20))

        # Procedures listbox with scrollbar
        proc_frame = tk.Frame(procedures_frame)
        proc_frame.pack(fill="x", padx=10, pady=10)

        self.procedures_listbox = tk.Listbox(proc_frame, height=8, font=("Arial", 10))
        proc_scrollbar = ttk.Scrollbar(proc_frame, orient="vertical", command=self.procedures_listbox.yview)
        self.procedures_listbox.configure(yscrollcommand=proc_scrollbar.set)

        self.procedures_listbox.pack(side="left", fill="both", expand=True)
        proc_scrollbar.pack(side="right", fill="y")

        # Procedure buttons
        proc_btn_frame = tk.Frame(procedures_frame, bg="#ecf0f1")
        proc_btn_frame.pack(pady=10)

        run_proc_btn = tk.Button(proc_btn_frame, text="▶️ Run Procedure",
                                 command=self.run_selected_procedure,
                                 bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                                 padx=20, pady=8, relief="flat", cursor="hand2")
        run_proc_btn.pack(side="left", padx=(0, 10))

        clear_proc_btn = tk.Button(proc_btn_frame, text="🗑️ Clear Results",
                                   command=lambda: self.procedures_output.delete("1.0", tk.END),
                                   bg="#95a5a6", fg="white", font=("Arial", 11, "bold"),
                                   padx=20, pady=8, relief="flat", cursor="hand2")
        clear_proc_btn.pack(side="left")

        # Results area for procedures
        results_frame = tk.LabelFrame(main_frame, text="Procedure Results",
                                      font=("Arial", 12, "bold"), bg="#ecf0f1")
        results_frame.pack(fill="both", expand=True)

        self.procedures_output = tk.Text(results_frame, height=15, wrap="none",
                                         font=("Courier", 10), bg="white")

        # Scrollbars
        proc_v_scroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.procedures_output.yview)
        proc_h_scroll = ttk.Scrollbar(results_frame, orient="horizontal", command=self.procedures_output.xview)

        self.procedures_output.configure(yscrollcommand=proc_v_scroll.set, xscrollcommand=proc_h_scroll.set)

        self.procedures_output.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        proc_v_scroll.pack(side="right", fill="y")
        proc_h_scroll.pack(side="bottom", fill="x")

        # Populate the listbox
        self.refresh_procedures()

    def get_function_parameters(self, func_name):
        """Get parameters for selected function with input dialog"""
        params = self.function_params.get(func_name, [])
        if not params:
            return []

        # Create parameter input dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Parameters for {func_name}")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(self.root)

        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))

        # Main container
        container = tk.Frame(dialog, bg="#ecf0f1")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(container, text=f"Enter parameters for:\n{func_name}",
                               font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title_label.pack(pady=(0, 20))

        # Parameter fields
        param_entries = {}
        for param in params:
            param_frame = tk.Frame(container, bg="#ecf0f1")
            param_frame.pack(fill="x", pady=5)

            label = tk.Label(param_frame, text=f"{param['name']} ({param['type']}):",
                             font=("Arial", 11, "bold"), bg="#ecf0f1", anchor="w")
            label.pack(side="left", fill="x", expand=True)

            entry = tk.Entry(param_frame, font=("Arial", 11), width=20)
            entry.pack(side="right")

            # Set default values for known functions
            if func_name == "count_active_employees_by_position" and param['name'] == "min_employees":
                entry.insert(0, "0")
            elif func_name == "get_active_employees_by_position_simple" and param['name'] == "p_positionid":
                entry.insert(0, "1")
            elif func_name == "get_equipment_residents_summary":
                if param['name'] == "min_devices":
                    entry.insert(0, "3")
                elif param['name'] == "min_rentals":
                    entry.insert(0, "5")
                elif param['name'] == "min_current_rentals":
                    entry.insert(0, "2")

            param_entries[param['name']] = entry

        # Result storage
        result = {'values': None, 'cancelled': True}

        # Buttons
        button_frame = tk.Frame(container, bg="#ecf0f1")
        button_frame.pack(side="bottom", fill="x", pady=(20, 0))

        def on_ok():
            values = []
            for param in params:
                value = param_entries[param['name']].get().strip()
                if value:
                    # Convert based on type
                    try:
                        if param['type'] in ['integer', 'int']:
                            value = int(value)
                        elif param['type'] in ['date']:
                            # Keep as string, PostgreSQL will handle conversion
                            pass
                        # Add more type conversions as needed
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Invalid value for {param['name']}: {value}")
                        return
                else:
                    messagebox.showerror("Missing Parameter", f"Please enter a value for {param['name']}")
                    return
                values.append(value)

            result['values'] = values
            result['cancelled'] = False
            dialog.destroy()

        def on_cancel():
            result['cancelled'] = True
            dialog.destroy()

        ok_btn = tk.Button(button_frame, text="✅ OK", command=on_ok,
                           bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                           padx=30, pady=8, relief="flat", cursor="hand2")
        ok_btn.pack(side="left", padx=(0, 10))

        cancel_btn = tk.Button(button_frame, text="❌ Cancel", command=on_cancel,
                               bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=8, relief="flat", cursor="hand2")
        cancel_btn.pack(side="left")

        # Wait for dialog to close
        dialog.wait_window()

        if result['cancelled']:
            return None
        return result['values']

    def get_procedure_parameters(self, proc_name):
        """Get parameters for selected procedure with input dialog"""
        params = self.procedure_params.get(proc_name, [])
        if not params:
            return []

        # Create parameter input dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Parameters for {proc_name}")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(self.root)

        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))

        # Main container
        container = tk.Frame(dialog, bg="#ecf0f1")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(container, text=f"Enter parameters for:\n{proc_name}",
                               font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50")
        title_label.pack(pady=(0, 20))

        # Parameter fields
        param_entries = {}
        for param in params:
            param_frame = tk.Frame(container, bg="#ecf0f1")
            param_frame.pack(fill="x", pady=5)

            label = tk.Label(param_frame, text=f"{param['name']} ({param['type']}):",
                             font=("Arial", 11, "bold"), bg="#ecf0f1", anchor="w")
            label.pack(side="left", fill="x", expand=True)

            entry = tk.Entry(param_frame, font=("Arial", 11), width=20)
            entry.pack(side="right")

            # Set default values for known procedures
            if proc_name == "update_resident_medication_status" and param['name'] == "cutoff_date":
                entry.insert(0, "2024-06-02")

            param_entries[param['name']] = entry

        # Result storage
        result = {'values': None, 'cancelled': True}

        # Buttons
        button_frame = tk.Frame(container, bg="#ecf0f1")
        button_frame.pack(side="bottom", fill="x", pady=(20, 0))

        def on_ok():
            values = []
            for param in params:
                value = param_entries[param['name']].get().strip()
                if value:
                    # Convert based on type
                    try:
                        if param['type'] in ['integer', 'int']:
                            value = int(value)
                        elif param['type'] in ['date']:
                            # Keep as string, PostgreSQL will handle conversion
                            pass
                        # Add more type conversions as needed
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Invalid value for {param['name']}: {value}")
                        return
                else:
                    if param['type'] != 'date':  # Allow empty dates
                        messagebox.showerror("Missing Parameter", f"Please enter a value for {param['name']}")
                        return
                values.append(value)

            result['values'] = values
            result['cancelled'] = False
            dialog.destroy()

        def on_cancel():
            result['cancelled'] = True
            dialog.destroy()

        ok_btn = tk.Button(button_frame, text="✅ OK", command=on_ok,
                           bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                           padx=30, pady=8, relief="flat", cursor="hand2")
        ok_btn.pack(side="left", padx=(0, 10))

        cancel_btn = tk.Button(button_frame, text="❌ Cancel", command=on_cancel,
                               bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                               padx=30, pady=8, relief="flat", cursor="hand2")
        cancel_btn.pack(side="left")

        # Wait for dialog to close
        dialog.wait_window()

        if result['cancelled']:
            return None
        return result['values']

    def refresh_functions(self):
        """Refresh functions list"""
        self.load_functions_and_procedures()

        # Clear and populate functions listbox
        self.functions_listbox.delete(0, tk.END)
        for func in self.available_functions:
            params_info = ""
            if func in self.function_params and self.function_params[func]:
                param_count = len(self.function_params[func])
                params_info = f" ({param_count} params)"
            self.functions_listbox.insert(tk.END, f"{func}{params_info}")

    def refresh_procedures(self):
        """Refresh procedures list"""
        self.load_functions_and_procedures()

        # Clear and populate procedures listbox
        self.procedures_listbox.delete(0, tk.END)
        for proc in self.available_procedures:
            params_info = ""
            if proc in self.procedure_params and self.procedure_params[proc]:
                param_count = len(self.procedure_params[proc])
                params_info = f" ({param_count} params)"
            self.procedures_listbox.insert(tk.END, f"{proc}{params_info}")

    def run_selected_function(self):
        """Run selected function with parameter support"""
        selection = self.functions_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Function", "Please select a function to run")
            return

        func_display = self.functions_listbox.get(selection[0])
        func_name = func_display.split(" (")[0]  # Remove parameter info

        try:
            # Clear any previous transaction errors
            self.conn.rollback()

            # Get parameters if needed
            param_values = self.get_function_parameters(func_name)
            if param_values is None:  # User cancelled
                return

            # Build function call
            if param_values:
                placeholders = ', '.join(['%s'] * len(param_values))
                query = f"SELECT * FROM {func_name}({placeholders});"
                self.cursor.execute(query, param_values)
            else:
                query = f"SELECT * FROM {func_name}();"
                self.cursor.execute(query)

            results = self.cursor.fetchall()
            headers = [desc[0] for desc in self.cursor.description]

            self.display_function_results(f"Function: {func_name}", headers, results)

        except Exception as e:
            # Rollback the transaction on error
            try:
                self.conn.rollback()
            except:
                pass
            self.functions_output.delete("1.0", tk.END)
            self.functions_output.insert(tk.END, f"Error running function '{func_name}':\n{str(e)}")

    def run_selected_procedure(self):
        """Run selected procedure with parameter support"""
        selection = self.procedures_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Procedure", "Please select a procedure to run")
            return

        proc_display = self.procedures_listbox.get(selection[0])
        proc_name = proc_display.split(" (")[0]  # Remove parameter info

        try:
            # Clear any previous transaction errors
            self.conn.rollback()

            # Get parameters if needed
            param_values = self.get_procedure_parameters(proc_name)
            if param_values is None:  # User cancelled
                return

            # Build procedure call
            if param_values:
                placeholders = ', '.join(['%s'] * len(param_values))
                query = f"CALL {proc_name}({placeholders});"
                self.cursor.execute(query, param_values)
            else:
                query = f"CALL {proc_name}();"
                self.cursor.execute(query)

            self.conn.commit()

            self.procedures_output.delete("1.0", tk.END)
            self.procedures_output.insert(tk.END, f"=== Procedure: {proc_name} ===\n\n")
            self.procedures_output.insert(tk.END, f"Procedure '{proc_name}' executed successfully.\n")
            if param_values:
                self.procedures_output.insert(tk.END, f"Parameters: {param_values}\n")
            self.procedures_output.insert(tk.END, f"Execution time: {datetime.now().strftime('%H:%M:%S')}\n")

        except Exception as e:
            # Rollback the transaction on error
            try:
                self.conn.rollback()
            except:
                pass
            self.procedures_output.delete("1.0", tk.END)
            self.procedures_output.insert(tk.END, f"Error running procedure '{proc_name}':\n{str(e)}")

    def run_selected_query(self):
        """Run selected query with appropriate visualization"""
        selection = self.query_var.get()
        if not selection:
            messagebox.showwarning("Select Query", "Please select a query to run")
            return

        # Extract query number
        query_num = selection.split(".")[0]

        # Define all 8 queries with corrected SQL
        queries = {
            "1": {
                "name": "Residents with more than 4 devices",
                "sql": '''
                    SELECT r.resident_id, r.r_fname AS first_name, r.r_lname AS last_name, COUNT(m.equipment_id) AS total_devices
                    FROM residents r
                    JOIN medicalequipmentreceiving m ON r.resident_id = m.resident_id
                    GROUP BY r.resident_id, r.r_fname, r.r_lname
                    HAVING COUNT(m.equipment_id) > 4
                    ORDER BY r.resident_id;
                ''',
                "chart_type": "bar"
            },
            "2": {
                "name": "Most rented equipment",
                "sql": '''
                    SELECT 
                        equipment_type, 
                        COUNT(equipment_id) AS total_rentals
                    FROM 
                        medicalequipmentreceiving
                    GROUP BY 
                        equipment_type
                    ORDER BY total_rentals DESC
                    LIMIT 5;
                ''',
                "chart_type": "bar"
            },
            "3": {
                "name": "Currently rented equipment by type",
                "sql": '''
                    SELECT 
                        equipment_type AS device_type,
                        COUNT(*) AS currently_rented_count
                    FROM 
                        medicalequipmentreceiving
                    WHERE 
                        end_date IS NULL
                    GROUP BY 
                        equipment_type
                    ORDER BY 
                        currently_rented_count DESC;
                ''',
                "chart_type": "pie"
            },
            "4": {
                "name": "Doctors with most treatments",
                "sql": '''
                    SELECT 
                        d.employeeid_ AS doctor_id,
                        CONCAT(e.firstname_, ' ', e.lastname_) AS doctor_name,
                        COUNT(mt.treatmenttime) AS total_treatments
                    FROM 
                        doctors d
                    JOIN 
                        employee e ON d.employeeid_ = e.employeeid_
                    JOIN 
                        medicaltreatments mt ON d.employeeid_ = mt.employeeid_
                    GROUP BY 
                        d.employeeid_, e.firstname_, e.lastname_
                    ORDER BY 
                        total_treatments DESC
                    LIMIT 10;
                ''',
                "chart_type": "bar"
            },

            "5": {
                "name": "Equipment usage by year and visits",
                "sql": '''
                    SELECT
                      COALESCE(r.year, t.year) AS year,
                      COALESCE(total_devices, 0) AS total_devices,
                      COALESCE(total_visits, 0) AS total_visits
                    FROM
                      (
                        SELECT EXTRACT(YEAR FROM start_date) AS year, COUNT(*) AS total_devices
                        FROM medicalequipmentreceiving
                        WHERE start_date IS NOT NULL
                        GROUP BY EXTRACT(YEAR FROM start_date)
                      ) AS r
                    FULL OUTER JOIN
                      (
                        SELECT EXTRACT(YEAR FROM treatmentdate) AS year, COUNT(*) AS total_visits
                        FROM medicaltreatments
                        WHERE treatmentdate IS NOT NULL
                        GROUP BY EXTRACT(YEAR FROM treatmentdate)
                      ) AS t
                    ON r.year = t.year
                    ORDER BY year;
                ''',
                "chart_type": "line"
            },
            "6": {
                "name": "Medication count per resident",
                "sql": '''
                    SELECT 
                        r.resident_id, 
                        r.r_fname, 
                        r.r_lname, 
                        COUNT(rm.medication_id) AS total_medications
                    FROM residents r
                    LEFT JOIN residentmedications rm ON r.resident_id = rm.resident_id
                    GROUP BY r.resident_id, r.r_fname, r.r_lname
                    HAVING COUNT(rm.medication_id) > 0
                    ORDER BY total_medications DESC, r.resident_id
                    LIMIT 15;
                ''',
                "chart_type": "bar"
            },
            "7": {
                "name": "Oldest resident details",
                "sql": '''
                    SELECT 
                        r.resident_id,
                        r.r_fname AS first_name,
                        r.r_lname AS last_name,
                        r.birthdate AS date_of_birth,
                        EXTRACT(YEAR FROM AGE(r.birthdate)) AS age,
                        r.medicalstatus AS medical_status
                    FROM residents r
                    WHERE r.birthdate IS NOT NULL
                    ORDER BY r.birthdate ASC
                    LIMIT 5;
                ''',
                "chart_type": None  # No chart for detailed info
            },
            "8": {
                "name": "Patient visit history",
                "sql": '''
                    SELECT 
                        r.resident_id,
                        CONCAT(r.r_fname, ' ', r.r_lname) AS resident_name,
                        mt.treatmentdate AS treatment_date,
                        mt.purpose AS treatment_purpose,
                        CONCAT(e.firstname_, ' ', e.lastname_) AS doctor_name
                    FROM 
                        residents r
                    LEFT JOIN medicaltreatments mt ON r.resident_id = mt.resident_id
                    LEFT JOIN doctors d ON mt.employeeid_ = d.employeeid_
                    LEFT JOIN employee e ON d.employeeid_ = e.employeeid_
                    WHERE mt.treatmentdate IS NOT NULL
                    ORDER BY 
                        r.resident_id,
                        mt.treatmentdate DESC
                    LIMIT 20;
                ''',
                "chart_type": None  # No chart for historical data
            }

        }

        query_info = queries.get(query_num)
        if not query_info:
            messagebox.showerror("Query Error", "Query not found")
            return

        try:
            # Clear any previous transaction errors
            self.conn.rollback()

            self.cursor.execute(query_info["sql"])
            results = self.cursor.fetchall()
            headers = [desc[0] for desc in self.cursor.description]

            self.display_query_results(headers, results, query_info["name"])

            # Show appropriate graph for quantitative queries
            if query_info["chart_type"] and results and len(headers) >= 2:
                self.show_advanced_graph(headers, results, query_info["chart_type"], query_info["name"])

        except Exception as e:
            # Rollback the transaction on error to allow future queries
            try:
                self.conn.rollback()
            except:
                pass
            messagebox.showerror("Query Error", f"Failed to execute query:\n{str(e)}")

    def display_query_results(self, headers, results, query_name):
        """Display query results in formatted table"""
        self.query_output.delete("1.0", tk.END)

        # Add query name
        self.query_output.insert(tk.END, f"{'=' * 60}\n")
        self.query_output.insert(tk.END, f"{query_name.center(60)}\n")
        self.query_output.insert(tk.END, f"{'=' * 60}\n\n")

        if not results:
            self.query_output.insert(tk.END, "No results found.\n")
            return

        # Calculate column widths
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in results:
                if i < len(row) and row[i] is not None:
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(min(max_width + 2, 30))

        # Headers
        header_line = ""
        for i, header in enumerate(headers):
            header_line += header.ljust(col_widths[i])
        self.query_output.insert(tk.END, header_line + "\n")

        # Separator
        separator = ""
        for width in col_widths:
            separator += "=" * width
        self.query_output.insert(tk.END, separator + "\n")

        # Data rows
        for row in results:
            row_line = ""
            for i, cell in enumerate(row):
                cell_str = str(cell) if cell is not None else "NULL"
                if len(cell_str) > col_widths[i] - 2:
                    cell_str = cell_str[:col_widths[i] - 5] + "..."
                row_line += cell_str.ljust(col_widths[i])
            self.query_output.insert(tk.END, row_line + "\n")

        # Summary
        self.query_output.insert(tk.END, f"\n{'=' * 60}\n")
        self.query_output.insert(tk.END, f"Total: {len(results)} records\n")
        self.query_output.insert(tk.END, f"Execution time: {datetime.now().strftime('%H:%M:%S')}\n")

    def show_advanced_graph(self, headers, results, chart_type, query_name):
        """Show advanced graphs with different types"""
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        if not results or len(headers) < 2:
            return

        try:
            fig, ax = plt.subplots(figsize=(10, 5))

            if chart_type == "bar":
                # Bar chart
                if len(headers) >= 2:
                    labels = [str(row[0]) if len(row) > 0 else "" for row in results]
                    # Try to find the numeric column
                    values = []
                    for row in results:
                        for i in range(1, len(row)):  # Start from second column
                            try:
                                val = float(row[i]) if row[i] is not None else 0
                                values.append(val)
                                break
                            except (ValueError, TypeError):
                                continue
                        else:
                            values.append(0)

                    colors = ['#3498db', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6', '#e67e22', '#1abc9c', '#34495e']
                    bars = ax.bar(range(len(labels)), values,
                                  color=[colors[i % len(colors)] for i in range(len(labels))])

                    ax.set_xticks(range(len(labels)))
                    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)

                    ax.set_xlabel(headers[0])
                    ax.set_ylabel("Count")

                    # Add value labels on bars
                    for i, (bar, value) in enumerate(zip(bars, values)):
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2., height + max(values) * 0.01,
                                f'{int(value)}', ha='center', va='bottom', fontsize=9)

            elif chart_type == "pie":
                # Pie chart
                if len(headers) >= 2:
                    labels = [str(row[0]) if len(row) > 0 else "" for row in results]
                    values = []
                    for row in results:
                        for i in range(1, len(row)):
                            try:
                                val = float(row[i]) if row[i] is not None else 0
                                values.append(val)
                                break
                            except (ValueError, TypeError):
                                continue
                        else:
                            values.append(0)

                    colors = ['#3498db', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6', '#e67e22', '#1abc9c', '#34495e']
                    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                                      colors=colors[:len(values)], startangle=90)

                    # Improve text readability
                    for autotext in autotexts:
                        autotext.set_color('white')
                        autotext.set_fontweight('bold')

            elif chart_type == "line":
                # Line chart (trend)
                if len(headers) >= 3:  # Year, devices, visits
                    years = [str(int(row[0])) if row[0] is not None else "" for row in results]
                    devices = [float(row[1]) if row[1] is not None else 0 for row in results]
                    visits = [float(row[2]) if row[2] is not None else 0 for row in results]

                    ax.plot(years, devices, marker='o', linewidth=3, markersize=8,
                            color='#3498db', label='Equipment Usage')
                    ax.plot(years, visits, marker='s', linewidth=3, markersize=8,
                            color='#e74c3c', label='Medical Visits')

                    ax.set_xlabel('Year')
                    ax.set_ylabel('Count')
                    ax.legend()
                    ax.grid(True, alpha=0.3)

            ax.set_title(f"{query_name}", fontsize=14, fontweight='bold', pad=20)

            # Improve layout
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print(f"Error creating graph: {e}")

    def display_function_results(self, title, headers, results):
        """Display function results"""
        self.functions_output.delete("1.0", tk.END)

        # Title
        self.functions_output.insert(tk.END, f"{'=' * 60}\n")
        self.functions_output.insert(tk.END, f"{title.center(60)}\n")
        self.functions_output.insert(tk.END, f"{'=' * 60}\n\n")

        if not results:
            self.functions_output.insert(tk.END, "No results found.\n")
            return

        # Calculate column widths
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in results:
                if i < len(row) and row[i] is not None:
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(min(max_width + 2, 25))

        # Headers
        header_line = ""
        for i, header in enumerate(headers):
            header_line += header.ljust(col_widths[i])
        self.functions_output.insert(tk.END, header_line + "\n")

        # Separator
        separator = ""
        for width in col_widths:
            separator += "-" * width
        self.functions_output.insert(tk.END, separator + "\n")

        # Data rows
        for row in results:
            row_line = ""
            for i, cell in enumerate(row):
                cell_str = str(cell) if cell is not None else "NULL"
                if len(cell_str) > col_widths[i] - 2:
                    cell_str = cell_str[:col_widths[i] - 5] + "..."
                row_line += cell_str.ljust(col_widths[i])
            self.functions_output.insert(tk.END, row_line + "\n")

        # Summary
        self.functions_output.insert(tk.END, f"\n{'=' * 60}\n")
        self.functions_output.insert(tk.END, f"Total records: {len(results)}\n")
        self.functions_output.insert(tk.END, f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def clear_query_results(self):
        """Clear query results"""
        self.query_output.delete("1.0", tk.END)
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

    def show_database_info(self):
        """Show database information"""
        try:
            # Clear any previous transaction errors
            self.conn.rollback()

            info_window = tk.Toplevel(self.root)
            info_window.title("Database Information")
            info_window.geometry("600x500")
            info_window.resizable(True, True)

            # Get database info
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT current_database();")
            db_name = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT current_user;")
            user = self.cursor.fetchone()[0]

            # Get table count
            self.cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """)
            table_count = self.cursor.fetchone()[0]

            # Create info display
            info_text = tk.Text(info_window, wrap="word", font=("Courier", 10))
            info_text.pack(fill="both", expand=True, padx=10, pady=10)

            info_content = f"""
DATABASE INFORMATION
{'=' * 50}

Database: {db_name}
User: {user}
PostgreSQL Version: {version}

Tables: {table_count}
Functions: {len(self.available_functions)}
Procedures: {len(self.available_procedures)}

Connection Details:
- Host: {self.host_entry.get()}
- Port: 5432
- Connected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Available Functions:
{chr(10).join(f"  • {func}" for func in self.available_functions)}

Available Procedures:
{chr(10).join(f"  • {proc}" for proc in self.available_procedures)}
            """

            info_text.insert("1.0", info_content)
            info_text.config(state="disabled")

        except Exception as e:
            # Rollback on error
            try:
                self.conn.rollback()
            except:
                pass
            messagebox.showerror("Database Info Error", f"Failed to get database info:\n{str(e)}")

    def logout(self):
        """Logout from system"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if self.conn:
                self.conn.close()
            self.create_login_screen()

    def show_about(self):
        """Show about information"""
        about_text = """
        Enhanced Database Management System
        Version 5.1

        Developed by: Aharon Raanan & Levi Yitzchak Grinfeld
        Year: 2025

        Features:
        • Manage residents, doctors, and employees
        • Track medications and medical equipment
        • Handle medical treatments
        • Manage departments and positions

        • Display reports and graphs
        • Complete CRUD operations for all tables
        • 8 comprehensive database queries with visualizations
        • Custom Functions and Procedures with parameter support
        • Advanced data visualization (Bar, Pie, Line charts)
        • Export functionality
        • Advanced search and filtering
        • Real-time database schema detection

        Available Functions:
        • count_active_employees_by_position (min_employees)
        • get_active_employees_by_position_simple (p_positionid)
        • get_equipment_residents_summary (min_devices, min_rentals, min_current_rentals)

        Available Procedures:
        • update_doctors_email_by_firstname ()
        • update_resident_medication_status (cutoff_date)

        Enhanced Features (v5.1):
        • Function parameter detection and input dialogs
        • Procedure parameter detection and input dialogs
        • Automatic parameter type conversion
        • Filtered list showing only your custom functions and procedures
        • Enhanced error handling with transaction rollback

        Query Visualizations:
        • Bar Charts for counts and comparisons
        • Pie Charts for distributions
        • Line Charts for trends over time
        • Text results for detailed information

        © 2025 All rights reserved
        """
        messagebox.showinfo("About", about_text)


def main():
    """Main function"""
    root = tk.Tk()

    # Set font
    try:
        root.option_add('*Font', 'Arial 10')
    except:
        pass

    app = DatabaseGUI(root)

    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            if app.conn:
                app.conn.close()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()