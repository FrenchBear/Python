# Python regular expression tests

import re

s = "Pierre Paul\rJérôme\r\nHenri   Jacques\r\n\n"
print(re.split(r"\W+", s))
print(re.findall(r"\w+", s))

CODEPOINT_RE = re.compile(r"{([0-9a-fA-F]+)}")
s = "AB{41}CD{CAFE}Hello"
t = re.sub(CODEPOINT_RE, lambda ma: '<'+str(ma.group(0))+'>', s)
print(t)
