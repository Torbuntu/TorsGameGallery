# brickerGlobals.py
import upygame as upg
import umachine as pok
import urandom as rand
import sprites
import sounds

bricks = []
ball = {}
paddle = {}
particles = []
score = 0
active = False
game_over = False
life = 3
win = False
menu = True
intX = 42
intY = 40
intYS = 5
quit = False

def initBricker():
    global quit, ball, bricks, paddle, score, active, game_over, life, win, intX, intY, intYS
    quit = False
    for x in range(0,9):
        brick = {"x":(x*12)+1,"y":74,"w":10,"h":4, "img":sprites.BrickRed, "hit":False}
        bricks.append(brick)
    for x in range(0,9):
        brick = {"x":(x*12)+1,"y":68,"w":10,"h":4, "img":sprites.BrickGreen, "hit":False}
        bricks.append(brick)
    for x in range(0,9):
        brick = {"x":(x*12)+1,"y":62,"w":10,"h":4, "img":sprites.BrickBlue, "hit":False}
        bricks.append(brick)
    for x in range(0,9):
        brick = {"x":(x*12)+1,"y":56,"w":10,"h":4, "img":sprites.BrickPurp, "hit":False}
        bricks.append(brick)
    ball = {"x":5, "y":5, "w":4,"h":4,"ys":2,"xs":3}
    paddle = {"x":5, "y":5, "w":14,"h":3,"xs":0}
    score = 0
    active = False
    game_over = False
    life = 3
    win = False
    particles = []
    intX = 42
    intY = 40
    intYS = 5
 

def bouncy(screen):
    global intYS, intY, intX
    screen.blit(sprites.Paddle, 30,35)
    screen.blit(sprites.Ball, intX, intY)
    if intY > 60:
        intYS = -intYS
    if intY < 40:
        intYS = -intYS
    intY = intY + intYS

#collide methods
def collide(rx, ry, ax, ay):
    if ((rx > ax) and (rx < ax+12) and (ry+4 > ay) and (ry < ay+4)):
        return True
    else:
        return False
 
def collideP(rx, ry, ax, ay):
    global ball
    if ((rx > ax) and (rx < ax+28) and (ry+4 > ay) and (ry < ay+4)):
        if (rx < ax+14):
            ball["xs"] = ball["xs"] - 1
        else:
            ball["xs"] = ball["xs"] + 1
        return True
    else:
        return False  
        
def collideT(rx, ry, ax, ay):
    if ((rx > ax) and (rx < ax+28) and (ry+4 > ay) and (ry < ay+4)):
        return True
    else:
        return False 
###########################


def playBricker(screen, upg, eventtype, audio):
    global life, paddle, active, ball, bricks, particles, score, game_over, win 
    if eventtype != upg.NOEVENT:
        if eventtype.type== upg.KEYDOWN:
            if eventtype.key == upg.K_RIGHT or eventtype.key == upg.BUT_A:
                paddle["xs"] = 5
            if eventtype.key == upg.K_LEFT or eventtype.key == upg.BUT_B:
                paddle["xs"] = -5
        if eventtype.type == upg.KEYUP:
            if eventtype.key == upg.BUT_C:
                if active is False:
                    active = True
                    ball["xs"] = rand.getrandbits(2)-1
                    if ball["xs"] is 0:
                        ball["xs"] = -3
                    ball["ys"] = -2
            if eventtype.key == upg.K_RIGHT or eventtype.key == upg.BUT_A:
                paddle["xs"] = 0
            if eventtype.key == upg.K_LEFT or eventtype.key == upg.BUT_B:
                paddle["xs"] = 0
    
    #Collision checks
    for x in list(bricks):
        if collide(ball["x"], ball["y"], x["x"], x["y"]):
            ball["ys"] = -ball["ys"]
            part = {"x": (ball["x"]+1), "y": ball["y"]}
            particles.append(part)
            bricks.remove(x)
            audio.play_sfx(sounds.high, len(sounds.high), True)
            
            
    for x in list(particles):
        x["y"] = x["y"] - 1
        if collideT(x["x"], x["y"], paddle["x"], paddle["y"]):
            particles.remove(x)
            score = score + 10
        else:
            screen.blit(sprites.particle, x["x"], x["y"])
    
    if collideP(ball["x"], ball["y"], paddle["x"], paddle["y"]):
        ball["ys"] = -ball["ys"]
        audio.play_sfx(sounds.low, len(sounds.low), True)
        
    #Updating positions
    if ball["x"] > 106:
        ball["xs"] = -ball["xs"]
        audio.play_sfx(sounds.mid, len(sounds.mid), True)
    if ball["x"] < 1:
        ball["xs"] = -ball["xs"]
        audio.play_sfx(sounds.mid, len(sounds.mid), True)
    if ball["y"] > 84:
        ball["ys"] = -ball["ys"]
        audio.play_sfx(sounds.mid, len(sounds.mid), True)
    if ball["y"] < 1:
        active = False
        if life > 0:
            score = score - 10
            life = life -1
        else:
            audio.play_sfx(sounds.lost, len(sounds.lost), True)
            game_over = True
        
    if active is False:
        ball["xs"] = 0
        ball["ys"] = 0
        ball["x"] = paddle["x"] + 13
        ball["y"] = paddle["y"] + 4
        
    if paddle["x"]+28 > 106 and paddle["xs"] > 0:
        paddle["xs"] = 0
    if paddle["x"]-4 < 1 and paddle["xs"] < 0:
        paddle["xs"] = 0
        
    ball["x"] = ball["x"] + ball["xs"]
    ball["y"] = ball["y"] + ball["ys"]
    paddle["x"] = paddle["x"] + paddle["xs"]
    
    
    #Drawing
    if len(bricks) is 0:
        win = True
        audio.play_sfx(sounds.success, len(sounds.success), True)
        
    for x in range(life):
        screen.blit(sprites.Ball, x*4, 1)
    screen.blit(sprites.Ball, ball["x"], ball["y"] )
    screen.blit(sprites.Paddle, paddle["x"], paddle["y"])
    for b in bricks:
        screen.blit(b["img"], b["x"], b["y"])
    
    pok.draw_text(1, 80, "Score: "+str(score),6)
    pok.draw_text(2, 81, "Score: "+str(score),7)
    
def drawMenu(screen, upg, eventtype):
    global quit, menu
    bouncy(screen)
    pok.draw_text(1, 2, "Press `C`\n  to begin",6)
    pok.draw_text(2, 3, "Press `C`\n  to begin",7)
    if eventtype != upg.NOEVENT:
        if eventtype.type == upg.KEYUP:
            if eventtype.key == upg.BUT_C:
                initBricker()
                menu = False
            if eventtype.key == upg.BUT_B:
                quit = True
def drawWin(screen, upg, eventtype):
    global quit
    bouncy(screen)
    pok.draw_text(1, 2, "You Won!\n Score: "+str(score),6)
    pok.draw_text(2, 3, "You Won!\n Score: "+str(score),7)
    if eventtype != upg.NOEVENT:
        if eventtype.type == upg.KEYUP:
            if eventtype.key == upg.BUT_C:
                initBricker()
            if eventtype.key == upg.BUT_B:
                quit = True
                
def drawGameOver(screen, upg, eventtype):
    global quit
    pok.draw_text(1, 2, "Game Over...\n Score: "+str(score),6)
    pok.draw_text(2, 3, "Game Over...\n Score: "+str(score),7)
    if eventtype != upg.NOEVENT:
        if eventtype.type == upg.KEYUP:
            if eventtype.key == upg.BUT_C:
                initBricker()
            if eventtype.key == upg.BUT_B:
                quit = True