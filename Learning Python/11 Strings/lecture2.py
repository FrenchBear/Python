s = "hello \
world"
print(s)

t = "Hello " "world"
print(t)

b = "ba" + "na"*2
print(b)
print(type(b))

print(1,2,3)
print(1,2,3, sep=', ', end='\n\n')
print(1,2,3, sep='\n')

print("{:~^50}".format(42))
print("{:>50}".format("Hello"))

print("{} {}".format("Hello","world"))

print("f: {:0.1f}\nh: {}\nt: {}".format(0.23, 'Hello', 12))
print("Time: {h}:{m}".format(h=11, m=45))

print('{0}, {1}, {2}'.format('a', 'b', 'c'))
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
print("a: {:f} \nb: {:%}\nc: {:E}".format(a,b,c))

print("{:2d}".format(4))
