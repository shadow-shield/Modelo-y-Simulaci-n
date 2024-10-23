import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Búsqueda y Recolección de Materiales")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Cargar imágenes
cart_image = pygame.image.load("cart.png")
material_image = pygame.image.load("material.png")
drop_location_image = pygame.image.load("entrega.png")

# Escalar imágenes
cart_image = pygame.transform.scale(cart_image, (80, 60))
material_image = pygame.transform.scale(material_image, (20, 20))
drop_location_image = pygame.transform.scale(drop_location_image, (40, 40))

# Fuente
font = pygame.font.Font(None, 36)

# Clase Recolector
class Collector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.speed = 100
        self.materials_collected = 0
        self.materials_delivered = 0
        self.state = 'collecting'
        self.target_material = None
        self.collection_start_time = pygame.time.get_ticks()
        self.time_to_deliver = 0

    def update(self, dt, materials):
        if self.state == 'collecting':
            if len(materials) == 0:
                materials.extend([Material() for _ in range(5)])

            # Mover hacia el material más cercano
            if self.target_material is None and materials:
                self.target_material = min(materials, key=lambda m: (m.x - self.x) ** 2 + (m.y - self.y) ** 2)

            if self.target_material:
                # Mover hacia el material
                if self.x < self.target_material.x:
                    self.x += self.speed * dt
                elif self.x > self.target_material.x:
                    self.x -= self.speed * dt

                if self.y < self.target_material.y:
                    self.y += self.speed * dt
                elif self.y > self.target_material.y:
                    self.y -= self.speed * dt

                # Recoger material
                if (self.x < self.target_material.x + self.target_material.size and
                    self.x + self.size > self.target_material.x and
                    self.y < self.target_material.y + self.target_material.size and
                    self.y + self.size > self.target_material.y):
                    if self.target_material in materials:  # Verifica si el material aún está en la lista
                        self.materials_collected += 1
                        materials.remove(self.target_material)
                    self.target_material = None

            if len(materials) == 0:
                self.state = 'delivering'
                self.collection_start_time = pygame.time.get_ticks()  # Inicia el tiempo de entrega

        elif self.state == 'delivering':
            drop_location = (WIDTH - 100, HEIGHT - 100)
            if self.x < drop_location[0]:
                self.x += self.speed * dt
            elif self.x > drop_location[0]:
                self.x -= self.speed * dt

            if self.y < drop_location[1]:
                self.y += self.speed * dt
            elif self.y > drop_location[1]:
                self.y -= self.speed * dt

            # Entregar materiales
            if (self.x < drop_location[0] + 20 and
                self.x + self.size > drop_location[0] and
                self.y < drop_location[1] + 20 and
                self.y + self.size > drop_location[1]):
                if self.materials_collected > 0:
                    self.materials_delivered += self.materials_collected
                    self.materials_collected = 0
                    self.time_to_deliver = (pygame.time.get_ticks() - self.collection_start_time) / 1000.0  # Tiempo de entrega
                self.state = 'collecting'
                self.target_material = None

    def draw(self, screen):
        screen.blit(cart_image, (self.x - cart_image.get_width() / 2, self.y - cart_image.get_height() / 2))

# Clase Material
class Material:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = random.randint(0, HEIGHT - 20)
        self.size = 20

    def draw(self, screen):
        screen.blit(material_image, (self.x, self.y))

# Función principal
def main():
    collectors = []  # Lista para almacenar múltiples recolectores
    materials = [Material() for _ in range(5)]
    drop_location = (WIDTH - 100, HEIGHT - 100)
    running = True
    clock = pygame.time.Clock()

    # Variables de entrada
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 32, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    start_simulation = False

    while running:
        dt = clock.tick(60) / 1000
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.isdigit():
                            num_collectors = int(text)
                            for _ in range(num_collectors):
                                x = random.randint(0, WIDTH - 80)
                                y = random.randint(0, HEIGHT - 60)
                                collectors.append(Collector(x, y))  # Crear recolectores
                            start_simulation = True
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        if start_simulation:
            for collector in collectors:
                collector.update(dt, materials)

        # Dibujar materiales
        for material in materials:
            material.draw(screen)

        # Dibujar ubicación de entrega
        drop_location_rect = drop_location_image.get_rect(topleft=(drop_location[0], drop_location[1]))
        screen.blit(drop_location_image, drop_location_rect)

        # Dibujar recolectores
        for collector in collectors:
            collector.draw(screen)

        # Mostrar el texto de cantidad de recolectores
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Etiqueta de entrada
        label = font.render("Ingrese Numero recolectores:", True, BLACK)
        screen.blit(label, (WIDTH // 2 - 150, HEIGHT // 2 - 70))

        # Mostrar información de recolectores
        for i, collector in enumerate(collectors):
            stats = f"Recolector {i+1}: Recogidos: {collector.materials_collected}, Entregados: {collector.materials_delivered}, Tiempo: {collector.time_to_deliver:.2f}s"
            stat_text = font.render(stats, True, BLACK)
            screen.blit(stat_text, (10, 10 + i * 30))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
