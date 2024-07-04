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

	def desenhar(self):
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

		# desenhar a imagem


class Cano:
	pass

class Chao:
	pass
