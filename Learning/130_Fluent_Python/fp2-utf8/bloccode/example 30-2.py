# Example 30-2. Bobo knows that hello requires a person argument, and retrieves it from the HTTP request

import bobo

@bobo.query('/')
def hello(person):
    return f'Hello {person}!'
