import math
import sys
import pygame
from pygame.display import update
from pygame.locals import QUIT


# Inicialização do Pygame e Configurações da Janela
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1280, 720))  # Tamanho da tela
pygame.display.set_caption('Pato Game')

# Inicialização do mixer de som do Pygame
pygame.mixer.init()

# Carregar som de clique
click_sound = pygame.mixer.Sound('quack.wav')  # Substitua 'click.wav' pelo caminho do seu arquivo de som


# Carregando Imagens
mapa = pygame.image.load("mapa.png").convert_alpha()  # Mapa de fundo
screen_width, screen_height = DISPLAYSURF.get_size()  # Tamanho da tela
mapa = pygame.transform.scale(mapa, (screen_width, screen_height))  # Redimensiona o mapa

DEFAULT_IMAGE_SIZE = (200,200)

#---------------------------
def format_number(num):
    if num >= 1_000_000_000:
        return f'{num / 1_000_000_000:.0f}Bi'
    elif num >= 1_000_000:
        return f'{num / 1_000_000:.0f}Mi'
    elif num >= 1_000:
        return f'{num / 1_000:.0f}K'
    else:
        return str(num)

# Imagens de pato
patoinicial = pygame.image.load('patoinicial.png').convert_alpha()
patosiames = pygame.image.load('patosiames.png').convert_alpha()
patodobrado = pygame.image.load('patodobrado.png').convert_alpha()
patomusculoso = pygame.image.load('patomusculoso.png').convert_alpha()
patorealista = pygame.image.load('patorealista.png').convert_alpha()
patoburgues = pygame.image.load('patoburgues.png').convert_alpha()
mousedesenho = pygame.image.load('mouse.png').convert_alpha()
mousedesenho = pygame.transform.scale(mousedesenho, DEFAULT_IMAGE_SIZE)

nivelbloqimagem = pygame.image.load('nivelbloq.png').convert_alpha()
nivelavancaimagem = pygame.image.load('nivelavanca.png').convert_alpha()


# Carregando as imagens de torradas
torrada_nerd_image = pygame.image.load('torradanerd.png').convert_alpha()
torrada_feliz_image = pygame.image.load('torradafeliz.png').convert_alpha()
torradaaocontrarioimagem = pygame.image.load('torrada_virada.png').convert_alpha()
torradacoquetteimagem = pygame.image.load('torradacoquette.png').convert_alpha()
torradamofadaimagem = pygame.image.load('torradamofada.png').convert_alpha()
oquevoceestafazendoimagem = pygame.image.load('oquevoceestafazendo.png').convert_alpha()
torradainterrogacaoimagem = pygame.image.load('torradainterrogacao.png').convert_alpha()
torradinhaimagem = pygame.image.load('torradinha.png').convert_alpha()
torradapalhacoimagem = pygame.image.load('torradapalhaco.png').convert_alpha()
torradauwuimagem = pygame.image.load('torradauwu.png').convert_alpha()
torradadechapeuimagem = pygame.image.load('torradadechapeu.png').convert_alpha()
bloqueiopatorealista = pygame.image.load('bloqueado.png').convert_alpha()
bloqueiopatoburgues = pygame.image.load('bloqueiopatoburgues.png').convert_alpha()
bloqueiopatomusculoso = pygame.image.load('bloqueiopatomusculoso.png').convert_alpha()
bloqueiopatodobrado = pygame.image.load('bloqueiopatodobrado.png').convert_alpha()
ponteiro = pygame.image.load('museA.png').convert_alpha()

# Definição de Cores
BLACK = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (234, 95, 112)
CYAN = (0, 255, 255)
DARK_PURPLE = (128, 0, 128)
azul = (121, 161, 191)
azulclaro = (207, 228, 245)
verde = (114, 167, 139)
# Variáveis do Jogo
mouse_button_down = False
patocoins = 0
Patomusculoso = 0
vida = 1
maxVida = 1
desenho = ""
nivel = 1
dano = 1
dps = 0
custo_botao_1 = 200
custo_botao_2 = 5000 
custo_botao_3 = 50000
custo_botao_4 = 200000
custo_botao_5 = 0
#custo_botao_5 = 5000
danoclique = 0
vaiganhar = 50
valornivelanterior = 0

#-------------------------------
nivelavanca = True  # Controla se o nível avança ou não
# Configuração do botão de ativação/desativação do avanço de nível
botao_toggle_nivel_pos = pygame.math.Vector2(1121, 127)  # Posição do botão
botao_toggle_nivel_rad = 40  # Raio do botão
# Função para alternar o modo de avanço de nível
def toggle_nivel():
    global nivelavanca
    nivelavanca = not nivelavanca  # Alterna entre True e False

# Variável para controlar o estado do avanço de nível

#0-------------------------------


# Configuração do botão de voltar nível
botao_voltar_nivel_pos = pygame.math.Vector2(1047, 79)  # Posição do botão
botao_voltar_nivel_rad = 20  # Raio do botão

# Variáveis de controle
mostrar_mouse_desenho = False  # Controla a exibição da imagem mouse

# Variáveis para dano de clique do pato musculoso
danoclique_interval = 800  # Intervalo de tempo em milissegundos para aplicar o DPS
last_danoclique_time = pygame.time.get_ticks()  # Tempo do último cálculo de DPS
# Lista para textos de dano
dano_textos = []

# Variáveis para DPS
dps_interval = 1000  # Intervalo de tempo em milissegundos para aplicar o DPS
last_dps_time = pygame.time.get_ticks()  # Tempo do último cálculo de DPS

# Variáveis para o temporizador
tempo_inicial_boss = 0
tempo_limite_boss = 10000  # Tempo em milissegundos (10 segundos, por exemplo)


# Configuração de Botões
buttons = [
    {"pos": pygame.math.Vector2(157, 605), "rad": 40},
    {"pos": pygame.math.Vector2(399, 603), "rad": 40},
    {"pos": pygame.math.Vector2(641, 603), "rad": 40},
    {"pos": pygame.math.Vector2(883, 603), "rad": 40},
    {"pos": pygame.math.Vector2(1125, 603), "rad": 40},
]

# Lista para armazenar patos que devem aparecer na tela
patos_na_tela = []

# Funções para Configuração de Torradas
def torradanerd():
    global vida, maxVida, desenho, patocoins, vaiganhar
    if nivel == 1:
        vida = maxVida = 25
        vaiganhar = 50
            
    if nivel == 2:
        vida = maxVida = 50 
        vaiganhar = 120
        
        
    if nivel == 3:
        vida = maxVida = 100
        vaiganhar = 230

        
    if nivel == 4:
        vida = maxVida = 140
        vaiganhar = 300
  
    desenho = "torradanerd"
        

def torradafeliz():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 5:
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador
        vaiganhar = 700
        vida = maxVida = 300
    if nivel == 6:
        vida = maxVida = 400
        vaiganhar = 600
    if nivel == 7:
        vida = maxVida = 1500
        vaiganhar = 2100
    if nivel == 8:
        vida = maxVida = 2000
        vaiganhar = 2500
    if nivel == 9:
        vida = maxVida = 2500
        vaiganhar = 2700
    desenho = "torradafeliz"


def torradaaocontrario():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 10:
        vida = maxVida = 6000
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador
  
        vaiganhar = 10000
    if nivel == 11:
        vida = maxVida = 4000
        vaiganhar = 5000
    if nivel == 12:
        vida = maxVida = 4200
        vaiganhar = 5360
    if nivel == 13:
        vida = maxVida = 4400
        vaiganhar = 5620
    if nivel == 14:
        vida = maxVida = 4800
        vaiganhar = 5800
    desenho = "torradaaocontrarioimagem"

def torradamofada():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 15:
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador

        vida = maxVida = 10000
        vaiganhar = 8000
    if nivel == 16:
        vida = maxVida = 12000
        vaiganhar = 6024
    if nivel == 17:
        vida = maxVida = 14600
        vaiganhar = 6200
    if nivel == 18:
        vida = maxVida = 16320
        vaiganhar = 6580

    if nivel == 19:
        vida = maxVida = 5

        vaiganhar = 6200
    desenho = "torradamofadaimagem"

def torradacoquette():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 20:
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 21:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 22:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 23:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 24:
        vida = maxVida = 5
        vaiganhar = 10000

    desenho = "torradacoquetteimagem"


def torradainterrogacao():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 25:
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 26:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 27:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 28:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 29:
        vida = maxVida = 5
        vaiganhar = 10000

    desenho = "torradainterrogacaoimagem"

def torradapalhaco():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 30:
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 31:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 32:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 33:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 34:
        vida = maxVida = 5
        vaiganhar = 10000

    desenho = "torradapalhacoimagem"


def torradauwu():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 35:
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 36:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 37:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 38:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 39:
        vida = maxVida = 5
        vaiganhar = 10000

    desenho = "torradauwuimagem"

def torradinha():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 40:
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 41:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 42:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 43:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 44:
        vida = maxVida = 5
        vaiganhar = 10000
        

    desenho = "torradinhaimagem"

def torradadechapeu():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 45:
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 46:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 47:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 48:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 49:
        vida = maxVida = 5
        vaiganhar = 10000

    desenho = "torradadechapeuimagem"

def oquevoceestafazendo():
    global vida, maxVida, desenho, patocoins, tempo_inicial_boss, vaiganhar
    if nivel == 50:
        tempo_inicial_boss = pygame.time.get_ticks()  # Inicia o temporizador
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 51:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 52:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 53:
        vida = maxVida = 5
        vaiganhar = 10000
    if nivel == 54:
        vida = maxVida = 5
        vaiganhar = 10000

    desenho = "oquevoceestafazendoimagem"

def update_torrada(): #chama isso quando a vida chega em 0 ou quando aperta botao de voltar e quando iniciao jogo
    global nivel
       
    if nivel < 5:
        torradanerd()  # Torrada nerd aparece nos níveis menores que 5
    elif 5 <= nivel <= 9:
        torradafeliz()  # Torrada feliz aparece entre os níveis 5 e 9
    elif 10 <= nivel <= 14:
        torradaaocontrario() 
    elif 15 <= nivel <= 19:
        torradamofada()
    elif 20 <= nivel <= 24:
        torradacoquette()
    elif 25 <= nivel <=29:
        torradainterrogacao()
    elif 30 <= nivel <= 34:
        torradapalhaco()
    elif 35 <= nivel <= 39:
        torradauwu()
    elif 40 <= nivel <= 44:
        torradinha()
    elif 45 <= nivel <= 49:
        torradadechapeu()
    elif 50 <= nivel <= 59:
        oquevoceestafazendo()


# Configuração da Torrada
torrada = pygame.Rect(510, 201, 260, 242)  # Retângulo da torrada
torrada_surface = pygame.Surface((torrada.width, torrada.height), pygame.SRCALPHA)
torrada_surface.fill((0, 0, 0, 0))  # Retângulo transparente

# Configuração da Fonte
font = pygame.font.SysFont(None, 48)  # Fonte padrão, tamanho 48

#-----------------------------------------------------------------------------

# Funções de Ação para Cada Botão
def acao_botao_1():
    global patocoins, custo_botao_1, dps, mouse  # Certifique-se de que está usando as variáveis globais
    if patocoins >= custo_botao_1:  # Verifica se o jogador tem patocoins suficientes
        if patosiames not in patos_na_tela:
            patos_na_tela.append(patosiames)
        patocoins -= custo_botao_1  # Subtrai o custo atual de patocoins
        dps += 2
        if dps >= 4:
            dps *= 2
        custo_botao_1 *= 2  # Dobra o custo para a próxima vez

#---------------------------------------------------------------------------------------

def acao_botao_2():
    global patocoins, custo_botao_2, dano  # Certifique-se de que está usando as variáveis globais
    if patocoins >= custo_botao_2:  # Verifica se o jogador tem patocoins suficientes
        if patodobrado not in patos_na_tela:
            patos_na_tela.append(patodobrado)
        patocoins -= custo_botao_2  # Subtrai o custo atual de patocoins
        dano *= 2  # Incrementa o dano
        custo_botao_2 *= 4  # Dobra o custo para a próxima vez

#---------------------------------------------------------------------------------------

def acao_botao_3():
    global patocoins, custo_botao_3, dano, danoclique, mousedesenho, mostrar_mouse_desenho  # Certifique-se de que está usando as variáveis globais
    if patocoins >= custo_botao_3:  # Verifica se o jogador tem patocoins suficientes
        if patomusculoso not in patos_na_tela:
            patos_na_tela.append(patomusculoso)
            
        patocoins -= custo_botao_3  # Subtrai o custo atual de patocoins
        danoclique = dano 
        custo_botao_3 *= 2  # Dobra o custo para a próxima vez

        mostrar_mouse_desenho = True  # Define a variável para mostrar a imagem do mouse
          # Ajuste a posição conforme necessário

#---------------------------------------------------------------------------------------

def acao_botao_4():
    global patocoins, custo_botao_4, dps  # Certifique-se de que está usando as variáveis globais
    if patocoins >= custo_botao_4:  # Verifica se o jogador tem patocoins suficientes
        if patorealista not in patos_na_tela:
            patos_na_tela.append(patorealista)
        patocoins -= custo_botao_4  # Subtrai o custo atual de patocoins
        dps *= 1.5  # Incrementa o dano
        custo_botao_4 *= 5  # Dobra o custo para a próxima vez

#---------------------------------------------------------------------------------------

def acao_botao_5():
    global patocoins, custo_botao_5, dano  # Certifique-se de que está usando as variáveis globais
    if patocoins >= custo_botao_5:  # Verifica se o jogador tem patocoins suficientes
        if patoburgues not in patos_na_tela:
            patos_na_tela.append(patoburgues)
        patocoins -= custo_botao_5  # Subtrai o custo atual de patocoins
        dano *= 2  # Incrementa o dano
        custo_botao_5 *= 2  # Dobra o custo para a próxima vez

    # Função para adicionar um texto de dano na tela
    def adicionar_dano_texto(dano, x, y):
        global dano_textos
        dano_textos.append({
            "dano": dano,
            "x": x,
            "y": y,
            "opacity": 255
        })

#---------------------------------------------------------------------------------------

update_torrada()
# Loop Principal do Jogo
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_button_down:
            mouse_button_down = True
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")

            # Detecta se o botão de alternar nível foi clicado
            distance_toggle_nivel = math.sqrt((botao_toggle_nivel_pos.x - mouse_x) ** 2 + (botao_toggle_nivel_pos.y - mouse_y) ** 2)
            if distance_toggle_nivel < botao_toggle_nivel_rad:
                toggle_nivel()  # Alterna o modo de avanço de nível

            # Tocar som de clique
            click_sound.play()

            # Verificar se o botão de voltar nível foi clicado
            distance_voltar = math.sqrt((botao_voltar_nivel_pos.x - mouse_x) ** 2 + (botao_voltar_nivel_pos.y - mouse_y) ** 2)
            if distance_voltar < botao_voltar_nivel_rad:
                if nivel > 1:  # Garante que não volte além do nível 1
                    nivel -= 1
                    update_torrada()

            # Aqui você adiciona a verificação do dano à torrada
            if event.button == 1:  # Garante que é o botão esquerdo
                if torrada.collidepoint(mouse_x, mouse_y):
                    # Aplica dano à torrada
                    vida = max(vida - dano, 0)
                    print(f"Torrada atingida! Vida restante: {vida}")


           # if torrada.collidepoint(mouse_x, mouse_y):
                #vida = max(vida - dano, 0)  # Diminui a vida da torrada

                for i, button in enumerate(buttons):
                    distance = math.sqrt((button["pos"].x - mouse_x) ** 2 + (button["pos"].y - mouse_y) ** 2)
                    if distance < button["rad"]:
                    # Ações para cada botão
                        if i == 0:
                            acao_botao_1()
                        elif i == 1:
                            acao_botao_2()
                        elif i == 2:
                            acao_botao_3()
                        elif i == 3:
                            acao_botao_4()
                        elif i == 4:
                            acao_botao_5()
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False

    
    DISPLAYSURF.blit(mousedesenho, (200, 200))
    
    # Atualização do Nível e Estado da Torrada
    if vida == 0:
        if nivelavanca:  # Só avança o nível se o avanço de nível estiver ativado
            nivel += 1
        patocoins += vaiganhar
        update_torrada()





    # Aplicar o dano do pato musculoso
    current_time = pygame.time.get_ticks()
    if current_time - last_danoclique_time >= danoclique_interval and danoclique > 0:
        vida = max(vida - danoclique, 0)
        last_danoclique_time = current_time

    #dps
    current_time = pygame.time.get_ticks()
    if current_time - last_dps_time >= dps_interval and dps > 0:
        vida = max(vida - dps, 0)
        last_dps_time = current_time

    # Desenho dos Elementos na Tela
    DISPLAYSURF.blit(mapa, (0, 0))  # Desenha o mapa


    # Barra de HP da Torrada
    HPbar_torrada = pygame.Rect(518, 160, vida * (243 / maxVida), 20)
    pygame.draw.rect(DISPLAYSURF, RED, HPbar_torrada)

    # Desenha todos os patos na tela
    for pato in patos_na_tela:
        DISPLAYSURF.blit(pato, (0, 0))  # Ajuste a posição conforme necessário

    # Desenha a Torrada Correspondente
    if desenho == "torradanerd":
        DISPLAYSURF.blit(torrada_nerd_image, (0, 0))
    elif desenho == "torradafeliz":
        DISPLAYSURF.blit(torrada_feliz_image, (0, 0))
    elif desenho == "torradaaocontrarioimagem":
        DISPLAYSURF.blit(torradaaocontrarioimagem, (0,0))
    elif desenho == "torradamofadaimagem":
        DISPLAYSURF.blit(torradamofadaimagem, (0,0))
    elif desenho == "torradacoquetteimagem":
        DISPLAYSURF.blit(torradacoquetteimagem, (0,0))
    elif desenho == "torradainterrogacaoimagem":
        DISPLAYSURF.blit(torradainterrogacaoimagem, (0,0))
    elif desenho == "torradinhaimagem":
        DISPLAYSURF.blit(torradinhaimagem, (0,0))
    elif desenho == "torradadechapeuimagem":
        DISPLAYSURF.blit(torradadechapeuimagem, (0,0))
    elif desenho == "torradauwuimagem":
        DISPLAYSURF.blit(torradauwuimagem, (0,0))
    elif desenho == "torradapalhacoimagem":
        DISPLAYSURF.blit(torradapalhacoimagem, (0,0))


    DISPLAYSURF.blit(patoinicial, (0, 0))

    # Desenhar textos de dano
    for texto in dano_textos:
        dano_surface = font.render(str(texto["dano"]), True, RED)
        dano_surface.set_alpha(texto["opacity"])  # Aplica a opacidade
        DISPLAYSURF.blit(dano_surface, (texto["x"], texto["y"]))

    # texto da vida
    vida_text_surface = font.render(str(round(vida)), True, RED)
    DISPLAYSURF.blit(vida_text_surface, (590, 115))

    # Desenha o Texto de Patocoins
    text_surface = font.render(str(patocoins), True, azulclaro)
    DISPLAYSURF.blit(text_surface, (130, 45))

    # Desenha o Custo de Patocoins do Botão 1
    custo_text_surface = font.render(f'{format_number(custo_botao_1)}', True, azul)
    DISPLAYSURF.blit(custo_text_surface, (119, 664))  # Ajuste a posição conforme necessário

    # Desenha o Custo de Patocoins do Botão 2
    custo_text_surface2 = font.render(f'{format_number(custo_botao_2)}', True, azul)
    DISPLAYSURF.blit(custo_text_surface2, (366, 664))  # Ajuste a posição conforme necessário

    # Desenha o Custo de Patocoins do Botão 3
    custo_text_surface3 = font.render(f'{format_number(custo_botao_3)}', True, azul)
    DISPLAYSURF.blit(custo_text_surface3, (616, 664))

    # Desenha o Custo de Patocoins do Botão 4
    custo_text_surface4 = font.render(f'{format_number(custo_botao_4)}', True, azul)
    DISPLAYSURF.blit(custo_text_surface4, (863, 664))

    # Desenha o Texto de DPS
    dps_text_surface = font.render(str(round(dps)), True, azulclaro)
    DISPLAYSURF.blit(dps_text_surface, (110, 145))  # Ajuste a posição conforme necessário

    #texto do dano
    dano_text_surface = font.render(f'{dano}', True, azulclaro)
    DISPLAYSURF.blit(dano_text_surface, (90, 235))

    #moedas que vai ganhar
    dano_text_surface = font.render(f'{vaiganhar}', True, verde)
    DISPLAYSURF.blit(dano_text_surface, (610, 448))


    # Desenha a imagem do mouse se necessário
    if mostrar_mouse_desenho:
        DISPLAYSURF.blit(ponteiro, (200, 200))  # Ajuste a posição conforme necessário

    # Dentro do loop principal
    current_time = pygame.time.get_ticks()

    # Verifique se a torrada feliz está no nível atual e se o tempo limite foi atingido
    if nivel % 5 == 0:
        if current_time - tempo_inicial_boss >= tempo_limite_boss:
            if vida > 0 and nivel % 5 == 0:
                vida = maxVida
                tempo_inicial_boss = pygame.time.get_ticks()


    # Dentro do loop principal, após atualizar a tela

    if nivel % 5 == 0:  # Verifica se o nível é múltiplo de 5
        tempo_restante = max(0, (tempo_inicial_boss + tempo_limite_boss - current_time) // 1000)
        tempo_surface = font.render(f' {tempo_restante} s', True, (108, 137, 244))
        DISPLAYSURF.blit(tempo_surface, (450, 115))  # Ajuste a posição conforme necessário

    # Desenhar o botão com a imagem apropriada (dependendo se o nível avança ou não)
    if nivelavanca:
        DISPLAYSURF.blit(nivelavancaimagem, (0, 0))
    else:
        DISPLAYSURF.blit(nivelbloqimagem, (0, 0))

    # Desenhar o nível atual na tela
    nivel_text_surface = font.render(f'{nivel}', True, azulclaro)
    DISPLAYSURF.blit(nivel_text_surface, (1100, 68))  # Ajuste a posição conforme necessário

    if patocoins <= custo_botao_2:
        DISPLAYSURF.blit(bloqueiopatodobrado, (0, 0))
    if patocoins <= custo_botao_3:
        DISPLAYSURF.blit(bloqueiopatomusculoso, (0, 0))
    if patocoins <= custo_botao_4:
        DISPLAYSURF.blit(bloqueiopatorealista, (0, 0))
    
    DISPLAYSURF.blit(bloqueiopatoburgues, (0, 0))





    pygame.display.update()  # Atualiza a tela
