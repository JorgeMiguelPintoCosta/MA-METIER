-- Script SQL pour la base de données de détection de drones
-- Base de données PostgreSQL

-- Table Drones
-- Stocke les informations sur les drones détectés
CREATE TABLE IF NOT EXISTS Drones (
    ID SERIAL PRIMARY KEY,
    drone_type TEXT NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Signal_events
-- Stocke les événements de signal associés aux drones
CREATE TABLE IF NOT EXISTS Signal_events (
    ID SERIAL PRIMARY KEY,
    ID_Drones INT NOT NULL REFERENCES Drones(ID),
    signal_strength INT,
    approx_distance INT,
    relative_power REAL,
    bandwidth REAL,
    score INT,
    detection_time REAL
);

-- Table Alerts
-- Stocke les alertes générées par le système
CREATE TABLE IF NOT EXISTS Alerts (
    ID SERIAL PRIMARY KEY,
    level TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour améliorer les performances des requêtes
CREATE INDEX IF NOT EXISTS idx_drones_detected_at ON Drones(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_signal_events_drone_id ON Signal_events(ID_Drones);
CREATE INDEX IF NOT EXISTS idx_alerts_level ON Alerts(level);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON Alerts(created_at DESC);
