import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

# Define the Excel file
FILE_NAME = "test_requests.xlsx"

# Check if file exists, if not create it with headers
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(
        columns=["Test Type", "Measurement Tool", "Polarisers", "Voltage (V)", "Expected Value", "Deadline", "Notes"])
    df.to_excel(FILE_NAME, index=False)


# Function to save request
def save_request():
    test_type = "Transmittance"
    tool = tool_var.get()
    polarisers = polarisers_var.get()
    voltage = voltage_entry.get()
    expected_value = expected_entry.get()
    deadline = deadline_entry.get()
    notes = notes_entry.get()

    # Validate inputs
    if not tool or not voltage or not deadline:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    # Load existing data
    df = pd.read_excel(FILE_NAME)

    # Append new data
    new_entry = pd.DataFrame({
        "Test Type": [test_type],
        "Measurement Tool": [tool],
        "Polarisers": [polarisers],
        "Voltage (V)": [voltage],
        "Expected Value": [expected_value],
        "Deadline": [deadline],
        "Notes": [notes]
    })

    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_excel(FILE_NAME, index=False)
    messagebox.showinfo("Success", "Test request saved successfully!")
    root.destroy()


# Create GUI
root = tk.Tk()
root.title("Test Request Form")

# Dropdown for measurement tool
ttk.Label(root, text="Select Measurement Tool:").grid(row=0, column=0, padx=10, pady=5)
tool_var = ttk.Combobox(root, values=["Tool A", "Tool B", "Tool C"], state="readonly")
tool_var.grid(row=0, column=1, padx=10, pady=5)

# Dropdown for polarisers
ttk.Label(root, text="Use Polarisers:").grid(row=1, column=0, padx=10, pady=5)
polarisers_var = ttk.Combobox(root, values=["Yes", "No"], state="readonly")
polarisers_var.grid(row=1, column=1, padx=10, pady=5)

# Voltage input
ttk.Label(root, text="Voltage (V):").grid(row=2, column=0, padx=10, pady=5)
voltage_entry = ttk.Entry(root)
voltage_entry.grid(row=2, column=1, padx=10, pady=5)

# Expected Value input
ttk.Label(root, text="Expected Value:").grid(row=3, column=0, padx=10, pady=5)
expected_entry = ttk.Entry(root)
expected_entry.grid(row=3, column=1, padx=10, pady=5)

# Deadline input
ttk.Label(root, text="Deadline (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
deadline_entry = ttk.Entry(root)
deadline_entry.grid(row=4, column=1, padx=10, pady=5)

# Notes input
ttk.Label(root, text="Notes:").grid(row=5, column=0, padx=10, pady=5)
notes_entry = ttk.Entry(root)
notes_entry.grid(row=5, column=1, padx=10, pady=5)

# Save button
submit_btn = ttk.Button(root, text="Submit Request", command=save_request)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
