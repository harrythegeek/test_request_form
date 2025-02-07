from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

"this is a comment for git"

app = Flask(__name__)
FILE_NAME = "test_requests.xlsx"

# Check if file exists, if not create it with headers
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(
        columns=["Request ID", "Test Type", "Deadline", "Notes", "Measurement Tool (Images)", "Voltage (Images)",
                 "Expected Value (Images)", "Polarisers (Images)", "Cell Orientation", "Polariser Number",
                 "State of Cell", "Measurement Tool (Test B)", "Voltage (Test B)", "Expected Value (Test B)",
                 "Test B Field 1", "Test B Field 2", "Measurement Tool (Test C)", "Voltage (Test C)",
                 "Expected Value (Test C)", "Test C Field 1", "Test C Field 2"])
    df.to_excel(FILE_NAME, index=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    deadline = request.form.get("deadline")
    notes = request.form.get("notes")

    tool_images = request.form.get("tool_images")
    voltage_images = request.form.get("voltage_images")
    expected_value_images = request.form.get("expected_value_images")
    polarisers_images = request.form.get("polarisers_images")
    cell_orientation = request.form.get("cell_orientation")
    polariser_number = request.form.get("polariser_number")
    state_of_cell = request.form.get("state_of_cell")

    tool_b = request.form.get("tool_b")
    voltage_b = request.form.get("voltage_b")
    expected_value_b = request.form.get("expected_value_b")
    test_b_field1 = request.form.get("test_b_field1")
    test_b_field2 = request.form.get("test_b_field2")

    tool_c = request.form.get("tool_c")
    voltage_c = request.form.get("voltage_c")
    expected_value_c = request.form.get("expected_value_c")
    test_c_field1 = request.form.get("test_c_field1")
    test_c_field2 = request.form.get("test_c_field2")

    if not deadline:
        return "Error: Please fill in the required fields."

    df = pd.read_excel(FILE_NAME)
    request_id = len(df) + 1
    new_entry = pd.DataFrame({
        "Request ID": [request_id],
        "Test Type": ["Transmittance"],
        "Deadline": [deadline],
        "Notes": [notes],
        "Measurement Tool (Images)": [tool_images],
        "Voltage (Images)": [voltage_images],
        "Expected Value (Images)": [expected_value_images],
        "Polarisers (Images)": [polarisers_images],
        "Cell Orientation": [cell_orientation],
        "Polariser Number": [polariser_number],
        "State of Cell": [state_of_cell],
        "Measurement Tool (Test B)": [tool_b],
        "Voltage (Test B)": [voltage_b],
        "Expected Value (Test B)": [expected_value_b],
        "Test B Field 1": [test_b_field1],
        "Test B Field 2": [test_b_field2],
        "Measurement Tool (Test C)": [tool_c],
        "Voltage (Test C)": [voltage_c],
        "Expected Value (Test C)": [expected_value_c],
        "Test C Field 1": [test_c_field1],
        "Test C Field 2": [test_c_field2]
    })
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_excel(FILE_NAME, index=False)

    return redirect(url_for('index'))


@app.route('/requests')
def view_requests():
    df = pd.read_excel(FILE_NAME)
    return df.to_html()


if __name__ == '__main__':
    app.run(debug=True)
