# Example 4-18. Two examples using asciize from Example 4-17

>>> order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí”.'
>>> dewinize(order)
'"Herr Voß: - ½ cup of Oetker(TM) caffè latte - bowl of açaí."'
>>> asciize(order)
'"Herr Voss: - 1⁄2 cup of Oetker(TM) caffe latte - bowl of acai."'
