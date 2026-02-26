import math
from database import get_connection


def round_weight(weight):
    if weight <= 0.25:
        return 0.25
    return math.ceil(weight * 2) / 2


def load_all_trackon_hyd_rates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT zone, slab_weight, rate, is_per_kg
        FROM trackon_hyd_rates
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    rate_dict = {}

    for zone, slab_weight, rate, is_per_kg in rows:

        if zone not in rate_dict:
            rate_dict[zone] = {
                "slabs": {},
                "per_500gm": None
            }

        if is_per_kg:
            rate_dict[zone]["per_500gm"] = float(rate)
        else:
            rate_dict[zone]["slabs"][float(slab_weight)] = float(rate)

    return rate_dict


def calculate_trackon_hyd_rate(city, weight, rate_dict):

    rounded_weight = round_weight(weight)

    # 🔥 City Logic
    city_clean = city.strip().lower()

    if city_clean == "hyderabad":
        zone = "HYD"
    else:
        zone = "EX_HYD"

    zone_data = rate_dict.get(zone)

    if not zone_data:
        raise Exception(f"Zone not found: {zone}")

    # <= 1kg slab logic
    if rounded_weight <= 1:

        if rounded_weight not in zone_data["slabs"]:
            raise Exception(
                f"No slab found for {zone} weight {rounded_weight}"
            )

        return rounded_weight, zone_data["slabs"][rounded_weight]

    # > 1kg logic (per 500gm)
    base_rate = zone_data["slabs"].get(1)
    per_500gm = zone_data["per_500gm"]

    if base_rate is None or per_500gm is None:
        raise Exception(f"Incomplete rate setup for zone {zone}")

    extra_weight = rounded_weight - 1

    # convert extra weight to number of 0.5 increments
    increments = extra_weight / 0.5

    final_rate = base_rate + (increments * per_500gm)

    return rounded_weight, final_rate