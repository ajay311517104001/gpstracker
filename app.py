from flask import Flask, request, jsonify
import pandas as pd
from waitress import serve  # Use waitress for Windows

app = Flask(__name__)
EXCEL_FILE = "gps_data.xlsx"

@app.route('/send_gps', methods=['POST'])
def receive_gps():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    # Save GPS data to Excel
    df = pd.DataFrame([[latitude, longitude, pd.Timestamp.now()]], columns=["Latitude", "Longitude", "Timestamp"])
    try:
        with pd.ExcelWriter(EXCEL_FILE, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets["Sheet1"].max_row)
    except:
        df.to_excel(EXCEL_FILE, index=False)

    return jsonify({"status": "success", "latitude": latitude, "longitude": longitude})

if __name__ == '__main__':
    print("Running Flask server with Waitress on port 5000...")
    serve(app, host="0.0.0.0", port=5000)  # Use Waitress instead of Gunicorn
