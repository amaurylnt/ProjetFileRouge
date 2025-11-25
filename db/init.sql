CREATE TABLE IF NOT EXISTS cameras (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    status VARCHAR(10) NOT NULL CHECK (status IN ('UP', 'DOWN')),
    location VARCHAR(255)
);

INSERT INTO cameras (name, ip_address, status, location) VALUES
('Caméra Entrée Mairie', '10.0.10.11', 'UP', 'Mairie'),
('Caméra Parking Centre', '10.0.10.12', 'DOWN', 'Parking du centre'),
('Caméra École Primaire', '10.0.10.13', 'UP', 'École primaire'),
('Caméra Parc Municipal', '10.0.10.14', 'UP', 'Parc municipal');
