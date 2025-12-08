from ..core.models import Thruster, DebrisItem

def test_thruster_mass():
    thr = Thruster(id=1)
    assert thr.total_mass() == 0.0
    thr.debris_collected.append(DebrisItem(material="metal", mass_kg=10.0))
    thr.debris_collected.append(DebrisItem(material="plastic", mass_kg=5.0))
    assert thr.total_mass() == 15.0
    bd = thr.material_breakdown()
    assert bd["metal"] == 10.0 and bd["plastic"] == 5.0
