CREATE TABLE hospitals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lat FLOAT NOT NULL,
    lng FLOAT NOT NULL,
    capacity INT NOT NULL,
    available_beds INT NOT NULL,
    specialty VARCHAR(100)
);

CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_type VARCHAR(50) NOT NULL, -- Ambulance, Firetruck, Police
    status VARCHAR(50) NOT NULL, -- Available, Dispatched, Maintenance
    lat FLOAT NOT NULL,
    lng FLOAT NOT NULL,
    current_case_id VARCHAR(255) -- Connects to MongoDB case ID or a postgres uuid
);

CREATE TABLE routing_logs (
    id SERIAL PRIMARY KEY,
    case_id VARCHAR(255) NOT NULL,
    vehicle_id INT REFERENCES vehicles(id),
    hospital_id INT REFERENCES hospitals(id),
    start_lat FLOAT NOT NULL,
    start_lng FLOAT NOT NULL,
    end_lat FLOAT NOT NULL,
    end_lng FLOAT NOT NULL,
    estimated_time INT NOT NULL, -- in seconds
    route_geometry TEXT, -- JSON string or encoded polyline
    dispatched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert dummy data for hospitals
INSERT INTO hospitals (name, lat, lng, capacity, available_beds, specialty) VALUES
('City General Hospital', 40.7128, -74.0060, 500, 45, 'General'),
('Trauma Center One', 40.7580, -73.9855, 200, 12, 'Trauma'),
('St. Jude Medical', 40.7829, -73.9654, 300, 80, 'Pediatrics');

-- Insert dummy data for vehicles (e.g. Ambulances scattered around)
INSERT INTO vehicles (vehicle_type, status, lat, lng) VALUES
('Ambulance', 'Available', 40.7300, -73.9950),
('Ambulance', 'Available', 40.7400, -73.9800),
('Firetruck', 'Available', 40.7100, -74.0100),
('Police Car', 'Available', 40.7500, -73.9900),
('Ambulance', 'Maintenance', 40.7800, -73.9700);
