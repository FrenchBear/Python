# Example 9-21. Abridged registration.py module from Example 9-2, repeated here for convenience

registry = []

def register(func):
    print(f'running register({func})')
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

print('running main()')
print('registry ->', registry)
f1()
