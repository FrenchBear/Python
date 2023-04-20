# Jinja tests - https://realpython.com/primer-on-jinja-templating/
# j3 - Format html template
#
# 2023-04-20    PV

from jinja2 import Environment, FileSystemLoader

max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine",  "score": 100},
    {"name": "George", "score": 87},
    {"name": "Frieda", "score": 92},
    {"name": "Fritz", "score": 40},
    {"name": "Sirius", "score": 75},
]

environment = Environment(loader=FileSystemLoader("templates/"))
results_template = environment.get_template("results.html")
results_filename = "students_results.html"
context = {
    "students": students,
    "test_name": test_name,
    "max_score": max_score,
}
with open(results_filename, mode="w", encoding="utf-8") as results:
    results.write(results_template.render(context))
    print(f"... wrote {results_filename}")
