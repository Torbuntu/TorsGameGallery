import upygame as upg
import umachine as pok
import framebuf
import urandom as rand
import sprites
import narwhalGlobals
import toastGlobals
import brickerGlobals

upg.display.init()
screen = upg.display.set_mode() # full screen
upg.display.set_palette_16bit([0,4124,0xd819,65535,0xf807,0xfe8c,0x07fe,])#default palette

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
            narwhalGlobals.drawMain(screen, upg, eventtype)
        
        if narwhalGlobals.quit:
            play = False
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
            toastGlobals.playAst(screen, upg, eventtype)
        
        if toastGlobals.quit:
            play = False
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
            brickerGlobals.playBricker(screen, upg, eventtype)
    
        if brickerGlobals.quit:
            play = False
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
        pok.draw_text(1,1,"Tor's Game Gallery", 3)
        if gameSelect == 1:
            pok.draw_text(1,12,"Press `C` to play:\n\nMecha Narwhal", 3)
        if gameSelect == 2:
            pok.draw_text(1,12,"Press `C` to play:\n\nAngry Space Toast", 3)
        if gameSelect == 3:
            pok.draw_text(1,12,"Press `C` to play:\n\nInverted Bricker", 3)
        
    upg.display.flip()# Do regardless
