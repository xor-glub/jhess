from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class JumpGame(App):
    def build(self):
        self.grid = GridLayout(cols=10, spacing=1)

        # Initialiser la grille de jeu
        self.grid_data = [['  ' for _ in range(10)] for _ in range(10)]
        self.player_pos = None
        self.move_number = 1
        self.visited = set()

        # Créer les boutons de la grille
        for i in range(10):
            for j in range(10):
                button = Button(text=self.grid_data[i][j])
                button.bind(on_press=self.on_button_press)
                self.grid.add_widget(button)

        return self.grid

    def on_button_press(self, button):
        # Si la position initiale n'a pas encore été choisie, mettre à jour la position du joueur
        if self.player_pos is None:
            self.player_pos = (self.grid.children.index(button) // 10, self.grid.children.index(button) % 10)
            self.update_grid()
        # Sinon, déplacer le joueur vers la case sélectionnée si elle est valide
        elif self.player_pos is not None and (self.grid.children.index(button) // 10, self.grid.children.index(button) % 10) in self.possible_moves():
            new_pos = (self.grid.children.index(button) // 10, self.grid.children.index(button) % 10)
            self.move_number += 1
            self.visited.add(self.player_pos)
            self.player_pos = new_pos
            self.update_grid()

    def update_grid(self):
        # Mettre à jour le texte et la couleur des boutons
        for i in range(10):
            for j in range(10):
                button = self.grid.children[i * 10 + j]
                if (i, j) == self.player_pos:
                    button.text = str(self.move_number)
                    button.background_color = (1, 0, 0, 1)  # Rouge pour la position actuelle du joueur
                elif (i, j) in self.visited:
                    button.text = ' '
                    button.background_color = (0, 1, 0, 1)  # Vert pour les cases déjà jouées
                elif (i, j) in self.possible_moves():
                    button.text = 'O'
                    button.background_color = (1, 1, 1, 1)  # Blanc pour les cases possibles
                else:
                    button.text = ' '
                    button.background_color = (0, 0, 1, 1)  # Bleu pour les cases jamais jouées

    def possible_moves(self):
        # Retourner les positions possibles pour le prochain déplacement
        moves = set()
        if self.player_pos is not None:
            x, y = self.player_pos
            for i in range(-3, 4):
                for j in range(-3, 4):
                    # Ne pas autoriser les déplacements nuls
                    if i != 0 or j != 0:
                        # Vérifier les mouvements horizontaux et verticaux de 3 cases
                        if (abs(i) == 3 and j == 0) or (abs(j) == 3 and i == 0):
                            new_pos = (x + i, y + j)
                            if 0 <= new_pos[0] < 10 and 0 <= new_pos[1] < 10 and new_pos not in self.visited:
                                moves.add(new_pos)
                        # Vérifier les mouvements diagonaux de 2 cases
                        elif abs(i) == 2 and abs(j) == 2:
                            new_pos = (x + i, y + j)
                            if 0 <= new_pos[0] < 10 and 0 <= new_pos[1] < 10 and new_pos not in self.visited:
                                moves.add(new_pos)
        return moves

if __name__ == "__main__":
    JumpGame().run()
