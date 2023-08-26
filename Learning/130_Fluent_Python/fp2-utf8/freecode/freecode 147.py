# Iterators in Python aren't a matter of type but of protocol.  A large
# and changing number of built-in types implement *some* flavor of
# iterator.  Don't check the type!  Use hasattr to check for both
# "__iter__" and "__next__" attributes instead.
