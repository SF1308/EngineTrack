from engine_model import EngineModel
import tkinter as tk
from tkinter import ttk
import time
from engine_model import EngineModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

if __name__ == "__main__":
    engine = EngineModel()

    root = tk.Tk()
    root.title("EngineTrack - Simulador de Conducción Virtual")

    # Simulation parameters
    delta_time = 0.1  # Simulation time step in seconds
    throttle_level = 0.0
    brake_level = 0.0

    # Matplotlib figures
    fig_rpm, ax_rpm = plt.subplots()
    ax_rpm.set_xlabel("Tiempo (s)")
    ax_rpm.set_ylabel("RPM")
    ax_rpm.set_title("RPM del Motor")
    rpm_line, = ax_rpm.plot([], [])

    fig_torque, ax_torque = plt.subplots()
    ax_torque.set_xlabel("Tiempo (s)")
    ax_torque.set_ylabel("Torque")
    ax_torque.set_title("Torque del Motor")
    torque_line, = ax_torque.plot([], [])

    fig_temp, ax_temp = plt.subplots()
    ax_temp.set_xlabel("Tiempo (s)")
    ax_temp.set_ylabel("Temperatura (°C)")
    ax_temp.set_title("Temperatura del Motor")
    temp_line, = ax_temp.plot([], [])

    # Initialize the plot datasets
    canvas_rpm = FigureCanvasTkAgg(fig_rpm, master=root)
    canvas_rpm_widget = canvas_rpm.get_tk_widget()
    canvas_rpm_widget.grid(row=0, column=0, padx=5, pady=5)  # Ubicar gráfico RPM

    canvas_torque = FigureCanvasTkAgg(fig_torque, master=root)
    canvas_torque_widget = canvas_torque.get_tk_widget()
    canvas_torque_widget.grid(row=0, column=1, padx=5, pady=5)  # Ubicar gráfico Torque

    canvas_temp = FigureCanvasTkAgg(fig_temp, master=root)
    canvas_temp_widget = canvas_temp.get_tk_widget()
    canvas_temp_widget.grid(row=0, column=2, padx=5, pady=5)  # Ubicar gráfico Temp

    # set up the plot data
    time_data = []
    rpm_data = []
    torque_data = []
    temp_data = []
    simulation_time = 0.0

    # input controls
    throttle_label = tk.Label(root, text="Acelerador:")
    throttle_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)  # Etiqueta Acelerador
    throttle_scale = tk.Scale(root, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="Posición",
                           command=lambda value: globals().update(throttle_level=float(value)))
    throttle_scale.set(throttle_level)  # Set initial value of the slider
    throttle_scale.grid(row=2, column=0, sticky="ew", padx=5, pady=5)  # Slider Acelerador

    brake_label = tk.Label(root, text="Freno:")
    brake_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)  # Etiqueta Freno
    brake_scale = tk.Scale(root, from_=0.0, to_=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="Pressure",
                         command=lambda value: globals().update(brake_level=float(value)))
    brake_scale.set(brake_level)  # Set initial value of the slider
    brake_scale.grid(row=2, column=1, sticky="ew", padx=5, pady=5)  # Slider Freno

    gear_label = tk.Label(root, text="Marcha: 0")
    gear_label.grid(row=1, column=2, sticky="w", padx=5, pady=5) # Etiqueta Marcha
    gear_up_button = tk.Button(root, text="Subir Marcha",
                              command=lambda: [setattr(engine, 'current_gear', engine.current_gear + 1),
                                               gear_label.config(text=f"Gear: {engine.current_gear}")])
    gear_up_button.grid(row=2, column=2, sticky="ew", padx=5, pady=5)  # Botón Subir Marcha
    gear_down_button = tk.Button(root, text="Bajar Marcha",
                                command=lambda: [setattr(engine, 'current_gear', max(0, engine.current_gear - 1)),
                                                 gear_label.config(text=f"Gear: {engine.current_gear}")])
    gear_down_button.grid(row=3, column=2, sticky="ew", padx=5, pady=5)  # Botón Bajar Marcha

    # Output indicator (RPM, Torque, Temperatura)
    rpm_label = tk.Label(root, text="RPM: 0")
    rpm_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)  # Etiqueta RPM
    torque_label = tk.Label(root, text="Torque: 0.0")
    torque_label.grid(row=3, column=1, sticky="w", padx=5, pady=5)  # Etiqueta Torque
    temp_label = tk.Label(root, text="Temperatura: 20 °C")
    temp_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)  # Etiqueta Temperatura

    # Simulation loop
    def update_simulation():
        engine.update_rpm(throttle_level, engine.current_gear)
        engine.calculate_torque(throttle_level)
        engine.update_temperature(delta_time)

        rpm_label.config(text=f"RPM: {engine.rpm:.2f}")
        torque_label.config(text=f"Torque: {engine.torque:.2f}")
        temp_label.config(text=f"Temperature: {engine.temperature:.2f} °C")

        global simulation_time
        simulation_time += delta_time

        time_data.append(simulation_time)
        rpm_data.append(engine.rpm)
        torque_data.append(engine.torque)
        temp_data.append(engine.temperature)

        # Update RPM graph
        ax_rpm.clear()
        ax_rpm.set_xlabel("Tiempo (s)")
        ax_rpm.set_ylabel("RPM")
        ax_rpm.set_title("RPM del Motor")
        ax_rpm.plot(time_data, rpm_data)
        canvas_rpm.draw()

        # Update Torque graph
        ax_torque.clear()
        ax_torque.set_xlabel("Tiempo (s)")
        ax_torque.set_ylabel("Torque")
        ax_torque.set_title("Torque del Motor")
        ax_torque.plot(time_data, torque_data)
        canvas_torque.draw()

        # Update Temperature graph
        ax_temp.clear()
        ax_temp.set_xlabel("Tiempo (s)")
        ax_temp.set_ylabel("Temperatura (°C)")
        ax_temp.set_title("Temperatura del Motor")
        ax_temp.plot(time_data, temp_data)
        canvas_temp.draw()

        root.after(int(delta_time * 1000), update_simulation)  # Corregido: Una sola llamada

    update_simulation()
    root.mainloop()
    # Main loop to update the simulation
    # delta_time = 0.1  # Time step in seconds