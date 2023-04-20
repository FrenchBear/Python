# Jinja tests - https://realpython.com/primer-on-jinja-templating/
# j1 - Very first and basic example
#
# 2023-04-20    PV

import jinja2

environment = jinja2.Environment()
template = environment.from_string("Hello, {{ name }}!")
print(template.render(name="World"))
