import pygame 	# INFO biblioteca de jogos em python
import os 		# INFO integrar o código que eu estou fazendo com os arquivos do meu computador
import random 	# INFO biblioteca de geração de números aleatórios em python

# constantes => configs do jogo
TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = 		pygame.image.load(os.path.join('imgs', 'pipe.png'))
IMAGEM_CHAO = 		pygame.image.load(os.path.join('imgs', 'base.png'))
IMAGEM_BACKGROUND = pygame.image.load(os.path.join('imgs', 'bg.png'))
IMAGEM_PASSARO = 	[
	pygame.image.load(os.path.join('imgs', 'bird1.png')),
	pygame.image.load(os.path.join('imgs', 'bird2.png')),
	pygame.image.load(os.path.join('imgs', 'bird3.png'))
]

pygame.font.init()
FONTE_PONTUACAO = pygame.font.SysFont('arial', 50)
# FIM constantes => configs do jogo

# OBJETOS => Aquilo que se mexe
class Passaro:
	IMAGENS = IMAGEM_PASSARO

	# animações
	ROTACAO_MAXIMA = 		25
	VELOCIDADE_ROTACAO = 	20
	TEMPO_ANIMACAO = 		5

	# atributos pássaro
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.angulo = 0
		self.velocidade = 0
		self.altura = self.y
		self.tempo = 0
		self.contador_da_imagem = 0
		self.imagem_do_passaro = self.IMAGENS[0]

	def pular(self):
		# INFO fórmula física do deslocamento => S = so + vot + at²/2 (sorvetão rs)
		self.velocidade = -10.5
		self.tempo = 0
		self.altura = self.y

	def mover(self):
		# INFO calcular o deslocamento
		self.tempo += 1
		deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

		# INFO restringir o deslocamento
		if deslocamento > 16:
			deslocamento = 16
		elif deslocamento < 0:
			deslocamento -= 2

		# movimentar o pássaro
		self.x += deslocamento

		# INFO ângulo do pássaro
		if deslocamento < 0 or self.y < (self.altura + 50):
			if self.angulo < self.ROTACAO_MAXIMA:
				self.angulo = self.ROTACAO_MAXIMA
		else:
			if self.angulo > -90:
				self.angulo -= self.VELOCIDADE_ROTACAO

	def desenhar(self, tela):
		# definir qual imagem do pássaro vamos usar
		self.contador_da_imagem += 1
		if self.contador_da_imagem < self.TEMPO_ANIMACAO:
			self.imagem_do_passaro = self.IMAGENS[0]
		elif self.contador_da_imagem < self.TEMPO_ANIMACAO * 2:
			self.imagem_do_passaro = self.IMAGENS[1]
		elif self.contador_da_imagem < self.TEMPO_ANIMACAO * 3:
			self.imagem_do_passaro = self.IMAGENS[2]
		elif self.contador_da_imagem < self.TEMPO_ANIMACAO * 4:
			self.imagem_do_passaro = self.IMAGENS[1]
		elif self.contador_da_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
			self.imagem_do_passaro = self.IMAGENS[0]
			self.imagem_do_passaro = 0

		# se o pássaro estiver caindo, ele não deve bater a asa
		if self.angulo <= -80:
			self.imagem = self.IMAGENS[1]
			self.contador_da_imagem = self.TEMPO_ANIMACAO * 2

		# desenhar a imagem
		imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
		posicao_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
		retangulo = imagem_rotacionada.get_rect(center=posicao_centro_imagem)
		tela.blit(imagem_rotacionada, retangulo.topleft)
	
	# colisão do objeto
	def pega_mascara(self): # get_mask do passaro
		pygame.mask.from_surface(self.imagem)

class Cano:
	DISTANCIA_PASSAGEM_PASSARO_ENTRE_O_CANO_TOPO_E_CANO_BASE = 200 # PIXELS
	VELOCIDADE = 5 # dupla de canos: de quanto em quanto aparecerá na tela

	def __init__(self, x):
		self.x = x
		self.altura = 0
		self.posicao_top = 0
		self.posicao_base = 0
		self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True) # (eixo_x = rotate na horizontal, eixo_y = rotate na vertical)
		self.CANO_BASE = IMAGEM_CANO
		self.passaro_passou_do_cano = False # passaro já conseguiu passar pelo cano
		#essa função serve para, quando criarmos o cano, ele chame a função que irá gerar a altura do cano
		self.definir_altura()

	def definir_altura(self):
		self.altura = random.randrange(50, 450) # Como definimos a tela em 800px de height, definimos um espaço menor para a criação dos canos, garantindo assim que não haja uma discrepancia entre o cano do topo e o cano base
		self.posicao_top = self.altura - self.CANO_TOPO.get_height()
		self.posicao_base = self.altura - self.DISTANCIA_PASSAGEM_PASSARO_ENTRE_O_CANO_TOPO_E_CANO_BASE
		# WIP 


class Chao:
	pass
