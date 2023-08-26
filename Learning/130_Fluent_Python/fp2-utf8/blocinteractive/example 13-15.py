# Example 13-15. Using SupportsComplex at runtime

>>> from typing import SupportsComplex
>>> import numpy as np
>>> c64 = np.complex64(3+4j)
>>> isinstance(c64, complex)
False
>>> isinstance(c64, SupportsComplex)
True
>>> c = complex(c64)
>>> c
(3+4j)
>>> isinstance(c, SupportsComplex)
False
>>> complex(c)
(3+4j)
