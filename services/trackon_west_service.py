import math
from database import get_connection


def round_weight(weight):
    # 🔥 Whole number rounding
    return math.ceil(weight)


def load_all_trackon_west_rates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT zone, slab_weight, rate, is_per_kg
        FROM trackon_west_rates
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


def calculate_trackon_west_rate(zone_input, weight, rate_dict):

    rounded_weight = round_weight(weight)

    zone_clean = zone_input.strip().lower()

    # 🔥 Zone logic
    if zone_clean == "west":
        zone = "WEST"
    else:
        zone = "ROI"

    zone_data = rate_dict.get(zone)

    if not zone_data:
        raise Exception(f"Zone not found: {zone}")

    # <= 5kg slab logic
    if rounded_weight <= 5:

        if float(rounded_weight) not in zone_data["slabs"]:
            raise Exception(
                f"No slab found for {zone} weight {rounded_weight}"
            )

        return rounded_weight, zone_data["slabs"][float(rounded_weight)]

    # > 5kg logic
    base_rate = zone_data["slabs"].get(5.0)
    per_kg = zone_data["per_kg"]

    if base_rate is None or per_kg is None:
        raise Exception(f"Incomplete rate setup for zone {zone}")

    extra_weight = rounded_weight - 5
    final_rate = base_rate + (extra_weight * per_kg)

    return rounded_weight, final_rate