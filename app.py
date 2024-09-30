from flask import Flask, render_template, jsonify, request
import sqlite3
import json
import os

app = Flask(__name__)

# Function to reverse coordinates for Leaflet.js compatibility
def reverse_coordinates(coords):
    return [[lat, lon] for lon, lat, _ in coords]

# Function to get filtered coordinates from the database for car_01
def get_car_01_coordinates():
    conn = sqlite3.connect('filtered_coordinates.db')  # Connect to the filtered database
    cursor = conn.cursor()

    # Fetch car_01 coordinates
    cursor.execute("""
        SELECT latitude, longitude, timestamp 
        FROM coordinates 
        WHERE device_id = 'car_01'
        ORDER BY timestamp ASC
    """)
    car_01_data = cursor.fetchall()
    conn.close()

    # Return only the first 5000 rows for smoother animation
    return car_01_data[:5000]


# Function to get all unique cars from the database
def get_all_cars():
    conn = sqlite3.connect('filtered_coordinates.db')  # Connect to the filtered database
    cursor = conn.cursor()

    # Fetch all unique cars (device_id)
    cursor.execute("SELECT DISTINCT device_id FROM coordinates")
    cars = cursor.fetchall()
    conn.close()

    return [car[0] for car in cars]  # List of car ids (device_id)

# Function to get coordinates for a specific car
def get_car_coordinates(car_id):
    conn = sqlite3.connect('filtered_coordinates.db')  # Connect to the filtered database
    cursor = conn.cursor()

    # Fetch car coordinates by device_id
    cursor.execute("""
        SELECT latitude, longitude, timestamp 
        FROM coordinates 
        WHERE device_id = ?
        ORDER BY timestamp ASC
    """, (car_id,))
    car_data = cursor.fetchall()
    conn.close()

    return car_data[:5000]  # Limit the number of rows for smoother animation


# Route for the simulation of all cars
@app.route('/simulation')
def simulation():
    # New track polygon coordinates from the KML file
    track_polygon_coords = reverse_coordinates([
        [-122.6970419, 45.5957071, 0], [-122.6893068, 45.5936127, 0], [-122.6889849, 45.5936503, 0],
        [-122.6884163, 45.5936127, 0], [-122.6880408, 45.5936878, 0], [-122.6877726, 45.5939806, 0],
        [-122.6879013, 45.5942959, 0], [-122.6880837, 45.5946187, 0], [-122.6884378, 45.5950091, 0],
        [-122.6887274, 45.5951592, 0], [-122.6891673, 45.5952343, 0], [-122.6895214, 45.5953094, 0],
        [-122.6897252, 45.595452, 0], [-122.6905835, 45.5962703, 0], [-122.6921821, 45.5976891, 0],
        [-122.6939417, 45.5988714, 0], [-122.694462, 45.5991116, 0], [-122.6951862, 45.5993181, 0],
        [-122.6960552, 45.599487, 0], [-122.6963503, 45.5995057, 0], [-122.696817, 45.599487, 0],
        [-122.6974607, 45.5994907, 0], [-122.6977128, 45.5995395, 0], [-122.6986623, 45.5998285, 0],
        [-122.699231, 45.6000012, 0], [-122.6993597, 45.5999899, 0], [-122.6995046, 45.5999036, 0],
        [-122.6995314, 45.5997685, 0], [-122.6994187, 45.5986913, 0], [-122.6995099, 45.5983985, 0],
        [-122.6996655, 45.5981132, 0], [-122.6999176, 45.5979556, 0], [-122.7002717, 45.5978843, 0],
        [-122.7006253, 45.5979292, 0], [-122.7009901, 45.5982595, 0], [-122.7012262, 45.5985448, 0],
        [-122.7016768, 45.5987399, 0], [-122.7021274, 45.5987549, 0], [-122.702814, 45.5983946, 0],
        [-122.703093, 45.5980343, 0], [-122.7030715, 45.5975989, 0], [-122.7027926, 45.5972836, 0],
        [-122.6970419, 45.5957071, 0]
    ])

    # New camera polygons from the KML file
    camera_1_fence_coords = reverse_coordinates([
        [-122.6882533, 45.59542, 0], [-122.6895032, 45.5958892, 0], [-122.6899967, 45.595619, 0],
        [-122.6895246, 45.5952258, 0], [-122.6888058, 45.5947538, 0], [-122.6884665, 45.5943202, 0],
        [-122.6884095, 45.59414, 0], [-122.687395, 45.5944628, 0], [-122.6877061, 45.5950503, 0],
        [-122.6879582, 45.5952539, 0], [-122.6882533, 45.59542, 0]
    ])

    camera_2_fence_coords = reverse_coordinates([
        [-122.6887817, 45.5937647, 0], [-122.6885644, 45.5935076, 0], [-122.6880521, 45.5933593, 0],
        [-122.6875907, 45.5932673, 0], [-122.6873118, 45.5934156, 0], [-122.6870778, 45.5936417, 0],
        [-122.6870905, 45.5938078, 0], [-122.687395, 45.5944628, 0], [-122.6884095, 45.59414, 0],
        [-122.6887817, 45.5937647, 0]
    ])

    # Get all cars
    all_cars = get_all_cars()

    return render_template('simulation.html', 
                           track_polygon_coords=track_polygon_coords, 
                           camera_1_fence_coords=camera_1_fence_coords, 
                           camera_2_fence_coords=camera_2_fence_coords, 
                           cars=all_cars)

# API route to get coordinates for a specific car (used in JavaScript)
@app.route('/api/car_coordinates/<car_id>')
def car_coordinates(car_id):
    car_data = get_car_coordinates(car_id)
    return jsonify(car_data)

# Default route to show editable zones (Program 2)
@app.route('/')
def index():
    # New track polygon coordinates from the KML file
    track_polygon_coords = reverse_coordinates([
        [-122.6970419, 45.5957071, 0], [-122.6893068, 45.5936127, 0], [-122.6889849, 45.5936503, 0],
        [-122.6884163, 45.5936127, 0], [-122.6880408, 45.5936878, 0], [-122.6877726, 45.5939806, 0],
        [-122.6879013, 45.5942959, 0], [-122.6880837, 45.5946187, 0], [-122.6884378, 45.5950091, 0],
        [-122.6887274, 45.5951592, 0], [-122.6891673, 45.5952343, 0], [-122.6895214, 45.5953094, 0],
        [-122.6897252, 45.595452, 0], [-122.6905835, 45.5962703, 0], [-122.6921821, 45.5976891, 0],
        [-122.6939417, 45.5988714, 0], [-122.694462, 45.5991116, 0], [-122.6951862, 45.5993181, 0],
        [-122.6960552, 45.599487, 0], [-122.6963503, 45.5995057, 0], [-122.696817, 45.599487, 0],
        [-122.6974607, 45.5994907, 0], [-122.6977128, 45.5995395, 0], [-122.6986623, 45.5998285, 0],
        [-122.699231, 45.6000012, 0], [-122.6993597, 45.5999899, 0], [-122.6995046, 45.5999036, 0],
        [-122.6995314, 45.5997685, 0], [-122.6994187, 45.5986913, 0], [-122.6995099, 45.5983985, 0],
        [-122.6996655, 45.5981132, 0], [-122.6999176, 45.5979556, 0], [-122.7002717, 45.5978843, 0],
        [-122.7006253, 45.5979292, 0], [-122.7009901, 45.5982595, 0], [-122.7012262, 45.5985448, 0],
        [-122.7016768, 45.5987399, 0], [-122.7021274, 45.5987549, 0], [-122.702814, 45.5983946, 0],
        [-122.703093, 45.5980343, 0], [-122.7030715, 45.5975989, 0], [-122.7027926, 45.5972836, 0],
        [-122.6970419, 45.5957071, 0]
    ])

    # New camera polygons from the KML file
    camera_1_fence_coords = reverse_coordinates([
        [-122.6882533, 45.59542, 0], [-122.6895032, 45.5958892, 0], [-122.6899967, 45.595619, 0],
        [-122.6895246, 45.5952258, 0], [-122.6888058, 45.5947538, 0], [-122.6884665, 45.5943202, 0],
        [-122.6884095, 45.59414, 0], [-122.687395, 45.5944628, 0], [-122.6877061, 45.5950503, 0],
        [-122.6879582, 45.5952539, 0], [-122.6882533, 45.59542, 0]
    ])

    camera_2_fence_coords = reverse_coordinates([
        [-122.6887817, 45.5937647, 0], [-122.6885644, 45.5935076, 0], [-122.6880521, 45.5933593, 0],
        [-122.6875907, 45.5932673, 0], [-122.6873118, 45.5934156, 0], [-122.6870778, 45.5936417, 0],
        [-122.6870905, 45.5938078, 0], [-122.687395, 45.5944628, 0], [-122.6884095, 45.59414, 0],
        [-122.6887817, 45.5937647, 0]
    ])

    return render_template('index.html', 
                           track_polygon_coords=track_polygon_coords, 
                           camera_1_fence_coords=camera_1_fence_coords, 
                           camera_2_fence_coords=camera_2_fence_coords)

@app.route('/car_01_movement')
def car_01_movement():
    # New track polygon coordinates from the KML file
    track_polygon_coords = reverse_coordinates([
        [-122.6970419, 45.5957071, 0], [-122.6893068, 45.5936127, 0], [-122.6889849, 45.5936503, 0],
        [-122.6884163, 45.5936127, 0], [-122.6880408, 45.5936878, 0], [-122.6877726, 45.5939806, 0],
        [-122.6879013, 45.5942959, 0], [-122.6880837, 45.5946187, 0], [-122.6884378, 45.5950091, 0],
        [-122.6887274, 45.5951592, 0], [-122.6891673, 45.5952343, 0], [-122.6895214, 45.5953094, 0],
        [-122.6897252, 45.595452, 0], [-122.6905835, 45.5962703, 0], [-122.6921821, 45.5976891, 0],
        [-122.6939417, 45.5988714, 0], [-122.694462, 45.5991116, 0], [-122.6951862, 45.5993181, 0],
        [-122.6960552, 45.599487, 0], [-122.6963503, 45.5995057, 0], [-122.696817, 45.599487, 0],
        [-122.6974607, 45.5994907, 0], [-122.6977128, 45.5995395, 0], [-122.6986623, 45.5998285, 0],
        [-122.699231, 45.6000012, 0], [-122.6993597, 45.5999899, 0], [-122.6995046, 45.5999036, 0],
        [-122.6995314, 45.5997685, 0], [-122.6994187, 45.5986913, 0], [-122.6995099, 45.5983985, 0],
        [-122.6996655, 45.5981132, 0], [-122.6999176, 45.5979556, 0], [-122.7002717, 45.5978843, 0],
        [-122.7006253, 45.5979292, 0], [-122.7009901, 45.5982595, 0], [-122.7012262, 45.5985448, 0],
        [-122.7016768, 45.5987399, 0], [-122.7021274, 45.5987549, 0], [-122.702814, 45.5983946, 0],
        [-122.703093, 45.5980343, 0], [-122.7030715, 45.5975989, 0], [-122.7027926, 45.5972836, 0],
        [-122.6970419, 45.5957071, 0]
    ])

    # New camera polygons from the KML file
    camera_1_fence_coords = reverse_coordinates([
        [-122.6882533, 45.59542, 0], [-122.6895032, 45.5958892, 0], [-122.6899967, 45.595619, 0],
        [-122.6895246, 45.5952258, 0], [-122.6888058, 45.5947538, 0], [-122.6884665, 45.5943202, 0],
        [-122.6884095, 45.59414, 0], [-122.687395, 45.5944628, 0], [-122.6877061, 45.5950503, 0],
        [-122.6879582, 45.5952539, 0], [-122.6882533, 45.59542, 0]
    ])

    camera_2_fence_coords = reverse_coordinates([
        [-122.6887817, 45.5937647, 0], [-122.6885644, 45.5935076, 0], [-122.6880521, 45.5933593, 0],
        [-122.6875907, 45.5932673, 0], [-122.6873118, 45.5934156, 0], [-122.6870778, 45.5936417, 0],
        [-122.6870905, 45.5938078, 0], [-122.687395, 45.5944628, 0], [-122.6884095, 45.59414, 0],
        [-122.6887817, 45.5937647, 0]
    ])

    return render_template('car_simulation.html', 
                           track_polygon_coords=track_polygon_coords, 
                           camera_1_fence_coords=camera_1_fence_coords, 
                           camera_2_fence_coords=camera_2_fence_coords)

import json

@app.route('/save_zones', methods=['POST'])
def save_zones():
    data = request.json['zones']

    # Ensure the 'camera_zones' directory exists
    save_dir = 'camera_zones'
    os.makedirs(save_dir, exist_ok=True)

    # Create a unique file name
    file_name = f"camera_zone_{len(os.listdir(save_dir)) + 1}.json"
    file_path = os.path.join(save_dir, file_name)

    # Save the zone data as JSON
    with open(file_path, 'w') as f:
        json.dump(data, f)

    return jsonify({"status": "success", "file": file_name}), 200




@app.route('/load_zone/<filename>', methods=['GET'])
def load_zone(filename):
    file_path = os.path.join('camera_zones', filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        # Read the saved zone data as JSON
        with open(file_path, 'r') as f:
            zones = json.load(f)

        return jsonify({"zones": zones}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to get saved zone files
@app.route('/get_saved_zones', methods=['GET'])
def get_saved_zones():
    save_dir = 'camera_zones'
    files = os.listdir(save_dir)
    return jsonify({"files": files}), 200

# Route to delete a specific zone file
@app.route('/delete_zone/<filename>', methods=['DELETE'])
def delete_zone(filename):
    file_path = os.path.join('camera_zones', filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return jsonify({"success": True}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        return jsonify({"success": False, "error": "File not found"}), 404




# API endpoint to serve car_01 coordinates as JSON for simulation
@app.route('/api/car_01_movement_data')
def car_01_movement_data():
    car_01_coords = get_car_01_coordinates()
    return jsonify(car_01_coords)

if __name__ == '__main__':
    app.run(debug=True)