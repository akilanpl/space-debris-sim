import tkinter as tk
from tkinter import ttk, messagebox
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ..core.simulation import Simulation
from ..core.data_manager import DataManager

class MainWindow:
    def __init__(self, root: tk.Tk, config):
        self.root = root
        self.config = config
        self.root.title("Space Debris — Mission")
        self.root.geometry("1100x680")

        # simulation core
        self.sim = Simulation(config, log_callback=self._log)
        self.data_manager = DataManager()

        # UI state
        self.running = False
        self._build_ui()
        self._log("Mission GUI ready. Start when prepared.")

    def _build_ui(self):
        pane = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        pane.pack(fill="both", expand=True)

        left = ttk.Frame(pane, padding=8)
        right = ttk.Frame(pane, padding=8)
        pane.add(left, weight=1)
        pane.add(right, weight=3)

        # Left panel: mission info + controls
        info = ttk.Label(
            left,
            text=(
                f"Commander: {self.config.commander}\n"
                f"Rocket: {self.config.rocket_name}\n"
                f"Orbit: {self.config.orbit_range_km} km\n"
                f"Launch site: {self.config.space_station}, {self.config.country}"
            ),
            justify="left"
        )
        info.pack(anchor="w", pady=6)

        ctrl = ttk.LabelFrame(left, text="Controls")
        ctrl.pack(fill="x", pady=(8, 10))
        self.start_btn = ttk.Button(ctrl, text="Start", command=self._start)
        self.start_btn.pack(fill="x", pady=6)
        self.stop_btn = ttk.Button(ctrl, text="Pause", command=self._stop, state="disabled")
        self.stop_btn.pack(fill="x", pady=6)
        self.export_btn = ttk.Button(ctrl, text="Export telemetry", command=self._export, state="disabled")
        self.export_btn.pack(fill="x", pady=6)
        self.show_thrusters_btn = ttk.Button(
            ctrl, text="Show thruster loads", command=self._show_thrusters, state="disabled"
        )
        self.show_thrusters_btn.pack(fill="x", pady=6)

        # Legend
        legend = ttk.LabelFrame(left, text="Legend")
        legend.pack(fill="both", expand=True, pady=(8, 0))
        ttk.Label(
            legend,
            text=(
                "Phases:\n  prelaunch → ascent → collection → return\n"
                "Telemetry: temperature, avg thruster speed\n"
                "Use export to save CSV for analysis."
            ),
            wraplength=220,
            justify="left"
        ).pack(anchor="w", pady=6)

        # Right panel: log + plots
        log_frame = ttk.LabelFrame(right, text="Mission Log")
        log_frame.pack(fill="both", expand=True)
        self.log_text = tk.Text(log_frame, height=12, state="disabled", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, side="left")
        ttk.Scrollbar(log_frame, command=self.log_text.yview, orient="vertical").pack(side="right", fill="y")
        self.log_text["yscrollcommand"] = lambda *args: None

        # Telemetry plots
        plot_frame = ttk.LabelFrame(right, text="Telemetry")
        plot_frame.pack(fill="both", expand=True, pady=(8, 0))
        self.fig = Figure(figsize=(7, 4), dpi=100)
        self.ax_temp = self.fig.add_subplot(211)
        self.ax_spd = self.fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _log(self, message: str):
        ts = time.strftime("%H:%M:%S")
        text = f"[{ts}] {message}\n"
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _start(self):
        if self.running:
            return
        self.running = True
        self.sim.reset()
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.export_btn.configure(state="disabled")
        self.show_thrusters_btn.configure(state="disabled")
        self._log("Mission start requested.")
        self._tick()

    def _stop(self):
        if not self.running:
            return
        self.running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.export_btn.configure(state="normal")
        self._log("Mission paused by operator.")

    def _tick(self):
        # run one simulation step and update UI
        if not self.running:
            return
        self.sim.step()
        # update plots
        t_axis = self.sim.time_axis
        temps = self.sim.temperature_values
        speeds = self.sim.avg_speed_values

        self.ax_temp.clear()
        self.ax_spd.clear()
        self.ax_temp.plot(t_axis, temps, marker="o")
        self.ax_temp.set_ylabel("Temperature (°C)")
        self.ax_temp.grid(True, linestyle=":")
        self.ax_spd.plot(t_axis, speeds, marker="o")
        self.ax_spd.set_ylabel("Avg thruster speed (m/s)")
        self.ax_spd.set_xlabel("Time step")
        self.ax_spd.grid(True, linestyle=":")
        self.fig.tight_layout()
        self.canvas.draw()

        # phase transitions enable other controls
        if self.sim.phase == "collection" and self.sim.thrusters_deployed:
            # while collecting, show thruster view disabled; enable when finished
            pass
        if self.sim.phase == "return" and self.sim.collection_done:
            self.show_thrusters_btn.configure(state="normal")
            self.export_btn.configure(state="normal")

        # schedule next tick
        self.root.after(500, self._tick)

    def _export(self):
        fname = self.data_manager.export_session(self.sim)
        messagebox.showinfo("Export", f"Telemetry and debris exported to {fname}")

    def _show_thrusters(self):
        # open small window showing thruster mass & breakdown
        win = tk.Toplevel(self.root)
        win.title("Thruster loads")
        win.geometry("520x360")
        frm = ttk.Frame(win, padding=8)
        frm.pack(fill="both", expand=True)
        tree =
