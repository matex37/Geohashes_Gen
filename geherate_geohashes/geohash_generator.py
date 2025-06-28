import tkinter as tk
from tkinter import ttk, messagebox
import pygeohash as pgh
import pandas as pd
import os

def start_geohash_gui():
    def generate_geohashes():
        try:
            # Get user inputs
            min_lat = float(entry_bottom_left_lat.get())
            min_lon = float(entry_bottom_left_lon.get())
            max_lat = float(entry_top_right_lat.get())
            max_lon = float(entry_top_right_lon.get())
            map_name = entry_map_name.get().strip()

            if not map_name:
                messagebox.showerror("Error", "Map name cannot be empty.")
                return

            if min_lat >= max_lat or min_lon >= max_lon:
                messagebox.showerror("Error", "Bottom left must be less than top right coordinates.")
                return

            # Set precision and step size
            precision = 5
            lat_step = 0.01
            lon_step = 0.01

            # Generate geohashes
            geohashes = set()
            lat = min_lat
            while lat <= max_lat:
                lon = min_lon
                while lon <= max_lon:
                    geohash = pgh.encode(lat, lon, precision=precision)
                    geohashes.add(geohash)
                    lon += lon_step
                lat += lat_step

            geohashes = sorted(list(geohashes))

            # Display in GUI output box
            output_text.delete(1.0, tk.END)
            for gh in geohashes:
                output_text.insert(tk.END, gh + "\n")

            # Excel file handling
            file_name = 'Geohash data.xlsx'

            if os.path.exists(file_name):
                df_existing = pd.read_excel(file_name)
            else:
                df_existing = pd.DataFrame()

            # Add geohashes as a new column
            df_new = pd.DataFrame({map_name: pd.Series(geohashes)})

            # Combine with existing data (side by side columns)
            df_combined = pd.concat([df_existing, df_new], axis=1)

            # Save to Excel
            df_combined.to_excel(file_name, index=False)

            messagebox.showinfo("Success", f"Geohashes added as column '{map_name}' in '{file_name}'")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_fields():
        """Reset all input fields and output box."""
        entry_bottom_left_lat.delete(0, tk.END)
        entry_bottom_left_lon.delete(0, tk.END)
        entry_top_right_lat.delete(0, tk.END)
        entry_top_right_lon.delete(0, tk.END)
        entry_map_name.delete(0, tk.END)
        output_text.delete(1.0, tk.END)

    # ----------------- GUI -----------------
    window = tk.Tk()
    window.title("Geohash Generator")

    # Labels and entries for bottom-left
    ttk.Label(window, text="Bottom Left Lat:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_bottom_left_lat = ttk.Entry(window)
    entry_bottom_left_lat.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="Bottom Left Long:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_bottom_left_lon = ttk.Entry(window)
    entry_bottom_left_lon.grid(row=1, column=1, padx=5, pady=5)

    # Labels and entries for top-right
    ttk.Label(window, text="Top Right Lat:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_top_right_lat = ttk.Entry(window)
    entry_top_right_lat.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(window, text="Top Right Long:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_top_right_lon = ttk.Entry(window)
    entry_top_right_lon.grid(row=3, column=1, padx=5, pady=5)

    # Map name
    ttk.Label(window, text="Map Name / Description:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    entry_map_name = ttk.Entry(window)
    entry_map_name.grid(row=4, column=1, padx=5, pady=5)

    # Buttons
    generate_button = ttk.Button(window, text="Generate & Save", command=generate_geohashes)
    generate_button.grid(row=5, column=0, padx=5, pady=10)

    reset_button = ttk.Button(window, text="Reset", command=reset_fields)
    reset_button.grid(row=5, column=1, padx=5, pady=10)

    # Output text box
    output_text = tk.Text(window, height=15, width=50)
    output_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    window.mainloop()
