import pygame

SPRITESHEET = [pygame.image.load("rolling-1.png"),pygame.image.load("rolling-2.png"),pygame.image.load("rolling-3.png"),pygame.image.load("jump-1.png"),pygame.image.load("jump-2.png"),pygame.image.load("jump-3.png")]

titulo = "Só os skate sabem"
width = 480
height = 640
fps = 60

black = (0,0,0)

still = 0
jumping_1 = 1
jumping_2 = 2
smile = 3
morte = 4



class Jogador(pygame.sprite.Sprite):
    def __init__(self,player_sheet):
        pygame.sprite.Sprite.__init__(self)

        self.animations = {
            still: SPRITESHEET[0:2],
            jumping_1: SPRITESHEET[2:6],
        }

        self.state = still
        self.animation = self.animations[self.state]
        self.frame = 0
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()

        self.rect.centerx = width/2
        self.rect.centery = height/2

        self.last_update = pygame.time.get_ticks()

        self.frame_ticks = 300
    
    def update(self):
        agora = pygame.time.get_ticks()

        ticks = self.last_update
        print(ticks)

        elapsed_ticks = agora - ticks

        if elapsed_ticks>self.frame_ticks:
            self.last_update = agora
            self.frame += 1
            self.animation = self.animations[self.state]
            if self.frame >= len(self.animation):
                self.frame = 0
            
            center = self.rect.center

            self.image = self.animation[self.frame]

            self.rect = self.image.get_rect()
            self.rect.center = center
    

def telones(tela):
    tempo = pygame.time.Clock()

    player_sheet = SPRITESHEET
    # Cria Sprite do jogador
    player = Jogador(player_sheet)
    # Cria um grupo de todos os sprites e adiciona o jogador.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    PLAYING = 0
    DONE = 1

    state = PLAYING
    while state != DONE:
        
        # Ajusta a velocidade do jogo.
        tempo.tick(fps)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = DONE
            
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_1:
                    player.state = still
                elif event.key == pygame.K_2:
                    player.state = jumping_1

                
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite. O grupo chama o método update() de cada Sprite dentre dele.
        all_sprites.update()
        
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(black)
        all_sprites.draw(screen)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()


# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((width, height))

# Nome do jogo
pygame.display.set_caption(titulo)

# Imprime instruções
print('*' * len(titulo))
print(titulo.upper())
print('*' * len(titulo))
print('Utilize as teclas "1" e "2" do seu teclado para mudar a animação atual.')

# Comando para evitar travamentos.
try:
    telones(screen)
finally:
    pygame.quit()



