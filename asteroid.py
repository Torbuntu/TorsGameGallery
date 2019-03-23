# asteroid.py
# asteroid.py
class asteroid():
    x = 0
    y = 0
    vx = 0
    vy = 0
    
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
def createAsteroid(x1, y1, vx1, vy1 ):
    ast = asteroid(x1, y1, vx1, vy1)
    return ast