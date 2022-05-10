import pygame

class Morte:

    def __init__(self):
        self.tela = pygame.image.load("Morte.png")
        self.buttons = 1
        self.coord = (125,510),(390,75)
        self.nome = "morte"
        self.mouse_pos = False
    
    def desenha(self,window):
        window.blit(self.tela,(0,0))
        if self.mouse_pos:
            self.desenha_rect(window)

    
    def clique(self,x,y):
        ret1 = pygame.rect.Rect(self.coord)

        if ret1.collidepoint(x,y):
            return True
        return False

    def desenha_rect(self,window:pygame.Surface):
        pygame.draw.rect(window,(255, 238, 204),state["tela"].coord,3)
        
        

class Início:

    def __init__(self):
        self.tela = pygame.image.load("Início.png")
        self.buttons = 2
        self.coord = (196,432),(247,48)
        self.coord2 = (196,497),(247,48)
        self.nome = "início"
        self.mouse_pos = False
    
    def desenha(self,window):
        window.blit(self.tela,(0,0))
        if self.mouse_pos:
            self.desenha_rect(window)


    def clique(self,x,y):
        ret1 = pygame.rect.Rect(self.coord)
        ret2 = pygame.rect.Rect(self.coord2)

        if ret1.collidepoint(x,y):
            self.colide = 1
            return True

        elif ret2.collidepoint(x,y):
            self.colide = 2
            return True

        return False

    def desenha_rect(self,window:pygame.Surface):
        if self.colide == 1:
            pygame.draw.rect(window,(255, 238, 204),state["tela"].coord,3)
            
        else:
            pygame.draw.rect(window,(255, 238, 204),state["tela"].coord2,3)
            

        


class Regras:

    def __init__(self):
        self.tela = pygame.image.load("Regras.png")
        self.buttons = 1
        self.coord = (81,460),(478,90)
        self.nome = "regras"
        self.mouse_pos = False
    
    def desenha(self,window):
        window.blit(self.tela,(0,0))
        if self.mouse_pos:
            self.desenha_rect(window)

    def clique(self,x,y):
        ret1 = pygame.rect.Rect(self.coord)
        
        if ret1.collidepoint(x,y):
            return True
        return False
    
    def desenha_rect(self,window:pygame.Surface):
        pygame.draw.rect(window,(255, 238, 204),state["tela"].coord,3)
        
    


def inicializa():
    pygame.init()
    w = pygame.display.set_mode((640, 640))
    pygame.key.set_repeat(50)
    myfont = pygame.font.SysFont("Minecraft Médio",70)

    morte = Morte()
    início = Início()
    regras = Regras()

    assets = {"morte":morte,"início":início,"regras":regras,"fonte":myfont}
    state = {"tela":início}
    
    return w, assets, state


def finaliza():
    pygame.quit()


def desenha(window: pygame.Surface, state):
    window.fill((0, 0, 0))
    state["tela"].desenha(window)
    pygame.display.update()



def atualiza_estado(assets, state):

    x,y = pygame.mouse.get_pos()
    resultado = state["tela"].clique(x,y)
    if resultado:
        state["tela"].mouse_pos = True
    else:
        state["tela"].mouse_pos = False

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return False
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_1:
                # print("1")
                state["tela"] = assets["início"]
            elif ev.key == pygame.K_2:
                # print("2")
                state["tela"] = assets["regras"]
            elif ev.key == pygame.K_3:
                # print("3")
                state["tela"] = assets["morte"]

        elif ev.type == pygame.MOUSEBUTTONUP:
            x,y = ev.pos
            resultado = state["tela"].clique(x,y)
            if resultado:
                if state["tela"].nome == "início":
                    
                        
                    if state["tela"].colide == 1:
                        state["tela"] = assets["morte"]
                    
                    elif state["tela"].colide == 2:
                        state["tela"] = assets["regras"]
                    
                elif state["tela"].nome == "regras" or state["tela"].nome == "morte":
                    
                    state["tela"] = assets["início"]

    return True


def gameloop(window, assets, state):
    while atualiza_estado(assets,state):
        desenha(window,state)

    
if __name__ == '__main__':
    window, assets, state= inicializa()
    gameloop(window, assets, state)
    finaliza()

