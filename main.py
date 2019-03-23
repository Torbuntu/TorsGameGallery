import upygame as upg
import umachine as pok
import urandom as rand
import sprites
import sounds
import narwhalGlobals
import toastGlobals
import brickerGlobals

upg.display.init()
screen = upg.display.set_mode() # full screen
upg.display.set_palette_16bit([0,4124,0xd819,65535,0xf807,0xfe8c,0x07fe,])#default palette

#initialize the audio mixer: 
audio = upg.mixer.Sound() 
audio.reset() 
audio.play() 


#default settings
narwhalGlobals.title = True
narwhalGlobals.gameover = False

play = False
gameSelect = 1

while True:
    eventtype = upg.event.poll()
    
    #Game 1 Mecha Narwhal
    if gameSelect == 1 and play:
        # Set palette
        upg.display.set_palette_16bit([0xffff,0x03bb,0xf017,65535,0x5acb,0x07e8,0x0000,0xf800]);

        narwhalGlobals.time += 1
        screen.fill(1, upg.Rect(0,0,110,88)) 
        
        if narwhalGlobals.title:
            narwhalGlobals.drawTitle(screen, upg, eventtype)
        elif narwhalGlobals.gameover:
            narwhalGlobals.drawGameOver(screen, upg, eventtype)
        else:
            narwhalGlobals.drawMain(screen, upg, eventtype, audio)
        
        if narwhalGlobals.quit:
            play = False
            narwhalGlobals.quit = False
            #default settings
            narwhalGlobals.title = True
            narwhalGlobals.gameover = False
            upg.display.set_palette_16bit([0,4124,0xd819,65535,0xf807,0xfe8c,0x07fe,])
    
    #Game 2 is Angry Space Toast
    if gameSelect == 2 and play:  
        upg.display.set_palette_16bit([0,4124,0xd819,65535,0xf807,0xfe8c,0x07fe,])
        
        if toastGlobals.wait:
            toastGlobals.drawIntro(screen, upg, eventtype)
        else:
            toastGlobals.playAst(screen, upg, eventtype, audio)
        
        if toastGlobals.quit:
            play = False
            toastGlobals.quit = False
            upg.display.set_palette_16bit([0,4124,0xd819,65535,0xf807,0xfe8c,0x07fe,])
    
    #Game 3 is Inverted Bricker
    if gameSelect == 3 and play:
        # Set palette
        upg.display.set_palette_16bit([0xffff,0x4248,0x02dd,0xf819,0x5acb,0x07e8,0x0000,0xf800]);
        screen.fill(1, upg.Rect(0,0,110,88)) 
        
        if brickerGlobals.game_over:
            brickerGlobals.drawGameOver(screen, upg, eventtype)
        elif brickerGlobals.win:
            brickerGlobals.drawWin(screen, upg, eventtype)
        elif brickerGlobals.menu:
            brickerGlobals.drawMenu(screen, upg, eventtype)
        else:
            brickerGlobals.playBricker(screen, upg, eventtype, audio)
    
        if brickerGlobals.quit:
            play = False
            brickerGlobals.quit = False
            upg.display.set_palette_16bit([0,4124,0xd819,65535,0xf807,0xfe8c,0x07fe,])
        
    
    # Game menu settings
    if eventtype != upg.NOEVENT and not play:
            if eventtype.type == upg.KEYUP:
                if eventtype.key == upg.BUT_C:
                    play = True
                if eventtype.key == upg.K_RIGHT or eventtype.key == upg.K_DOWN:
                    if gameSelect < 3:
                        gameSelect = gameSelect + 1
                if eventtype.key == upg.K_LEFT or eventtype.key == upg.K_UP:
                    if gameSelect > 1:
                        gameSelect = gameSelect - 1
    if not play:
        
        if gameSelect == 1:
            upg.display.set_palette_16bit([0xffff,0x03bb,0xf017,65535,0x5acb,0x07e8,0x0000,0xf800])
            screen.fill(1, upg.Rect(0,0,110,88)) 
            
            pok.draw_text(1,1,"Tor's Game Gallery", 6)
            pok.draw_text(2,2,"Tor's Game Gallery", 3)
            pok.draw_text(1,12,"Press `C` to play:\n\nMecha Narwhal", 6)
            pok.draw_text(2,13,"Press `C` to play:\n\nMecha Narwhal", 3)
            screen.blit(sprites.narwhal_sprites[3], 40,45)
            screen.blit(sprites.enemies_sprites[0], 20,45)
            screen.blit(sprites.enemies_sprites[1], 75,45)
            
        if gameSelect == 2:
            upg.display.set_palette_16bit([0,4124,0xd819,65535,0xf807,0xfe8c,0x07fe,])
            pok.draw_text(2,2,"Tor's Game Gallery", 6)
            pok.draw_text(2,13,"Press `C` to play:\n\nAngry Space Toast", 6)
            screen.blit(sprites.asteroid, 45, 40)
            screen.blit(sprites.asteroid, 45, 74)
            screen.blit(sprites.asteroid, 24, 64)
            screen.blit(sprites.asteroid, 68, 45)
            screen.blit(sprites.introRocket, 50, 60)
            screen.blit(sprites.introThrusters, 46, 62)
            
            
        if gameSelect == 3:
            upg.display.set_palette_16bit([0xffff,0x4248,0x02dd,0xf819,0x5acb,0x07e8,0x0000,0xf800])
            screen.fill(1, upg.Rect(0,0,110,88)) 
            screen.blit(sprites.Paddle, 35, 45)
            screen.blit(sprites.Ball, 42, 50)
            screen.blit(sprites.BrickPurp, 50, 74)
            pok.draw_text(1,1,"Tor's Game Gallery", 6)
            pok.draw_text(2,2,"Tor's Game Gallery", 7)
            pok.draw_text(1,12,"Press `C` to play:\n\nInverted Bricker", 6)
            pok.draw_text(2,13,"Press `C` to play:\n\nInverted Bricker", 7)
        
    upg.display.flip()# Do regardless
