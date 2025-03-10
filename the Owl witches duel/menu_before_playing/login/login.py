import global_var
import pygame
from usefull_classes.button import button
import sentOperations.sendingOperations as sockF
from usefull_classes.textEnterens import textEnterens
from usefull_classes.elart import elart

def toOtherFile(file):
    """go to another window
    :param file: path to next window
    :type file: string"""
    global done
    global_var.nextRunFileName=file
    done=True

def sendrequest():
    """send login request"""
    global username
    username= entrens[0].get_text()
    sockF.sendMesegTCP(global_var.server_TCP_sock,"LOGIN|LOGIN|"+entrens[0].get_text()+"|"+entrens[1].get_text())

def main():
    """the code of this window. it's screen is in global_var.screen."""
    global done
    global entrens
    global username

    global_var.unconnected_exit_check("menu_before_playing.mane_menu")
    
    done = False
    clock = pygame.time.Clock()

    buttons=[button(lambda: toOtherFile("menu_before_playing.mane_menu"),(20,20,200,50),(255,0,0),"back"),
             button(sendrequest,(700,600,200,50),(255,0,0),"login"),
             button(lambda: toOtherFile("menu_before_playing.login.singIn"),(1280,20,200,50),(255,0,0),"sign in")]
    username= None

    font= pygame.font.SysFont("Algerian", 30)
    title_font= pygame.font.SysFont("Algerian", 50)
    texts= [((740,160),title_font.render("Log in", True, (186, 201, 0))),
            ((450,250),font.render("username:", True, (186, 201, 0))),
            ((450,410),font.render("password:", True, (186, 201, 0)))]
    entrens= [textEnterens((450, 290, 750, 100),(255,255,255)),
              textEnterens((450, 450, 750, 100),(255,255,255),enter_type="password")]

    while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            global_var.for_menu_screen()

            #ticking anything
            for o in buttons+entrens:
                o.tick()

            for t in texts:
                if t!=None:
                    global_var.screen.blit(t[1], t[0])

            #server meseges handeling
            serverMsg= sockF.unpucketMasegTCP(global_var.server_TCP_sock)
            if serverMsg!="":
                serverMsg=serverMsg.split("|")
                print(serverMsg)
                if len(serverMsg)==1 and serverMsg[0]=="UNCORRECT CERTIFICATES":
                    global_var.alert_data= ("username or password is wrong",(600,10,300,100))
                if len(serverMsg)==2 and serverMsg[0]=="DONE":
                    global_var.from_str_to_settings(serverMsg[1])
                    global_var.sound_volume_correct()
                    global_var.username= username
                    toOtherFile("menu_before_playing.mane_menu")

            global_var.before_menu_screen_display()

            pygame.display.flip()
            clock.tick(24)
            

if __name__=="__main__":
        main()
else:
        print(__name__)
