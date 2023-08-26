# Example 23-14. method_is_descriptor.py: a Text class, derived from UserString

import collections

class Text(collections.UserString):
    def __repr__(self):
        return 'Text({!r})'.format(self.data)

    def reverse(self):
        return self[::-1]
