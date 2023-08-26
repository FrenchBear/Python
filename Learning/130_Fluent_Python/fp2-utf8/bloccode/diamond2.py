# Example 14-6. diamond2.py: classes to demonstrate the dynamic nature of super()

from diamond import A

class U():
    def ping(self):
        print(f'{self}.ping() in U')
        super().ping()

class LeafUA(U, A):
    def ping(self):
        print(f'{self}.ping() in LeafUA')
        super().ping()
