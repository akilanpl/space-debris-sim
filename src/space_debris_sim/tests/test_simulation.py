from ..core.simulation import Simulation
from ..core.models import MissionConfig

def dummy_logger(msg):
    pass

def test_sim_basic():
    cfg = MissionConfig("t", "r", 500, 0, 0, "India", "Satish Dhawan")
    sim = Simulation(cfg, log_callback=dummy_logger)
    sim.reset()
    for _ in range(30):
        sim.step()
    # after 25+ steps, expect collection_done True
    assert sim.collection_done is True
    # thrusters should have some debris (stochastic, but high chance)
    # we do not assert on mass presence to keep test stable, but thrusters exist
    assert len(sim.thrusters) == 3
