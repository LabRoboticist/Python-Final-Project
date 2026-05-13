import tkinter as tk
from tkinter import ttk




#---------------------------------------------------INSERT CLASS METHODS HERE---------------------------------------------------#        ttk.Button(self.center_frame, text="Check In", command=check_in, style="Dark.TButton").pack(side=tk.LEFT, padx=5)

def check_in():
    pass

def check_out():
    pass

def view_all():
    pass

def show_tracks():
    pass

def parked_hours():
    pass

# Drop-down option placeholders
# These placeholder functions represent each dropdown choice.
# They currently return 0, and can later be connected to real Vehicle Class meber functions.
def car_option():
    return 0

def truck_option():
    return 0

def motorcycle_option():
    return 0

# Checkbox state placeholder
#  check whether the VIP checkbox is selected.
def checkbox_state():
    return 0 # technically should be 1 because it returns if it is selected

# Inventory display placeholder functions -----------------------------------------------------
def show_license_plate_inventory():
    pass

def show_vehicle_type_inventory():
    pass

def show_hours_parked_inventory():
    pass

def show_vip_status_inventory():
    pass

class GUI:
    def __init__(self):
        # Initialize the main application window
        self.root = tk.Tk()
        self.root.title("Doug the dougster's app :P")
        self.root.geometry("800x600")  # Set the window dimensions to 800x600 pixels
        self.root.resizable(False, False)  # Disable manual window resizing

        # Set up the UI structure + keybinds
        self.create_style()
        self.create_bottom_button_bar()
        self.create_frames()
        self.create_widgets()
        self.create_bindings() # keybinds thingy

    def create_style(self): # BABY css function
        # Configure dark mode for the root window and ttk widgets
        self.root.configure(bg="black") # bacjground black 
        self.style = ttk.Style(self.root) # object to set dark modes for widgets
        self.style.theme_use("default") # Other themese are doodoo stkinky and just sad 
        self.style.configure("Dark.TFrame", background="black")
        self.style.configure("Dark.TLabel", background="black", foreground="white")
        self.style.configure("Dark.TCheckbutton", background="black", foreground="white")
        # self.style.configure("Dark.TButton", background="black", foreground="white")
        self.style.map(
            "Dark.TButton",
            foreground=[("active", "white")],
            background=[("active", "purple")],
        )
        self.style.map(
            "Dark.TCheckbutton",
            foreground=[("active", "white")],
            background=[("active", "purple")],
        )

    def create_bottom_button_bar(self): # sudo menu bar at the bottom of the screen
        # Bottom separator border line above the button bar
        self.bottom_separator = tk.Frame(self.root, height=2, bg="purple")
        self.bottom_separator.pack(side=tk.BOTTOM, fill=tk.X)

        self.button_bar = ttk.Frame(self.root, style="Dark.TFrame")
        self.button_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.center_frame = ttk.Frame(self.button_bar, style="Dark.TFrame")
        self.center_frame.pack(anchor=tk.CENTER, pady=5)

        ttk.Button(self.center_frame, text="Check In", command=check_in, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(self.center_frame, text="Check Out", command=check_out, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(self.center_frame, text="View All", command=view_all, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(self.center_frame, text="SHow Tracks", command=show_tracks, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(self.center_frame, text="Parked > Hours", command=parked_hours, style="Dark.TButton").pack(side=tk.LEFT, padx=5)

        # VIP prompt below the bottom button menu
        self.vip_prompt_frame = ttk.Frame(self.button_bar, style="Dark.TFrame")
        self.vip_prompt_frame.pack(anchor=tk.CENTER, pady=(5, 8))

        ttk.Label(
            self.vip_prompt_frame,
            text="If NOT a VIP click this box",
            style="Dark.TLabel",
        ).pack(side=tk.LEFT)

        self.not_vip_var = tk.BooleanVar(value=False)
        self.not_vip_var.trace_add("write", self.on_not_vip_toggled)
        ttk.Checkbutton(
            self.vip_prompt_frame,
            variable=self.not_vip_var,
            text="",
            command=checkbox_state,
            style="Dark.TCheckbutton",
        ).pack(side=tk.LEFT, padx=(5, 0))

    def create_frames(self):
        # Main content frame for the app widgets
        self.main_frame = ttk.Frame(self.root, padding=10, style="Dark.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Status frame for the status text label at the bottom
        self.status_frame = ttk.Frame(self.root, padding=(10, 5), style="Dark.TFrame")
        self.status_frame.pack(fill=tk.X)

    def create_widgets(self):
        # Title label shown in the main frame
        self.title_label = ttk.Label(
            self.main_frame,
            text="Welcome To the dougster's garage :D",
            font=("Segoe UI", 16),
            style="Dark.TLabel",
        )
        self.title_label.pack(pady=(0, 10))

        # Under title text "prapgraph" with all the widgets inside--------------------------------------- #
        self.sentence_frame = ttk.Frame(self.main_frame, style="Dark.TFrame") # dark mode
        self.sentence_frame.pack(anchor=tk.CENTER, pady=(0, 15))

        # License plate [ENTRY]
        ttk.Label(self.sentence_frame, text="License Plate:", style="Dark.TLabel").pack(side=tk.LEFT)
        self.vehicle_entry = ttk.Entry(self.sentence_frame, width=12)
        self.vehicle_entry.pack(side=tk.LEFT, padx=(5, 15))

        # Vehicle Type [DROPDOWN Menu]
        ttk.Label(self.sentence_frame, text="Vehicle Type:", style="Dark.TLabel").pack(side=tk.LEFT)
        self.status_dropdown = ttk.Combobox(
            self.sentence_frame,
            values=["Car", "Truck", "Motorcycle"],
            width=12,
            state="readonly",
        )
        self.status_dropdown.current(0)
        self.status_dropdown.pack(side=tk.LEFT, padx=(5, 15))

        self.confirm_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.sentence_frame,
            text="VIP Vehicle [Check if true]",
            variable=self.confirm_var,
            style="Dark.TCheckbutton",
        ).pack(side=tk.LEFT, padx=(5, 15))

        # Paragraph / sentence separator border
        self.paragraph_separator = tk.Frame(self.main_frame, height=2, bg="purple")
        self.paragraph_separator.pack(fill=tk.X, padx=10, pady=(0, 15))

        # Inventory columns block with internal purple borders between each column
        self.inventory_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.inventory_frame.pack(anchor=tk.CENTER, pady=(0, 15), padx=10)

        # Column 1: License Plates
        # Vehicle license plate inventory is shown here.
        self.column1 = ttk.Frame(self.inventory_frame, style="Dark.TFrame", padding=(10, 10))
        self.column1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        ttk.Label(self.column1, text="License Plates", font=("Segoe UI", 12, "bold"), style="Dark.TLabel").pack(anchor=tk.N)
        ttk.Label(self.column1, text="[data goes here]", style="Dark.TLabel").pack(anchor=tk.N, pady=(10, 0))

        # Vertical border between column 1 and column 2
        self.col_border1 = tk.Frame(self.inventory_frame, width=2, bg="purple")
        self.col_border1.pack(side=tk.LEFT, fill=tk.Y, pady=5)

        # Column 2: Vehicle Types
        # Vehicle type inventory is shown here.
        self.column2 = ttk.Frame(self.inventory_frame, style="Dark.TFrame", padding=(10, 10))
        self.column2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        ttk.Label(self.column2, text="Vehicle Types", font=("Segoe UI", 12, "bold"), style="Dark.TLabel").pack(anchor=tk.N)
        ttk.Label(self.column2, text="[data goes here]", style="Dark.TLabel").pack(anchor=tk.N, pady=(10, 0))

        # Vertical border between column 2 and column 3
        self.col_border2 = tk.Frame(self.inventory_frame, width=2, bg="purple")
        self.col_border2.pack(side=tk.LEFT, fill=tk.Y, pady=5)

        # Column 3: Hours Parked
        # Hours parked inventory is shown here.
        self.column3 = ttk.Frame(self.inventory_frame, style="Dark.TFrame", padding=(10, 10))
        self.column3.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        ttk.Label(self.column3, text="Hours Parked", font=("Segoe UI", 12, "bold"), style="Dark.TLabel").pack(anchor=tk.N)
        ttk.Label(self.column3, text="[data goes here]", style="Dark.TLabel").pack(anchor=tk.N, pady=(10, 0))

        # Vertical border between column 3 and column 4
        self.col_border3 = tk.Frame(self.inventory_frame, width=2, bg="purple")
        self.col_border3.pack(side=tk.LEFT, fill=tk.Y, pady=5)

        # Column 4: VIP Statuses
        # VIP status inventory is shown here.
        self.column4 = ttk.Frame(self.inventory_frame, style="Dark.TFrame", padding=(10, 10))
        self.column4.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        ttk.Label(self.column4, text="VIP Statuses", font=("Segoe UI", 12, "bold"), style="Dark.TLabel").pack(anchor=tk.N)
        ttk.Label(self.column4, text="[data goes here]", style="Dark.TLabel").pack(anchor=tk.N, pady=(10, 0))

        # Status label inside the status frame
        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready",
            anchor=tk.W,
            style="Dark.TLabel",
        )
        self.status_label.pack(fill=tk.X)

    def create_bindings(self):
        # Bind the Enter key to a handler method
        self.root.bind("<Return>", self.on_enter_pressed)

    def on_new(self):
        # Handle the File > New menu selection
        self.update_status("New action triggered")

    def on_exit(self):
        # Quit the tkinter application
        self.root.quit()

    # def on_button_click(self):
    #     # Handle the button click event
    #     self.update_status("Button clicked")

    def on_enter_pressed(self, event=None):
        # Handle pressing Enter on the keyboard
        self.update_status("Enter pressed")

    def update_status(self, message: str):
        # Change the status label text to the provided message
        self.status_label.config(text=message)

    def on_not_vip_toggled(self, *args):
        # Open or close the VIP confirmation popup when the checkbox changes.
        if self.not_vip_var.get():
            self.show_vip_popup()
        elif hasattr(self, "vip_popup") and self.vip_popup is not None:
            self.vip_popup.destroy()
            self.vip_popup = None

    def show_vip_popup(self):
        # Small popup shown after clicking the NOT VIP checkbox.
        if hasattr(self, "vip_popup") and self.vip_popup is not None:
            return

        self.vip_popup = tk.Toplevel(self.root)
        self.vip_popup.title("VIP Confirmation")
        self.vip_popup.configure(bg="black")
        self.vip_popup.resizable(False, False)
        self.vip_popup.geometry("330x140")
        self.vip_popup.transient(self.root)
        self.vip_popup.grab_set()
        self.vip_popup.protocol("WM_DELETE_WINDOW", self.close_vip_popup)

        popup_frame = ttk.Frame(self.vip_popup, padding=10, style="Dark.TFrame")
        popup_frame.pack(fill=tk.BOTH, expand=True)

        # Close button to exit and uncheck the parent checkbox
        ttk.Button(
            popup_frame,
            text="X",
            width=3,
            command=self.close_vip_popup,
            style="Dark.TButton",
        ).pack(anchor=tk.NE)

        # Bold green subscription text inside the popup
        popup_message = ttk.Label(
            popup_frame,
            text="Join Our Monthly Subscription to become a lookcrative dougstrer VIP :)",
            font=("Segoe UI", 10, "bold"),
            foreground="lime",
            background="black",
            style="Dark.TLabel",
            wraplength=240,
            justify=tk.LEFT,
        )
        popup_message.pack(anchor=tk.W, pady=(5, 10))

        # Second popup checkbox uses the same global command function.
        popup_confirm_frame = ttk.Frame(popup_frame, style="Dark.TFrame")
        popup_confirm_frame.pack(fill=tk.X)

        ttk.Label(
            popup_confirm_frame,
            text="Just Check THIS BOX to confirm -->",
            style="Dark.TLabel",
        ).pack(side=tk.LEFT)

        self.vip_confirm_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            popup_confirm_frame,
            variable=self.vip_confirm_var,
            text="",
            command=checkbox_state,
            style="Dark.TCheckbutton",
        ).pack(side=tk.LEFT, padx=(5, 0))

    def close_vip_popup(self):
        # Close popup and uncheck the NOT VIP checkbox.
        self.not_vip_var.set(False)
        if hasattr(self, "vip_popup") and self.vip_popup is not None:
            self.vip_popup.destroy()
            self.vip_popup = None

    def run(self):
        # Start the tkinter event loop
        self.root.mainloop()

# Run the GUI only when this file is executed directly
if __name__ == "__main__":
    app = GUI()
    app.run() # actually runs the appp and keeps it running