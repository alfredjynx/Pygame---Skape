from random import randint, seed
from classes import *
import pygame
import math


def inicializa():
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode((640, 640), vsync=True, flags=pygame.SCALED)
    pygame.key.set_repeat(50)

#----Inicializa as telas
    morte = Morte()
    inicio = Inicio()
    regras = Regras()
#---- Guarda todos os assets(Músicas, Imagens, Fontes, Telas) em um dicionario. 
    assets = {
        'fonte_28': pygame.font.Font('Fontes/ARCADE.TTF', 28),
        'fonte_50': pygame.font.Font('Fontes/ARCADE.TTF', 50),
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
        'pontos_long': pygame.image.load('Imagens/pontos_long.png'),
        'policial': pygame.image.load('Imagens/policial.png'),
        'inicio': inicio,
        'morte':morte,
        'regras':regras,

#---- Guarda valores que mudam conforme o andar do jogo, dicionário com chaves
#       e valores como: mouse_pressed, tela atual, se o jogo está rodando, etc.
    }
    state = {
        'nome_musica_tocando': '',
        'relogio_musica': pygame.time.Clock(),
        'tempo_inicio':0,
        'tempo_full_run':0,
        'pontos':0,
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
        'pulou': True,
        'jump_timer': 1000,
        'ponto_comecou_morro': 0,
        'total_updated': 0,
        'morro_last_updated': 641,
        'morreu': False,
        'tela': inicio,
        'jogo_run' : False,
        'restart': True,
        'quitou': False, 
    }
    #---- Seed: Feito para criar aparencia da terra do morro ser uniforme.
    #          Como a terra vai ser gerada usando vários rects de cores
    #          marrrons diferentes, se não criasse um seed para a terra,
    #          a terra constantemente mudaria de cor, desorientando o jogador.
    seed = randint(0,1000)
    state['morro_seed'] = seed
    #---- Adiciona sprites para um grupo, que vai ser utilizado na animação
    cria_sprites(assets, state)
    #---- Cria morros que serão percorridos pelo jogador
    cria_morros(state)
    return window, assets, state

def cria_morros(state):
    #---- Cria morros baseados em funções seno. O construtor de cada ponto recebe 5 variaveis,
    #     que definem onde os morros são desenhados e colidem com o personagem. O jeito que a classe
    #     de morros foi para ampliar a extensibilidade dessa função, possivelmente implementando
    #     uma versão onde os morros vão mudando de tamanho (essa versão foi testada, mas como a
    #     física demoraria muito mais tempo para aperfeicoar, incluimos ela como um easter egg e não a versão principal)
    for x in range (50000):
        ponto = Morros(x, 2, 50, -70, 0)
        state['linha_morro'].append(ponto)

# verifica se o jogo foi ou não fechado
def jogo_rodando():
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            state['quitou'] = True
            return False
    return True

# apenas para a formações das telas de menu, regras e morte
def desenha_tela(window: pygame.Surface, state):
    window.fill((0, 0, 0))
    state['tela'].desenha(window,state)

# apenas serve para trocar entre as telas de menu, regras e morte
def atualiza_tela(assets, state):
    # verifica onde que o mouse está localizado para desenhar os quadrados apropriados em volta dos botões
    x,y = pygame.mouse.get_pos()
    resultado = state['tela'].clique(x,y)
    if resultado:
        state['tela'].mouse_pos = True
    else:
        state['tela'].mouse_pos = False

    # checa inputs do mouse
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            state['quitou'] = True
            return False
        elif ev.type == pygame.MOUSEBUTTONUP:

            # quando um botão do mouse é solto, o programa começa a checar onde que ele está 
            x,y = ev.pos
            
            # se a tela não for o jogo principal
            if state['tela'] != 'jogo': 

                # resultado sempre é o resultado do clique, um método dentro de todos as classes (telas)
                resultado = state['tela'].clique(x,y)
                if resultado:
                    if state['tela'].nome == 'inicio':

                        # o início é a única tela com mais de um botões, portanto o resultado não pode ser apenas booleano
                            
                        # botão de jogar
                        if state['tela'].colide == 1:
                            state['tempo_inicio'] = pygame.time.get_ticks() - state['tempo_full_run']
                            state['jogo_run'] = True
                            return False
                        
                        # botão de regras
                        elif state['tela'].colide == 2:
                            state['tela'] = assets['regras']
                    
                    # se for qualquer um dos outros botões que foi pressionados, voltar ao menu
                    elif state['tela'].nome == 'regras' or state['tela'].nome == 'morte':
                        return

    return True

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
    ## A função draw_policia_box retorna um boolean que avisa se a posição do policial atingiu a posição do jogador.
    state['morreu'] = draw_policia_box(window, get_policia_pos((pygame.time.get_ticks()-state['tempo_inicio']-state['tempo_full_run'])/1000) - 1000, round(state['skate_pos'][0]), assets, state)
    if state['morreu']:
    #---- Perceba que quase sempre estou subtraindo o tempo que o jogador gastou no menu de
    #     inicio e na jogada anterior quando utilizo get_ticks()
        state['pontos'] = pygame.time.get_ticks() - state['tempo_inicio']-state['tempo_full_run']
        return  # Se o usuário morrer, pula o resto da função
    marcador_linha = 0
    seed(state['morro_seed'])
    ## Gera paredes com street art ao longo do y==345
    for i in range (0, int(state['skate_pos'][0]//(3298-640) + 1)):
        if i == 0: window.blit(assets['graff_wall'], (-state['skate_pos'][0],345))
        if i > 0: 
            window.blit(assets['graff_wall'], (-state['skate_pos'][0]+3298*(i)-60,345))
    # Desenha os morros criados no inicio. Os morros que estão fora da tela entram na tela baseado
    # na distância percorrida e velocidade atual.
    for morro in range(state['total_updated'], state['morro_last_updated']):
        state['total_updated'] = state['morro_last_updated'] - 641
        pygame.draw.circle(window, (188,188,188), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y), state['linha_morro'][morro].linhaMorro.raio)
        pygame.draw.rect(window, (58,58,58), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y, 2, 81))
        if marcador_linha % 20 < 9:   # Cria brechas na linha amarela da rua 
            pygame.draw.circle(window, (state['linha_morro'][morro].linhaMorro.cor[0], state['linha_morro'][morro].linhaMorro.cor[1], state['linha_morro'][morro].linhaMorro.cor[2]), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y+40), state['linha_morro'][morro].linhaMorro.raio)
        pygame.draw.circle(window, (188,188,188), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y+80), state['linha_morro'][morro].linhaMorro.raio)
        pygame.draw.rect(window, (randint(110,120),randint(65,70), randint(1,4)), (state['linha_morro'][morro].linhaMorro.x-state['total_updated'], state['linha_morro'][morro].linhaMorro.y+81, 2, 480-state['linha_morro'][morro].linhaMorro.y+81))
        state['morro_last_updated'] = 641 + round(state['skate_pos'][0])-50+180
        marcador_linha += 1
        animacao_skate(window, state)
    # Desenha os pontos live no canto da tela, ajusta o tamanho do quadrado se passar de 100000
    draw_pontos(window, assets, state)
    pygame.display.update()

def animacao_skate(window, state):
    #----- Desenha sprites do personagem
    for personagem in state['skate_sprites']:
        personagem.rect.center = [50, state['skate_pos'][1]]
        maxSeno = Funcao_e_derivado.get_crest(2,-70)
        if not state['pulou']:
            #----- Se estiver perto do pico da curva, comeca a animação do pulo
            if abs((state['total_updated'] - maxSeno)) % 180 > 70 and abs((state['total_updated'] - maxSeno)) % 180 < 100 and personagem.name == 'pula1':
                personagem.render(window)
                return
            time = pygame.time.get_ticks() - state['tempo_full_run']
            #----- 1/3 do tempo desenha animações diferentes
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
            #----- Desenha animação do pulo baseado no vetor de direção do personagem
            state['skate_vetor'] = calcula_vetor(state)
            if state['skate_vetor'] < 0 and personagem.name == 'pula2':
                personagem.render(window)
                return
            if state['skate_vetor'] >= 0 and personagem.name == 'pula3':
                personagem.render(window)
                return
        
def calcula_vetor(state):
    #----- Calcula vetor de direção do usuário
    try: return (state['skate_pos'][0]-state['skate_prev_pos'][0])/(state['skate_pos'][1]-state['skate_prev_pos'][1])
    except: return 0

def adapta_gravidade_velocidade_colisao_morro(state):
    #----- Detecta uma collisão entre o personagem e a linha
    if colisao_ponto_circulo(0, Funcao_e_derivado.get_function(state['skate_pos'][0], 2, 50, -70, 0), 0, state['skate_pos'][1], 10):
        #----- Calcula o derivado do local de colisão na curva.
        derivado = Funcao_e_derivado.get_derivado(state['skate_pos'][0],2,50,-70)
        #----- Calcula o x do pico inicial da curva
        maxSeno = Funcao_e_derivado.get_crest(2,-70)
        #----- Calcula o x do vale inicial da curva
        minSeno = Funcao_e_derivado.get_trough(2,-70)
        #----- Muda a velocidade y de acordo com o valor do derivado
        state['skate_vel'] = [state['skate_vel'][0], derivado]
        #----- Se o usuário estiver pulando e o timer do pulo ainda não começou, começa o timer
        if state['pulou'] == True and state['jump_timer'] == 0:
            state['jump_timer'] = pygame.time.get_ticks()
        #----- Se o timer atingir 500, vai cancelar o 'pulo, preparando o personagem para outro pulo'
        if (pygame.time.get_ticks() - state['jump_timer']) > 500 and state['jump_timer'] != 0 and state['pulou']:  
            state['pulou'] = False
        #----- Se o derivado do local da colisão for positivo, ou o usuário ja ter caido na descida
        #      da curva, e o usuário não estiver pulando ou subindo a curva, o if abaixo acelera o
        #      usuário, e acelera-o rápidamente se o usuário estiver clicando o botão de gravidade.
        if (derivado > 0 or state['fez_contato_descida']) and not state['fez_contato_subida'] and not state['pulou']:
            state['fez_contato_descida'] = True
            if state['skate_vel'][0] < 100:
                state['skate_vel'][0] *= 1.1
                if derivado > 0 and state['grav_forte']:
                    state['skate_vel'][0]*=2
            ## Se o usuário se aproximar do pico, a velocidade y acelera, criando um efeito de pulo.
            if abs((state['skate_pos'][0] - maxSeno)) % 180 > 160:
                if pygame.time.get_ticks() - state['jump_timer'] > 1000:
                    state['jump_timer'] = 0
                    state['skate_vel'][1] = -2*state['skate_vel'][0]*math.sin(math.cos(derivado/100))
                    state['pulou'] = True
                    state['fez_contato_descida'] = False
        #----- Se o derivado for negativo, e o usuário não fez contato inicial com a descida e não está pulando, dá um debuff de velocidade para o personagem.
        if (derivado < 0 or state['fez_contato_subida']) and not state['fez_contato_descida'] and not state['pulou']:
            if abs((state['skate_pos'][0] - minSeno)+10) % 180 < 85:
                state['fez_contato_subida'] = True
                state['skate_vel'] = [20,20]
            ## Se o personagem se aproximar do pico, vai cancelar o debuff e possibilitar o pulo na proxima descida.
            if abs((state['skate_pos'][0] - maxSeno)) % 180 > 150:
                state['fez_contato_descida'] = False
                state['fez_contato_subida'] = False
                state['jump_timer'] = pygame.time.get_ticks()
        state['skate_pos'][1] = Funcao_e_derivado.get_function(state['skate_pos'][0], 2, 50, -70, 0) - 12

# a música é dependente da posição do policial em relação à posição do jogador, com uma música para cada valor da porcentagem possível
def roda_musica(porcentagem, assets, state):
    if pygame.time.get_ticks()-state['tempo_full_run']-state['tempo_inicio']<5000:
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
                if state['relogio_musica'].get_time() > 2000 or state['relogio_musica'].get_time() < 62:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['36_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '36_musica'                
        elif porcentagem <= 0.52:
            if state['nome_musica_tocando'] != '52_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000 or state['relogio_musica'].get_time() < 62:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['52_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '52_musica'        
        elif porcentagem <= 0.68:
            if state['nome_musica_tocando'] != '68_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000 or state['relogio_musica'].get_time() < 62:
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['68_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '68_musica'                
        elif porcentagem <= 0.84:
            if state['nome_musica_tocando'] != '84_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000 or state['relogio_musica'].get_time() < 62:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['84_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '84_musica'        
        elif porcentagem <= 1:
            if state['nome_musica_tocando'] != '100_musica':
                state['relogio_musica'].tick()
                if state['relogio_musica'].get_time() > 2000  or state['relogio_musica'].get_time() < 62:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(assets['100_musica'])
                    pygame.mixer.music.set_volume(0.9)
                    pygame.mixer.music.play()
                    state['nome_musica_tocando'] = '100_musica'         

# retorna a posição do policial atualizada
def get_policia_pos(s):
    return 6969*(1.01**s - 1)

# Desenha uma caixa que vai se enchendo pelo percurso do jogo, indicando quão perto o policial está de te atingir.
# Também roda a música, e desenha caverias representando o nível de perigo do jogador.
# Retorna true se o policial alcançar o jogador
def draw_policia_box(window, POPOpos, sk8Pos, assets, state):
    porcentagem = POPOpos/sk8Pos
    if porcentagem < 0: porcentagem = 0
    if porcentagem > 1: 
        porcentagem = 1
    roda_musica(porcentagem, assets, state)
    pygame.draw.rect(window, (30,30,30), (100, 30, 440, 50))
    pygame.draw.rect(window, (255,26,26), (120, 40, round(400*porcentagem), 30))
    pygame.draw.rect(window, (0,128,0), (120 + round(400*porcentagem), 40, round(400*(1-porcentagem)), 30))
    window.blit(assets['andou2'], (506, 37))
    window.blit(assets['policial'], (115 + round(400*porcentagem),38))
    if pygame.time.get_ticks()-state['tempo_inicio']-state['tempo_full_run'] < 3420:
        avisoText = assets['fonte_50'].render('Um policial te persegue!', True, (255,255,255))
        window.blit(avisoText, (50,300))
    elif pygame.time.get_ticks()-state['tempo_inicio']-state['tempo_full_run'] < 6969:
        avisoText2 = assets['fonte_50'].render("     Fuja, 'Skape!", True, (255,255,255))
        window.blit(avisoText2, (50,300))
    for x in range(1,int((porcentagem-0.2)//0.16)+2):
        if x<6:
            window.blit(assets['caveira'], (69+75*x, 100))
    return porcentagem == 1

# desenha a quantidade de pontos e o retângulo onde eles são guardados
def draw_pontos(window, assets, state):

    # caixa menor, apenas o necessário para uma pontuação menor do que 99999
    if pygame.time.get_ticks()-state['tempo_inicio']-state['tempo_full_run'] < 99999:
        window.blit(assets['pontos'],(500,560))
        pontosText = assets['fonte_28'].render(str(pygame.time.get_ticks()-state['tempo_inicio']-state['tempo_full_run']), True, (0,0,0))
        window.blit(pontosText, (517,574))

    # caixa maior, necessária para uma pontuação maior que o valor mencionado anteriormente
    else:
        window.blit(assets['pontos_long'],(508,560))
        pontosText = assets['fonte_28'].render(str(pygame.time.get_ticks()-state['tempo_inicio']-state['tempo_full_run']), True, (0,0,0))
        window.blit(pontosText, (517,574))
   
# checa se o círculo do jogador entrou em contato com algum ponto da curva, e retorna um valor booleano se houve ou não colisão
def colisao_ponto_circulo(ponto_x, ponto_y, circulo_x, circulo_y, circulo_raio):
    if math.sqrt((ponto_x-circulo_x)**2 + (ponto_y-circulo_y)**2) <= circulo_raio:
        return True
    return False


def atualiza_estado(assets, state):
    # ---- Atualliza a posição dependendo na velocidade
    state['skate_prev_pos'] = [state['skate_pos'][0], state['skate_pos'][1]]
    totalTicks = pygame.time.get_ticks()-state['tempo_inicio']- state['tempo_full_run']
    deltaT = (totalTicks - state['last_updated'])/1000
    state['skate_pos'][0] += (state['skate_vel'][0] * deltaT)
    state['skate_vel'][1] += state['gravidade'] * deltaT
    state['skate_pos'][1] += (state['skate_vel'][1] * deltaT)
    # ---- Atualliza a posição e velocidade se tiver colisão
    adapta_gravidade_velocidade_colisao_morro(state)
    if state['mouse_pressed'] and not state['grav_forte']:
        state['gravidade'] *= 5
        state['grav_forte'] = True
    if not state['mouse_pressed'] and state['grav_forte']:
        state['gravidade'] /= 5
        state['grav_forte'] = False

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT or state['morreu']:
            if not state['morreu']: state['quitou'] = True
            return False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                state['mouse_pressed'] = True
        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 1:
                state['mouse_pressed'] = False
    state['last_updated'] = totalTicks
    return True


# gameloop principal
def gameloop(window, assets, state):
    
    # sempre checa se o jogo foi finalizado antes de rodar as funções necessárias para rodar o jogo
    while state['restart']:
        
        # verifica se a tela atual é a tela de início (também funciona com a tela de regras)
        if state['tela'].nome == 'inicio' and not state['quitou']:
            while atualiza_tela(assets,state):
                desenha_tela(window,state)
                pygame.display.update()
        
        # verifica se o jogo está sendo rodado
        if state['jogo_run'] and not state['quitou']:
            while atualiza_estado(assets, state) and not state['morreu']:
                desenha(window, assets, state)
            if state['morreu']:
                    state['tela'] = assets['morte']
        
        # verifica se a tela é a de morte
        if state['tela'].nome == 'morte' and not state['quitou']:
            while atualiza_tela(assets,state):
                desenha_tela(window,state)
                pontosText = assets['fonte_50'].render(str(state['pontos']), True, (255,255,255))
                window.blit(pontosText, (300,469))
                pygame.display.update()

        # verifica se o jogador saiu do jogo no meio do while principal de state["restart"]
        if state['quitou']:
            break
            
        # se o jogador decidir jogar novamente, as variáveis e dicionários são resetados (pegando tudo menos a inicialização do pygame e criação da tela)
        if state['restart']:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            reset_gameloop(state, assets)
        state['tempo_full_run'] = pygame.time.get_ticks()


# reseta as funcionalidades do jogo enquanto você reinicia ele (apertar o botão de jogar novamente na tela de morte)
def reset_gameloop(state, assets):
    morte = Morte()
    inicio = Inicio()
    regras = Regras()
    assets['morte'] = morte
    assets['inicio'] = inicio
    assets['regras'] = regras
    state['nome_musica_tocando'] = ''
    state['relogio_musica'] = pygame.time.Clock()
    state['tempo_inicio'] = 0
    state['skate_pos'] = [10, 120]
    state['skate_prev_pos'] = [0,0]
    state['skate_vetor'] = 0
    state['skate_vel'] = [20, -10]
    state['multiplicador'] = 10
    state['last_updated'] = 0
    state['fez_contato_descida'] = False
    state['fez_contato_subida'] = False
    state['pulou'] = True
    state['jump_timer'] = 1000
    state['ponto_comecou_morro'] = 0
    state['total_updated'] = 0
    state['morro_last_updated'] = 641
    state['morreu'] = False
    state['tela'] = inicio
    state['jogo_run'] = False
    state['restart'] = True
    state['pontos'] = 0

# finaliza o jogo
def finaliza():
    pygame.quit()

# começa a rodar o programa
if __name__ == '__main__':
    window, assets, state = inicializa()
    gameloop(window, assets, state)
    finaliza()
    


# pepePog
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

