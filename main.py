import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fanorona Telo - Menu")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Police de texte
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# Texte du titre
title_text = font.render("Fanorona Telo", True, BLACK)
title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

# Bouton "Jouer"
play_text = small_font.render("Jouer", True, BLACK)
play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Bouton "Quitter"
quit_text = small_font.render("Quitter", True, BLACK)
quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

def draw_menu():
    screen.fill(WHITE)
    screen.blit(title_text, title_rect)
    
    # Dessiner le bouton "Jouer"
    pygame.draw.rect(screen, GRAY, play_rect.inflate(20, 10))  # Agrandir le rectangle du bouton
    screen.blit(play_text, play_rect)
    
    # Dessiner le bouton "Quitter"
    pygame.draw.rect(screen, GRAY, quit_rect.inflate(20, 10))  # Agrandir le rectangle du bouton
    screen.blit(quit_text, quit_rect)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier si le clic est sur le bouton "Jouer"
                if play_rect.collidepoint(event.pos):
                    print("Lancement du jeu...")  # Ici, tu peux lancer le jeu
                
                # Vérifier si le clic est sur le bouton "Quitter"
                if quit_rect.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    sys.exit()
        
        draw_menu()
        pygame.display.flip()

if __name__ == "__main__":
    main()
