import pygame
import random
import imutils
# Inicialização do Pygame
pygame.init()

# Configurações da janela do jogo
largura, altura = 480, 360
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Alone Pong")

# Cores
preto = (0, 0, 0)
verde = (0, 255 , 0)

# Bola
bola_tamanho = 20
bola_x = largura // 2 - bola_tamanho // 2
bola_y = altura // 2 - bola_tamanho // 2
bola_velocidade_x = random.choice([-0.1, -0.3]) * 25
bola_velocidade_y = random.choice([-0.1, -0.3]) * 25

# Barra do jogador
barra_largura = 100
barra_altura = 10
barra_x = largura // 2 - barra_largura // 2
barra_y = altura - 30
barra_velocidade = 1

# Loop do jogo
import cv2  
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
vid = cv2.VideoCapture(0)

#Marca de inicio
mean_brightness=0
running = True
disponible=0
cX= 240
counter=0
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
#START OF CHANGES
    # Controle da barra do jogador
    ret, frame = vid.read()
    scale=480
    frame = imutils.resize(frame, width=scale)
    #one frame every 5 to make the game look less nevrotic
    if(counter%5==0):
        if ret:
            if disponible > 0:
                dif = cv2.absdiff(frame, pframe)     
                # Muestra resultado
                dif = cv2.cvtColor(dif, cv2.COLOR_BGR2GRAY)
                mean_brightness = cv2.mean(dif)[0]
                valorUmbral = 100 
                #Obtiene imagen umbralizada para dicho valor definido
                _, dif = cv2.threshold(dif, valorUmbral, 255, cv2.THRESH_BINARY)
                kernel_size = 21

                # Convert binary image from [0, 255] to [0, 1]
                binary_norm = dif // 255

                density_map = cv2.boxFilter(binary_norm, ddepth=-1, ksize=(kernel_size, kernel_size), normalize=False)

                # max_loc is the max density pixel
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(density_map)
                cX,cY=max_loc
                cX=cX+(scale//2-cX)*2

            else:
                disponible=1
                #Copia fotograma actual para la diferencia en el siguiente forograma
            pframe = frame.copy()
    counter+=1
    counter=counter%1000
    # Detenemos pulsado ESC
    if cv2.waitKey(20) == 27:
        break
    if barra_x>cX*(largura//scale) and barra_x > 0:
        barra_x -= barra_velocidade*mean_brightness*0.5
    if barra_x<cX*(largura//scale) and barra_x < largura - barra_largura:
        barra_x += barra_velocidade*mean_brightness*0.5
#END OF CHANGES
    # Movimento da bola
    bola_x += bola_velocidade_x
    bola_y += bola_velocidade_y

    # Colisão com as paredes e a barra
    if bola_x <= 0 or bola_x >= largura - bola_tamanho:
        bola_velocidade_x = -bola_velocidade_x

    if bola_y <= 0:
        bola_velocidade_y = -bola_velocidade_y

    if (
        barra_y <= bola_y + bola_tamanho <= barra_y + barra_altura
        and barra_x <= bola_x <= barra_x + barra_largura
    ):
        bola_velocidade_y = -bola_velocidade_y

    # Verifica se a bola caiu
    if bola_y >= altura:
        bola_x = largura // 2 - bola_tamanho // 2
        bola_y = altura // 2 - bola_tamanho // 2
        bola_velocidade_x = random.choice([-0.1, -0.3]) * 25
        bola_velocidade_y = random.choice([-0.1, -0.3]) * 25

    # Limpa a tela
    janela.fill(preto)

    # Desenha a bola
    pygame.draw.ellipse(janela, verde, (bola_x, bola_y, bola_tamanho, bola_tamanho))

    # Desenha a barra do jogador
    pygame.draw.rect(janela, verde, (barra_x, barra_y, barra_largura, barra_altura))

    pygame.display.update()

# Libera el objeto de captura
vid.release()
# Destruye ventanas
cv2.destroyAllWindows()
# Encerramento do Pygame
pygame.quit()