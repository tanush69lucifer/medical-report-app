import json
with open("modules/medicine_db.json") as f:
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
    for issue in overall_findings:
        if issue in med_data:
            for med in med_data[issue]:
                summary += f"- {med['name']}: {med['dose']} for {med['duration']}\n"
        else:
            summary += f"- {issue}: No fixed medication. Consult your doctor.\n"

    summary += """
\n=== Recommendations ===
- Stay hydrated (8–10 glasses daily)
- Avoid alcohol, fried food
- Get 7–8 hours of sleep
- Regular health checkups recommended
"""
    diagnosis.append(summary)
    return "\n".join(diagnosis)
