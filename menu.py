import pygame
import carSimulator
import RecoleccionBusqueda 
import ReconocimeintoArea  

# Colores
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# Dimensiones de la ventana
WIDTH = 800
HEIGHT = 600

# Tamaño de los botones
BUTTON_WIDTH = 350
BUTTON_HEIGHT = 50

# Clase para el menú principal
class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

        self.buttons = [
            ("Velocidades", "velocidades"),
            ("Recorrido de Polígonos", "poligonos"),
            ("Área de Trabajo", "ReconocimeintoArea"),  
            (" Búsqueda y Recolección", "RecoleccionBusqueda"),
           
        ]

    def draw(self):
        self.screen.fill(WHITE)
        button_rects = []
        for i, (text, action) in enumerate(self.buttons):
            rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 150 + i * (BUTTON_HEIGHT + 10), BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(self.screen, LIGHT_BLUE, rect, border_radius=10)
            button_text = self.font.render(text, True, DARK_BLUE)
            text_rect = button_text.get_rect(center=rect.center)
            self.screen.blit(button_text, text_rect)
            button_rects.append((rect, action))

        return button_rects

    def run(self):
        running = True
        from poligonos import PolygonsSimulation
        polygons_simulation = PolygonsSimulation()

        while running:
            button_rects = self.draw()
            for button_rect, action in button_rects:
                if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    if action == "poligonos":
                        polygons_simulation.run()
                    elif action == "velocidades":
                        self.run_car_simulation()
                    elif action == "RecoleccionBusqueda":  
                        RecoleccionBusqueda.main()  
                    elif action == "ReconocimeintoArea":  
                        ReconocimeintoArea.main()  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()

    def run_car_simulation(self):
        """Ejecuta el simulador de vehículos."""
        carSimulator.main()  # Llama a la función main del simulador de vehículos        

# Código para inicializar Pygame y ejecutar el menú
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    menu = MainMenu(screen)
    menu.run()
    pygame.quit()
