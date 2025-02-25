from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

EXCEL_FILE = "gps_data.xlsx"

# Ensure Excel file exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Latitude", "Longitude", "Timestamp"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "GPS Tracker API is running!"})

@app.route('/send_gps', methods=['POST'])
def receive_gps():
    try:
        data = request.json
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if latitude is None or longitude is None:
            return jsonify({"error": "Invalid GPS data"}), 400

        df = pd.DataFrame([[latitude, longitude, pd.Timestamp.now()]],
                          columns=["Latitude", "Longitude", "Timestamp"])
        
        with pd.ExcelWriter(EXCEL_FILE, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets["Sheet1"].max_row)

        return jsonify({"status": "success", "latitude": latitude, "longitude": longitude})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    from gunicorn.app.wsgiapp import run
    run()
