# SMART PARKING GARAGE SIMULATION

# tkinter is used to create the graphical user interface 
import tkinter as tk

# ttk gives access to advanced widgets like Treeview tables
#ttk provides themed widgets
# messagebox creates popup error windows
from tkinter import ttk, messagebox

# datetime allows the program to track exact entry times
#calculate parking duration
#determine peak pricing hours
from datetime import datetime

# ABC and abstractmethod are used to create an abstract base class
#Imports tools for abstract classes.
#ABC - Allows Vehicle to become a parent template class.
#abstractmethod - Forces subclasses to create required methods.
#every vehicle MUST define calculate_fee()
from abc import ABC, abstractmethod

# pickle allows Python objects to be saved into a file
import pickle

# os helps check if save files already exist
#helps-checking if save files exist
import os


# Vehicle is the parent class for all vehicle types.
# Since every vehicle shares common features,
# inheritance makes the program more organized.
#Creates the Vehicle class.
#This class inherits from: ABC, making it an abstract base class
class Vehicle(ABC):

    # This constructor runs whenever a new vehicle object is created.
    #self - the object itself
    #license_plate - vehicle identifier
    #is_vip=False - optional VIP status
    def __init__(self, license_plate, is_vip=False):

        # Stores the vehicle's license plate number inside the object.
        self.license_plate = license_plate

        # Saves the exact time the vehicle entered the garage
        self.entry_time = datetime.now()

        # Default type before subclasses overwrite it
        #Sets a default type.
        self.vehicle_type = "Vehicle"

        # Tracks whether the vehicle has VIP status
        #Stores whether the vehicle is VIP.
        #This will later be used for discounts, GUI display, and special pricing.
        self.is_vip = is_vip

    # Every subclass has to create its own calculate_fee method, because we have changes in the price rate.
    # Needed for polymorphism.
    #Marks the next method as abstract.
    @abstractmethod
    def calculate_fee(self):
        pass

    # Creates a method to calculate parking duration.
    # Calculates how long the vehicle has been parked.
    def get_duration(self):

        # Finds the difference between current time and entry time
        duration = datetime.now() - self.entry_time

        # Converts seconds into hours
        hours = duration.total_seconds() / 3600

        # Rounds to 2 decimal places for cleaner output
        return round(hours, 2)

    # Checks whether the current time falls during peak hours.
    #Creates a method to determine if peak pricing should apply.
    def is_peak_hour(self):

        # I used military time
        #Gets only the hour portion of current time.
        current_hour = datetime.now().hour

        # Peak hours are from 5 PM to 8 PM
        #True if between 5 PM and 8 PM
        return 17 <= current_hour <= 20

    # Applies dynamic pricing rules.
    # Peak hours increase prices and VIP vehicles receive discounts.
    #Creates pricing modification method.
    # takes the base fee and then applies peak pricing and VIP discount
    def apply_special_pricing(self, fee):

        # Peak hour pricing multiplier
        #Checks if current time is peak hour.
        if self.is_peak_hour():
            fee *= 1.5

        # VIP vehicles receive 20% off
        #Checks VIP status.
        #Applies 20% discount.
        if self.is_vip:
            fee *= 0.8

        return round(fee, 2)
        #I set it to return the final fee rounded to 2 decimals.

    # Controls how the object prints when displayed.
    #Python needs this to print readable memory addresses
    def __str__(self):

        # Converts VIP status into readable text
        #Uses a ternary operator.
        vip_text = "VIP" if self.is_vip else "Regular"

        return (
            #displays Car, Truck, or Motorcycle
            f"{self.vehicle_type} | "
            #Displays license plate
            f"Plate: {self.license_plate} | "
            #Displays parked duration
            f"Hours Parked: {self.get_duration()} | "
            #Displays VIP Status
            f"{vip_text}"
        )


# Car inherits from Vehicle.
# Cars use the standard parking rate.
#Creates Car subclass - inherents from Vehicle 
#automatically gains the entry time, duration logic, VIP logic, and printing logic
class Car(Vehicle):
    def __init__(self, license_plate, is_vip=False):

        # Calls the constructor from the parent Vehicle class
        #Calls the parent constructor - initializes the license plate, entry time, and VIP Status
        super().__init__(license_plate, is_vip)

        # Sets the specific vehicle type
        #Overwrite the default type
        self.vehicle_type = "Car"

    # Cars calculate fees differently than other vehicle types.
    def calculate_fee(self):

        # Cars cost $2 per hour
        fee = self.get_duration() * 2

        # Applies VIP discounts and peak hour pricing before returning the fee
        return self.apply_special_pricing(fee)

# Truck inherits from Vehicle.
# Trucks have higher rates because they take up more space.
class Truck(Vehicle):
    def __init__(self, license_plate, is_vip=False):

        super().__init__(license_plate, is_vip)
        self.vehicle_type = "Truck"
        
    # Trucks override calculate_fee using their own pricing.
    def calculate_fee(self):

        # Trucks cost $3.50 per hour
        fee = self.get_duration() * 3.5
        return self.apply_special_pricing(fee)

# Motorcycles use lower parking rates.
class Motorcycle(Vehicle):

    def __init__(self, license_plate, is_vip=False):

        # Calls the constructor from the parent Vehicle class
        #Calls the parent constructor - initializes the license plate, entry time, and VIP Status
        super().__init__(license_plate, is_vip)

        #sets type
        self.vehicle_type = "Motorcycle"

    # Motorcycles calculate fees using a cheaper rate.
    def calculate_fee(self):

        # Motorcycles cost $1 per hour
        fee = self.get_duration() * 1

        return self.apply_special_pricing(fee)

# ParkingGarage acts as the main control center for the program.
# It manages all vehicles currently parked.
class ParkingGarage:
    def __init__(self):

        # Dictionary storage:
        # key = license plate
        # value = vehicle object
        self.vehicles = {}

        # Loads previously saved garage data when program starts
        self.load_data()

    # Handles vehicle check-in.
    def check_in(self, plate, vehicle_type, is_vip=False):

        # Removes spaces and standardizes capitalization
        plate = plate.strip().upper()

        # Prevents empty plate entries
        if plate == "":
            raise ValueError("License plate cannot be empty.")

        # Prevents duplicate vehicles from entering
        if plate in self.vehicles:
            raise ValueError("Vehicle is already parked.")

        # Creates the correct object based on vehicle type
        if vehicle_type == "Car":
            vehicle = Car(plate, is_vip)
        elif vehicle_type == "Truck":
            vehicle = Truck(plate, is_vip)
        elif vehicle_type == "Motorcycle":
            vehicle = Motorcycle(plate, is_vip)
        else:
            raise ValueError("Invalid vehicle type.")

        # Stores the object in the dictionary
        self.vehicles[plate] = vehicle

        # Saves updated data immediately
        self.save_data()

    # Handles vehicle checkout.
    def check_out(self, plate):
        plate = plate.strip().upper()

        # Prevents checkout of vehicles not in garage
        if plate not in self.vehicles:
            raise ValueError("Vehicle not found.")

        # Removes and returns the vehicle object
        vehicle = self.vehicles.pop(plate)

        # Polymorphism automatically calls the correct fee method
        fee = vehicle.calculate_fee()

        # Saves updated garage state
        self.save_data()
        return vehicle, fee

    # Saves garage data into a pickle file.
    def save_data(self):
        try:
            # "wb" means write binary
            with open("garage_data.pkl", "wb") as file:

                # pickle.dump serializes the dictionary
                pickle.dump(self.vehicles, file)
        except Exception as e:

            # Displays popup error instead of crashing
            messagebox.showerror("Save Error", str(e))

    # Loads saved garage data back into the program.
    def load_data(self):
        try:

            # Prevents errors if file doesn't exist yet
            if os.path.exists("garage_data.pkl"):

                # "rb" means read binary
                with open("garage_data.pkl", "rb") as file:

                    # Restores the dictionary from file
                    self.vehicles = pickle.load(file)
            else:
                self.vehicles = {}
        except Exception:

            # Starts with empty dictionary if file is corrupted
            self.vehicles = {}

    # Returns only vehicles matching the selected type.
    def filter_by_type(self, vehicle_type):
        return [
            vehicle
            for vehicle in self.vehicles.values()
            if vehicle.vehicle_type == vehicle_type
        ]

    # Finds vehicles parked longer than a specified number of hours.
    def parked_longer_than(self, hours):
        return [
            vehicle
            for vehicle in self.vehicles.values()
            if vehicle.get_duration() > hours
        ]

# Creates the main garage object used throughout the program.
garage = ParkingGarage()

import tkinter as tk

    ttk.Button(self.center_frame, text="Check In", command=check_in, style="Dark.TButton").pack(side=tk.LEFT, padx=5)

# These functions connect the GUI directly
# to the ParkingGarage backend logic.


def check_in():

    try:

        # Gets license plate from entry box
        plate = app.vehicle_entry.get()

        # Gets selected vehicle type
        vehicle_type = app.status_dropdown.get()

        # Gets VIP checkbox state
        is_vip = app.confirm_var.get()

        # Calls backend garage check-in method
        garage.check_in(

            plate,

            vehicle_type,

            is_vip
        )

        # Updates status label
        app.update_status(
            f"{plate.upper()} checked in successfully."
        )

        # Refresh inventory display
        refresh_inventory()

    except Exception as e:

        # Prevents GUI crashes
        app.update_status(str(e))


def check_out():

    try:

        # Gets entered plate number
        plate = app.vehicle_entry.get()

        # Calls backend checkout method
        vehicle, fee = garage.check_out(plate)

        # Displays checkout fee
        app.update_status(
            f"{plate.upper()} checked out. Total Fee: ${fee}"
        )

        # Updates inventory after checkout
        refresh_inventory()

    except Exception as e:

        app.update_status(str(e))


def view_all():

    # Displays all parked vehicles
    refresh_inventory()

    app.update_status("Showing all parked vehicles.")


def show_trucks():

    # Shows only truck objects
    refresh_inventory(vehicle_type="Truck")

    app.update_status("Showing only trucks.")


def parked_hours():

    # Shows vehicles parked longer than 1 hour
    refresh_inventory(hours_filter=1)

    app.update_status(
        "Showing vehicles parked longer than 1 hour."
    )


# Drop-down option placeholders
# These placeholder functions represent each dropdown choice.
# They currently return 0, and can later be connected to real Vehicle Class meber functions.
def car_option():
    return "Car"

def truck_option():
    return "Truck"

def motorcycle_option():
    return "Motorcycle"

# Checkbox state placeholder
#  check whether the VIP checkbox is selected.
def checkbox_state():

    # Returns checkbox state safely
    if hasattr(app, "confirm_var"):

        return app.confirm_var.get()

    return False


# Inventory display placeholder functions -----------------------------------------------------

# Refreshes inventory columns using backend vehicle data
def refresh_inventory(vehicle_type=None, hours_filter=None):

    # Clears previous inventory labels safely
    for frame in [app.column1, app.column2, app.column3, app.column4]:

        widgets = frame.winfo_children()

        # Keeps title label but removes old data
        for widget in widgets[1:]:

            widget.destroy()

    # Gets all vehicles from garage
    vehicles = list(garage.vehicles.values())

    # Filters by vehicle type if selected
    if vehicle_type:

        vehicles = [

            vehicle

            for vehicle in vehicles

            if vehicle.vehicle_type == vehicle_type
        ]

    # Filters by parked hours if selected
    if hours_filter is not None:

        vehicles = [

            vehicle

            for vehicle in vehicles

            if vehicle.get_duration() > hours_filter
        ]

    # Displays message if garage empty
    if len(vehicles) == 0:

        ttk.Label(
            app.column1,
            text="No Vehicles",
            style="Dark.TLabel"
        ).pack(anchor=tk.N, pady=(10, 0))

        return

    # Displays updated inventory data
    for vehicle in vehicles:

        ttk.Label(
            app.column1,
            text=vehicle.license_plate,
            style="Dark.TLabel"
        ).pack(anchor=tk.N, pady=2)

        ttk.Label(
            app.column2,
            text=vehicle.vehicle_type,
            style="Dark.TLabel"
        ).pack(anchor=tk.N, pady=2)

        ttk.Label(
            app.column3,
            text=f"{vehicle.get_duration()} hrs",
            style="Dark.TLabel"
        ).pack(anchor=tk.N, pady=2)

        ttk.Label(
            app.column4,
            text="VIP" if vehicle.is_vip else "Regular",
            style="Dark.TLabel"
        ).pack(anchor=tk.N, pady=2)


def show_license_plate_inventory():

    refresh_inventory()


def show_vehicle_type_inventory():

    refresh_inventory()


def show_hours_parked_inventory():

    refresh_inventory()


def show_vip_status_inventory():

    refresh_inventory()


class GUI:
    def __init__(self):
        # Initialize the main application window
        self.root = tk.Tk()
        self.root.title("Doug & London Intelligent Parking :P")
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

        # Added button style so buttons fully match dark theme
        self.style.configure(
            "Dark.TButton",
            background="black",
            foreground="white"
        )

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

        ttk.Button(
    self.center_frame,
    text="Search",
    command=view_all,
    style="Dark.TButton"
).pack(side=tk.LEFT, padx=5)
    
        ttk.Button(self.center_frame, text="Show Trucks", command=show_trucks, style="Dark.TButton").pack(side=tk.LEFT, padx=5)
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
            text="Welcome To Doug & London Intelligent Parking :D",
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

        ttk.Label(
            self.column1,
            text="License Plates",
            font=("Segoe UI", 12, "bold"),
            style="Dark.TLabel"
        ).pack(anchor=tk.N)

        # Vertical border between column 1 and column 2
        self.col_border1 = tk.Frame(self.inventory_frame, width=2, bg="purple")
        self.col_border1.pack(side=tk.LEFT, fill=tk.Y, pady=5)

        # Column 2: Vehicle Types
        # Vehicle type inventory is shown here.
        self.column2 = ttk.Frame(self.inventory_frame, style="Dark.TFrame", padding=(10, 10))
        self.column2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        ttk.Label(
            self.column2,
            text="Vehicle Types",
            font=("Segoe UI", 12, "bold"),
            style="Dark.TLabel"
        ).pack(anchor=tk.N)

        # Vertical border between column 2 and column 3
        self.col_border2 = tk.Frame(self.inventory_frame, width=2, bg="purple")
        self.col_border2.pack(side=tk.LEFT, fill=tk.Y, pady=5)

        # Column 3: Hours Parked
        # Hours parked inventory is shown here.
        self.column3 = ttk.Frame(self.inventory_frame, style="Dark.TFrame", padding=(10, 10))
        self.column3.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        ttk.Label(
            self.column3,
            text="Hours Parked",
            font=("Segoe UI", 12, "bold"),
            style="Dark.TLabel"
        ).pack(anchor=tk.N)

        # Vertical border between column 3 and column 4
        self.col_border3 = tk.Frame(self.inventory_frame, width=2, bg="purple")
        self.col_border3.pack(side=tk.LEFT, fill=tk.Y, pady=5)

        # Column 4: VIP Statuses
        # VIP status inventory is shown here.
        self.column4 = ttk.Frame(self.inventory_frame, style="Dark.TFrame", padding=(10, 10))
        self.column4.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        ttk.Label(
            self.column4,
            text="VIP Statuses",
            font=("Segoe UI", 12, "bold"),
            style="Dark.TLabel"
        ).pack(anchor=tk.N)

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

        try:

            # Enter key now triggers check-in automatically
            check_in()

        except Exception as e:

            self.update_status(str(e))

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
            text="Join Our Monthly Subscription to become a lookcrative Doug & London Intelligent Parking VIP :)",
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

    # Waits for tkinter to fully initialize before refreshing inventory
    app.root.after(100, refresh_inventory)

    app.run() # actually runs the appp and keeps it running
