# Example 9-19. htmlize() generates HTML tailored to different object types

>>> htmlize({1, 2, 3})
'<pre>{1, 2, 3}</pre>'
>>> htmlize(abs)
'<pre>&lt;built-in function abs&gt;</pre>'
>>> htmlize('Heimlich & Co.\n- a game')
'<p>Heimlich &amp; Co.<br/>\n- a game</p>'
>>> htmlize(42)
'<pre>42 (0x2a)</pre>'
>>> print(htmlize(['alpha', 66, {3, 2, 1}]))
<ul>
<li><p>alpha</p></li>
<li><pre>66 (0x42)</pre></li>
<li><pre>{1, 2, 3}</pre></li>
</ul>
>>> htmlize(True)
'<pre>True</pre>'
>>> htmlize(fractions.Fraction(2, 3))
'<pre>2/3</pre>'
>>> htmlize(2/3)
'<pre>0.6666666666666666 (2/3)</pre>'
>>> htmlize(decimal.Decimal('0.02380952'))
'<pre>0.02380952 (1/42)</pre>'
