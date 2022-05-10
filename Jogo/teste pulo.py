from random import randint
from classes import *
import pygame
import math


def inicializa():
    pygame.init()
    window = pygame.display.set_mode((640, 480), vsync=True, flags=pygame.SCALED)
    pygame.key.set_repeat(50)

    assets = {
    }
    skatista = Skatista(120)
    state = {
        'mouse_pressed' : False,
        'grav_forte': False,
        'gravidade' : 98,
        'skate_pos': [skatista.x, skatista.y],
        'skate_raio': skatista.raio,
        'skate_cor': skatista.cor,
        'skate_vel': [20, -10],
        'last_updated': 0,
        'linha_morro': [],
        'fez_contato_descida': False,
        'fez_contato_subida': False,
        'pulou': False,
        'ponto_comecou_morro': 0,
        'morro_last_updated': 0
    }
    cria_morros(state)
    return window, assets, state

def cria_morros(state):
    for x in range (640):
        morro = Morros(x)
        state['linha_morro'].append(morro)

def desenha(window: pygame.Surface, assets, state):
    window.fill((0, 0, 0))
    for morro in state['linha_morro']:
        pygame.draw.circle(window, (morro.linhaMorro.cor[0], morro.linhaMorro.cor[1], morro.linhaMorro.cor[2]), (morro.linhaMorro.x, morro.linhaMorro.y), morro.linhaMorro.raio)
        state['morro_last_updated'] = 641
    pygame.draw.circle(window, (255, 0, 0), (state['skate_pos'][0], state['skate_pos'][1]), state['skate_raio'])
    pygame.display.update()

def reverte_velocidades(state):
    if state['skate_pos'][0] + 10 > 640:
        state['skate_vel'][0] = -(abs(state['skate_vel'][0]))
    if state['skate_pos'][1] + 10 > 480:
        state['skate_vel'][1] = -(abs(state['skate_vel'][1]))
    if state['skate_pos'][0] - 10 < 0:
        state['skate_vel'][0] = abs(state['skate_vel'][0])
    if state['skate_pos'][1] - 10 < 0:
        state['skate_vel'][1] = abs(state['skate_vel'][1])

def adapta_gravidade_velocidade_colisao_morro(state):
    if colisao_ponto_circulo(state['skate_pos'][0], Funcao_e_derivado.get_function(state['skate_pos'][0]), state['skate_pos'][0], state['skate_pos'][1], 10):
        derivado = Funcao_e_derivado.get_derivado(state['skate_pos'][0],2,-70)
        maxSeno = Funcao_e_derivado.get_crest(2,-70)
        minSeno = Funcao_e_derivado.get_trough(2,-70)
        state['skate_vel'] = [state['skate_vel'][0], derivado]
        if (derivado > 0 or state['fez_contato_descida']) and not state['fez_contato_subida']:
            state['fez_contato_descida'] = True
            if state['skate_vel'][0] < 100:
                state['skate_vel'][0] *= 1.1
            if abs((state['skate_pos'][0] - maxSeno)) % 180 < 20:
                print('vel y:, {}'.format(state['skate_vel'][1]))
                # state['skate_vel'][1] = derivado * 100 ##mudar para b*a
                # state['skate_vel'][1] = derivado * 100
                print(derivado)
                state['pulou'] = True
                state['fez_contato_descida'] = False
        if (derivado < 0 or state['fez_contato_subida']) and not state['fez_contato_descida'] and not state['pulou']:
            if abs((state['skate_pos'][0] - minSeno)) % 180 < 90:
                state['fez_contato_subida'] = True
                state['skate_vel'][0] = 20
                if abs((state['skate_pos'][0] - maxSeno)) % 180 < 5:
                    state['fez_contato_descida'] = True
                    state['fez_contato_subida'] = False
        state['skate_pos'][1] = Funcao_e_derivado.get_function(state['skate_pos'][0]) - 12
def colisao_ponto_circulo(ponto_x, ponto_y, circulo_x, circulo_y, circulo_raio):
    if math.sqrt((ponto_x-circulo_x)**2 + (ponto_y-circulo_y)**2) <= circulo_raio:
        return True
    return False

# def colisao_ponto_retangulo(ponto_x, ponto_y, rect_x, rect_y, rect_w, rect_h):
#     if (ponto_x > rect_x and ponto_x < rect_x + rect_w) and (ponto_y > rect_y and ponto_y < rect_y + rect_h):
#         return True
#     return False

def atualiza_estado(assets, state):
    totalTicks = pygame.time.get_ticks()
    deltaT = (totalTicks - state['last_updated'])/1000
    state['skate_pos'][0] += (state['skate_vel'][0] * deltaT)
    state['skate_vel'][1] += state['gravidade'] * deltaT
    state['skate_pos'][1] += (state['skate_vel'][1] * deltaT)
    reverte_velocidades(state)
    adapta_gravidade_velocidade_colisao_morro(state)


    if state['skate_pos'][1] <= 340 and state['mouse_pressed'] and not state['grav_forte']:
        state['gravidade'] *= 4
        state['grav_forte'] = True
    if state['skate_pos'][1] > 340 and state['grav_forte']:
        state['gravidade'] /= 4
        state['grav_forte'] = False

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                state['mouse_pressed'] = True
        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                state['mouse_pressed'] = False
                if state['skate_pos'][0] <= 340 and state['grav_forte']:
                    state['gravidade'] /= 4
                    state['grav_forte'] = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                state['skate_vel'][1] = -200
                state['skate_vel'][0] = 50
    state['last_updated'] = totalTicks
    return True

def gameloop(window, assets, state):
    while atualiza_estado(assets, state):
        desenha(window, assets, state)

def finaliza():
    pygame.quit()

if __name__ == '__main__':
    window, assets, state = inicializa()
    gameloop(window, assets, state)
    finaliza()

'''
⠄⠄⠄⠄⠄⠄⠄⠄⣀⣠⣶⣾⣿⣶⣦⣀⠄⣀⣶⣾⣷⣶⣤⡀⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠄⣠⣿⣿⢟⣯⣶⣶⣼⣻⣧⡙⣿⢫⣶⣶⣬⣿⡆⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⢀⣿⡿⢣⣾⣿⣿⣿⣿⣿⣿⣿⡱⣾⣿⣿⣿⣿⣿⣇⠄⠄⠄⠄
⠄⠄⠄⠄⠄⢀⣾⣿⣶⣿⣿⡿⢿⡛⠛⠛⠛⣿⣷⢹⡿⣿⠿⣟⡛⠛⣷⠄⠄⠄
⠄⠄⠄⣴⡆⣼⣿⣿⣿⣿⣿⡾⣵⠖⣹⣿⣭⠐⠈⢸⣝⣵⠟⣴⣾⣷⡖⢀⠄⠄
⠄⢀⣿⣿⣧⣿⣿⠿⠽⣟⣷⡟⣥⣿⣿⣿⣧⠉⠭⢸⣿⡏⠘⡻⢿⣿⣧⠁⠄⠄
⢀⣿⣿⣿⣿⣿⣿⠭⣟⣻⣷⣤⣄⣀⣤⣤⣴⣶⢿⡃⣿⣇⣻⢲⣮⣑⣲⣶⡂⠄
⢸⣿⣿⣿⣿⣿⣿⣿⣯⣷⣿⣿⣿⣿⣯⣭⣭⠽⣃⣵⣿⣿⣿⣷⣸⣯⣔⣒⡀⠄
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣶⣿⣿⣿⣿⠿⣛⣋⣩⣭⣭⣭⣙⡀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⠟⣽⡅⣫⡀⣼⣿⣿⣿⢋⢼⠞⠛⠁⠄⠄⠄⠄⡼⠋⠄
⢸⣿⠿⣛⣉⣄⠌⡿⣣⣿⢏⣜⡟⢀⣰⢆⡶⠛⠄⠄⠄⠄⠄⠄⠄⠄⡈⠄⠄⠄
⠄⠻⣰⣿⣿⢷⣚⣵⠿⢏⣼⡿⣡⣿⠋⢾⣿⣶⡹⣦⡀⠄⠄⠄⠄⣰⠇⠄⠄⠄
⠄⠄⣿⣿⣧⡿⣛⣽⣿⣿⣿⠿⠿⣥⡞⣸⣿⣿⣧⢹⣧⣤⣤⣤⣼⠏⠄⠄⠄⠄
⠄⢼⣿⣿⣿⣿⣯⣶⣿⣿⣿⣿⠿⣛⣽⣿⣿⣿⣿⣷⣼⣿⣿⣭⣵⠄⠄⠄⠄⠄
⠄⠄⠉⠻⠿⠿⠿⠉⠉⠉⠁⠄⠛⠛⠛⠻⠿⠿⠿⠿⠿⠏⠿⠿⠃⠄⠄⠄⠄⠄'''

