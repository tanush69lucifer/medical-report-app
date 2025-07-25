import re, json

def extract_values(text):
    files = ["liver_ranges", "blood_ranges", "kidney_ranges", "cardio_ranges", "neuro_ranges", "eye_ranges", "gallbladder_ranges"]
    results = {}
    for file in files:
        with open(f"knowledge/{file}.json") as f:
            ranges = json.load(f)
        for param, rng in ranges.items():
            match = re.search(rf"{param}[^0-9]*(\d+\.?\d*)", text, re.IGNORECASE)
            if match:
                val = float(match.group(1))
                status = "High" if val > rng["max"] else "Low" if val < rng["min"] else "Normal"
                results[param] = {"value": val, "status": status}
    return results
