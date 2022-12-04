from math import pi

def square(a):
    S = (a * a) * 2
    return S

def circle(diameter):
    S = diameter * diameter / 4 * pi
    return S

def rectangle(a, b):
    S = (a * b) * 2
    return S 