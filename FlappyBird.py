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
	ROTACAO_MAXIMA = 25
	VELOCIDADE_ROTACAO = 20
	TEMPO_ANIMACAO = 5

	# atributos pássaro
	def __init__(self, eixoX, eixoY):
		self.eixoX = eixoX
		self.eixoY = eixoY
		self.angulo = 0
		self.velocidade = 0
		self.altura = self.eixoY
		self.tempo = 0
		self.contador_da_imagem = 0
		self.imagem_do_passaro = self.IMAGENS[0]

	def pular(self):
		# INFO fórmula física do deslocamento => S = so + vot + at²/2 (sorvetão rs)
		self.velocidade = -10.5
		self.tempo = 0
		self.altura = self.eixoY

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
		self.eixoX += deslocamento

		# INFO ângulo do pássaro
		if deslocamento < 0 or self.eixoY < (self.altura + 50):
			if self.angulo < self.ROTACAO_MAXIMA:
				self.angulo = self.ROTACAO_MAXIMA
		else:
			if self.angulo > -90:
				self.angulo -= self.VELOCIDADE_ROTACAO

	def desenhar_passaro(self, tela):
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
		posicao_centro_imagem = self.imagem.get_rect(topleft=(self.eixoX, self.eixoY)).center
		retangulo = imagem_rotacionada.get_rect(center=posicao_centro_imagem)
		tela.blit(imagem_rotacionada, retangulo.topleft)
	
	# colisão do objeto
	def pega_mascara(self): # get_mask do passaro
		pygame.mask.from_surface(self.imagem)

class Cano:
	DISTANCIA_PASSAGEM_PASSARO_ENTRE_O_CANO_TOPO_E_CANO_BASE = 200 # PIXELS
	VELOCIDADE = 5 # dupla de canos: de quanto em quanto aparecerá na tela

	def __init__(self, eixoX):
		self.eixoX = eixoX
		self.altura = 0
		self.posicao_topo = 0
		self.posicao_base = 0
		self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True) # (eixo_x = rotate na horizontal, eixo_y = rotate na vertical)
		self.CANO_BASE = IMAGEM_CANO
		self.passaro_passou_do_cano = False # passaro já conseguiu passar pelo cano
		#essa função serve para, quando criarmos o cano, ele chame a função que irá gerar a altura do cano
		self.definir_altura()

	def definir_altura(self):
		self.altura = random.randrange(50, 450) # Como definimos a tela em 800px de height, definimos um espaço menor para a criação dos canos, garantindo assim que não haja uma discrepancia entre o cano do topo e o cano base
		self.posicao_topo = self.altura - self.CANO_TOPO.get_height()
		self.posicao_base = self.altura - self.DISTANCIA_PASSAGEM_PASSARO_ENTRE_O_CANO_TOPO_E_CANO_BASE
	
	def mover_cano(self): # TODO ALGO ERRADO AQUI?
		self.eixoX -= self.VELOCIDADE

	def desenhar_cano(self, tela):
		tela.blit(self.CANO_TOPO, (self.eixoX, self.posicao_topo)) # 2º parâmetro do blit é uma tupla
		tela.blit(self.CANO_BASE, (self.eixoX, self.posicao_base))

	def colidir_passaro_cano(self, passaro):
		passaro_mask = passaro.get_mask()
		cano_topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
		cano_base_mask = pygame.mask.from_surface(self.CANO_BASE)

		# Calcular a distancia do passaro - topo e passaro - base
		distancia_passaro_topo = (self.eixoX - passaro.eixoX, self.posicao_topo - round(passaro.eixoY)) # calculo é uma tupla / o round precisa ser adicionado pois o valor precisa ser um valor inteiro e como a posição do pássaro é muito quebrada, precisamos arredondar. Inclusive é ibnteressante arredondar o valor da self.posicao_topo também
		distancia_passaro_base = (self.eixoX - passaro.eixoX, self.posicao_base - round(passaro.eixoY))

		ponto_colisao_topo = passaro_mask.overlap(cano_topo_mask, distancia_passaro_topo) # overlap() verifica se há dois elementos dentro do mesmo pixel
		ponto_colisao_base = passaro_mask.overlap(cano_base_mask, distancia_passaro_base) # ponto_colisao_topo e base são valores booleans

		if ponto_colisao_topo or ponto_colisao_base:
			return True
		else:
			return False


class Chao:
	VELOCIDADE_CHAO = 5 # Mesma velocidade cano
	LARGURA_CHAO = IMAGEM_CHAO.get_width()
	IMAGEM = IMAGEM_CHAO

	def __init__(self, eixoY) -> None:
		self.eixoY = eixoY
		self.eixoX_imagem_chao_1 = 0 # imagem chão 1
		# self.x1 = self.eixoY + self.LARGURA_CHAO # imagem chão 2
		self.eixoX_imagem_chao_2 = self.LARGURA_CHAO # imagem chão 2 / como self.x0 começa com zero e nós sempre vamos movimentar as duas imagens ao mesmo tempo, não é necessário somar x0 com LARGURA

	def mover_chao(self):
		self.self.eixoX_imagem_chao_1 -= self.VELOCIDADE_CHAO
		self.self.eixoX_imagem_chao_2 -= self.VELOCIDADE_CHAO

		if self.eixoX_imagem_chao_1 + self.LARGURA_CHAO < 0:
			self.eixoX_imagem_chao_1 += self.LARGURA_CHAO # self.eixoX_imagem_chao_1 = self.eixoX_imagem_chao_1 + self.LARGURA_CHAO
		if self.eixoX_imagem_chao_2 + self.LARGURA_CHAO < 0:
			self.eixoX_imagem_chao_2 += self.LARGURA_CHAO

	def desenhar_chao(self, tela):
		tela.blit(self.IMAGEM, (self.eixoX_imagem_chao_1, self.eixoY))
		tela.blit(self.IMAGEM, (self.eixoX_imagem_chao_2, self.eixoY))

def desenhar_tela_completa(): # (chao, cano, passaro) WIP 
    pass