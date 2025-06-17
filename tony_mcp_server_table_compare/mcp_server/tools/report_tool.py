import json


def generate_report(differences):
    if not differences:
        return "No differences found."

    report = f"Found {len(differences)} differences:\n\n"
    for idx, diff in enumerate(differences, 1):
        report += f"{idx}. {json.dumps(diff, indent=2)}\n\n"
    return report
