import fileinput
from itertools import pairwise

reports: list[list[int]] = list(
    list(map(lambda x: int(x), line.split())) for line in fileinput.input()
)


def report_is_safe(report: list[int]) -> bool:
    diff = report[1] - report[0]
    premier_croissant_vrai_ou_faux = diff > 0

    for current, next in pairwise(report):
        diff = next - current
        croissant_vrai_ou_faux = diff > 0
        if not 1 <= abs(diff) <= 3:
            return False
        if premier_croissant_vrai_ou_faux != croissant_vrai_ou_faux:
            return False
    return True


safe_reports = 0

for report in reports:
    if report_is_safe(report):
        safe_reports += 1
    else:
        for i in range(len(report)):
            if report_is_safe(report[:i] + report[i + 1 :]):
                safe_reports += 1
                break

print(f"Total safe reports: {safe_reports}")

# complexité etoile 1 => o(n * m)
# complexité etoile 2 => o(n * m * m)
