# toastGlobals.py
import upygame as upg
import umachine as pok
import urandom as rand
import asteroid as ast
import sprites
import sounds

acc = False # Accelerating
health = 25
shieldpercent = 100
a1 = ast.createAsteroid(5, 0, 1, 1)
a2 = ast.createAsteroid(10, 0, -1, 2)
a3 = ast.createAsteroid(20, 0, 1, 1)
a4 = ast.createAsteroid(35, 0, -1, 2)
a5 = ast.createAsteroid(50, 0, 1, 1)
a6 = ast.createAsteroid(75, 0, -1, 2)
asteroids = [a1, a2, a3, a4, a5, a6]

dustParts = []
for i in range(0, 25):
    dus = {"x": rand.getrandbits(8), "y": 0, "vy": rand.getrandbits(3)+1}
    dustParts.append(dus)

# Player coords and velocity
x=20
y=80
vx = 0
vy = 0

wait = True
score = 0
best = 0

introX = 60
introY = 20
introvy = 1
introvx = 1
quit = False
# Reinitialize game variables
def initToast():
    global quit, a1, a2, a3, a4, a5, a6, acc, health, shieldpercent, x, y, vx, vy, wait, score, introX, introY, asteroids, dustParts
    quit = False
    acc = False
    health = 25
    shieldpercent = 100
    a1 = ast.createAsteroid(5, 0, 1, 1)
    a2 = ast.createAsteroid(10, 0, -1, 2)
    a3 = ast.createAsteroid(20, 0, 1, 1)
    a4 = ast.createAsteroid(35, 0, -1, 2)
    a5 = ast.createAsteroid(50, 0, 1, 1)
    a6 = ast.createAsteroid(75, 0, -1, 2)
    asteroids = [a1, a2, a3, a4, a5, a6]
    dustParts = []
    for i in range(0, 25):
        dus = {"x": rand.getrandbits(8), "y": 0, "vy": rand.getrandbits(3)+1}
        dustParts.append(dus)
    
    x=20
    y=80
    vx = 0
    vy = 0
    wait = True
    score = 0
    introX = 60
    introY = 20
################End initialize   

#collide with asteroid
def collide(rx, ry, ax, ay):
    global shieldpercent, health, wait, score, best
    
    if ((rx+2 < ax + 16) and (rx + 6 > ax) and (ry < ay + 16) and (ry + 8 > ay)):
        shieldpercent -= 1
        if shieldpercent < 0:
            health -= 1
        return True
    else:
        return False
###########################


#move asteroids
def moveA(ax, ay, avx, avy):
    if ay > 90:
        ay = -16
        avy = rand.getrandbits(1)
        if avy == 0:
            avy = 2
        ax = rand.getrandbits(6)
        if avx < 0:
            avx = 1
        else:
            avx = -1
            
    if ax > 110:
        ax = -16
    if ax < -17:
        ax = 100
    
    ax = ax + avx
    ay = ay + avy
    
    return ax, ay, avx, avy
################################

# Intro drawing and updating.
def drawIntro(screen, upg, eventtype):
    global quit, introX, introY, introRocket, introThrusters, introvx, introvy, wait, Title
    
    rand.getrandbits(10)#generate more randoms when starting
    screen.blit(sprites.Title, 0, 0)
    pok.draw_text( 8, 62, "Press A", 2) 
    pok.draw_text(8, 72, "Avoid The Toast!", 2)
    
    screen.blit(sprites.asteroid, 12, introY - 2)
    screen.blit(sprites.asteroid, 32, introY - 4)
    
    screen.blit(sprites.introRocket, introX, introY)
    screen.blit(sprites.introThrusters, introX-4, introY+2)
    if introX > 85:
        introvx = -1
    if introX < 60:
        introvx = 1
    if introY > 25:
        introvy = -1
    if introY < 15:
        introvy = 1
    introX = introX + introvx
    introY = introY + introvy
        
    if score > 0:
        pok.draw_text(8, 52, "Best: " + str(score), 2)
    if eventtype != upg.NOEVENT:
        if eventtype.key == upg.BUT_A:
            initToast()
            wait = False
        if eventtype.key == upg.BUT_B:
            quit = True
#################################


#Move Player
def moveP(upg, eventtype):
    global x, y, vx, vy, shieldpercent, acc
    
    if eventtype != upg.NOEVENT:
        if eventtype.type== upg.KEYDOWN:
            if eventtype.key == upg.K_RIGHT:
                if shieldpercent > 0:
                    vx = 1
                else:
                    vx = 2
            if eventtype.key == upg.K_LEFT:
                if shieldpercent > 0:
                    vx = -1
                else:
                    vx = -2
            if eventtype.key == upg.BUT_A or eventtype.key == upg.K_UP:
                vy = -2
                acc = True
        if eventtype.type == upg.KEYUP:
            if eventtype.key == upg.K_RIGHT:
                vx = 0
            if eventtype.key == upg.K_LEFT:
                vx = 0
            if eventtype.key == upg.BUT_A or eventtype.key == upg.K_UP:
                vy = 1
                acc = False

    if y == 80 and vy > 0:
        vy = 0
        
    if x+vx == 0 or x+vx == 102:
        vx = 0
        
    if y+vy < 4:
        vy = 0
        
    x = x + vx
    y = y + vy
    
###############


def playAst(screen, upg, eventtype, audio):
    global score, asteroids, health, shieldpercent, acc, dustParts, wait, best
    #Score logic
    score += 1
    
    # Start player movement
    moveP(upg, eventtype)
    #End player movement
    
    
    # Check player collide on asteroids
    for a in asteroids:
        if collide(x, y, a.x, a.y):
            screen.blit(sprites.danger, 1, 16)
    ###################################
    
    # Draw and move asteroids    
    for a in asteroids:
        a.x, a.y, a.vx, a.vy = moveA(a.x, a.y, a.vx, a.vy)
        screen.blit(sprites.asteroid, a.x, a.y)
    ##########################
    
    # Check shields and health
    if shieldpercent > 0:
        screen.blit(sprites.shield, x-2, y-2)
        for slx in range(shieldpercent):
            screen.blit(sprites.shieldicon, slx+15, 1)
            
    if health > 0:
        pok.draw_text(1, 5, str(score), 2)
        for hlx in range(health):
            screen.blit(sprites.healthicon, hlx, 1)
            
    if health < 0:
        print("ded")
        audio.play_sfx(sounds.lost, len(sounds.lost), True)
        if best < score:
            best = score
        wait = True
    ###############################
        
    # Draw rocket thrusters and dust particles
    screen.blit(sprites.rocket, x, y)
    if acc:
        screen.blit(sprites.thrusters, x+2, y+8)
        
    for i in dustParts:
        i["y"] = i["y"] + i["vy"]
        if i["y"] > 90:
            i["y"] = 0
            i["vy"] = rand.getrandbits(3)+1
        screen.blit(sprites.dust, i["x"], i["y"])
    #########################################
