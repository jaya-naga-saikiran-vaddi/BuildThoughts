CREATE TABLE health_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_date DATE NOT NULL UNIQUE,
    water_liters FLOAT,
    sleep_hours FLOAT,
    steps_walked INT,
    calories INT,
    mood VARCHAR(50)
);
