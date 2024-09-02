import tkinter as tk
from tkinter import ttk, Menu, filedialog, messagebox, Listbox, simpledialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class DataVisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analysis Application")
        self.geometry("1200x800")

        # Initialize attributes
        self.data = None
        self.current_plot = 0
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.loaded_data = []
        self.y_col = None
        self.x_col = None
        self.filters = None
        self.col_filters = None
        self.filter_window = False

        # Create the GUI components
        self.create_widgets()

    def create_widgets(self):
        # Menu Bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.select_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        file_menu.add_command(label="Save file", command=self.save_file)
        menu_bar.add_cascade(label="File", menu=file_menu)

        window_menu = tk.Menu(menu_bar, tearoff=0)
        window_menu.add_command(label="Filter Window", command=self.open_filter_window)
        menu_bar.add_cascade(label="Windows", menu=window_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Create the PanedWindow with horizontal orientation
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Data bar
        self.sidebar_window = tk.PanedWindow(self.paned_window, orient=tk.VERTICAL)
        self.databar_frame = ttk.Frame(self.sidebar_window, relief=tk.RAISED, borderwidth=2)
        self.databar_label = ttk.Label(self.databar_frame, text="Imported Data", font=('Helvetica', 11))
        self.databar_label.pack(side=tk.TOP, fill=tk.X, padx=(2.5, 2), pady=(2, 2))
        self.sidebar_window.add(self.databar_frame, minsize=250)

        # Sidebar
        self.sidebar_frame = ttk.Frame(self.sidebar_window, relief=tk.RAISED, borderwidth=2)
        self.sidebar_window.add(self.sidebar_frame, minsize=200)  # Adding sidebar to the PanedWindow with a minimum size
        self.paned_window.add(self.sidebar_window, minsize=200)

        # Filter Bar
        self.filterbar_frame = ttk.Frame(self.sidebar_window, relief=tk.RAISED, borderwidth=2)
        # self.sidebar_window.add(self.filterbar_frame, minsize=200)
        

        # Import File button
        import_file_button = ttk.Button(self.sidebar_frame, text="Import File", command=self.select_file)
        import_file_button.pack(side=tk.TOP, fill=tk.X)

        # Plotting selection
        plotting_button = ttk.Button(self.sidebar_frame, text="Plotting", command=self.select_plotting)
        plotting_button.pack(side=tk.TOP, fill=tk.X)

        # Button to show transformation options
        transform_button = ttk.Button(self.sidebar_frame, text="Transformations", command=self.select_transformations)
        transform_button.pack(side=tk.TOP, fill=tk.X)

        # Databar list
        self.list_of_data = tk.Listbox(self.databar_frame)
        self.list_of_data.pack(fill=tk.BOTH, expand=1, pady=5, padx=5)

        self.list_data_remove_button = ttk.Button(self.databar_frame, text="Remove Data", command=self.remove_data)
        self.list_data_remove_button.pack(side=tk.TOP, fill=tk.X)

        def on_double_click(event):
            selected_file = event.widget.curselection()
            try:
                selected_file = event.widget.get(selected_file)
                if self.data is None or self.data[0] != selected_file:
                    for i in self.loaded_data:
                        if i[0] == selected_file:
                            self.data = i
                    self.select_plotting()
                    self.plot()
                self.status_var.set(f'Successfully loaded {selected_file}')
            except Exception as e:
                self.status_var.set(f"Failed to load due to error: {e}")

        self.list_of_data.bind("<Double-1>", on_double_click)

        # Populate the listbox with some attributes
        for attr in self.loaded_data:
            self.list_of_data.insert(tk.END, attr[0])

        # Main Content Area
        self.main_frame = ttk.Frame(self.paned_window, borderwidth=2)
        self.paned_window.add(self.main_frame, minsize=250)  # Adding main content area to the PanedWindow

        self.graph_frame = ttk.Frame(self.main_frame, relief=tk.RAISED, borderwidth=2)
        self.graph_frame.pack(fill=tk.BOTH, expand=1)

        # Toolbar
        toolbar_frame = ttk.Frame(self.main_frame, relief=tk.RAISED, borderwidth=2)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Table Data button
        self.table_data_button = ttk.Button(toolbar_frame, text='Table', command=self.display_data)
        # self.table_data_button.pack(side=tk.LEFT, padx=2, pady=2) # Packed later

        # Plot graph button in the toolbar (Initially hidden)
        self.plot_graph_button = ttk.Button(toolbar_frame, text='Plot Graph', command=self.plot_graph)
        # self.plot_graph_button.pack(side=tk.LEFT, padx=2, pady=2)  # Packed later if file is selected

        # Change filters
        self.change_filters_button = ttk.Button(toolbar_frame, text="Set Filters", command=self.ask_for_columns)

        # Apply log transformation button
        self.apply_log_transform = ttk.Button(toolbar_frame, text='Log Transform', command=self.log_transform)
        # self.apply_log_transform.pack(side=tk.LEFT, padx=2, pady=2) # Packed later

        # Status Bar
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def pack_transforms(self, pack):
        if pack == True:
            self.apply_log_transform.pack(side=tk.LEFT, padx=2, pady=2)
        else:
            self.apply_log_transform.pack_forget()
    
    def pack_plotting(self, pack):
        if pack == True:
            self.table_data_button.pack(side=tk.LEFT, padx=2, pady=2)
            self.plot_graph_button.pack(side=tk.LEFT, padx=2, pady=2)
            self.change_filters_button.pack(side=tk.RIGHT, padx=2, pady=2)
        else:
            self.table_data_button.pack_forget()
            self.plot_graph_button.pack_forget()
            self.change_filters_button.pack_forget()

    def set_filters(self, filters):
        if self.filters != filters:
            self.filters = filters
            if self.filter_window == True:
                self.populate_filter_window()

    def select_transformations(self):
        if self.data is not None:
            self.pack_transforms(True)
            self.pack_plotting(False)
        else:
            self.status_var.set("Please select or import data")

    def select_plotting(self):
        if self.data is not None:
            self.pack_plotting(True)
            self.pack_transforms(False)
        else:
            self.status_var.set("Please select or import data")

    def open_filter_window(self):
        if self.filters is not None:
            try:
                if len(self.filters) > 0:
                    self.sidebar_window.add(self.filterbar_frame, minsize=200)
                    ttk.Label(self.filterbar_frame, text="Filters", font=('Helvetica', 11)).pack(side=tk.TOP, fill=tk.X, pady=2)
                    self.populate_filter_window()
                    self.filter_submit_button = ttk.Button(self.filterbar_frame, text='Add Filter', command=self.filter_data)
                    self.filter_submit_button.pack(pady=15)
                    self.status_var.set('Successfully added filter window')
                else:
                    self.status_var.set("No Filters Set")
            except Exception as e:
                self.status_var.set(f'Error while adding Filter window: {e}')
        else:
            self.status_var.set("No Filters Set")

    def populate_filter_window(self):
        if self.filters is not None:
            if len(self.filters) > 0:
                for widget in self.filterbar_frame.winfo_children():
                    widget.destroy()
                self.col_filters = []
                for filter in self.filters:
                    ttk.Label(self.filterbar_frame, text=f'{filter}:').pack(side=tk.TOP, fill=tk.X)
                    new_entry = ttk.Entry(self.filterbar_frame)
                    new_entry.pack(pady=5)
                    self.col_filters.append([filter, new_entry])
            else:
                self.status_var.set("No Filters Set")
        #self.filterbar_frame
        else:
            self.status_var.set("No Filters Set")

    def filter_data(self):
        filter_info = []
        if self.col_filters is not None:
            for i in self.col_filters:
                info = i[1].get()
                filter_info.append([i[0], info])
            df = self.data[3].copy() # Copy original data
            numerics = df.select_dtypes(include=['number']).columns
            for i in filter_info:
                if i[0] in numerics[0]:
                    settings = i[1].split(" ")
                    if len(settings) > 1:
                        for k in settings:
                            if k not in [">", "<", "="]:
                                k = float(k)
                        for k in range(0, len(settings)):
                            print(settings[k])
                            if settings[k] in ["<"]:
                                if k + 1 < len(settings):
                                    # less than
                                    value = float(settings[k + 1])
                                    df = df[df[i[0]] < value]
                            if settings[k] in [">"]:
                                if k + 1 < len(settings):
                                    # greator than
                                    value = float(settings[k + 1])
                                    df = df[df[i[0]] > value]
                                    print(df.head())
                            if settings[k] in ["="]:
                                if k + 1 < len(settings):
                                    value = float(settings[k + 1])
                                    df = df[df[i[0]] == value]
                                    print(df.head())
            self.data[2] = df
            self.plot()

    def log_transform(self):
        if self.data is not None:
            try:
                df = self.data[2]
                self.data[3] = df #backup original data
                # Numeric columns
                numerics = df.select_dtypes(include=['number']).columns
                df[numerics] = np.log(df[numerics])
                self.data[2] = df
                self.plot()

            except Exception as e:
                self.status_var.set(f"Error in Log Transformation: {e}")
        else:
            self.status_var.set("No data available to transform")

    def plot(self):
        match self.current_plot:
            case 0:
                self.display_data()
            case 1:
                self.plot_graph()
    
    def remove_data(self):
        try:
            selected_index = self.list_of_data.curselection()
            dataName = self.list_of_data.selection_get()
            if selected_index:
                self.list_of_data.delete(selected_index)
                for i in self.loaded_data:
                    if i[0] == dataName:
                        self.loaded_data.remove(i)
                        if i == self.data:
                            self.data = None
                            self.plot_graph_button.pack_forget() #hide button
                            for widget in self.graph_frame.winfo_children():
                                widget.destroy()

                self.status_var.set(f"Successfully removed {dataName}")
        except Exception as e:
            self.status_var.set(f"Error: {e}")

    def save_file(self):
        if self.data is not None:
            try:
                self.data[2].to_csv(self.data[1], index=False)
                self.status_var.set(f"Successfully saved file: {self.data[0]}")
            except Exception as e:
                self.status_var.set(f"Failed to save file, Error: {e}")

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if file_path:
            try:
                df = pd.read_csv(file_path)  # Save DataFrame to class attribute
                data = [file_path.split('/')[-1], file_path, df, df] #second df is backup for original data
                if len(self.loaded_data) > 0:
                    for i in self.loaded_data:
                        if i[2].equals(df) != False:
                            if i[0] == data[0]:
                                data[0] = f'Copy - {data[0]}'
                                self.status_var.set("Loaded identical dataset under new name")
                self.status_var.set(f"Loaded {file_path}")
                self.loaded_data.append(data)
                self.list_of_data.insert(tk.END, data[0])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
                self.status_var.set("Failed to load file")

    def display_data(self):
        if self.data is not None:
            if self.current_plot != 0:
                self.current_plot = 0
            try:
                df = self.data[2]
                # Clear any previous content in the graph_frame
                for widget in self.graph_frame.winfo_children():
                    widget.destroy()
                
                # Create a Treeview widget
                columns = list(df.columns)
                if self.filters is not None:
                    if (self.x_col is None or self.y_col is None) or (self.x_col not in columns or self.y_col not in columns) or any(i not in columns for i in self.filters):
                        self.ask_for_columns()
                    columns = self.filters
                tree = ttk.Treeview(self.graph_frame, columns=columns, show='headings')

                # Define heading and column widths
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=100, anchor=tk.CENTER)

                # Insert data into the treeview
                for index, row in df.iterrows():
                    tree.insert("", tk.END, values=list(row))

                # Pack the treeview to fill the graph view
                tree.pack(fill=tk.BOTH, expand=True)

                self.status_var.set("Table displayed successfully")
            except Exception as e:
                self.status_var.set(f"Error in displaying table: {e}")
        else:
            self.status_var.set("No data available to display")

    def ask_for_columns(self):
        if self.data is not None:
            # Create a new top-level window
            col_selector = tk.Toplevel(self)
            col_selector.title("Select Plot Settings")
            col_selector.geometry("800x400")

            # Get the list of columns
            columns = list(self.data[2].columns)

            # Column Filter
            tk.Label(col_selector, text="Filter by Columns:").pack(pady=5)
            checks = []
            col_filters = []
            for i in range(len(columns)):
                n = columns[i]
                col_var = tk.IntVar()  # Create an IntVar for each column
                col_filters.append([col_var, n])  # Append the IntVar and column name to the list
                checks.append(ttk.Checkbutton(col_selector, text=n, variable=col_var))
            for i in checks:
                i.pack(pady=2)
                

            # X-axis column selection
            tk.Label(col_selector, text="Select X-axis column:").pack(pady=5)
            x_combobox = ttk.Combobox(col_selector, values=columns)
            x_combobox.pack(pady=5)
            x_combobox.current(0)  # Set default selection

            # Y-axis column selection
            tk.Label(col_selector, text="Select Y-axis column:").pack(pady=5)
            y_combobox = ttk.Combobox(col_selector, values=columns)
            y_combobox.pack(pady=5)
            y_combobox.current(1)  # Set default selection

            def on_select():
                x_col = x_combobox.get()
                y_col = y_combobox.get()
                filters = []
                for i in col_filters:
                    val = i[0].get()
                    if val:
                        filters.append(i[1])

                if x_col in columns and y_col in columns:
                    col_selector.destroy()  # Close the selector window
                    self.y_col = y_col
                    self.x_col = x_col
                    self.set_filters(filters)
                    self.plot()
                else:
                    messagebox.showerror("Error", "Invalid column selection")

            # Submit button
            submit_button = ttk.Button(col_selector, text="Submit", command=on_select)
            submit_button.pack(pady=20)

            col_selector.grab_set()  # Make the window modal

    def plot_graph(self):
        if self.data is not None:
            if self.current_plot != 1:
                self.current_plot = 1
            try:
                df = self.data[2]
                columns = list(df.columns)
                if (self.x_col == None or self.y_col == None) or (self.x_col not in columns or self.x_col not in columns) or any(i not in columns for i in self.filters):
                    self.ask_for_columns()
                # for i in self.filters:
                #     if i not in columns:
                #         self.ask_for_columns()

                fig = Figure(dpi=100)
                ax = fig.add_subplot(111)
                ax.plot(df[self.x_col], df[self.y_col], marker='o')
                ax.set_title('Data Plot')
                ax.set_xlabel(self.x_col)
                ax.set_ylabel(self.y_col)

                for widget in self.graph_frame.winfo_children():
                    widget.destroy()

                # Create a new canvas and place it in graph_frame
                canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
                canvas.draw()

                # Get the widget from the canvas and pack it with expand options
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)

                # Optional: resize the plot whenever the window is resized
                def on_resize(event):
                    canvas_widget.configure(width=event.width-20, height=event.height-20)
                    canvas.draw()

                self.graph_frame.bind("<Configure>", on_resize)

                self.status_var.set("Successfully plotted data")
            except Exception as e:
                self.status_var.set(f"Error in plotting data: {e}")
        else:
            self.status_var.set("Failed to plot data")

if __name__ == "__main__":
    app = DataVisApp()
    app.mainloop()