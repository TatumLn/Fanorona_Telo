import time

class Noeud:
    def __init__(self, plateau, joueur_actuel):
        self.plateau = plateau  # Représentation du plateau de jeu
        self.joueur_actuel = joueur_actuel  # Joueur actuel (1 ou 2)

    def get_successor(self):
        successeurs = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for i in range(3):
            for j in range(3):
                if self.plateau[i][j] == self.joueur_actuel:
                    for direction in directions:
                        di, dj = direction
                        ni, nj = i + di, j + dj
                        if 0 <= ni < 3 and 0 <= nj < 3 and self.plateau[ni][nj] == 0:
                            # Generate new board state without deepcopy
                            nouveau_plateau = [row[:] for row in self.plateau]
                            nouveau_plateau[i][j] = 0
                            nouveau_plateau[ni][nj] = self.joueur_actuel
                            successeurs.append(Noeud(nouveau_plateau, 3 - self.joueur_actuel))
        return successeurs

    def est_victoire(self, joueur):
        opponent = 3 - joueur
        for row in self.plateau:
            if opponent in row:
                return False
        return True

    def est_match_nul(self):
        # Check for draw condition (no possible moves for both players)
        return not self.get_successor() and not Noeud(self.plateau, 3 - self.joueur_actuel).get_successor()

class Minimax:
    @staticmethod
    def minimax(noeud, profondeur, maximisant):
        if noeud.est_victoire(1) or noeud.est_victoire(2) or noeud.est_match_nul() or profondeur == 0:
            if noeud.est_victoire(1):
                return 1
            elif noeud.est_victoire(2):
                return -1
            else:
                return 0

        if maximisant:
            max_eval = -float('inf')
            for successeur in noeud.get_successor():
                eval = Minimax.minimax(successeur, profondeur - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for successeur in noeud.get_successor():
                eval = Minimax.minimax(successeur, profondeur - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

class AlphaBeta:
    @staticmethod
    def alphabeta(noeud, profondeur, alpha, beta, maximisant):
        if noeud.est_victoire(1) or noeud.est_victoire(2) or noeud.est_match_nul() or profondeur == 0:
            if noeud.est_victoire(1):
                return 1
            elif noeud.est_victoire(2):
                return -1
            else:
                return 0

        if maximisant:
            max_eval = -float('inf')
            for successeur in noeud.get_successor():
                eval = AlphaBeta.alphabeta(successeur, profondeur - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for successeur in noeud.get_successor():
                eval = AlphaBeta.alphabeta(successeur, profondeur - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

class PerformanceComparator:
    @staticmethod
    def comparer_performances(noeud_initial, profondeur, threshold=12):
        debut = time.time()
        Minimax.minimax(noeud_initial, min(profondeur, threshold), True)
        if profondeur > threshold:
            # Call minimax recursively without resetting the timer
            Minimax.minimax(noeud_initial, profondeur - threshold, True)
        fin = time.time()
        temps_minimax = fin - debut

        debut = time.time()
        AlphaBeta.alphabeta(noeud_initial, min(profondeur, threshold), -float('inf'), float('inf'), True)
        if profondeur > threshold:
            # Call alphabeta recursively without resetting the timer
            AlphaBeta.alphabeta(noeud_initial, profondeur - threshold, -float('inf'), float('inf'), True)
        fin = time.time()
        temps_alphabeta = fin - debut

        print(f"Temps Minimax: {temps_minimax}")
        print(f"Temps Alpha-Beta: {temps_alphabeta}")
