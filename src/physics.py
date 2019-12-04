## physics.py ##
## Author: Carson Foster ##

## Purpose: model real-world physics to an extent ##

import math, copy

class Vector():
    def __init__(self, angle, magnitude): ## pass angle in degrees
        self.angle = round(math.radians(angle), 3)
        self.speed = round(magnitude, 3)
    def setSpeed(self, speed):
        self.speed = round(speed, 3)
    def setAngle(self, angle):
        self.angle = round(math.radians(angle), 3)
    def head(self):
        return (round(self.speed * math.cos(self.angle), 3), round(self.speed * math.sin(self.angle), 3))
    def __add__(self, other):
        selfHead = self.head()
        otherHead = other.head()
        newHead = (selfHead[0] + otherHead[0], selfHead[1] + otherHead[1])
        newSpeed = round(math.hypot(newHead[0], newHead[1]), 3)
        newAngle = math.radians(90) - math.atan2(newHead[0], newHead[1])
        return Vector(round(math.degrees(newAngle), 3), newSpeed)
    def __str__(self):
        return "(" + str(math.degrees(self.angle)) + " degrees, " + str(self.speed) + ")"

class Environment():
    ## TODO: determine values for constants
    gravity = Vector(90, .5) ## default = .002
    ## RIGHT = 0 degrees
    ## LEFT = 180 degrees
    ## DOWN = 90 degrees
    ## UP = 270 degrees
    drag = .999
    elasticity = .75
    width = 0
    height = 0
    funcs = {}
    def __init__(self, objects=[], func=[], display=None):
        self.func = func
        self.originalFunc = copy.deepcopy(func)
        self.objects = objects
        self.display = display
    def update(self):
        for object in self.objects:
            for function in self.func:
                function(object)
            if type(object) == PygameObject:
                object.update(self.display)
            else:
                object.update()
    @classmethod
    def setDimensions(self, w, h):
        self.width = w
        self.height = h
    @classmethod
    def setFunc(self, name, func):
        self.funcs[name] = func
    def applyGravity(self, object):
        object.addVector(Environment.gravity)
    def applyDrag(self, object):
        assert "inAir" in Environment.funcs.keys()
        if Environment.funcs["inAir"](object):
            object.dilateSpeed(Environment.drag)
    def applyElasticity(self, object):
        object.dilateSpeed(Environment.elasticity)
    def solidGround(self, object):
        assert "underground" in Environment.funcs.keys() and "putAtGround" in Environment.funcs.keys() and "inAir" in Environment.funcs.keys()
        if Environment.funcs["underground"](object):
            Environment.funcs["putAtGround"](object)
            object.velocity = Vector(0, 0)
            if self.applyGravity in self.func:
                self.func.remove(self.applyGravity)
        elif self.funcs["inAir"](object):
            if self.applyGravity not in self.func and self.applyGravity in self.originalFunc:
                self.func.append(self.applyGravity)
        else: ## atGround
            if round(math.degrees(object.velocity.angle)) > 0  and round(math.degrees(object.velocity.angle)) < 180:
                object.velocity = Vector(0, 0)
            if self.applyGravity in self.func:
                self.func.remove(self.applyGravity)
    def keepInWindow(self, object):
        assert "putAtGround" in Environment.funcs.keys() and "underground" in Environment.funcs.keys()
        if object.x < 0 or object.x + object.w > self.width or object.y < 0 or object.y + object.h > self.height:
            if object.x < 0:
                object.x = 0
            elif object.x + object.w > self.width:
                object.x = self.width - object.w
            elif object.y < 0:
                object.y = 0
            else:
                object.y = self.height - object.h
            if Environment.funcs["underground"](object):
                Environment.funcs["putAtGround"](object)
            object.velocity.angle = - object.velocity.angle
            self.applyElasticity(object)
    def collide(self, object):
        assert "collide" in Environment.funcs.keys() and "inAir" in Environment.funcs.keys()
        if Environment.funcs["inAir"](object):
            if Environment.funcs["collide"](object):
                object.velocity = self.gravity
        else:
            if Environment.funcs["collide"](object):
                object.velocity = Vector(0, 0)
    def stickToClimbable(self, object):
        assert "climbableCollision" in Environment.funcs.keys() and "restrictDirections" in Environment.funcs.keys() and "underground" in Environment.funcs.keys() and "putAtGround" in Environment.funcs.keys() and "inAir" in Environment.funcs.keys()
        tile = Environment.funcs["climbableCollision"](object)
        if tile:
            Environment.funcs["restrictDirections"](object, tile)
        if Environment.funcs["underground"](object):
            Environment.funcs["putAtGround"](object)
            object.velocity = Vector(0, 0)
        elif not Environment.funcs["inAir"](object): ## atGround
            if round(math.degrees(object.velocity.angle)) > 0  and round(math.degrees(object.velocity.angle)) < 180:
                object.velocity = Vector(0, 0)

EnvironmentReference = Environment([], [])

class Object():
    def __init__(self, x, y, w=1, h=1, velocity=None):
        self.x = x
        self.y = y
        self.intx = int(x)
        self.inty = int(y)
        self.velocity = velocity
        self.w = int(w)
        self.h = int(h)
    def move(self):
        head = self.velocity.head()
        self.x += round(head[0], 3)
        self.y += round(head[1], 3)
        if self.x < 0:
            self.x = 0.0
        if self.y < 0:
            self.y = 0.0
        self.intx = int(self.x)
        self.inty = int(self.y)
    def moveAbsolute(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = round(self.x, 3)
        self.y = round(self.y, 3)
        if self.x < 0:
            self.x = 0.0
        if self.y < 0:
            self.y = 0.0
        self.intx = int(self.x)
        self.inty = int(self.y)
    def setPoint(self, x, y):
        self.x = round(x, 3)
        self.y = round(y, 3)
        self.intx = int(self.x)
        self.inty = int(self.y)
    def update(self):
        self.move()
    def addVector(self, otherVector):
        self.velocity += otherVector
    def dilateSpeed(self, scalar):
        self.velocity.speed *= scalar
        self.velocity.speed = round(self.velocity.speed, 3)

class PygameObject(Object):
    def __init__(self, x, y, w=1, h=1, velocity=None, draw=None):
        super().__init__(x, y, w, h, velocity)
        self.draw = draw
    def update(self, DISPLAY):
        self.move()
        self.draw(self, DISPLAY)