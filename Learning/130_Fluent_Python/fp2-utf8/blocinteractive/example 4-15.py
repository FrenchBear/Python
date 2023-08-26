# Example 4-15. Two examples using shave_marks from Example 4-14

>>> order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí”.'
>>> shave_marks(order)
'“Herr Voß: • ½ cup of Œtker™ caffe latte • bowl of acai”.'
>>> Greek = 'Ζέφυρος, Zéfiro'
>>> shave_marks(Greek)
'Ζεφυρος, Zefiro'
