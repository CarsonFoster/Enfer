# Enfer.py ##
## Author: Carson Foster ##

## Purpose: run a 2D platformer ##

import pygame, sys, pytmx, pyscroll, os, time, random, math
from pygame.locals import *
from physics import *

WIDTH = 500
HEIGHT = 500
TITLE = "Enfer"
FPS = 60
clock = pygame.time.Clock()
DT = 2
SPRING = 4
WalkingLayer = 1
paused = False
timeBetweenSprings = 1
climbMax = 4
onlyDirs = ["up", "down", "right", "left", None]

class Protagonist(pygame.sprite.Sprite, Object):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.setImage(filename)
        self.rect = pygame.Rect(0, 0, 16, 16)
        Object.__init__(self, 0, 0, self.rect.w, self.rect.h, Vector(0, 0))
        self.oldx, self.oldy = self.x, self.y
        self.notUnderground = None
        self.feet = pygame.Rect(0, 0, 8, 8)
        self.radius = .5
    def position(self):
        return [self.x, self.y]
    def update(self):
        if self.velocity.speed != 0:
            self.oldx, self.oldy = self.x, self.y
            self.move()
            self.rect.topleft = (self.x, self.y)
    def updateAbsolute(self, dx, dy):
        if dx != 0 or dy != 0:
            self.oldx, self.oldy = self.x, self.y
            self.moveAbsolute(dx, dy)
            self.rect.topleft = (self.x, self.y)
    def move_back(self):
        tmp = (self.x, self.y)
        self.x, self.y = self.oldx, self.oldy
        self.oldx, self.oldy = tmp
        self.rect.topleft = (self.x, self.y)
        self.intx = int(self.x)
        self.inty = int(self.y)
    def setPoint(self, x, y):
        self.x = round(x, 3)
        self.y = round(y, 3)
        self.intx = int(self.x)
        self.inty = int(self.y)
        self.rect.topleft = (self.x, self.y)
    def setImage(self, path):
        self.image = pygame.image.load(path)
        #self.mask = pygame.mask.from_surface(self.image)

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, coords, id):
        self.image = image
        self.rect = pygame.Rect(tileToPx(coords[0], coords[1]), (16, 16))
        #self.mask = pygame.mask.from_surface(self.image)
        self.radius = 6 if id == 0 else 4

class Particle(PygameObject):
    def __init__(self, x, y, w, h, speed, sinangle):
        PygameObject.__init__(self, x, y, w, h, None, lambda self, disp: pygame.draw.rect(disp, (128, 128, 128), (self.x, self.y, self.w, self.h)))
        self.speed = speed
        self.sinangle = math.radians(sinangle)
    def move(self):
        self.x += self.speed
        self.y += math.sin(self.sinangle)
        self.sinangle += min(math.radians(.05 * 360), math.radians(self.speed / 32)) ## TODO

class Ash():
    def __init__(self, number, display):
        self.num = number
        self.display = display
        self.WAVEWIDTH = 40
        self.WAVEHEIGHT = 20
        self.particles = self.getInitialParticles()
        self.part = 1 ## 1 = down, 2 = up
        self.first = True
    def getInitialParticles(self):
        tmp = []
        rand = random.Random()
        for i in range(self.num):
            lenSide = rand.randint(2, 8) ## size
            x, y = rand.randint(0, WIDTH), rand.randint(0, HEIGHT)
            obj = Particle(x, y, lenSide, lenSide, rand.uniform(1.0, 3.0), rand.randint(0, 359))
            tmp.append(obj)
        return tmp
    def update(self):
        rand = random.Random()
        for obj in self.particles:
            obj.update(self.display)
            if obj.x >= WIDTH or obj.y >= HEIGHT:
                x, y = -4, rand.randint(0, HEIGHT)
                obj.setPoint(x, y)
    def setDisplay(self, display):
        self.display = display

# simple wrapper to keep the screen resizeable
def init_screen(width, height, flags=pygame.RESIZABLE):
    global temp_surface
    screen = pygame.display.set_mode((width, height), flags)
    temp_surface = pygame.Surface((width / 2, height / 2)).convert()
    return screen

def pxToTile(x, y):
    tilex, tiley = x // 16, y // 16
    assert tilex >= 0 and tiley >= 0, "({}, {})".format(tilex, tiley)
    return tilex, tiley

def tileToPx(x, y):
    return x * 16, y * 16

def keysFromDict(d):
    keys = []
    for k in d.keys():
        keys.append(k)
    return keys

def getTop(tiles):
    smallestY = 1000000
    for tile in tiles:
        if tile[1] < smallestY:
            smallestY = tile[1]
    tmp = []
    for tile in tiles:
        if tile[1] == smallestY:
            tmp.append(tile)
    return tmp

def inAir(hero):
    tmp = True
    collisions = getCollisions(hero)#, ["se", "sw"])
    tiles = keysFromDict(collisions)
    top = getTop(tiles)
    for tile in top:
        propsBelow = tmx_data.get_tile_properties(tile[0], tile[1] + (1 if tile[1] + 1 < tmx_data.height else 0), WalkingLayer)
        tmp = tmp and (propsBelow == None or ("Type" in propsBelow.keys() and propsBelow["Type"] in ["Sign", "Kill"]))
    return tmp

def putAtGround(hero):
    testHero = Protagonist("dudes\\dude_right0.png")
    testHero.setPoint(hero.oldx, hero.oldy)
    if underground(testHero):
        x, y = hero.notUnderground
        hero.setPoint(x, y)
    else:
        hero.move_back()
    del testHero

def getCollisions(hero, quads=["ne", "sw", "se", "nw"]):
    tmp = {}
    if len(quads) == 4:
        collisions = quad.hit(hero.rect)
    else:
        collisions = set()
        if "ne" in quads:
            collisions |= quad.ne.hit(hero.rect)
        if "nw" in quads:
            collisions |= quad.nw.hit(hero.rect)
        if "se" in quads:
            collisions |= quad.se.hit(hero.rect)
        if "sw" in quads:
            collisions |= quad.sw.hit(hero.rect)
    if collisions != set():
        for rect in collisions:
            tile = pxToTile(rect[0], rect[1])
            prop = tmx_data.get_tile_properties(tile[0], tile[1], WalkingLayer)
            tmp[tile] = prop
    return tmp

def underground(hero):
    for tile, props in getCollisions(hero).items():#, ["se", "sw"]).items():
        if props != None and "Type" in props.keys() and props["Type"] not in ["Sign", "Kill"]:
            return True
    if not(hero.x < 0 or hero.x + hero.w > WIDTH or hero.y < 0 or hero.y + hero.h > HEIGHT):
        hero.notUnderground = (hero.x, hero.y)
    return False

def atGround(hero):
    return not underground(hero) and not inAir(hero)

def collideTiles(hero):
    for tile, props in getCollisions(hero).items():
        if props != None and "Type" in props.keys() and props["Type"] not in ["Sign", "Kill"]:
            return True
    return False

def collideKill(hero, tile):
    props = tmx_data.get_tile_properties(tile[0], tile[1], WalkingLayer)
    tileSprite = Tile(tmx_data.get_tile_image(tile[0], tile[1], WalkingLayer), tile, props["id"])
    c = pygame.sprite.spritecollide(hero, [tileSprite], False, pygame.sprite.collide_circle)
    return c

def restrictDirections(hero, tile):
    global onlyDirs
    heroTile = pxToTile(hero.x, hero.y)
    dir = (int(tile[0] - heroTile[0]), int(tile[1] - heroTile[1]))
    if dir in [(1, 0), (-1, 0)]:
        onlyDirs = ["up", "down", None]
    elif dir == (0, -1):
        onlyDirs = ["right", "left", None]
    elif dir == (0, 0):
        pass
    else:
        assert False, "Tiles below you should never be climbable:\nTile: {}\nDir: {}\nHero Tile:{}".format(tile, dir, heroTile)

def climbableCollision(hero):
    tmp = []
    heroTile = pxToTile(hero.x, hero.y)
    x, y = getDelta()
    tx, ty = heroTile[0] + x, heroTile[1] + y
    props = tmx_data.get_tile_properties(tx, ty, WalkingLayer)
    if props != None and "Type" in props.keys() and "Climbable" in props["Type"]:
        return (tx, ty)
    return False

def getDelta(dirLocal=None):
    if dirLocal == None:
        dirLocal = dir
    x, y = (0, 0)
    if dirLocal == "up":
        y = -1
    elif dirLocal == "down":
        y = 1
    elif dirLocal == "right":
        x = 1
    elif dirLocal == "left":
        x = -1
    elif dir != None:
        assert False, "There aren't any more directions: {}".format(dir)
    return x, y

def canMoveClimb(hero, dir):
    heroTile = pxToTile(hero.x, hero.y)
    dx, dy = getDelta(dir)
    x, y = (heroTile[0] + dx, heroTile[1] + dy)
    if onlyDirs == ["right", "left", None]: ## hanging on to bottom
        tx, ty = x, y - 1
        props = tmx_data.get_tile_properties(tx, ty, WalkingLayer)
        return props != None and "Type" in props.keys() and "Climbable" in props["Type"] 
    elif onlyDirs == ["up", "down", None]: ## hanging on to side
        sideX = 0
        leftX = - 1
        rightX = 1
        for dirX in [leftX, rightX]:
            props = tmx_data.get_tile_properties(dirX + heroTile[0], heroTile[1], WalkingLayer)
            if props != None and "Type" in props.keys() and "Climbable" in props["Type"]:
                sideX = dirX
                break
        props = tmx_data.get_tile_properties(sideX + x, y, WalkingLayer)
        return props != None and "Type" in props.keys() and "Climbable" in props["Type"]

def getAllRects():
    tmp = []
    for x, y, gid in tmx_data.get_layer_by_name("WalkingLayer").iter_data():
        prop = tmx_data.get_tile_properties_by_gid(gid)
        tmp.append(pygame.Rect(tileToPx(x, y), (16, 16)))
    return tmp

def checkForExit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == KEYUP and event.key == K_SPACE:
            return True
    return False

def gameOverAnimation(display, hero, ash):
    hero.velocity = Vector(90, 4)
    num = 0
    if not paused:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("ded.ogg")
        pygame.mixer.music.play()
    while hero.y < tmx_data.height * 16:
        checkForExit()
        hero.setImage("dudes//dude_ded{}.png".format(num))
        hero.update()
        map_layer.draw(temp_surface, display.get_rect())
        temp_surface.blit(hero.image, map_layer.translate_rect(hero.rect))
        ash.update()
        pygame.transform.scale(temp_surface, display.get_size(), display)
        pygame.display.flip()
        num = (num + 1 if num + 1 <= 3 else 0)
        clock.tick(20)
    hero.setImage("dudes//dude_right0.png")

def text(DISPLAY, txt, tile):
    font = pygame.font.Font("code_8x8.ttf", 6)
    txtSurface = font.render(txt, False, (255, 255, 255))
    txtRect = txtSurface.get_rect()
    r = pygame.Rect(map_layer.translate_point(tileToPx(tile[0], tile[1])), (16, 16))
    txtRect.center = r.center
    txtRect.bottom = r.top
    while txtRect.left < 0:
        txtRect.center = (txtRect.center[0] + 1, txtRect.center[1])
    while txtRect.right > DISPLAY.get_size()[1]:
        txtRect.center = (txtRect.center[0] - 1, txtRect.center[1])
    temp_surface.blit(txtSurface, txtRect)
    pygame.transform.scale(temp_surface, DISPLAY.get_size(), DISPLAY)
    pygame.display.flip()

def startingAnimation(display, ash):
    start = pygame.image.load("start.png")
    startSpace = pygame.image.load("startSpace.png")
    while not checkForExit():
        display.blit(start, (0, 0))
        ash.update()
        pygame.display.flip()
        clock.tick(30)
    startTime = time.time()
    while startTime + .5 >= time.time():
        display.blit(startSpace, (0, 0))
        ash.update()
        pygame.display.flip()
        clock.tick(30)

def winningAnimation(display, ash):
    end = pygame.image.load("end.png")
    while not checkForExit():
        display.blit(end, (0, 0))
        ash.update()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit(0)

def drawLoad(display, outline, fill, color):
    pygame.draw.rect(display, (0, 0, 0), map_layer.translate_rect(outline), 1)
    pygame.draw.rect(display, color, map_layer.translate_rect(fill))

def showLoad(display, outOf16, hero):
    outline = pygame.Rect(0, 0, 16, 2)
    outline.bottom = hero.rect.top - 2
    outline.centerx = hero.rect.centerx
    fill = pygame.Rect(outline.topleft, (outOf16, 2))
    drawLoad(display, outline, fill, (0, 255, 0))

def showClimbMeter(display, outOf16, hero):
    if outOf16 == 0:
        return
    outline = pygame.Rect(0, 0, 16, 2)
    outline.bottom = hero.rect.top - 2 - 2 - 2 ## first 2 = loadbar x, second 2 = loadbar height, third 2 = spacing
    outline.centerx = hero.rect.centerx
    fill = pygame.Rect(outline.topleft, (outOf16, 2))
    drawLoad(display, outline, fill, (0, 0, 255))

## Priority:
#   - controls DONE
#   - physics DONE
#   - death DONEISH *****
#   - game over/restart DONE
#   - signs DONE
#   - starting animation DONE
#   - ash DONE
#   - icon DONE
#   - extra mechanics WORKING ON IT
#   - fine tune controls

def endTiles(end):
    x, y, w, h = end.x, end.y, end.width, end.height
    tiles = []
    for i in range(int(w) // 16):
        for j in range(int(h) // 16):
            tiles.append(pxToTile(int(x + i * 16), int(y + j * 16)))
    return tiles

def main():
    os.chdir(os.path.dirname(sys.argv[0]))
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    DISPLAY = init_screen(WIDTH, HEIGHT, 0) ## not resizable in the beginning
    pygame.mixer.music.load("Overworld.ogg")
    pygame.mixer.music.play(-1)
    
    ash = Ash(30, DISPLAY)
    startingAnimation(DISPLAY, ash)
    #DISPLAY = init_screen(WIDTH, HEIGHT)
    ash.setDisplay(temp_surface)

    global tmx_data, quad, map_layer, paused, onlyDirs, dir
    tmx_data = pytmx.load_pygame("level1.tmx")
    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.BufferedRenderer(map_data, (WIDTH/2, HEIGHT/2), clamp_camera=True)
    group = pyscroll.PyscrollGroup(map_layer=map_layer)
    hero = Protagonist("dudes//dude_right0.png")
    start = tmx_data.get_object_by_name("Start")
    end = tmx_data.get_object_by_name("End")
    hero.setPoint(start.x, start.y)
    group.add(hero)
    quad = pyscroll.quadtree.FastQuadTree(getAllRects())
    Environment.setDimensions(tmx_data.width * 16, tmx_data.height * 16)
    env = Environment([hero], [EnvironmentReference.applyGravity, EnvironmentReference.applyDrag, EnvironmentReference.solidGround, EnvironmentReference.keepInWindow, EnvironmentReference.collide])
    envSpring = Environment([hero], [EnvironmentReference.solidGround, EnvironmentReference.keepInWindow, EnvironmentReference.collide])
    envClimb = Environment([hero], [EnvironmentReference.keepInWindow, EnvironmentReference.stickToClimbable])

    dir = None
    pointDir = "right"
    jump = True
    num = -1
    springLoad = 0
    lastSpring = None
    startTime = None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            #elif event.type == VIDEORESIZE:
            #    init_screen(event.w, event.h)
            #    map_layer.set_size((event.w / 2, event.h / 2))
            elif event.type == KEYDOWN:
                if event.key in [K_w, K_UP] and jump:
                    jump = False
                    if inAir(hero) and round(math.degrees(hero.velocity.angle)) > 45  and round(math.degrees(hero.velocity.angle)) < 135 and hero.velocity.speed > Environment.gravity.speed:
                        hero.addVector(Vector(270, 8))
                    else:
                        hero.addVector(Vector(270, 6))
                    hero.update()
                    dir = "up"
                    num = 0
            elif event.type == KEYUP:
                if event.key == K_F12:
                    if not paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    paused = not paused
                if event.key == K_SPACE and springLoad > 0 and dir != None and (lastSpring == None or lastSpring + timeBetweenSprings <= time.time()):
                    lastSpring = time.time()
                    num = 5
                    x, y = getDelta()
                    if (x, y) != (0, 0):
                        jump = True
                        hero.setImage("dudes//dude_{}{}.png".format(dir, num))
                        hero.velocity = Vector(0, 0)
                        for i in range(springLoad * SPRING):
                            hero.updateAbsolute(x , y)
                            group.draw(temp_surface)
                            envSpring.update()
                            ash.update()
                            pygame.transform.scale(temp_surface, DISPLAY.get_size(), DISPLAY)
                            pygame.display.flip()
                            clock.tick(200)
                        springLoad = 0
                        hero.addVector(Environment.gravity)
                if event.key in [K_LSHIFT, K_v] and startTime == None:
                    startTime = time.time()
                    ## climbing
                    env, envClimb = envClimb, env
                    jump = False
            pygame.display.update()
        keysDown = pygame.key.get_pressed()
        if keysDown[K_d] or keysDown[K_RIGHT] and "right" in onlyDirs and (startTime == None or canMoveClimb(hero, "right")):
            hero.updateAbsolute(DT, 0)
            dir = "right"
            pointDir = "right"
            num = (num + 1) if num + 1 <= 4 else 1
        elif keysDown[K_LEFT] or keysDown[K_a] and "left" in onlyDirs and (startTime == None or canMoveClimb(hero, "left")):
            hero.updateAbsolute(-DT, 0)
            dir = "left"
            pointDir = "left"
            num = (num + 1) if num + 1 <= 4 else 1
        elif (keysDown[K_s] or keysDown[K_DOWN]) and inAir(hero) and "down" in onlyDirs and (startTime == None or canMoveClimb(hero, "down")):
            hero.updateAbsolute(0, DT)
            dir = "down"
            num = 0
        elif (keysDown[K_w] or keysDown[K_UP]) and "up" in onlyDirs and startTime != None and canMoveClimb(hero, "up"):
            hero.updateAbsolute(0, -DT)
            dir = "up"
        elif jump == True:
            dir = None
            num = -1
        if keysDown[K_SPACE]:
            if springLoad < 16 and startTime == None:
                springLoad += 1
                num = 6
        if atGround(hero) and not jump:
            jump = True
            dir = None
            num = -1
        if startTime != None:
            pass ## num = 9
        if dir in ["right", "left"]:
            hero.setImage("dudes//dude_{}{}.png".format(dir, num))
        elif dir in ["down", "up"] and num in (0, 5):
            hero.setImage("dudes//dude_{}{}.png".format(dir, num))
        elif dir == None and num == -1:
            hero.setImage("dudes//dude_{}0.png".format(pointDir))
        elif dir == None and num == 6:
            hero.setImage("dudes//dude_{}6.png".format(pointDir))
        group.center(hero.rect.center)
        group.draw(temp_surface)
        env.update()
        if springLoad > 0:
            showLoad(temp_surface, springLoad, hero)
        if startTime != None and startTime + climbMax <= time.time():
            startTime = None
            env, envClimb = envClimb, env
            onlyDirs = ["up", "down", "left", "right", None]
        elif startTime != None:
            timeToStop = startTime + climbMax - time.time()
            showClimbMeter(temp_surface, round(timeToStop * (16 // climbMax)), hero)
        for tile, props in getCollisions(hero).items():
            if props != None and "Type" in props.keys():
                if props["Type"] == "Kill":
                    if collideKill(hero, tile):
                        gameOverAnimation(DISPLAY, hero, ash)
                        hero.setPoint(start.x, start.y)
                        springLoad = 0
                        lastSpring = None
                        group.center(hero.rect.center)
                        group.draw(temp_surface)
                        pygame.transform.scale(temp_surface, DISPLAY.get_size(), DISPLAY)
                        pygame.display.flip()
                        while pygame.mixer.music.get_busy() and not paused:
                            pass
                        if not paused:
                            pygame.mixer.music.load("Overworld.ogg")
                            pygame.mixer.music.play(-1)
                elif props["Type"] == "Sign":
                    intro = tmx_data.get_object_by_name("Intro")
                    special = tmx_data.get_object_by_name("Special")
                    if tile[0] * 16 == intro.x:
                        text(DISPLAY, "Reach the other side", tile)
                    elif tile[0] * 16 == special.x:
                        text(DISPLAY, "Try out SPACE", tile)
                    else:
                        assert False, "There shouldn't be any other Signs"
            if tile in endTiles(end):
                winningAnimation(DISPLAY, ash)
        ash.update()
        pygame.transform.scale(temp_surface, DISPLAY.get_size(), DISPLAY)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(TITLE)
    Environment.setFunc("inAir", inAir)
    Environment.setFunc("putAtGround", putAtGround)
    Environment.setFunc("underground", underground)
    Environment.setFunc("atGround", atGround)
    Environment.setFunc("collide", collideTiles)
    Environment.setFunc("climbableCollision", climbableCollision)
    Environment.setFunc("restrictDirections", restrictDirections)
    main()
