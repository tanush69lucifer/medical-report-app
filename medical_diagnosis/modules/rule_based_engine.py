import json
import os

# Dynamically locate the JSON file path relative to this script
json_path = os.path.join(os.path.dirname(__file__), "medicine_db.json")
with open(json_path) as f:
    med_data = json.load(f)

def interpret_results(report_list, age=0, gender="N/A", conditions="None"):
    diagnosis = []
    overall_findings = set()

    for idx, report in enumerate(report_list):
        diagnosis.append(f"--- Analysis for Report {idx + 1} ---")
        for test, result in report.items():
            val = result["value"]
            status = result["status"]
            if status == "Normal":
                diagnosis.append(f"{test}: {val} - ✅ Normal")
            else:
                diagnosis.append(f"{test}: {val} - ⚠️ {status}")
                if test in ["ALT", "AST"]:
                    overall_findings.add("Liver enzyme imbalance")
                elif test == "Bilirubin":
                    overall_findings.add("Possible jaundice or liver dysfunction")
                elif test == "ALP":
                    overall_findings.add("Bone or bile duct issues")
                elif test == "Creatinine":
                    overall_findings.add("High Creatinine")
                elif test == "WBC" and status == "High":
                    overall_findings.add("High WBC")

    summary = "\n\n=== Summary of Findings ===\n"
    summary += "\n".join([f"- {issue}" for issue in overall_findings]) if overall_findings else "All values normal.\n"

    summary += "\n\n=== Medication Plan ===\n"
    comorb_list = [c.strip().lower() for c in conditions.split(",") if c.strip()]
    for issue in overall_findings:
        if issue in med_data:
            # Age Grouping
            if age <= 12:
                age_group = "0-12"
            elif age <= 60:
                age_group = "13-60"
            else:
                age_group = "60+"

            treatments = med_data[issue].get(age_group, [])
            if not treatments:
                summary += f"- {issue}: No treatment found for age group.\n"
                continue

            for med in treatments:
                name = med.get("name", "Unknown")
                dose = med.get("dose", "N/A")
                duration = med.get("duration", "N/A")
                note = ""

                # Check comorbidities
                if "comorbidities" in med:
                    for comorb in comorb_list:
                        c_info = med["comorbidities"].get(comorb)
                        if c_info:
                            if c_info.get("avoid"):
                                note += f"❌ Avoid due to {comorb}. "
                                continue
                            dose = c_info.get("dose", dose)
                            duration = c_info.get("duration", duration)
                            note += c_info.get("note", "")
                            if "monitor" in c_info:
                                note += f"Monitor: {c_info['monitor']}. "

                summary += f"- {name}: {dose} for {duration}. {note}\n"
        else:
            summary += f"- {issue}: No medication guidance available.\n"

    summary += """
\n=== Recommendations ===
- Stay hydrated (8–10 glasses daily)
- Avoid alcohol, fried food
- Get 7–8 hours of sleep
- Regular health checkups recommended
"""
    diagnosis.append(summary)
    return "\n".join(diagnosis)
