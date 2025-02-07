from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os
import uuid

app = Flask(__name__)
FILE_NAME = "test_requests.xlsx"

# Check if file exists, if not create it with headers
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Request ID", "Test Type", "Instance ID", "Voltage", "Polarisers", "Cell Orientation",
                               "Polariser Number", "State of Cell", "Tool", "Notes"])
    df.to_excel(FILE_NAME, index=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    request_id = str(uuid.uuid4())  # Generate a unique ID for the test request
    test_instances = request.json.get("test_instances", [])

    if not test_instances:
        return jsonify({"error": "No test instances provided"}), 400

    df = pd.read_excel(FILE_NAME)

    for instance in test_instances:
        instance_id = str(uuid.uuid4())  # Unique ID for each test instance
        new_entry = pd.DataFrame({
            "Request ID": [request_id],
            "Test Type": [instance.get("test_type", "")],
            "Instance ID": [instance_id],
            "Voltage": [instance.get("voltage", "")],
            "Polarisers": [instance.get("polarisers", "")],
            "Cell Orientation": [instance.get("cell_orientation", "")],
            "Polariser Number": [instance.get("polariser_number", "")],
            "State of Cell": [instance.get("state_of_cell", "")],
            "Tool": [instance.get("tool", "")],
            "Notes": [instance.get("notes", "")]
        })
        df = pd.concat([df, new_entry], ignore_index=True)

    df.to_excel(FILE_NAME, index=False)
    return jsonify({"message": "Test request submitted successfully", "request_id": request_id})


@app.route('/requests')
def view_requests():
    df = pd.read_excel(FILE_NAME)
    return df.to_html()


if __name__ == '__main__':
    app.run(debug=True)
