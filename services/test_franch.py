from services.franch_service import calculate_franch_rate

zone = "Tamilnadu"
weight = 1.27

rounded, rate = calculate_franch_rate(zone, weight)

print("Rounded Weight:", rounded)
print("Final Rate:", rate)