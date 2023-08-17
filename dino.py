import pygame  #  importa o módulo principal
from pygame.locals import *    # importa várias constantes e eventos do Pygame 
from sys import exit #importa a função sair, é usada para encerrar o programa 
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()
                                                 #diretorio de aqrquivos das imagens e dos sons do jogo 
diretorio_principal = os.path.dirname(__file__)  
diretorio_imagens = os.path.join(diretorio_principal, 'imagens') 
diretorio_sons = os.path.join(diretorio_principal, 'sons')

LARGURA = 640         #parametros da tela do jogo 
ALTURA = 460
    
BRANCO = (255,215,0)

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption('Dino Game')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha() 

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'death_sound.wav')) #som quando o personagem morre
som_colisao.set_volume(1)

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav')) #implementação do som da pontuação 
som_pontuacao.set_volume(1)

colidiu = False

escolha_obstaculo = choice([0, 1])

pontos = 0 

velocidade_jogo = 10
imagen_defundo=pygame.image.load("imagens/cenariofundo.png") #implementação do Cenario de fundo do Jogo

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}' 
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo(): # reinicialização do jogo 
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    dino.rect.y = ALTURA - 64 - 96//2
    dino.pulo = False
    dino_voador.rect.x = LARGURA
    cacto.rect.x = LARGURA
    escolha_obstaculo = choice([0, 1])

class Dino(pygame.sprite.Sprite): #implementação do personagem do Metal Slug spritesheet parte por parte 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'jump_sound.wav')) #implementação ddo som de pular
        self.som_pulo.set_volume(1)
        self.imagempersonagem = []
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo0.png'))
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo1.png'))    
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo2.png'))
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo3.png'))
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo4.png'))
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo5.png'))
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo6.png'))
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo7.png'))
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo8.png'))
        self.imagempersonagem.append(pygame.image.load('imagens/imagempersonagemcorrendo9.png'))
        self.index_lista = 0
        self.image = self.imagempersonagem[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = ALTURA - 40 - 96//2
        self.rect.topleft = (100, self.pos_y_inicial) #368   416(centro y)
        self.pulo = False
        self.image = pygame.transform.scale(self.image,(34*1.5,37*1.5)) #aumento do personagem que mutiplica o tamanho da imagem por 1,5
    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self): #atualiza a posição do objeto na tela para indicar que ele esta se movendo 

        if self.pulo == True:
            if self.rect.y <= self.pos_y_inicial - 110:
                self.pulo = False
            self.rect.y -= 15

        else:
            if self.rect.y >= self.pos_y_inicial:
                self.rect.y = self.pos_y_inicial
            else:
                self.rect.y += 15
        
 
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagempersonagem[int(self.index_lista)]
        self.image = pygame.transform.scale(self.image,(34*1.5,37*1.5))#aumento do personagem que mutiplica o tamanho da imagem por 1,5
class Nuvens(pygame.sprite.Sprite): #implementação das Nuvens e das cores das nuvens utilizando o piskel app
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = LARGURA - randrange(30, 300, 90)

    def update(self): #atualiza a posição do objeto na tela para indicar que ele esta se movendo 
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= velocidade_jogo

class Chao(pygame.sprite.Sprite): #implementação das Chao e das cores das nuvens utilizando o piskel app
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 64
        self.rect.x = pos_x * 64

    def update(self): #atualiza a posição do objeto na tela para indicar que ele esta se movendo 
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= 10
    
class Cacto(pygame.sprite.Sprite):   #implementação das Cacto e das cores das nuvens utilizando o piskelapp
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (LARGURA,  ALTURA - 64)
        self.rect.x = LARGURA

    def update(self): #atualiza a posição do objeto na tela para indicar que ele esta se movendo 
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i*32, 0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 300)
        self.rect.x = LARGURA
    
    def update(self):  #atualiza a posição do objeto na tela para indicar que ele esta se movendo 
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_dinossauro[int(self.index_lista)]

todas_as_sprites = pygame.sprite.Group() #adicionei todas as sprites ao Jogo
dino = Dino()
todas_as_sprites.add(dino)

for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

for i in range(LARGURA*2//64):
    chao = Chao(i)
    todas_as_sprites.add(chao)

cacto = Cacto() #sprite do Cacto 
todas_as_sprites.add(cacto)

dino_voador = DinoVoador() #sprite do DinoVoador
todas_as_sprites.add(dino_voador)

grupo_obstaculos = pygame.sprite.Group() #sprite dos obstaculos
grupo_obstaculos.add(cacto)
grupo_obstaculos.add(dino_voador)

relogio = pygame.time.Clock() # controla a quantidade de frames por segundo do jogo
while True:
    tela.blit(imagen_defundo,[0,0])
    relogio.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu == False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()

            if event.key == K_r and colidiu == True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)

    todas_as_sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1])
        cacto.rect.x = LARGURA
        dino_voador.rect.x = LARGURA
        cacto.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True

    if colidiu == True:
        if pontos % 100 == 0:
            pontos += 1
        game_over = exibe_mensagem('GAME OVER', 40, (255,255,255)) #exibe a mensagem em cor Branca 
        tela.blit(game_over, (LARGURA//2, ALTURA//2))
        restart = exibe_mensagem('Pressione R para reiniciar', 20, (255,255,255)) #exibe a mensagem em cor Branca
        tela.blit(restart, (LARGURA//2, (ALTURA//2) + 60))

    else:
        pontos += 1
        todas_as_sprites.update()
        texto_pontos = exibe_mensagem(pontos, 40, (0,0,0))

    if pontos % 100 == 0:
        som_pontuacao.play()
        if velocidade_jogo >= 23:
            velocidade_jogo += 0
        else:
            velocidade_jogo += 1
        
    tela.blit(texto_pontos, (520, 30))

    pygame.display.flip()