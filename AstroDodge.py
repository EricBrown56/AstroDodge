import pygame
import random

pygame.init()

# Set up the display
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AstroDodge")

player_image_original = pygame.transform.scale(pygame.image.load("./assets/astronaut.png"),(100, 100))
enemy_image = pygame.transform.scale(pygame.image.load("./assets/asteroid.png"),(50, 50))
blast_image = pygame.transform.scale(pygame.image.load("./assets/blast.jpg"),(50, 50))
explode_image = pygame.transform.scale(pygame.image.load("./assets/explode.png"),(50, 50))

player_size = player_image_original.get_size()
player_pos = [screen_width // 2, screen_height - player_size[1]]
player_image = player_image_original.copy() 
facing_right = False

enemy_size = enemy_image.get_size()
enemy_pos = [random.randint(0, screen_width - enemy_size[0]), 0]
enemy_speed = 5

blast_size = blast_image.get_size()
blast_pos = [player_pos[0], player_pos[1]]
blast_speed = 10

bg = pygame.image.load('./assets/space_moon.png')

pygame.mixer.music.load('./assets/Glory.mp3')
pygame.mixer.music.play(-1)
blaster_sound = pygame.mixer.Sound('./assets/blaster.wav')
explosion_sound = pygame.mixer.Sound('./assets/explosion.wav')

clock = pygame.time.Clock()
game_over = False
speed_clock = 0

def paused():
    pause = True
    while pause:
        pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                    pygame.mixer.music.unpause()
        screen.blit(bg, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))
        pygame.display.update()
        clock.tick(30)

def blast():
    global blast_pos
    blast_pos = [player_pos[0], player_pos[1]]
    screen.blit(blast_image, (blast_pos[0], blast_pos[1]))
    pygame.display.update()
    blaster_sound.play()

# Game loop

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    if speed_clock % 50 == 0:
        enemy_speed += .5

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 10
        if facing_right:
            player_image = pygame.transform.flip(player_image, True, False)
            facing_right = False
    elif keys[pygame.K_RIGHT]:
        player_pos[0] += 10
        if not facing_right:
            player_image = pygame.transform.flip(player_image, True, False)
            facing_right = True
    elif keys[pygame.K_p]:
        paused()
    elif keys[pygame.K_SPACE]:
        blast()
        blast_pos[1] -= blast_speed
        if blast_pos[1] < 0:
            blast_pos = [player_pos[0], player_pos[1]]

    # Update enemy position
    player_pos[0] = max(0, min(player_pos[0], screen_width - player_size[0]))

    enemy_pos[1] += enemy_speed

    if enemy_pos[1] > screen_height:
        enemy_pos = [random.randint(0, screen_width - enemy_size[0]), -enemy_size[1]]

    # Check for collision

    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
    enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size[0], enemy_size[1])
    blast_rect = pygame.Rect(blast_pos[0], blast_pos[1], blast_size[0], blast_size[1])
    

    

    if blast_rect.colliderect(enemy_rect):
        enemy_pos = [random.randint(0, screen_width - enemy_size[0]), -enemy_size[1]]
        screen.blit(explode_image, (enemy_pos[0], enemy_pos[1]))
        pygame.display.update()
        explosion_sound.play()

    if player_rect.colliderect(enemy_rect):
        game_over = True


    
    screen.blit(bg, (0, 0))
    screen.blit(player_image, (player_pos[0], player_pos[1]))
    screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))
    pygame.display.update()

    speed_clock += 1

    clock.tick(30)

pygame.quit()

