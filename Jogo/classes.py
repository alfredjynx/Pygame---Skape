import pygame
from random import randint, seed
import math

# carrega o sprite do personagem principal, o skatista
class SkatistaSprite(pygame.sprite.Sprite):

    # inicializa a classe com os valores do retângulo da imagem, a imagem em si, o nome da classe e o centro do retângulo
    # valores mudam conforme o jogo vai sendo jogado
    def __init__(self, picture_load, name, y):
        super().__init__()
        self.image = picture_load
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.center = [50, y]

    # desenha a imagem na tela utilizando os valores da inicialização
    def render(self, window):
        window.blit(self.image, self.rect.center)


# serve para concentrar todas as funções relacionadas a funções matemáticas e derivados da curva principal do jogo
class Funcao_e_derivado:

    # inicializa a classe com a posição do x
    def __init__ (self, x):
        self.x = x

    # devolve a função da linha
    def get_function(x, a, b, c, d):
        return (((math.sin(math.radians(a*x+c)))+1)*b)+440+d

    # retorna o derivado da curva
    def get_derivado(x,a,b,c):
        return a*b*math.cos(math.radians(x*a+c))

    # retorna o vale (oposto do pico) da curva de seno
    def get_trough(a,c):
        return (90-c)/a

    # faz um update no valor do vale (trough)
    def update_trough(before, a):
        return before + 360/a

    # retorna o pico (oposto de vale) da curva de seno
    def get_crest(a,c):
        return (270-c)/a

    # faz um update no valor do pico (crescent)
    def update_crest(before, a):
        return before + 360/a 


# não possui métodos adicionais pois serve para guardar o valores da curva de seno
# IMPORTANTE: no caso de uma expansão, é importante que esses valores não sejam fixos, e sim, definidos pelo construtor (randomização de curvas)
class Morro:
    def __init__ (self,x,a,b,c,d):
        self.x = x
        self.y = Funcao_e_derivado.get_function(x,a,b,c,d)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.cor = (253, 218, 13)
        self.raio = 2

# classe da linha como um todo, com todos os morros
class Morros:
    def __init__ (self,x,a,b,c,d):
            self.linhaMorro = Morro(x, a, b, c, d)


# Tela de morte e todas informações pertinentes ao seu botão e método de desenhar a tela
class Morte:

    # inicia a classe com número de botões, a imagem da tela, coordenadas dos botões (com altura e largura) e posição do mouse
    def __init__(self):
        self.tela = pygame.image.load("Telas/Morte.png")
        self.buttons = 1
        self.coord = (125,510),(390,75)
        self.nome = "morte"
        self.mouse_pos = False

    # desenha tela e os retângulos que indicam se o mouse está em cima do botão ou não
    def desenha(self,window,state):
        window.blit(self.tela,(0,0))
        if self.mouse_pos:
            self.desenha_rect(window,state)

    # checa se o mouse está em cima do botão
    def clique(self,x,y):
        ret1 = pygame.rect.Rect(self.coord)

        if ret1.collidepoint(x,y):
            return True
        return False

    # desenha os retângulos que indicam se o mouse está ou não em cima do botão
    def desenha_rect(self,window:pygame.Surface,state):
        pygame.draw.rect(window,(255, 238, 204),state["tela"].coord,3)
        
        
# Tela de morte e todas informações pertinentes aos seus botões e método de desenhar a tela
class Inicio:

    # inicia a classe com número de botões, a imagem da tela, coordenadas dos botões (com altura e largura) e posição do mouse
    def __init__(self):
        self.tela = pygame.image.load("Telas/Inicio.png")
        self.buttons = 2
        self.coord = (196,432),(247,48)
        self.coord2 = (196,497),(247,48)
        self.nome = "inicio"
        self.mouse_pos = False
    
    # desenha tela e os retângulos que indicam se o mouse está em cima de um dos botões ou não
    def desenha(self,window,state):
        window.blit(self.tela,(0,0))
        if self.mouse_pos:
            self.desenha_rect(window,state)

    # checa se o mouse está em cima de um botão
    def clique(self,x,y):
        ret1 = pygame.rect.Rect(self.coord)
        ret2 = pygame.rect.Rect(self.coord2)

        # botão de jogar
        if ret1.collidepoint(x,y):
            self.colide = 1
            return True

        # botão de regras
        elif ret2.collidepoint(x,y):
            self.colide = 2
            return True

        return False

    # desenha os retângulos que indicam se o mouse está ou não em cima de um dos botões (checa qual que é)
    def desenha_rect(self,window:pygame.Surface,state):
        if self.colide == 1:
            pygame.draw.rect(window,(255, 238, 204),state["tela"].coord,3)
            
        else:
            pygame.draw.rect(window,(255, 238, 204),state["tela"].coord2,3)
            

# Tela de morte e todas informações pertinentes ao seu botão e método de desenhar a tela
class Regras:

    # inicia a classe com número de botões, a imagem da tela, coordenadas dos botões (com altura e largura) e posição do mouse
    def __init__(self):
        self.tela = pygame.image.load("Telas/Regras.png")
        self.buttons = 1
        self.coord = (81,460),(478,90)
        self.nome = "regras"
        self.mouse_pos = False
    
    # desenha tela e os retângulos que indicam se o mouse está em cima do botão ou não
    def desenha(self,window,state):
        window.blit(self.tela,(0,0))
        if self.mouse_pos:
            self.desenha_rect(window,state)

    # checa se o mouse está em cima do botão
    def clique(self,x,y):
        ret1 = pygame.rect.Rect(self.coord)
        
        if ret1.collidepoint(x,y):
            return True
        return False
    
    # desenha os retângulos que indicam se o mouse está ou não em cima do botão
    def desenha_rect(self,window:pygame.Surface,state):
        pygame.draw.rect(window,(255, 238, 204),state["tela"].coord,3)

