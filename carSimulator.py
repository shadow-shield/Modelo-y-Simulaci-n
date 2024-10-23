import pygame
import math

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Móvil con Frenado Gradual")

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# Fuente
font = pygame.font.Font(None, 36)

# Clase Móvil
class Mobile:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.angle = 0
        self.length = length
        self.vl = 0  # Velocidad motor izquierdo
        self.vr = 0  # Velocidad motor derecho
        self.mu = 0.7  # Coeficiente de fricción
        self.is_braking = False  # Control de frenado

    def apply_brake(self, dt):
        deceleration = self.mu * 9.81  # Deceleración debido a la fricción

        if self.vl > 0:
            self.vl -= deceleration * dt
            if self.vl < 0:
                self.vl = 0
        elif self.vl < 0:
            self.vl += deceleration * dt
            if self.vl > 0:
                self.vl = 0

        if self.vr > 0:
            self.vr -= deceleration * dt
            if self.vr < 0:
                self.vr = 0
        elif self.vr < 0:
            self.vr += deceleration * dt
            if self.vr > 0:
                self.vr = 0

    def update(self, dt):
        if self.is_braking:
            self.apply_brake(dt)

        speed = (self.vl + self.vr) / 2

        if self.vl != self.vr:
            self.angle += (self.vr - self.vl) / self.length

        dx = speed * math.cos(self.angle) * dt * 100
        dy = speed * math.sin(self.angle) * dt * 100

        self.x += dx
        self.y += dy

        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))

    def draw(self, screen):
        car_length = 40
        car_height = 20
        front = pygame.Rect(self.x - car_length / 2, self.y - car_height / 2, car_length, car_height)
        pygame.draw.rect(screen, GREEN, front)
        pygame.draw.circle(screen, BLACK, (int(self.x - car_length / 2 + 10), int(self.y + car_height / 2)), 5)
        pygame.draw.circle(screen, BLACK, (int(self.x + car_length / 2 - 10), int(self.y + car_height / 2)), 5)

# Detección de colisiones entre dos carros
def detect_collision(car1, car2, min_distance=50):
    dx = car1.x - car2.x
    dy = car1.y - car2.y
    distance = math.sqrt(dx**2 + dy**2)
    return distance < min_distance

# Asignación de posiciones iniciales para evitar superposiciones
def assign_initial_position(index, total_cars):
    rows = (total_cars + 4) // 5
    cols = min(total_cars, 5)
    row = index // cols
    col = index % cols
    x = WIDTH // 2 + (col - (cols // 2)) * 60
    y = HEIGHT // 2 + (row - (rows // 2)) * 60
    return x, y

# Función principal
def main():
    cars = [Mobile(*assign_initial_position(0, 1), length=60)]

    running = True
    clock = pygame.time.Clock()

    input_box_left = pygame.Rect(WIDTH // 2 - 200, HEIGHT - 150, 140, 32)
    input_box_right = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 150, 140, 32)
    input_box_num_cars = pygame.Rect(WIDTH // 2 - 70, HEIGHT - 250, 140, 32)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')

    active_left = False
    active_right = False
    active_num_cars = False
    text_left = '0'
    text_right = '0'
    text_num_cars = '1'

    brake_button = pygame.Rect(WIDTH // 2 - 70, HEIGHT - 100, 140, 40)

    # Etiquetas para las cajas de texto
    label_left = font.render("Vel. Izquierda", True, BLACK)
    label_right = font.render("Vel. Derecha", True, BLACK)
    label_num_cars = font.render("Num. Carros", True, BLACK)

    while running:
        dt = clock.tick(60) / 1000
        screen.fill(WHITE)

        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, HEIGHT))

        title_text = font.render("Movimiento en 2D", True, WHITE)
        screen.blit(title_text, (10, 10))

        back_button = pygame.Rect(WIDTH - 170, 20, 150, 40)
        pygame.draw.rect(screen, LIGHT_BLUE, back_button, border_radius=10)
        back_text = font.render("Volver", True, DARK_BLUE)
        text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_left.collidepoint(event.pos):
                    active_left = True
                    active_right = False
                    active_num_cars = False
                elif input_box_right.collidepoint(event.pos):
                    active_right = True
                    active_left = False
                    active_num_cars = False
                elif input_box_num_cars.collidepoint(event.pos):
                    active_num_cars = True
                    active_left = False
                    active_right = False
                elif brake_button.collidepoint(event.pos):
                    for car in cars:
                        car.is_braking = True
                elif back_button.collidepoint(event.pos):
                    return
                else:
                    active_left = False
                    active_right = False
                    active_num_cars = False

            if event.type == pygame.KEYDOWN:
                if active_left:
                    if event.key == pygame.K_RETURN:
                        active_left = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_left = text_left[:-1]
                    else:
                        text_left += event.unicode
                elif active_right:
                    if event.key == pygame.K_RETURN:
                        active_right = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_right = text_right[:-1]
                    else:
                        text_right += event.unicode
                elif active_num_cars:
                    if event.key == pygame.K_RETURN:
                        active_num_cars = False
                        try:
                            num_cars = int(text_num_cars)
                            current_num_cars = len(cars)

                            if num_cars < current_num_cars:
                                cars = cars[:num_cars]
                            elif num_cars > current_num_cars:
                                for i in range(num_cars - current_num_cars):
                                    x, y = assign_initial_position(current_num_cars + i, num_cars)
                                    cars.append(Mobile(x, y, length=60))
                        except ValueError:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        text_num_cars = text_num_cars[:-1]
                    else:
                        text_num_cars += event.unicode

                for car in cars:
                    car.is_braking = False

        if not any(car.is_braking for car in cars):
            try:
                vl = float(text_left)
                vr = float(text_right)
                for car in cars:
                    car.vl = vl
                    car.vr = vr
            except ValueError:
                pass

        for i, car1 in enumerate(cars):
            for car2 in cars[i + 1:]:
                if detect_collision(car1, car2):
                    car1.x -= 10
                    car2.x += 10

        for car in cars:
            car.update(dt)
            car.draw(screen)

        txt_surface_left = font.render(text_left, True, BLACK)
        txt_surface_right = font.render(text_right, True, BLACK)
        txt_surface_num_cars = font.render(text_num_cars, True, BLACK)

        width_left = max(200, txt_surface_left.get_width() + 10)
        width_right = max(200, txt_surface_right.get_width() + 10)
        width_num_cars = max(200, txt_surface_num_cars.get_width() + 10)

        input_box_left.w = width_left
        input_box_right.w = width_right
        input_box_num_cars.w = width_num_cars

        screen.blit(txt_surface_left, (input_box_left.x + 5, input_box_left.y + 5))
        screen.blit(txt_surface_right, (input_box_right.x + 5, input_box_right.y + 5))
        screen.blit(txt_surface_num_cars, (input_box_num_cars.x + 5, input_box_num_cars.y + 5))

        pygame.draw.rect(screen, color_active if active_left else color_inactive, input_box_left, 2)
        pygame.draw.rect(screen, color_active if active_right else color_inactive, input_box_right, 2)
        pygame.draw.rect(screen, color_active if active_num_cars else color_inactive, input_box_num_cars, 2)

        pygame.draw.rect(screen, RED, brake_button)
        brake_text = font.render("Frenar", True, WHITE)
        screen.blit(brake_text, (brake_button.x + 40, brake_button.y + 5))

        # Renderizar etiquetas
        screen.blit(label_left, (input_box_left.x, input_box_left.y - 30))
        screen.blit(label_right, (input_box_right.x, input_box_right.y - 30))
        screen.blit(label_num_cars, (input_box_num_cars.x, input_box_num_cars.y - 30))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
