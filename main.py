from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Serves the HTML frontend

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Retrieve data from the frontend
        ph = float(request.form['ph'])
        land_area = float(request.form['land_area'])
        area_unit = request.form['area_unit']
        elevation = request.form['elevation']

        # Convert land area to hectares
        if area_unit == "acres":
            land_area_hectares = land_area * 0.404686  # 1 acre = 0.404686 hectares
        elif area_unit == "perches":
            land_area_hectares = land_area * 0.002529  # 1 perch = 0.002529 hectares
        else:  # hectares
            land_area_hectares = land_area

        # Determine dolomite rate based on pH
        if ph < 3.9:
            dolomite_rate = 2500
        elif 3.9 <= ph < 4.2:
            dolomite_rate = 2000
        elif 4.2 <= ph < 4.5:
            dolomite_rate = 1500
        else:  # pH >= 4.5
            dolomite_rate = 1000

        # Adjust rate based on elevation
        if elevation == "low":
            dolomite_rate += 2000
        elif elevation == "mid":
            dolomite_rate += 3000
        elif elevation == "high":
            dolomite_rate += 4000

        # Calculate total dolomite
        total_dolomite = dolomite_rate * land_area_hectares

        # Return results as JSON
        return jsonify({
            "rate": f"{dolomite_rate} kg/ha",
            "total": f"{total_dolomite:.2f} kg"
        })

    except ValueError:
        return jsonify({"error": "Invalid input. Please enter numeric values."}), 400

if __name__ == '__main__':
    app.run(debug=True)
