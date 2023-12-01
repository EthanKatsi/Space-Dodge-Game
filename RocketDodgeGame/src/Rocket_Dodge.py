import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Square Dodge")

# Set up the game variables
player_size = 50
player_x = window_width // 2
player_y = window_height // 2
player_speed = 8

enemy_size = 50
enemies = []
num_enemies = 1

obstacle_size = 50
obstacles = []
num_obstacles = 0

level = 0
game_over = False
menu = True  # Menu state

clock = pygame.time.Clock()

# Set up player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("rocket ship.png").convert_alpha(), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, keys):
        # Handle player movement based on key input
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5
            
# Set up coin sprite  // WORK IN PROGRESS
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("coin.png").convert_alpha(), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, keys):
        pass

# Set up font
font = pygame.font.Font(None, 36)

# Game loop
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if menu:
        # Display the menu
        welcome_text = font.render("Welcome to Rocket Dodge!", True, (0, 0, 0))
        instructions_text = font.render("Instructions:", True, (0, 0, 0))
        description_text = font.render("Collect all the black squares without getting touched by the red ones.", True, (0, 0, 0))
        controls_text = font.render("Controls: Use the arrow keys to move.", True, (0, 0, 0))
        menu_text = font.render("Press SPACE to Start", True, (0, 200, 0))

        welcome_text_rect = welcome_text.get_rect(center=(window_width // 2, window_height // 2 - 30))
        instructions_text_rect = instructions_text.get_rect(center=(window_width // 2, window_height // 2 + 70))
        description_text_rect = description_text.get_rect(center=(window_width // 2, window_height // 2 + 105))
        controls_text_rect = controls_text.get_rect(center=(window_width // 2, window_height // 2 + 140))
        menu_text_rect = menu_text.get_rect(center=(window_width // 2, window_height // 2 + 30))

        window.fill((255, 255, 255))  # Clear the window
        window.blit(welcome_text, welcome_text_rect)
        window.blit(instructions_text, instructions_text_rect)
        window.blit(description_text, description_text_rect)
        window.blit(controls_text, controls_text_rect)
        window.blit(menu_text, menu_text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            menu = False  # Start the game when SPACE is pressed

    elif not game_over:
        # Update player sprite
        player = Player(player_x, player_y)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Border for user
        if player_x <= 0:
            player_x = 0
        elif player_x >= 751:
            player_x = 751

        if player_y <= 0:
            player_y = 0
        elif player_y >= 550:
            player_y = 550

        # Update player position
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Update enemy positions
        for enemy in enemies:
            enemy['x'] += enemy['speed_x']
            enemy['y'] += enemy['speed_y']

            if enemy['x'] <= 0 or enemy['x'] >= window_width - enemy_size:
                enemy['speed_x'] *= -1
            if enemy['y'] <= 0 or enemy['y'] >= window_height - enemy_size:
                enemy['speed_y'] *= -1

            # Check for collision with player
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_size, enemy_size)
            player_rect = player.rect
            if player_rect.colliderect(enemy_rect):
                game_over = True

        # Update coin sprite
        coin = Coin(window_width // 2, window_height // 2)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(coin)

        # Update obstacles positions
        for obstacle in obstacles[:]:  # Iterate over a copy of the list
            obstacle['x'] += obstacle['speed_x']
            obstacle['y'] += obstacle['speed_y']

            if obstacle['x'] <= 0 or obstacle['x'] >= window_width - obstacle_size:
                obstacle['speed_x'] *= -1
            if obstacle['y'] <= 0 or obstacle['y'] >= window_height - obstacle_size:
                obstacle['speed_y'] *= -1

            # Check for collision with player and remove the obstacle on collision
            obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle_size, obstacle_size)
            if player_rect.colliderect(obstacle_rect):
                obstacles.remove(obstacle)

        # Check if all obstacles are touched
        if len(obstacles) == 0:
            level += 1
            num_enemies += 0
            num_obstacles += 1

            for _ in range(num_enemies):
                enemy = {
                    'x': random.randint(0, window_width - enemy_size),
                    'y': random.randint(0, window_height - enemy_size),
                    'speed_x': random.choice([-3.5, 3.5]),
                    'speed_y': random.choice([-3.5, 3.5])
                }
                enemies.append(enemy)

            for _ in range(num_obstacles):
                obstacle = {
                    'x': random.randint(0, window_width - obstacle_size),
                    'y': random.randint(0, window_height - obstacle_size),
                    'speed_x': random.choice([-2, 2]),
                    'speed_y': random.choice([-2, 2])
                }
                obstacles.append(obstacle)

        # Clear the window
        window.fill((0, 0, 0)) # Background color (white)

        # Draw the player
        window.blit(player.image, player.rect)

        # Draw the enemies
        for enemy in enemies:
            pygame.draw.rect(window, (255, 0, 0), (enemy['x'], enemy['y'], enemy_size, enemy_size))

        # Draw the obstacles
        for obstacle in obstacles:
            pygame.draw.rect(window, (255, 255, 0), (obstacle['x'], obstacle['y'], obstacle_size, obstacle_size))

        # Display the level
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        window.blit(level_text, (10, 10))
    else:
        # Display "Game Over" text
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2))

        # Display "Restart Game" text
        restart_game_text = font.render("Press the SPACE bar to restart the game", True, (255, 0, 0))
        restart_text_rect = restart_game_text.get_rect(center=(window_width // 2, window_height // 2 + 100))

        # Display "Exit Game" text
        exit_game_text = font.render("Press ESCAPE to exit the game", True, (255, 0, 0))
        exit_text_rect = restart_game_text.get_rect(center=(window_width // 2, window_height // 2 + 150))

        window.fill((255, 255, 255))  # Clear the window
        window.blit(game_over_text, text_rect)
        window.blit(restart_game_text, restart_text_rect)
        window.blit(exit_game_text, exit_text_rect)

        # Restart game after game over
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # If the space bar is pressed
            game_over = False
            enemies = []
            num_enemies = 1
            obstacles = []
            num_obstacles = 0
            level = 0
            menu = True  # Menu state

        if keys[pygame.K_ESCAPE]:
            running = False

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
