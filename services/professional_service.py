import math
from database import get_connection


def round_weight(weight):
    if weight <= 0.25:
        return 0.25
    return math.ceil(weight * 2) / 2


def load_all_professional_rates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT zone, slab_weight, rate, is_per_kg
        FROM professional_rates
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    rate_dict = {}

    for zone, slab_weight, rate, is_per_kg in rows:
        if zone not in rate_dict:
            rate_dict[zone] = {
                "slabs": {},
                "per_kg": None
            }

        if is_per_kg:
            rate_dict[zone]["per_kg"] = float(rate)
        else:
            rate_dict[zone]["slabs"][float(slab_weight)] = float(rate)

    return rate_dict


def calculate_professional_rate(city, weight, rate_dict):

    rounded_weight = round_weight(weight)

    # 🔥 Zone logic
    if city.strip().lower() == "bangalore":
        zone = "Bangalore Local"
    else:
        zone = "Karnataka"

    zone_data = rate_dict.get(zone)

    if not zone_data:
        raise Exception(f"Zone not found: {zone}")

    # <= 5kg
    if rounded_weight <= 5:
        if rounded_weight not in zone_data["slabs"]:
            raise Exception(f"No slab found for {zone} weight {rounded_weight}")
        return rounded_weight, zone_data["slabs"][rounded_weight]

    # > 5kg
    base_rate = zone_data["slabs"].get(5)
    per_kg = zone_data["per_kg"]

    if base_rate is None or per_kg is None:
        raise Exception(f"Incomplete rate setup for zone {zone}")

    extra_weight = rounded_weight - 5
    final_rate = base_rate + (extra_weight * per_kg)

    return rounded_weight, final_rate