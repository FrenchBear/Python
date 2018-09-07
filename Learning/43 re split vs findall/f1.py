import re

s = "Pierre Paul\rJérôme\r\nHenri   Jacques\r\n\n"
print(re.split(r"\W+", s))
print(re.findall(r"\w+", s))

