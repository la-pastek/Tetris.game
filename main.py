import pygame
import sys
import IA

pygame.init()

# Initialiser la fenêtre
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tetris avec IA")
clock = pygame.time.Clock()

# Couleurs
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BUTTON_COLOR = (0, 128, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)

# Police de caractères
font = pygame.font.SysFont(None, 55)


# Fonction pour dessiner un bouton
def draw_button(text, x, y, w, h, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse_pos[0] > x and y + h > mouse_pos[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True  # Le bouton a été cliqué
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    # Ajouter le texte sur le bouton
    button_text = font.render(text, True, WHITE)
    screen.blit(button_text, (x + (w - button_text.get_width()) // 2, y + (h - button_text.get_height()) // 2))

    return False


# Simuler le lancement de Tetris (ici, on le remplace par un message)
def play_tetris():
    IA.main()
    print("Tetris avec IA est lancé !")
    # Ici, vous pouvez ajouter le code de votre jeu de Tetris ou l'IA


# Boucle principale
running = True
while running:
    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'écran avec une couleur
    screen.fill(PURPLE)

    # Dessiner le bouton "Play Tetris"
    if draw_button("Play Tetris", 300, 250, 200, 80, BUTTON_COLOR, BUTTON_HOVER_COLOR):
        play_tetris()  # Lancer le jeu si le bouton est cliqué

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter à 60 FPS
    clock.tick(60)

pygame.quit()
sys.exit()
