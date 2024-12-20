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

        # Determine dolomite rate based on current soil pH
        if ph < 4.5:
            # Calculate the amount of dolomite needed to raise pH to 4.5
            # This is a simplified approach; actual requirements may vary
            dolomite_rate = (4.5 - ph) * 1000  # Example calculation
        else:
            dolomite_rate = 0  # No application needed if pH is optimal

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
