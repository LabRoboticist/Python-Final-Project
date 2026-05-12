
# SMART PARKING GARAGE SIMULATION
# Full Project Code

# IMPORTS

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from abc import ABC, abstractmethod
import pickle
import os

# ABSTRACT BASE CLASS


class Vehicle(ABC):

    def __init__(self, license_plate, is_vip=False):

        # unique plate number
        self.license_plate = license_plate

        # exact entry time
        self.entry_time = datetime.now()

        # default type (overwritten in subclasses)
        self.vehicle_type = "Vehicle"

        # VIP status for discount feature
        self.is_vip = is_vip

    # every subclass MUST make its own fee system
    @abstractmethod
    def calculate_fee(self):
        pass

    # calculates how long vehicle has been parked
    def get_duration(self):

        duration = datetime.now() - self.entry_time

        # convert seconds to hours
        hours = duration.total_seconds() / 3600

        return round(hours, 2)

    # checks if current time is peak hour
    def is_peak_hour(self):

        current_hour = datetime.now().hour

        # peak hours from 5 PM to 8 PM
        return 17 <= current_hour <= 20

    # applies VIP discount + peak pricing
    def apply_special_pricing(self, fee):

        # peak hour multiplier
        if self.is_peak_hour():
            fee *= 1.5

        # VIP discount
        if self.is_vip:
            fee *= 0.8

        return round(fee, 2)

    # clean print format
    def __str__(self):

        vip_text = "VIP" if self.is_vip else "Regular"

        return (
            f"{self.vehicle_type} | "
            f"Plate: {self.license_plate} | "
            f"Hours: {self.get_duration()} | "
            f"{vip_text}"
        )

