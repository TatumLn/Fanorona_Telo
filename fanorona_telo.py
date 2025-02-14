import pygame

# Classe pour les pions
class Pawn:
    def __init__(self, color, position):
        self.color = color
        self.position = position  # (x, y)
        self.radius = 20  # Rayon du pion

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

# Fonction principale du jeu Fanorona Telo
def main_game():
    # Initialiser Pygame
    pygame.init()

    # Définition des dimensions de l'écran
    SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mini Fanorona 3x3")

    # Couleurs
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BOARD_COLOR = (139, 69, 19)  # Marron bois
    LINE_COLOR = (255, 255, 255)  # Lignes blanches

    # Définition de la grille 3x3
    ROWS, COLS = 3, 3
    CELL_SIZE = SCREEN_WIDTH // (COLS + 1)
    MARGIN = CELL_SIZE // 2

    # Liste des intersections où placer les pions
    intersections = [(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE) for row in range(ROWS) for col in range(COLS)]

    # Placement initial des pions (Noirs en haut, Blancs en bas)
    pawns = [Pawn(BLACK, pos) for i, pos in enumerate(intersections[:3])] + \
        [Pawn(WHITE, pos) for i, pos in enumerate(intersections[-3:])]

    # Fonction pour dessiner le plateau
    def draw_board():
        screen.fill(BOARD_COLOR)  # Fond marron

        # Dessiner les intersections
        for x, y in intersections:
            pygame.draw.circle(screen, LINE_COLOR, (x, y), 5)

        # Dessiner les lignes
        for row in range(ROWS):
            for col in range(COLS - 1):  
                pygame.draw.line(screen, LINE_COLOR, intersections[row * COLS + col], intersections[row * COLS + col + 1], 2)
        
        for col in range(COLS):
            for row in range(ROWS - 1):  
                pygame.draw.line(screen, LINE_COLOR, intersections[row * COLS + col], intersections[(row + 1) * COLS + col], 2)

        # Ajouter des diagonales centrales
        pygame.draw.line(screen, LINE_COLOR, intersections[0], intersections[4], 2)
        pygame.draw.line(screen, LINE_COLOR, intersections[4], intersections[8], 2)
        pygame.draw.line(screen, LINE_COLOR, intersections[2], intersections[4], 2)
        pygame.draw.line(screen, LINE_COLOR, intersections[4], intersections[6], 2)

    # Dessiner les pions
    def draw_pawns():
        for pawn in pawns:
            pawn.draw(screen)


    # Vérifier si un déplacement est valide (suivre une ligne et ne pas être occupé)
    def is_valid_move(selected_pawn, new_pos):
        if new_pos not in intersections:
            return False  # La position doit être une intersection valide

    # Vérifier si l'emplacement est déjà occupé
        for pawn in pawns:
            if pawn.position == new_pos:
                return False  # Un pion est déjà là

    # Vérifier si le déplacement suit une ligne
        x1, y1 = selected_pawn.position
        x2, y2 = new_pos
        dx, dy = abs(x2 - x1), abs(y2 - y1)

    # Déplacement valide si :
    # - Horizontale (dx > 0, dy = 0)
    # - Verticale (dx = 0, dy > 0)
    # - Diagonale (dx = dy)
        return (dx == 0 and dy == CELL_SIZE) or \
               (dy == 0 and dx == CELL_SIZE) or \
               (dx == dy == CELL_SIZE)


    # Gestion des clics pour déplacer les pions
    selected_pawn = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for pawn in pawns:
                    if (pawn.position[0] - x) ** 2 + (pawn.position[1] - y) ** 2 < pawn.radius ** 2:
                        selected_pawn = pawn
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_pawn:
                    x, y = pygame.mouse.get_pos()
                    # Trouver la position d'intersection la plus proche
                    closest_pos = min(intersections, key=lambda pos: (pos[0] - x) ** 2 + (pos[1] - y) ** 2)
                    # Vérifier si le déplacement est valide
                    if is_valid_move(selected_pawn, closest_pos):
                        selected_pawn.position = closest_pos
                    selected_pawn = None

        draw_board()
        draw_pawns()
        pygame.display.flip()

    pygame.quit()
