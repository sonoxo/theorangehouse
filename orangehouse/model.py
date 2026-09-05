"""Deterministic, dependency-free scenario projection model."""
from dataclasses import asdict, dataclass
from math import isfinite

@dataclass(frozen=True)
class Scenario:
    starting_value: float
    monthly_flow: float = 0.0
    annual_rate: float = 0.0
    volatility: float = 0.0
    months: int = 12

    def validate(self) -> None:
        if not all(isfinite(v) for v in (self.starting_value, self.monthly_flow, self.annual_rate, self.volatility)):
            raise ValueError("numeric inputs must be finite")
        if self.starting_value < 0: raise ValueError("starting_value must be non-negative")
        if not 1 <= self.months <= 600: raise ValueError("months must be between 1 and 600")
        if not 0 <= self.volatility <= 1: raise ValueError("volatility must be between 0 and 1")
        if self.annual_rate < -1: raise ValueError("annual_rate cannot be below -1")

def project(scenario: Scenario) -> dict:
    """Return baseline and transparent stress-band projections."""
    scenario.validate()
    rate = (1 + scenario.annual_rate) ** (1 / 12) - 1
    balance, timeline = scenario.starting_value, []
    for month in range(1, scenario.months + 1):
        balance = max(0.0, balance * (1 + rate) + scenario.monthly_flow)
        uncertainty = balance * scenario.volatility * (month / 12) ** 0.5
        timeline.append({"month": month, "baseline": round(balance, 2),
                         "low": round(max(0.0, balance - uncertainty), 2),
                         "high": round(balance + uncertainty, 2)})
    return {"model": "deterministic-compound-v1",
            "disclaimer": "Scenario analysis only; not financial advice or a market forecast.",
            "inputs": asdict(scenario), "timeline": timeline, "final": timeline[-1]}
