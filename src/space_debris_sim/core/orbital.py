"""
Simple orbital helper functions.


"""

import math

# Earth's gravitational parameter mu = GM (km^3 / s^2)
MU = 398600.4418

def orbital_radius_from_altitude(alt_km: float) -> float:
    """Return orbital radius (km) from altitude above Earth's mean radius."""
    R_earth = 6371.0
    return R_earth + alt_km

def estimate_orbital_velocity(alt_km: float) -> float:
    """
    Estimate circular orbital velocity (m/s) for given altitude (km).
    v = sqrt(mu / r) where mu in km^3/s^2 and r in km -> result in km/s -> convert to m/s.
    """
    r = orbital_radius_from_altitude(alt_km)
    v_km_s = (MU / r) ** 0.5
    v_m_s = v_km_s * 1000.0
    return v_m_s
