import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Управление самолетом")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Загрузка и изменение размеров изображений
plane_image = pygame.image.load("fighter.png")
plane_image = pygame.transform.scale(plane_image, (50, 50))  # Размеры самолета игрока

enemy_plane_image = pygame.image.load("enemy.png")
enemy_plane_image = pygame.transform.scale(enemy_plane_image, (50, 50))  # Размеры вражеского самолета

cloud_image = pygame.image.load("cloud.png")
cloud_image = pygame.transform.scale(cloud_image, (80, 40))  # Размеры облака

explosion_image = pygame.image.load("explosion.png")
explosion_image = pygame.transform.scale(explosion_image, (60, 60))  # Размеры взрыва

# Размеры самолета игрока
plane_width, plane_height = plane_image.get_size()

# Класс для самолета игрока
class Plane:
    def __init__(self):
        self.image = plane_image
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - plane_height - 10
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        elif self.x + plane_width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - plane_width
        self.rect.topleft = (self.x, self.y)

# Класс для вражеского самолета
class EnemyPlane:
    def __init__(self):
        self.image = enemy_plane_image
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.y = -self.image.get_height()
        self.speed = random.randint(1, 3)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.speed

    def off_screen(self):
        return self.y > SCREEN_HEIGHT

# Класс для пушки
class Cannon:
    def __init__(self, plane):
        self.plane = plane
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.midtop = (plane.x + plane_width // 2, plane.y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.y -= 5

# Класс для облака
class Cloud:
    def __init__(self):
        self.image = cloud_image
        self.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.y = -self.image.get_height()
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def off_screen(self):
        return self.y > SCREEN_HEIGHT

# Класс для взрыва
class Explosion:
    def __init__(self, x, y):
        self.image = explosion_image
        self.x = x
        self.y = y
        self.duration = 30  # Длительность взрыва

    def draw(self):
        if self.duration > 0:
            screen.blit(self.image, (self.x, self.y))
            self.duration -= 1

# Основная функция
def main():
    clock = pygame.time.Clock()
    plane = Plane()
    enemies = []
    cannons = []
    clouds = []
    explosions = []
    score = 0
    font = pygame.font.Font(None, 36)
    game_over = False
    game_running = True

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if game_running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                plane.move(-plane.speed)
            if keys[pygame.K_RIGHT]:
                plane.move(plane.speed)
            if keys[pygame.K_SPACE]:
                cannons.append(Cannon(plane))

            # Создание вражеских самолетов
            if random.randint(1, 50) == 1:
                enemies.append(EnemyPlane())

            # Создание облаков
            if random.randint(1, 100) == 1:
                clouds.append(Cloud())

            # Обновление вражеских самолетов
            for enemy in enemies[:]:
                enemy.move()
                if enemy.off_screen():
                    enemies.remove(enemy)
                # Проверка столкновения с пушками
                for cannon in cannons:
                    if pygame.Rect(enemy.x, enemy.y, enemy_plane_image.get_width(), enemy_plane_image.get_height()).colliderect(cannon.rect):
                        enemies.remove(enemy)
                        cannons.remove(cannon)
                        score += 1
                        explosions.append(Explosion(enemy.x, enemy.y))  # Создание взрыва при попадании

            # Обновление пушек
            for cannon in cannons:
                cannon.move()
                if cannon.rect.y < 0:
                    cannons.remove(cannon)

            # Обновление облаков
            for cloud in clouds:
                cloud.move()
                if cloud.off_screen():
                    clouds.remove(cloud)

                # Проверка столкновения самолёта игрока с облаками
                if plane.rect.colliderect(cloud.rect):
                    explosions.append(Explosion(plane.x, plane.y))
                    game_running = False  # Остановка игры при столкновении
                    clouds.remove(cloud)  # Удаление облака при столкновении

        # Рендеринг
        screen.fill(WHITE)
        if game_running:
            plane.draw()
            for enemy in enemies:
                enemy.draw()
            for cannon in cannons:
                cannon.draw()
            for cloud in clouds:
                cloud.draw()
        for explosion in explosions:
            explosion.draw()

        # Отображение счета
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Отображение надписи "Игра окончена"
        if not game_running:
            game_over_text = font.render("Игра окончена", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

