import tkinter as tk
from tkinter import ttk, messagebox
from ..core.models import MissionConfig
from .main_window import MainWindow

class MissionSetupWindow:
    COUNTRY_STATIONS = {
        "USA": ["Kennedy Space Center", "Vandenberg", "Wallops"],
        "India": ["Satish Dhawan", "Thumba"],
        "Russia": ["Baikonur", "Plesetsk", "Vostochny"],
        "China": ["Jiuquan", "Wenchang"],
        "Europe": ["Guiana Space Centre", "Esrange"]
    }

    def __init__(self, root: tk.Tk, commander: str):
        self.root = root
        self.commander = commander
        self._build()

    def _build(self):
        frm = ttk.Frame(self.root, padding=16)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text=f"Commander: {self.commander}", font=("Segoe UI", 12)).pack(pady=(0,8))
        form = ttk.Frame(frm)
        form.pack(fill="x", pady=6)

        ttk.Label(form, text="Rocket designation:").grid(row=0, column=0, sticky="w")
        self.rocket_var = tk.StringVar(value="MOD-ODC-1")
        ttk.Entry(form, textvariable=self.rocket_var).grid(row=0, column=1, sticky="ew", padx=8)

        ttk.Label(form, text="Orbit altitude (km):").grid(row=1, column=0, sticky="w", pady=(8,0))
        self.orbit = tk.StringVar(value="500")
        ttk.Entry(form, textvariable=self.orbit).grid(row=1, column=1, sticky="ew", padx=8, pady=(8,0))

        ttk.Label(form, text="Launch lat (°):").grid(row=2, column=0, sticky="w", pady=(8,0))
        self.lat = tk.StringVar(value="13.72")
        ttk.Entry(form, textvariable=self.lat).grid(row=2, column=1, sticky="ew", padx=8, pady=(8,0))

        ttk.Label(form, text="Launch lon (°):").grid(row=3, column=0, sticky="w", pady=(8,0))
        self.lon = tk.StringVar(value="80.23")
        ttk.Entry(form, textvariable=self.lon).grid(row=3, column=1, sticky="ew", padx=8, pady=(8,0))

        ttk.Label(form, text="Country:").grid(row=4, column=0, sticky="w", pady=(8,0))
        self.country = tk.StringVar()
        cbox = ttk.Combobox(form, textvariable=self.country, values=list(self.COUNTRY_STATIONS.keys()), state="readonly")
        cbox.grid(row=4, column=1, sticky="ew", padx=8, pady=(8,0))
        cbox.bind("<<ComboboxSelected>>", self._on_country)

        ttk.Label(form, text="Launch site:").grid(row=5, column=0, sticky="w", pady=(8,0))
        self.site = tk.StringVar()
        self.site_box = ttk.Combobox(form, textvariable=self.site, state="readonly")
        self.site_box.grid(row=5, column=1, sticky="ew", padx=8, pady=(8,0))

        form.columnconfigure(1, weight=1)
        ttk.Button(frm, text="Launch Mission", command=self._launch).pack(pady=12, anchor="e")

    def _on_country(self, event):
        c = self.country.get()
        stations = self.COUNTRY_STATIONS.get(c, [])
        self.site_box["values"] = stations
        if stations:
            self.site.set(stations[0])

    def _launch(self):
        try:
            orbit = float(self.orbit.get())
            lat = float(self.lat.get())
            lon = float(self.lon.get())
        except ValueError:
            messagebox.showerror("Invalid", "Numeric fields required.")
            return
        rocket = self.rocket_var.get().strip()
        country = self.country.get().strip()
        site = self.site.get().strip()
        if not rocket or not country or not site:
            messagebox.showerror("Invalid", "Fill all fields.")
            return
        config = MissionConfig(
            commander=self.commander,
            rocket_name=rocket,
            orbit_range_km=orbit,
            launch_lat=lat,
            launch_lon=lon,
            country=country,
            space_station=site
        )
        # destroy old UI ➝ open main window
        for w in self.root.winfo_children():
            w.destroy()
        MainWindow(self.root, config)
