import pygame
from ia import Noeud, Minimax, AlphaBeta  # Importer les classes pour l'IA

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
    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fanorona-Telo")

    # Couleurs
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BOARD_COLOR = (139, 69, 19)  # Marron bois
    LINE_COLOR = (255, 255, 255)  # Lignes blanches

    # Définition de la grille 3x3
    ROWS, COLS = 3, 3
    CELL_SIZE = 100  # Taille d'une cellule
    BOARD_SIZE = CELL_SIZE * (COLS - 1)  # Taille du plateau sans marges

    # Calcul du décalage pour centrer le plateau
    OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
    OFFSET_Y = (SCREEN_HEIGHT - BOARD_SIZE) // 2

    # Liste des intersections où placer les pions
    intersections = [(OFFSET_X + col * CELL_SIZE, OFFSET_Y + row * CELL_SIZE) for row in range(ROWS) for col in range(COLS)]

    # Placement initial des pions (Noirs en haut, Blancs en bas)
    pawns = [Pawn(BLACK, pos) for pos in intersections[:3]] + \
        [Pawn(WHITE, pos) for pos in intersections[-3:]]

    # Définition des connexions valides (lignes du plateau)
    connections = {
        intersections[0]: [intersections[1], intersections[3], intersections[4]],  # Haut gauche
        intersections[1]: [intersections[0], intersections[2], intersections[4]],  # Haut centre
        intersections[2]: [intersections[1], intersections[4], intersections[5]],  # Haut droite
        intersections[3]: [intersections[0], intersections[4], intersections[6]],  # Milieu gauche
        intersections[4]: [intersections[0], intersections[1], intersections[2],
        intersections[3], intersections[5], intersections[6], intersections[7], intersections[8]],  # Centre
        intersections[5]: [intersections[2], intersections[4], intersections[8]],  # Milieu droite
        intersections[6]: [intersections[3], intersections[4], intersections[7]],  # Bas gauche
        intersections[7]: [intersections[6], intersections[4], intersections[8]],  # Bas centre
        intersections[8]: [intersections[4], intersections[5], intersections[7]],  # Bas droite
    }

    # Fonction pour dessiner le plateau
    def draw_board():
        screen.fill(BOARD_COLOR)  # Fond marron

        # Dessiner les intersections
        for x, y in intersections:
            pygame.draw.circle(screen, LINE_COLOR, (x, y), 5)

        for pos, neighbors in connections.items():
            for neighbor in neighbors:
                pygame.draw.line(screen, LINE_COLOR, pos, neighbor, 2)

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
        return new_pos in connections[selected_pawn.position]  # Vérifie la connexion

    # Gestion des clics pour déplacer les pions
    selected_pawn = None
    running = True
    current_player = 1  # 1 pour le joueur humain, 2 pour l'IA

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == 1:
                x, y = pygame.mouse.get_pos()
                for pawn in pawns:
                    if (pawn.position[0] - x) ** 2 + (pawn.position[1] - y) ** 2 < pawn.radius ** 2:
                        selected_pawn = pawn
            elif event.type == pygame.MOUSEBUTTONUP and current_player == 1:
                if selected_pawn:
                    x, y = pygame.mouse.get_pos()
                    # Trouver la position d'intersection la plus proche
                    closest_pos = min(intersections, key=lambda pos: (pos[0] - x) ** 2 + (pos[1] - y) ** 2)
                    # Vérifier si le déplacement est valide
                    if is_valid_move(selected_pawn, closest_pos):
                        selected_pawn.position = closest_pos
                        current_player = 2  # Passer à l'IA
                    selected_pawn = None

        # Tour de l'IA
        if current_player == 2:
            # Convertir le plateau en représentation pour l'IA
            plateau_ia = [[0 for _ in range(3)] for _ in range(3)]
            for pawn in pawns:
                row = (pawn.position[1] - OFFSET_Y) // CELL_SIZE
                col = (pawn.position[0] - OFFSET_X) // CELL_SIZE
                plateau_ia[row][col] = 1 if pawn.color == BLACK else 2

            noeud_ia = Noeud(plateau_ia, 2)
            best_move = None
            best_eval = -float('inf')

            # Trouver le meilleur mouvement avec Minimax ou Alpha-Beta
            for successeur in noeud_ia.get_successor():
                eval = Minimax.minimax(successeur, 3, False)  # Profondeur de 3
                if eval > best_eval:
                    best_eval = eval
                    best_move = successeur

            # Appliquer le meilleur mouvement
            if best_move:
                for pawn in pawns:
                    if pawn.color == WHITE:
                        row = (pawn.position[1] - OFFSET_Y) // CELL_SIZE
                        col = (pawn.position[0] - OFFSET_X) // CELL_SIZE
                        if best_move.plateau[row][col] == 2:
                            new_row, new_col = None, None
                            for i in range(3):
                                for j in range(3):
                                    if best_move.plateau[i][j] == 2 and (i != row or j != col):
                                        new_row, new_col = i, j
                            if new_row is not None and new_col is not None:
                                pawn.position = intersections[new_row * 3 + new_col]
                                break
                current_player = 1  # Revenir au joueur humain

        draw_board()
        draw_pawns()
        pygame.display.flip()

    pygame.quit()