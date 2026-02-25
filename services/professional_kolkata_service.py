import math
from database import get_connection


def round_weight(weight):
    if weight <= 0.25:
        return 0.25
    return math.ceil(weight * 2) / 2


def load_all_professional_kolkata_rates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT rate_type, weight_slab, rate, additional_per_kg
        FROM courier_professional_kolkata_rates
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    rate_dict = {}

    for rate_type, slab_weight, rate, additional in rows:

        if rate_type not in rate_dict:
            rate_dict[rate_type] = {
                "slabs": {},
                "per_kg": None
            }

        if additional is not None:
            rate_dict[rate_type]["per_kg"] = float(additional)

        rate_dict[rate_type]["slabs"][float(slab_weight)] = float(rate)

    return rate_dict


def calculate_professional_kolkata_rate(city, state, weight, rate_dict):

    rounded_weight = round_weight(weight)

    # 🔥 Location logic
    city_clean = city.strip().lower()
    state_clean = state.strip().lower()

    if city_clean == "kolkata":
        rate_type = "within_city"

    elif state_clean in ["west bengal", "wb"]:
        rate_type = "within_state"

    else:
        rate_type = "within_zone"

    zone_data = rate_dict.get(rate_type)

    if not zone_data:
        raise Exception(f"Rate type not found: {rate_type}")

    # <= 5kg
    if rounded_weight <= 5:
        if rounded_weight not in zone_data["slabs"]:
            raise Exception(
                f"No slab found for {rate_type} weight {rounded_weight}"
            )

        return rounded_weight, zone_data["slabs"][rounded_weight]

    # > 5kg
    base_rate = zone_data["slabs"].get(5)
    per_kg = zone_data["per_kg"]

    if base_rate is None or per_kg is None:
        raise Exception(f"Incomplete rate setup for {rate_type}")

    extra_weight = rounded_weight - 5
    final_rate = base_rate + (extra_weight * per_kg)

    return rounded_weight, final_rate