class EngineModel:
    def __init__(self):
        self.rpm = 0.0
        self.torque = 0.0
        self.temperature = 20.0
        self.current_gear = 0

    def update_rpm(self, throttle, current_gear):
        max_rpm = 8000
        rpm_increment_base = 50 * throttle

        gear_multiplier = [0.5, 1.0, 0.8, 0.6, 0.5]  # Simple example
        if 0 <= current_gear < len(gear_multiplier):
            self.rpm += rpm_increment_base * gear_multiplier[current_gear]
        else:
            self.rpm += rpm_increment_base * 0.2  # Neutral or invalid gear

        self.rpm = max(0.0, min(self.rpm, max_rpm))

    def calculate_torque(self, throttle):
        max_torque = 200
        self.torque = max_torque * throttle * (1 - (self.rpm / 7000))  # Very simple example

    def update_temperature(self, delta_time):
        if self.rpm > 1000:
            self.temperature += 0.1 * delta_time
        else:
            self.temperature -= 0.05 * delta_time
        self.temperature = max(20.0, min(self.temperature, 120.0))


    def update_throttle(value):
        global throttle_level  # Declare throttle_level as global to modify it
        throttle_level = float(value)

        throttle_scale = tk.Scale(root, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="Posición", command=update_throttle)
        throttle_level = throttle_scale.get() # Get the initial value

    def update_brake(value):
        global brake_level
        brake_level = float(value)

        brake_scale = tk.Scale(root, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="Presión", command=update_brake)
        brake_level = brake_scale.get() # Get the initial value

    def gear_up():
        engine.current_gear += 1
        gear_label.config(text=f"Marcha: {engine.current_gear}")

    def gear_down():
        engine.current_gear = max(0, engine.current_gear - 1)
        gear_label.config(text=f"Marcha: {engine.current_gear}")

        gear_up_button.config(command=gear_up)
        gear_down_button.config(command=gear_down)