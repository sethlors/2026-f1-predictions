"""Quick smoke test for the data layer."""
from utils.data_helpers import (
    load_drivers, load_constructors, load_races,
    load_season_predictions, load_race_predictions, load_fun_predictions,
)

d = load_drivers()
c = load_constructors()
r = load_races()
print(f"Static: {len(d)} drivers, {len(c)} constructors, {len(r)} races")

sp = load_season_predictions()
rp = load_race_predictions()
fp = load_fun_predictions()
print(f"Predictions: {len(sp)} season, {len(rp)} race, {len(fp)} fun")

print("ALL OK")

