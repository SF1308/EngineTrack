from engine_model import EngineModel
import tkinter as tk
from tkinter import ttk
import time

if __name__ == "__main__":
    engine = EngineModel()
    
    root = tk.Tk()
    root.title("EngineTrack - Simulador de Conducción Virtual")

    # Simulation parameters
    delta_time = 0.1  # Simulation time step in seconds
    throttle_level = 0.0
    brake_level = 0.0
    
    #input controls
    throttle_label = tk.Label(root, text="Acelerador:")
    throttle_scale = tk.Scale(root, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="Posición")
    throttle_scale.set(throttle_level)  # Set initial value of the slider

    brake_label = tk.Label(root, text="Brake:")
    brake_scale = tk.Scale(root, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="Pressure", command=lambda value: globals().update(brake_level=float(value)))
    brake_scale.set(brake_level) # Set initial value of the slider

    gear_up_button = tk.Button(root, text="Subir Marcha")
    gear_down_button = tk.Button(root, text="Bajar Marcha")
    gear_label = tk.Label(root, text="Marcha: 0")

    throttle_label.pack()
    throttle_scale.pack()
    brake_label.pack()
    brake_scale.pack()
    gear_label.pack()
    gear_up_button.pack()
    gear_down_button.pack()

    # Output indicator (RPM, Torque, Temperatura)
    rpm_label = tk.Label(root, text="RPM: 0")
    torque_label = tk.Label(root, text="Torque: 0.0")
    temp_label = tk.Label(root, text="Temperatura: 20 °C")

    rpm_label.pack()
    torque_label.pack()
    temp_label.pack()

    #Simulation loop 
    def update_simulation():
        engine.update_rpm(throttle_level, engine.current_gear)
        engine.calculate_torque(throttle_level)
        engine.update_temperature(delta_time)

        rpm_label.config(text=f"RPM: {engine.rpm:.2f}")
        torque_label.config(text=f"Torque: {engine.torque:.2f}")
        temp_label.config(text=f"Temperature: {engine.temperature:.2f} °C")

        root.after(int(delta_time * 1000), update_simulation)

    update_simulation()
    root.mainloop()
    # Main loop to update the simulation
    # delta_time = 0.1  # Time step in seconds      