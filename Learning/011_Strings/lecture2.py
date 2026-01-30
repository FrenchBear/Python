s = "hello \
world"
print(s)

t = "Hello " "world"
print(t)

bs = "ba" + "na"*2
print(bs)
print(type(bs))

print(1,2,3)
print(1,2,3, sep=', ', end='\n\n')
print(1,2,3, sep='\n')

print(f"{42:~^50}")
print("{:>50}".format("Hello"))

print("{} {}".format("Hello","world"))

print("f: {:0.1f}\nh: {}\nt: {}".format(0.23, 'Hello', 12))
print(f"Time: {11}:{45}")

print('{}, {}, {}'.format('a', 'b', 'c'))
print('{2}, {1}, {0}'.format('a', 'b', 'c'))

# Can align
# forces the field to be left aligned
print('{:<30}'.format('Hello, class'))
# forces the field to be right aligned
print('{:>30}'.format('Hello, class'))
# forces the field to be center aligned
print('{:^30}'.format('Hello, class'))
# center aligns and fills with '~'
print('{:~^30}'.format('Hello, class'))

a, b, c = 10,.915, 42
print(f"a: {a:f} \nb: {b:%}\nc: {c:E}")

print(f"{4:2d}")
