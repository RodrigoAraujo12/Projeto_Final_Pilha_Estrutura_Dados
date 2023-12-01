import pygame
import sys

# Configurações da tela
WIDTH = 700
HEIGHT = 700
BG_COLOR = (255, 255, 255)
STACK_COLOR = (0, 0, 0)
TOP_COLOR = (255, 0, 0)
STACK_SIZE = 10
BUTTON_RADIUS = 0
STACK_RADIUS = 15
MESSAGE_DURATION = 1500  # 1,5 segundos em milissegundos

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pilha com Pygame")
clock = pygame.time.Clock()

# Classe para representar a pilha
class Stack:
    
    def __init__(self):
        self.stack = []
        self.message = ""
        self.message_timer = 0
        self.top_highlighted = False

    def push(self, item):
        if len(self.stack) < STACK_SIZE:
            self.stack.append(item)
            self.message = f"Inserindo '{item}' no topo da pilha"
            self.message_timer = pygame.time.get_ticks() + MESSAGE_DURATION

    def pop(self):
        if not self.is_empty():
            item = self.stack.pop()
            self.message = f"Número '{item}' foi removido"
            self.message_timer = pygame.time.get_ticks() + MESSAGE_DURATION
            return item
        else:
            self.message = "Pilha vazia"
            self.message_timer= pygame.time.get_ticks() + MESSAGE_DURATION

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

    def show_empty_message(self):
        font = pygame.font.SysFont(None, 24)
        text = font.render("Pilhae stá vazia", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT - 20))
        screen.blit(text, text_rect)

    def show_message(self):
        if self.message_timer > pygame.time.get_ticks():
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.message, True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT-660))
            screen.blit(text, text_rect)

    def highlight_top(self):
        self.top_highlighted = True

    def unhighlight_top(self):
        self.top_highlighted = False    

# Instância da pilha
stack = Stack()

# Função para desenhar botões com bordas arredondadas
def draw_button(text, x, y, width, height, active, hover):
    if hover:
        if text == "Adicionar":
            button_color = (0, 150, 0)  # Verde escuro
        elif text == "Remover":
            button_color = (150, 0, 0)  # Vermelho escuro
        elif text == "Buscar Topo":
            button_color = (0, 0, 150)  # Azul escuro
    elif active:
        button_color = (0, 255, 0)  # Verde
    else:
        button_color = (255, 0, 0)  # Vermelho

    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=BUTTON_RADIUS)
    font = pygame.font.SysFont(None, 24)
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text, text_rect)

# Classe para representar uma caixa de texto
class TextBox:
    def __init__(self, x, y, width, height, max_length):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.max_length = max_length

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < self.max_length:
                    self.text += event.unicode

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        pygame.draw.rect(screen, (255, 255, 255), self.rect.inflate(-2, -2))
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# Instância da caixa de texto
add_textbox = TextBox(20, 50, 100, 30, 10)

# Carregar imagem de fundo
background_image = pygame.image.load("zueira.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

searching_top = False

# Loop principal do programa
while True:
    # Manipulação de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos
                # Verificar clique no botão "Adicionar"
                if 20 <= x <= 120 and 100 <= y <= 150:
                    value = add_textbox.text
                    if value:
                        stack.push(value)
                        add_textbox.text = ""
                        # Atualizar cor do botão "Remover"
                        remove_button_hover = pygame.Rect(20, 160, 100, 50).collidepoint(mouse_pos)
                        draw_button("Remover", 20, 160, 100, 50, not stack.is_empty(), remove_button_hover)
                # Verificar clique no botão "Remover"
                elif 20 <= x <= 120 and 160 <= y <= 210:
                    stack.pop()
                    stack.unhighlight_top()
                # Verificar clique no botão "Buscar Topo"
                elif 20 <= x <= 120 and 220 <= y <= 270:
                    if not stack.is_empty():
                        stack.highlight_top()
        # Manipulação de eventos da caixa de texto
        add_textbox.handle_event(event)

    # Limpar a tela
    screen.fill(BG_COLOR)

    # Desenhar imagem de fundo
    screen.blit(background_image, (0, 0))

    # Desenhar texto "Pilha" centralizado
    font = pygame.font.SysFont(None, 48)
    text = font.render("Pilha", True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH / 2, 20))
    screen.blit(text, text_rect)

    # Desenhar caixa de texto
    add_textbox.draw()

    # Obter posição do mouse
    mouse_pos = pygame.mouse.get_pos()

    # Desenhar botões com bordas arredondadas
    add_button_hover = pygame.Rect(20, 100, 100, 50).collidepoint(mouse_pos)
    search_button_hover = pygame.Rect(20, 220, 100, 50).collidepoint(pygame.mouse.get_pos())
    remove_button_hover = pygame.Rect(20, 160, 100, 50).collidepoint(mouse_pos)
    draw_button("Adicionar", 20, 100, 100, 50, stack.size() < STACK_SIZE, add_button_hover)
    draw_button("Remover", 20, 160, 100, 50, not stack.is_empty(), remove_button_hover)
    draw_button("Buscar Topo", 20, 220, 100, 50, False, search_button_hover)

    # Desenhar a pilha com bordas arredondadas
    stack_height = stack.size()
    for i, item in enumerate(stack.stack):
        color = STACK_COLOR
        pygame.draw.rect(screen, color, (300, HEIGHT - 80 - (i * 60), 100, 50), border_radius=STACK_RADIUS)
        font = pygame.font.SysFont(None, 24)
        text = font.render(item, True, (255, 255, 255))
        text_rect = text.get_rect(center=(350, HEIGHT - 55 - (i * 60)))
        screen.blit(text, text_rect)

    if stack.top_highlighted:
        pygame.draw.rect(screen, TOP_COLOR, (300, HEIGHT - 80 - (i * 60), 100, 50), border_radius=STACK_RADIUS)
        font = pygame.font.SysFont(None, 24)
        text = font.render(stack.stack[-1], True, (255, 255, 255))
        text_rect = text.get_rect(center=(350, HEIGHT - 55 - (i * 60)))
        screen.blit(text, text_rect)

    # Desenhar texto "Valor" acima da caixa de texto
    font = pygame.font.SysFont(None, 24)
    text = font.render("Valor:", True, (0, 0, 0))
    text_rect = text.get_rect(center=(70, 35))
    screen.blit(text, text_rect)
    stack.show_message()

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)
