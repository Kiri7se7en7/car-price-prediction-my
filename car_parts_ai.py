import json

def load_parts_database():
    return {
        "turbos": [
            {"name": "GT3582", "power_range": (400, 650), "flange": "T4", "fuel_types": ["RON 95", "RON 97"]},
            {"name": "Precision 6266", "power_range": (500, 800), "flange": "T4", "fuel_types": ["RON 97", "E85"]},
            {"name": "BorgWarner S366", "power_range": (450, 850), "flange": "T4", "fuel_types": ["RON 97", "E85"]},
            {"name": "Garrett GTX3584RS", "power_range": (550, 1000), "flange": "V-Band", "fuel_types": ["RON 97", "E85"]}
        ],
        "injectors": [
            {"name": "ID1300x", "flow_cc": 1300, "power_support": 600, "fuel_types": ["RON 95", "RON 97"]},
            {"name": "ID1700x", "flow_cc": 1700, "power_support": 800, "fuel_types": ["RON 97", "E85"]},
            {"name": "Bosch 2200cc", "flow_cc": 2200, "power_support": 1000, "fuel_types": ["RON 97", "E85"]},
            {"name": "FIC 1650cc", "flow_cc": 1650, "power_support": 750, "fuel_types": ["RON 97", "E85"]}
        ],
        "intercoolers": [
            {"name": "600x300x100mm", "power_limit": 600},
            {"name": "800x400x100mm", "power_limit": 800},
            {"name": "1000x450x100mm", "power_limit": 1000},
            {"name": "1200x500x100mm", "power_limit": 1200}
        ],
        "fuel_pumps": [
            {"name": "Walbro 450 (F90000274)", "flow_lph": 450, "power_support": 700, "fuel_types": ["RON 95", "RON 97"]},
            {"name": "DeatschWerks DW400", "flow_lph": 415, "power_support": 650, "fuel_types": ["RON 97", "E85"]},
            {"name": "AEM 340LPH", "flow_lph": 340, "power_support": 500, "fuel_types": ["RON 95", "RON 97"]},
            {"name": "Bosch 044", "flow_lph": 300, "power_support": 600, "fuel_types": ["RON 97", "E85"]}
        ],
        "ecus": [
            {"name": "MaxxECU Race", "features": ["Standalone", "Flex Fuel", "Boost Control"], "engine_compatibility": ["2JZ-GTE", "RB26", "4G63"]},
            {"name": "Link G4X", "features": ["Standalone", "Advanced Logging", "Knock Control"], "engine_compatibility": ["2JZ-GTE", "SR20", "EJ25"]},
            {"name": "Haltech Elite 2500", "features": ["Standalone", "DBW Support", "Wideband O2"], "engine_compatibility": ["2JZ-GTE", "LS1", "4B11"]},
            {"name": "AEM Infinity", "features": ["Standalone", "Traction Control", "Launch Control"], "engine_compatibility": ["2JZ-GTE", "K20", "RB26"]}
        ],
        "radiators": [
            {"name": "Koyo Aluminum Racing Radiator", "cooling_capacity": "High", "compatibility": ["2JZ-GTE"]},
            {"name": "Mishimoto Performance Radiator", "cooling_capacity": "Medium", "compatibility": ["2JZ-GTE"]},
            {"name": "CSF High-Performance Radiator", "cooling_capacity": "Very High", "compatibility": ["2JZ-GTE"]}
        ],
        "clutches": [
            {"name": "ACT Heavy Duty Clutch", "torque_capacity": 700, "compatibility": ["2JZ-GTE"]},
            {"name": "OS Giken Twin Plate", "torque_capacity": 900, "compatibility": ["2JZ-GTE"]},
            {"name": "Exedy Hyper Multi", "torque_capacity": 1000, "compatibility": ["2JZ-GTE"]}
        ],
        "exhausts": [
            {"name": "HKS Hi-Power", "pipe_diameter": "3-inch", "compatibility": ["2JZ-GTE"]},
            {"name": "Greddy Revolution RS", "pipe_diameter": "3.5-inch", "compatibility": ["2JZ-GTE"]},
            {"name": "Tomei Expreme Ti", "pipe_diameter": "3-inch", "compatibility": ["2JZ-GTE"]}
        ]
    }

def recommend_parts(engine, power_goal, fuel_type):
    parts_db = load_parts_database()
    recommendations = {key: [] for key in parts_db.keys()}
    
    for category, parts in parts_db.items():
        for part in parts:
            if "power_range" in part and "fuel_types" in part:
                if part["power_range"][0] <= power_goal <= part["power_range"][1] and fuel_type in part["fuel_types"]:
                    recommendations[category].append(part["name"])
            elif "power_limit" in part and part["power_limit"] >= power_goal:
                recommendations[category].append(part["name"])
            elif "engine_compatibility" in part and engine in part["engine_compatibility"]:
                recommendations[category].append(part["name"])
    
    return recommendations

if __name__ == "__main__":
    engine = input("Enter engine type: ")
    power_goal = int(input("Enter power goal (HP): "))
    fuel_type = input("Enter fuel type (e.g., RON 95, RON 97, E85): ")
    
    recommendations = recommend_parts(engine, power_goal, fuel_type)
    print("\nRecommended Parts:")
    print(json.dumps(recommendations, indent=4))
