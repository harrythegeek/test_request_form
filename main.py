from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
FILE_NAME = "test_requests.xlsx"

# Check if file exists, if not create it with headers
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(
        columns=["Request ID", "Test Type", "Measurement Tool", "Polarisers", "Voltage (V)", "Expected Value",
                 "Deadline", "Notes"])
    df.to_excel(FILE_NAME, index=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    tool = request.form.get("tool")
    polarisers = request.form.get("polarisers")
    voltage = request.form.get("voltage")
    expected_value = request.form.get("expected_value")
    deadline = request.form.get("deadline")
    notes = request.form.get("notes")

    if not tool or not voltage or not deadline:
        return "Error: Please fill in all required fields."

    df = pd.read_excel(FILE_NAME)
    request_id = len(df) + 1
    new_entry = pd.DataFrame({
        "Request ID": [request_id],
        "Test Type": ["Transmittance"],
        "Measurement Tool": [tool],
        "Polarisers": [polarisers],
        "Voltage (V)": [voltage],
        "Expected Value": [expected_value],
        "Deadline": [deadline],
        "Notes": [notes]
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
