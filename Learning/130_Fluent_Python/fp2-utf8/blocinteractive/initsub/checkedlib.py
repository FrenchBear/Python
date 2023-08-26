# Example 24-3. initsub/checkedlib.py: doctest for creating a Movie subclass of Checked

>>> class Movie(Checked):
...     title: str
...     year: int
...     box_office: float
...
>>> movie = Movie(title='The Godfather', year=1972, box_office=137)
>>> movie.title
'The Godfather'
>>> movie
Movie(title='The Godfather', year=1972, box_office=137.0)
