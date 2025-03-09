from flask import Flask, request, render_template
import pyodbc

app = Flask(__name__)

# 1. Display the form at the root path
@app.route('/', methods=['GET'])
def index():
    # This references "index.html" if you put the above HTML in `templates/index.html`
    return render_template('index2.html')

# 2. Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Gather form data:
    field1 = request.form.get('field1')
    field2 = request.form.get('field2')

    # 3. Connect to your SQL Server database:
    #    Adjust DRIVER, SERVER, DATABASE, UID, PWD, etc. as needed.
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=FETRI\SQLFETRI;"  # e.g. DESKTOP-ABC\SQLEXPRESS
        "DATABASE=YourDatabaseName;"
        "UID=YourUserName;"  # Omit if using Trusted_Connection
        "PWD=YourPassword;"  # Omit if using Trusted_Connection
        "Trusted_Connection=no;" # or yes, depending on your setup
    )

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # 4. Perform the INSERT
        insert_query = "INSERT INTO YourTable (Column1, Column2) VALUES (?, ?);"
        cursor.execute(insert_query, (field1, field2))

        conn.commit()
        cursor.close()
        conn.close()

        return "Data successfully inserted!"
    except Exception as e:
        # In a production app, handle/log errors more gracefully
        return f"Error: {str(e)}"

if __name__ == '__main__':
    # 5. Run the Flask development server
    app.run(debug=True)
