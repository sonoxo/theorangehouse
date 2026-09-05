import unittest
from orangehouse.model import Scenario, project
class ProjectionTests(unittest.TestCase):
    def test_zero_rate_flow(self): self.assertEqual(project(Scenario(1000,monthly_flow=100,months=3))["final"]["baseline"],1300)
    def test_compounding(self): self.assertAlmostEqual(project(Scenario(1000,annual_rate=.12,months=12))["final"]["baseline"],1120,places=2)
    def test_stress_band(self):
        final=project(Scenario(1000,volatility=.2,months=12))["final"]
        self.assertEqual((final["low"],final["high"]),(800,1200))
    def test_invalid(self):
        with self.assertRaises(ValueError): project(Scenario(-1))
if __name__ == "__main__": unittest.main()
