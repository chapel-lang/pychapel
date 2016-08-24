from __future__ import print_function
class Pen(object):
    def __init__(self):
        self._color = 0 # "private" variable

    @property
    def color(self):
        print("I AM GETTING THIS")
        return self

    @color.setter
    def color(self, color):
        print("I AM SETTING THIS")
        #self._color = color

p = Pen()
print(p)
#print p.color

#p.color = 2

#print p.color
