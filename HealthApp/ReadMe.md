Flask Health App

![health app flow](https://github.com/user-attachments/assets/30825d36-3951-4560-beca-7a632009fc55)


CREATE TABLE health_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_date DATE NOT NULL UNIQUE,
    water_liters FLOAT,
    sleep_hours FLOAT,
    steps_walked INT,
    calories INT,
    mood VARCHAR(50)
);
