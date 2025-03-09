
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os
import uuid
import webbrowser




app = Flask(__name__)
FILE_NAME = "test_requests.xlsx"

# Check if file exists, if not create it with headers
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Request ID", "Test Type", "Instance ID", "Polarisers Type", "Polarisers Lamination",
                               "Number of Polarisers", "Orientation of Pol1", "Orientation of Cell Alignment Axis",
                               "Orientation of Pol2", "Voltage Range", "Voltage Single Point", "Voltage Sweep",
                               "Tool Setup", "Tool Angle of Incidence", "Sample Number",  "Cell structure", "Notes"])
    df.to_excel(FILE_NAME, index=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    request_id = str(uuid.uuid4())  # Generate a unique ID for the test request
    data = request.get_json()  # Get JSON data from request

    batch_id = data.get("batch_id", "")
    project = data.get("project", "")
    deadline = data.get("deadline", "")
    notes = data.get("notes", "")
    test_instances = data.get("test_instances", [])

    if not test_instances:
        return jsonify({"error": "No test instances provided"}), 400

    df = pd.read_excel(FILE_NAME)

    for instance in test_instances:
        instance_id = str(uuid.uuid4())  # Unique ID for each test instance
        new_entry = pd.DataFrame({
            "Request ID": [request_id],
            "Batch ID": [batch_id],
            "Project": [project],
            "Deadline": [deadline],
            "Notes": [notes],
            "Test Type": [instance.get("test_type", "")],
            "Instance ID": [instance_id],
            "Polarisers Type": [instance.get("polarisers_type", "")],
            "Polarisers Lamination": [instance.get("polarisers_lamination", "")],
            "Number of Polarisers": [instance.get("polarisers_number", "")],
            "Orientation of Pol1": [instance.get("polarisers_pol1", "")],
            "Orientation of Cell Alignment Axis": [instance.get("polarisers_cell_alignment", "")],
            "Orientation of Pol2": [instance.get("polarisers_pol2", "")],
            "Voltage Range": [instance.get("voltage_range", "")],
            "Voltage Single Point": [instance.get("voltage_single_point", "")],
            "Voltage Sweep": [instance.get("voltage_sweep", "")],
            "Tool Selection": [instance.get("tool_selection", "")],
            "Sample Number": [instance.get("sample_number", "")],
            "Cell Structure": [instance.get("cell_structure", "")]
        })
        df = pd.concat([df, new_entry], ignore_index=True)

    df.to_excel(FILE_NAME, index=False)
    return jsonify({"message": "Test request submitted successfully", "request_id": request_id})



@app.route('/requests')
def view_requests():
    df = pd.read_excel(FILE_NAME)
    return df.to_html()


if __name__ == '__main__':

        from threading import Timer
        Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
        app.run(debug=False)

