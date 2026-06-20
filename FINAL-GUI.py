import pygame
import random
import sys

# --- Initialization ---
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CodeJump: Pau’s Sky Mission")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial", 24)
score_font = pygame.font.SysFont("Times New Roman", 35, bold=True)
SCORE_COLOR = (76, 227, 45)  # Hex: #4ce32d

# --- Load Cover & Start Button ---
cover_image = pygame.image.load("COVER/GAME COVER.png")
cover_image = pygame.transform.scale(cover_image, (WIDTH, HEIGHT))

start_button = pygame.image.load("COVER/START.png")
start_button = pygame.transform.scale(start_button, (240, 100))
start_rect = pygame.Rect(0, 0, 200, 80)  # Set custom rect smaller than full image
start_rect.center = (WIDTH // 2, HEIGHT - 200)

# --- Name Input Screen ---
def name_input_screen():
    # Load the new orange input background (the one with white box)
    try:
        input_bg = pygame.image.load("photos/insert.png").convert_alpha()
        input_bg = pygame.transform.scale(input_bg, (WIDTH, HEIGHT))
    except pygame.error as e:
        print("❌ Could not load input background:", e)
        input_bg = None

    # Load YES and CANCEL buttons
    try:
        yes_img = pygame.image.load("photos/yes.png")
        cancel_img = pygame.image.load("photos/cancel.png")
        yes_img = pygame.transform.scale(yes_img, (100, 40))
        cancel_img = pygame.transform.scale(cancel_img, (100, 40))
    except pygame.error:
        yes_img = cancel_img = None

    font = pygame.font.Font(None, 36)

    # Set input_box dimensions to align with the white space (based on image layout)
    input_box = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2 - 20, 280, 40)  # Wider and lower for alignment
    user_text = ''
    active = False
    color_active = pygame.Color('black')
    color_inactive = pygame.Color('gray')
    color = color_inactive

    # Buttons under the input box
    yes_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 60, 100, 40)
    cancel_rect = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 60, 100, 40)

    while True:
        # Draw orange input background
        if input_bg:
            screen.blit(input_bg, (0, 0))
        else:
            screen.fill((255, 140, 0))  # fallback orange

        # Optional label above input
        label = font.render("ENTER YOUR NAME", True, (0, 0, 0))
        screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - 70))

        # Draw user input text (centered in white box)
        txt_surface = font.render(user_text, True, (0, 0, 0))  # black text
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 5))

        # Draw YES and CANCEL buttons
        if yes_img and cancel_img:
            screen.blit(yes_img, yes_rect)
            screen.blit(cancel_img, cancel_rect)
        else:
            pygame.draw.rect(screen, (0, 200, 0), yes_rect)
            pygame.draw.rect(screen, (200, 0, 0), cancel_rect)
            screen.blit(font.render("YES", True, (255, 255, 255)), (yes_rect.x + 25, yes_rect.y + 8))
            screen.blit(font.render("CANCEL", True, (255, 255, 255)), (cancel_rect.x + 10, cancel_rect.y + 8))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    color = color_active
                else:
                    active = False
                    color = color_inactive

                if yes_rect.collidepoint(event.pos) and user_text.strip() != '':
                    return user_text.strip()
                elif cancel_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) < 20 and event.unicode.isprintable():
                    user_text += event.unicode

        pygame.display.flip()
        clock.tick(60)


# --- Main Menu ---
def main_menu():
    start_hover_img = start_button.copy()
    start_hover_img.fill((200, 200, 200, 100), special_flags=pygame.BLEND_RGBA_MULT)

    # Load quit.png
    try:
        quit_button = pygame.image.load("COVER/quit.png")
        quit_button = pygame.transform.scale(quit_button, (240, 100))  # Adjusted size for better fit
        quit_rect = quit_button.get_rect()
    except pygame.error as e:
        print(f"❌ Failed to load quit button: {e}")
        quit_button = None
        quit_rect = pygame.Rect(WIDTH // 2 - 75, 0, 150, 70)

    # Set Start and Quit positions
    start_rect = start_button.get_rect(center=(WIDTH // 2, HEIGHT - 240))  # Moved Start a bit up
    quit_rect.centerx = WIDTH // 2
    quit_rect.top = start_rect.bottom + 10  # 10px space below Start

    # Hover image for Quit
    if quit_button:
        quit_hover_img = quit_button.copy()
        quit_hover_img.fill((200, 200, 200, 100), special_flags=pygame.BLEND_RGBA_MULT)
    else:
        quit_hover_img = None

    try:
        click_sound = pygame.mixer.Sound("sound/click.mp3")
        click_sound.set_volume(0.6)
    except pygame.error as e:
        print(f"❌ Failed to load click sound: {e}")
        click_sound = None

    while True:
        screen.blit(cover_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # START button hover
        if start_rect.collidepoint(mouse_pos):
            screen.blit(start_hover_img, start_rect.topleft)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            screen.blit(start_button, start_rect.topleft)

        # QUIT button hover
        if quit_button:
            if quit_rect.collidepoint(mouse_pos):
                screen.blit(quit_hover_img, quit_rect.topleft)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                screen.blit(quit_button, quit_rect.topleft)
        else:
            pygame.draw.rect(screen, (255, 0, 0), quit_rect)
            quit_font = pygame.font.SysFont("Arial", 30, bold=True)
            quit_text = quit_font.render("QUIT", True, (255, 255, 255))
            screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2, quit_rect.centery - quit_text.get_height() // 2))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                        pygame.time.delay(300)
                    return
                elif quit_rect.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()
                        pygame.time.delay(200)
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)


# --- Run Name Input & Menu ---
player_name = name_input_screen()
main_menu()

# --- Sound Setup ---
def play_music(path, volume=1.0):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"❌ Music load failed: {e}")

try:
    coin_sound = pygame.mixer.Sound("sound/coinsd.mp3")
    jump_sound = pygame.mixer.Sound("sound/jump.mp3")
    gameover_sound = pygame.mixer.Sound("sound/gamrover.mp3")
    coin_sound.set_volume(0.3)
    jump_sound.set_volume(0.4)
    gameover_sound.set_volume(1.0)
except pygame.error as e:
    print(f"❌ Sound effects error: {e}")
    coin_sound = jump_sound = gameover_sound = None

# --- Load Backgrounds & Music ---
def load_bg(path):
    try:
        bg = pygame.image.load(path).convert()
        return pygame.transform.scale(bg, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"❌ Background {path} not found: {e}")
        return None

bg_sequence = [
    ("photos/bg1-pup.png",     "sound/school-bg.mp3"),
    ("photos/stairs-final.png","sound/wind-bg.mp3"),
    ("photos/CREDITS1.png",    "sound/wind-bg.mp3"),
    ("photos/sky-final.png",   "sound/new-wind.mp3"),
    ("photos/final.jpg",       "sound/retro.mp3")
]

bg_surfaces = [load_bg(path) for path, _ in bg_sequence]
bg_music_paths = [music for _, music in bg_sequence]

# --- Load Images ---
try:
    score_label_img = pygame.image.load("photos/score1.png").convert_alpha()
    score_label_img = pygame.transform.scale(score_label_img, (140, 60))
except pygame.error as e:
    score_label_img = None
    print(f"❌ Failed to load score label image: {e}")

try:
    coin_ui_img = pygame.image.load("photos/coin.png").convert_alpha()
    coin_ui_img = pygame.transform.scale(coin_ui_img, (50, 50))
except pygame.error as e:
    coin_ui_img = None
    print(f"❌ Failed to load coin UI image: {e}")

try:
    player_img = pygame.image.load("photos/pau.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (60, 60))
except pygame.error as e:
    print(f"❌ Player image not found: {e}")
    pygame.quit()
    sys.exit()

player_rect = player_img.get_rect()
player_vel_y = 0
score = 0
coins_collected = 0

# --- Platform and Coin Setup ---
PLATFORM_WIDTH, PLATFORM_HEIGHT = 70, 40
try:
    platform_img = pygame.image.load("photos/platform1.png").convert_alpha()
    platform_img = pygame.transform.scale(platform_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
    use_platform_image = True
except pygame.error as e:
    platform_img = None
    use_platform_image = False
    print(f"❌ Platform image load error: {e}")

COIN_SIZE = 45
use_coin_image = False
try:
    coin_img = pygame.image.load("photos/coin2.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (COIN_SIZE, COIN_SIZE))
    use_coin_image = True
except pygame.error as e:
    coin_img = None
    print(f"❌ Coin image load error: {e}")

platforms = []
coins = []
max_platforms = 25
PLATFORM_GAP_MIN, PLATFORM_GAP_MAX = 15, 25
PLATFORM_MARGIN_X = 20
GRID_STEP_X = 60
SLOTS = list(range(PLATFORM_MARGIN_X, WIDTH - PLATFORM_WIDTH - PLATFORM_MARGIN_X + 1, GRID_STEP_X))

def maybe_add_coin(platform: pygame.Rect):
    if random.randint(1, 5) == 1:
        coin = pygame.Rect(platform.centerx - COIN_SIZE // 2, platform.top - (COIN_SIZE // 2), COIN_SIZE, COIN_SIZE)
        coins.append(coin)

def spawn_platforms():
    platforms.clear()
    coins.clear()
    spawn_y = HEIGHT
    for i in range(max_platforms // 2):
        y = spawn_y - sum(random.randint(PLATFORM_GAP_MIN, PLATFORM_GAP_MAX) for _ in range(i + 1))
        platform_count = random.choice([1, 2])
        used_slots = []
        for _ in range(platform_count):
            while True:
                x = random.choice(SLOTS)
                if all(abs(x - s) >= PLATFORM_WIDTH for s in used_slots):
                    used_slots.append(x)
                    break
            plat = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            platforms.append(plat)
            maybe_add_coin(plat)

spawn_platforms()
highest_y = min(p.y for p in platforms)
bottom_plat = max(platforms, key=lambda p: p.y)
player_rect.midbottom = (bottom_plat.centerx, bottom_plat.top)

def reset_game():
    global player_vel_y, score, coins_collected, highest_y, bg_music_played_index, last_music
    player_vel_y = 0
    score = 0
    coins_collected = 0
    spawn_platforms()
    highest_y = min(p.y for p in platforms)
    bottom_plat = max(platforms, key=lambda p: p.y)
    player_rect.midbottom = (bottom_plat.centerx, bottom_plat.top)
    bg_music_played_index = -1
    last_music = ""

# --- Game Loop ---
bg_music_played_index = -1
bg_cycle_count = 0
random_cycle = [2, 3, 4]
last_music = ""

running = True
while running:
    clock.tick(60)

    # Background and music logic
    cycle_index = score // 350
    if cycle_index < 5:
        current_bg_index = cycle_index
    else:
        if cycle_index != bg_cycle_count:
            current_bg_index = random.choice(random_cycle)
            bg_cycle_count = cycle_index
        else:
            current_bg_index = bg_music_played_index

    new_music = bg_music_paths[current_bg_index]
    if new_music != last_music:
        if not ((bg_music_played_index == 1 and current_bg_index == 2) or (bg_music_played_index == 2 and current_bg_index == 1)):
            play_music(new_music)
        last_music = new_music
    bg_music_played_index = current_bg_index

    if bg_surfaces[current_bg_index]:
        screen.blit(bg_surfaces[current_bg_index], (0, 0))
    else:
        screen.fill((135, 206, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if player_rect.left < 0:
        player_rect.right = WIDTH
    if player_rect.right > WIDTH:
        player_rect.left = 0

    # Gravity and jump
    player_vel_y += 0.30
    player_rect.y += player_vel_y

    if player_vel_y > 0:
        for plat in platforms:
            if player_rect.colliderect(plat) and player_rect.bottom <= plat.bottom + 10:
                player_vel_y = -18
                if jump_sound:
                    jump_sound.play()

    # Coin collection
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            coins.remove(coin)
            coins_collected += 1
            if coin_sound:
                coin_sound.play()

    # Scroll and score
    if player_rect.top <= HEIGHT // 3:
        scroll_y = abs(player_vel_y)
        player_rect.y += scroll_y
        for plat in platforms:
            plat.y += scroll_y
        for coin in coins:
            coin.y += scroll_y
        score += 1

    platforms = [p for p in platforms if p.y < HEIGHT + 70]
    coins = [c for c in coins if c.y < HEIGHT + 100]

    while len(platforms) < max_platforms:
        gap = random.randint(PLATFORM_GAP_MIN, PLATFORM_GAP_MAX)
        highest_y -= gap
        platform_count = random.choice([1, 2])
        used_slots = []
        for _ in range(platform_count):
            while True:
                x = random.choice(SLOTS)
                if all(abs(x - s) >= PLATFORM_WIDTH for s in used_slots):
                    used_slots.append(x)
                    break
            plat = pygame.Rect(x, highest_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            platforms.append(plat)
            maybe_add_coin(plat)

    gameover_font = pygame.font.SysFont("Times New Roman", 28, bold=True)

    if player_rect.top > HEIGHT:
        if gameover_sound:
            gameover_sound.play()

        # Load buttons and sounds
        try:
            play_again_img = pygame.transform.scale(pygame.image.load("photos/play-again.png"), (300, 140))
            main_menu_img = pygame.transform.scale(pygame.image.load("photos/main-menu.png"), (280, 120))
            change_name_img = pygame.transform.scale(pygame.image.load("photos/change-name.png"), (350, 160))
            restart_sound = pygame.mixer.Sound("sound/restart.mp3")
            restart_sound.set_volume(0.8 )
        except pygame.error as e:
            print(f"❌ Error loading Game Over assets: {e}")
            pygame.quit()
            sys.exit()

        # Hover effects
        play_again_hover = play_again_img.copy()
        main_menu_hover = main_menu_img.copy()
        change_name_hover = change_name_img.copy()
        play_again_hover.fill((200, 200, 200, 50), special_flags=pygame.BLEND_RGBA_MULT)
        main_menu_hover.fill((200, 200, 200, 50), special_flags=pygame.BLEND_RGBA_MULT)
        change_name_hover.fill((200, 200, 200, 50), special_flags=pygame.BLEND_RGBA_MULT)

        # Positions
        play_again_rect = play_again_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        main_menu_rect = main_menu_img.get_rect(center=(WIDTH // 2, play_again_rect.bottom + 20))
        change_name_rect = change_name_img.get_rect(center=(WIDTH // 2, main_menu_rect.bottom + 20))

        game_over_font = pygame.font.SysFont("Arial", 48, bold=True)

        waiting = True
        while waiting:
            screen.blit(bg_surfaces[current_bg_index], (0, 0))
            screen.blit(player_img, player_rect)

            for plat in platforms:
                screen.blit(platform_img, plat) if use_platform_image else pygame.draw.rect(screen, (0, 255, 0), plat)
            for coin in coins:
                screen.blit(coin_img, coin) if use_coin_image else pygame.draw.circle(screen, (255, 215, 0),
                                                                                      coin.center, COIN_SIZE // 2)

            if score_label_img:
                screen.blit(score_label_img, (10, 5))
            if coin_ui_img:
                screen.blit(coin_ui_img, (10, 60))

            screen.blit(score_font.render(f"{score}", True, SCORE_COLOR), (150, 10))
            screen.blit(score_font.render(f"{coins_collected}", True, SCORE_COLOR), (150, 65))
            screen.blit(FONT.render(f"Player: {player_name}", True, (255, 255, 255)), (WIDTH - 160, 10))

            game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))

            mouse_pos = pygame.mouse.get_pos()

            if play_again_rect.collidepoint(mouse_pos):
                screen.blit(play_again_hover, play_again_rect.topleft)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                screen.blit(play_again_img, play_again_rect.topleft)

            if main_menu_rect.collidepoint(mouse_pos):
                screen.blit(main_menu_hover, main_menu_rect.topleft)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                screen.blit(main_menu_img, main_menu_rect.topleft)

            if change_name_rect.collidepoint(mouse_pos):
                screen.blit(change_name_hover, change_name_rect.topleft)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                screen.blit(change_name_img, change_name_rect.topleft)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(event.pos):
                        if restart_sound:
                            restart_sound.play()
                        pygame.time.delay(300)
                        reset_game()
                        waiting = False
                    elif main_menu_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()  # 🔇 Stop background music
                        pygame.time.delay(300)
                        reset_game()
                        main_menu()
                        waiting = False
                    elif change_name_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()  # 🔇 Stop background music
                        player_name = name_input_screen()
                        reset_game()
                        waiting = False

            pygame.display.flip()
            clock.tick(60)

    # Draw everything
    screen.blit(player_img, player_rect)
    for plat in platforms:
        if use_platform_image and platform_img:
            screen.blit(platform_img, plat)
        else:
            pygame.draw.rect(screen, (0, 255, 0), plat)

    for coin in coins:
        if use_coin_image and coin_img:
            screen.blit(coin_img, coin)
        else:
            pygame.draw.circle(screen, (255, 215, 0), coin.center, COIN_SIZE // 2)

    if score_label_img:
        screen.blit(score_label_img, (10, 5))
    if coin_ui_img:
        screen.blit(coin_ui_img, (10, 60))

    screen.blit(score_font.render(f"{score}", True, SCORE_COLOR), (150, 10))
    screen.blit(score_font.render(f"{coins_collected}", True, SCORE_COLOR), (150, 65))
    name_surface = FONT.render(f"Player: {player_name}", True, (255, 255, 255))
    screen.blit(name_surface, (WIDTH - name_surface.get_width() - 10, 10))

    pygame.display.flip()
