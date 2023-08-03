from vector2d_v3 import Vector2d
class ShortVector2d(Vector2d):
    typecode = 'f'

sv = ShortVector2d(1/11, 1/27)
print(sv)
print(len(bytes(sv)))
