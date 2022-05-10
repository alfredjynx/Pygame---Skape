from random import randint, seed
from classes import *
import pygame
import math


def inicializa():
    pygame.init()
    window = pygame.display.set_mode((640, 640), vsync=True, flags=pygame.SCALED)
    pygame.key.set_repeat(50)

    assets = {
        'fonte_20': pygame.font.Font('Fontes/ARCADE.TTF', 28),
        '20_musica': 'Musica/So_Far_To_Go.mp3',
        '36_musica': 'Musica/Mushroom_Hunting.mp3',
        '52_musica': 'Musica/Roborgasm.mp3',
        '68_musica': 'Musica/Lunchtime.mp3',
        '84_musica': 'Musica/KoroneBGM.mp3',
        '100_musica': 'Musica/Midwest_Choppers.mp3',
        'background': pygame.image.load('Imagens/background.jpg'),
        'graff_wall': pygame.image.load('Imagens/graffWall.png'),
        'andou1': pygame.image.load('Imagens/rolling-1.png'),
        'andou2': pygame.image.load('Imagens/rolling-2.png'),
        'andou3': pygame.image.load('Imagens/rolling-2.png'),
        'pulou1': pygame.image.load('Imagens/jump-start.png'),
        'pulou2': pygame.image.load('Imagens/jump-middle.png'),
        'pulou3': pygame.image.load('Imagens/jump-end.png'),
        'caveira': pygame.image.load('Imagens/skull.png'),
        'pontos': pygame.image.load('Imagens/pontos.png'),
        'pontos_long': pygame.image.load('Imagens/pontos_long.png')
    }

    state = {
        'nome_musica_tocando': '',
        'relogio_musica': pygame.time.Clock(),
        'mouse_pressed' : False,
        'grav_forte': False,
        'gravidade' : 98,
        'skate_pos': [10, 120],
        'skate_prev_pos': [0,0],
        'skate_vetor': 0,
        'skate_vel': [20, -10],
        'multiplicador' : 10,
        'last_updated': 0,
        'linha_morro': [],
        'fez_contato_descida': False,
        'fez_contato_subida': False,
        'debuff_jump': False,
        'pulou': True,
        'jump_timer': 1000,
        'ponto_comecou_morro': 0,
        'total_updated': 0,
        'morro_last_updated': 641
    }
    cria_sprites(assets, state)
    cria_morros(state)
    return window, assets, state

def cria_morros(state):
    for x in range (50000):
        morro = Morros(x,1.4, 40, 0, 0)
        state['linha_morro'].append(morro)

def cria_sprites(assets, state):
    skate_group = pygame.sprite.Group()
    skate_group.add(SkatistaSprite(assets['pulou1'], 'pula1', state['skate_pos'][1]))
    skate_group.add(SkatistaSprite(assets['pulou2'], 'pula2', state['skate_pos'][1]))
    skate_group.add(SkatistaSprite(assets['pulou3'], 'pula3', state['skate_pos'][1]))
    skate_group.add(SkatistaSprite(assets['andou1'], 'anda1', state['skate_pos'][1]))
    skate_group.add(SkatistaSprite(assets['andou2'], 'anda2', state['skate_pos'][1]))
    skate_group.add(SkatistaSprite(assets['andou3'], 'anda3', state['skate_pos'][1]))
    state['skate_sprites'] = skate_group

def desenha(window: pygame.Surface, assets, state):
    window.blit(assets['background'], (0,0))
    draw_policia_box(window, get_policia_pos(pygame.time.get_ticks()/1000) - 400, round(state['skate_pos'][0]), assets, state)
    marcador_linha = 0
    seed()
    for i in range (0, int(state['skate_pos'][0]//(3298-640) + 1)):
        if i == 0: window.blit(assets['graff_wall'], (-state['skate_pos'][0],345))
        if i > 0: 
            window.blit(assets['graff_wall'], (-state['skate_pos'][0]+3298*(i)-60,345))
    for morro in range(state['total_updated'], state['morro_last_updated']):
        if marcador_linha % 80 == 0: cor = (randint(0,80),randint(160,185), randint(252,255))
        state['total_updated'] = state['morro_last_updated'] - 641
        pygame.draw.circle(window, (188,188,188), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y), state['linha_morro'][morro].linhaMorro.raio)
        pygame.draw.rect(window, (58,58,58), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y, 2, 81))
        if marcador_linha % 20 < 9 :
            pygame.draw.circle(window, (state['linha_morro'][morro].linhaMorro.cor[0], state['linha_morro'][morro].linhaMorro.cor[1], state['linha_morro'][morro].linhaMorro.cor[2]), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y+40), state['linha_morro'][morro].linhaMorro.raio)
        pygame.draw.circle(window, (188,188,188), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y+80), state['linha_morro'][morro].linhaMorro.raio)
        pygame.draw.rect(window, (randint(110,120),randint(65,70), randint(1,4)), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y+81, 2, 480-state['linha_morro'][morro].linhaMorro.y+81))
        state['morro_last_updated'] = 641 + round(state['skate_pos'][0])-50
        marcador_linha += 1
        animacao_skate(window, state)
    draw_pontos(window, assets)
    pygame.display.update()

def animacao_skate(window, state):
    a = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.a
    c = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.c
    for personagem in state['skate_sprites']:
        personagem.rect.center = [50, state['skate_pos'][1]]
        maxSeno = Funcao_e_derivado.get_crest(a,c)
        if not state['pulou']:
            if abs((state['total_updated'] - maxSeno)) % (360/1.4/2) > 70 and abs((state['total_updated'] - maxSeno)) % (360/1.4/2) < 100 and personagem.name == 'pula1':
                personagem.render(window)
                return
            time = pygame.time.get_ticks()
            if time % 1000 < 333 and personagem.name == 'anda1':
                personagem.render(window)
                return
            elif time > 333 and time < 666 and personagem.name == 'anda2':
                personagem.render(window)
                return
            elif personagem.name == 'anda3':
                personagem.render(window)
                return
        else:
            state['skate_vetor'] = calcula_vetor(state)
            if state['skate_vetor'] < 0 and personagem.name == 'pula2':
                personagem.render(window)
                return
            if state['skate_vetor'] >= 0 and personagem.name == 'pula3':
                personagem.render(window)
                return
        
def calcula_vetor(state):
    try: return (state['skate_pos'][0]-state['skate_prev_pos'][0])/(state['skate_pos'][1]-state['skate_prev_pos'][1])
    except: return 0

def adapta_gravidade_velocidade_colisao_morro(state):
    a = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.a
    b = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.b
    c = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.c
    d = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.d
    if colisao_ponto_circulo(0, Funcao_e_derivado.get_function(state['skate_pos'][0], a, b, c, d), 0, state['skate_pos'][1], 10):
        derivado = Funcao_e_derivado.get_derivado(state['skate_pos'][0],a,b,c)
        maxSeno = Funcao_e_derivado.get_crest(a,c)
        minSeno = Funcao_e_derivado.get_trough(a,c)
        state['skate_vel'] = [state['skate_vel'][0], derivado]
        if state['pulou'] == True and state['jump_timer'] == 0:
            state['jump_timer'] = pygame.time.get_ticks()
        if pygame.time.get_ticks() - state['jump_timer'] > 300: 
            state['pulou'] = False
            state['jump_timer'] = 0
        if (derivado > 0 or state['fez_contato_descida']) and not state['fez_contato_subida'] and not state['pulou']:
            state['fez_contato_descida'] = True
            if state['skate_vel'][0] < 100:
                state['skate_vel'][0] *= 1.1
                if derivado > 0 and state['grav_forte']:
                    state['skate_vel'][0]*=2
            if abs((state['skate_pos'][0] - maxSeno)) % (360/1.4/2) > 160:
                if pygame.time.get_ticks() - state['jump_timer'] > 1000:
                    state['jump_timer'] = 0
                    state['skate_vel'][1] = -2*state['skate_vel'][0]*math.sin(math.cos(derivado/100))
                    state['pulou'] = True
                    print('vx: {0}, vy: {1}'.format(state['skate_vel'][0],state['skate_vel'][1]))
                    state['fez_contato_descida'] = False

        if (derivado < 0 or state['fez_contato_subida']) and not state['fez_contato_descida'] and not state['pulou']:
            if abs((state['skate_pos'][0] - minSeno)+10) % (360/1.4/2) < 85:
                state['fez_contato_subida'] = True
                state['skate_vel'] = [20,20]
            if abs((state['skate_pos'][0] - maxSeno)) % (360/1.4/2) > 160:
                state['fez_contato_descida'] = False
                state['fez_contato_subida'] = False
                state['debuff_jump'] = True
                state['jump_timer'] = pygame.time.get_ticks()
        a = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.a
        b = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.b
        c = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.c
        d = state['linha_morro'][int(round(state['skate_pos'][0]))].linhaMorro.d
        state['skate_pos'][1] = Funcao_e_derivado.get_function(state['skate_pos'][0],a,b,c,d) - 12

def roda_musica(porcentagem, assets, state):
    if pygame.time.get_ticks()<5000:
        if state['nome_musica_tocando'] != '20_musica':
            state['relogio_musica'].tick()
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(assets['20_musica'])
            pygame.mixer.music.set_volume(0.9)
            pygame.mixer.music.play()
            state['nome_musica_tocando'] = '20_musica'
    else:
        if porcentagem <= 0.20:
            if state['nome_musica_tocando'] != '20_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['20_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '20_musica'
                    
        elif porcentagem <= 0.36:
            if state['nome_musica_tocando'] != '36_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['36_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '36_musica'
                    
        elif porcentagem <= 0.52:
            if state['nome_musica_tocando'] != '52_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['52_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '52_musica'
                    
        elif porcentagem <= 0.68:
            if state['nome_musica_tocando'] != '68_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000:
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['68_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '68_musica'
                    
        elif porcentagem <= 0.84:
            if state['nome_musica_tocando'] != '84_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['84_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '84_musica'
                    
        elif porcentagem <= 1:
            if state['nome_musica_tocando'] != '100_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['100_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '100_musica'
                    

def get_policia_pos(s):
    return 5420*(1.01**s - 1)

def draw_policia_box(window, POPOpos, sk8Pos, assets, state):
    porcentagem = POPOpos/sk8Pos
    if porcentagem < 0: porcentagem = 0
    if porcentagem > 1: porcentagem = 1
    roda_musica(porcentagem, assets, state)
    pygame.draw.rect(window, (30,30,30), (100, 30, 440, 50))
    pygame.draw.rect(window, (255,26,26), (120, 40, round(400*porcentagem), 30))
    pygame.draw.rect(window, (0,128,0), (120 + round(400*porcentagem), 40, round(400*(1-porcentagem)), 30))
    for x in range(1,int((porcentagem-0.2)//0.16)+3):
        if x<6:
            window.blit(assets['caveira'], (69+75*x, 100))

def draw_pontos(window, assets):
    if pygame.time.get_ticks() < 99999:
        window.blit(assets['pontos'],(500,560))
        pontosText = assets['fonte_20'].render(str(pygame.time.get_ticks()), True, (0,0,0))
        window.blit(pontosText, (517,574))
    else:
        window.blit(assets['pontos_long'],(508,560))
        pontosText = assets['fonte_20'].render(str(pygame.time.get_ticks()), True, (0,0,0))
        window.blit(pontosText, (517,574))

def colisao_ponto_circulo(ponto_x, ponto_y, circulo_x, circulo_y, circulo_raio):
    if math.sqrt((ponto_x-circulo_x)**2 + (ponto_y-circulo_y)**2) <= circulo_raio:
        return True
    return False

# def colisao_ponto_retangulo(ponto_x, ponto_y, rect_x, rect_y, rect_w, rect_h):
#     if (ponto_x > rect_x and ponto_x < rect_x + rect_w) and (ponto_y > rect_y and ponto_y < rect_y + rect_h):
#         return True
#     return False

def atualiza_estado(assets, state):
    state['skate_prev_pos'] = [state['skate_pos'][0], state['skate_pos'][1]]
    totalTicks = pygame.time.get_ticks()
    deltaT = (totalTicks - state['last_updated'])/1000
    state['skate_pos'][0] += (state['skate_vel'][0] * deltaT)
    state['skate_vel'][1] += state['gravidade'] * deltaT
    state['skate_pos'][1] += (state['skate_vel'][1] * deltaT)
    adapta_gravidade_velocidade_colisao_morro(state)

    if state['mouse_pressed'] and not state['grav_forte']:
        state['gravidade'] *= 5
        state['grav_forte'] = True
        print('ativado')
    if not state['mouse_pressed'] and state['grav_forte']:
        state['gravidade'] /= 5
        state['grav_forte'] = False
        print('deativado')

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                state['mouse_pressed'] = True
        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                state['mouse_pressed'] = False
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

