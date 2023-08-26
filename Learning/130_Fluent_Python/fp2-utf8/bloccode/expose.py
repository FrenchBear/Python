# Example 11-21. expose.py: Jython code to read the content of a private field in another class

#!/usr/bin/env jython
# NOTE: Jython is still Python 2.7 in late 2020

import Confidential

message = Confidential('top secret text')
secret_field = Confidential.getDeclaredField('secret')
secret_field.setAccessible(True)  # break the lock!
print 'message.secret =', secret_field.get(message)
