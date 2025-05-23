import pygame
import sys
import random

# --- Game Setup ---
pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Dev Simulation")
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

# --- Game State ---
money = 1000
time_days = 0
main_message = "Welcome to Game Dev Simulation!"
user_input = ""
awaiting_name = False
pending_dev_type = None

game_costs = {"small": 100, "medium": 500, "big": 1000}
game_times = {"small": 30, "medium": 60, "big": 120}
game_days = {"small": 7, "medium": 21, "big": 60}

# Development state
developing = False
dev_type = None
dev_name = ""
dev_end_time = 0

# Graph state
show_graph = False
graph_update_interval = 10  
graph_total_time = 60 
graph_last_update = 0
buyers = 0
buyers_history = []
buyers_max = 0

def set_main_message(message):
    global main_message
    main_message = message

def process_command(cmd):
    global money, time_days, developing, dev_type, dev_end_time, awaiting_name, pending_dev_type
    cmd = cmd.strip()
    if developing or awaiting_name or show_graph:
        set_main_message("Wait until the current process is finished.")
        return
    if cmd.lower().startswith("develop"):
        parts = cmd.lower().split()
        if len(parts) != 2 or parts[1] not in game_costs:
            set_main_message("Usage: develop small | medium | big")
            return
        size = parts[1]
        cost = game_costs[size]
        if money < cost:
            set_main_message(f"Not enough money for a {size} game! Need {cost}, have {money}.")
            return
        pending_dev_type = size
        set_main_message("What do you want to name your game?")
        awaiting_name = True
    elif cmd.lower() == "status":
        set_main_message(f"Money: {money} | Days: {time_days}")
    elif cmd.lower() == "help":
        set_main_message("Commands: develop [small|medium|big], status, help, quit")
    elif cmd.lower() == "quit":
        pygame.quit()
        sys.exit()
    else:
        set_main_message("Unknown command. Type 'help' for options.")

def start_development(name, size):
    global money, developing, dev_type, dev_name, dev_end_time, buyers, buyers_history, buyers_max, show_graph, graph_last_update, time_days, awaiting_name, pending_dev_type
    cost = game_costs[size]
    money -= cost
    developing = True
    dev_type = size
    dev_name = name
    dev_end_time = pygame.time.get_ticks() + game_times[size] * 1000  
    set_main_message(f"Started developing '{dev_name}' ({dev_type})! It will take {game_times[size]} seconds.")
    # Prepare graph
    show_graph = False
    buyers = -cost
    buyers_history = [buyers]
    buyers_max = 0
    graph_last_update = pygame.time.get_ticks()
    awaiting_name = False
    pending_dev_type = None

def finish_development():
    global developing, dev_type, time_days, show_graph, graph_last_update
    days = game_days[dev_type]
    time_days += days
    set_main_message(f"Development finished for '{dev_name}'! Now tracking sales for 60 seconds...")
    developing = False
    show_graph = True
    graph_last_update = pygame.time.get_ticks()

def update_graph():
    global buyers, buyers_history, buyers_max, show_graph, graph_last_update, money
    increase = random.randint(1, 20)
    buyers += increase
    buyers_history.append(buyers)
    buyers_max = max(buyers_max, buyers)
    if len(buyers_history) > graph_total_time // graph_update_interval + 1:
        show_graph = False
        set_main_message(f"Sales tracking finished for '{dev_name}'. Final buyers: {buyers}")
        money += max(0, buyers)

def draw_main_message(surface, message, font, color=(255,255,255)):
    lines = []
    while len(message) > 60:
        idx = message.rfind(' ', 0, 60)
        if idx == -1: idx = 60
        lines.append(message[:idx])
        message = message[idx+1:]
    lines.append(message)
    y = 30
    for line in lines:
        text_surf = font.render(line, True, color)
        surface.blit(text_surf, (20, y))
        y += font.get_height() + 2

def draw_graph(surface, buyers_history):
    graph_x = 500
    graph_y = 100
    graph_w = 350
    graph_h = 300
    pygame.draw.rect(surface, (200,200,200), (graph_x-2, graph_y-2, graph_w+4, graph_h+4), 2)
    min_b = min(buyers_history)
    max_b = max(buyers_history)
    if max_b == min_b:
        max_b += 1  
    steps = len(buyers_history)-1
    if steps == 0:
        steps = 1
    prev_px = prev_py = None
    for i, b in enumerate(buyers_history):
        px = graph_x + int(i * graph_w / steps)
        py = graph_y + graph_h - int((b - min_b) * graph_h / (max_b - min_b))
        if prev_px is not None:
            pygame.draw.line(surface, (0,255,0), (prev_px, prev_py), (px, py), 3)
        prev_px, prev_py = px, py
    label_font = pygame.font.Font(None, 24)
    min_label = label_font.render(str(min_b), True, (255,255,255))
    max_label = label_font.render(str(max_b), True, (255,255,255))
    surface.blit(min_label, (graph_x-40, graph_y+graph_h-10))
    surface.blit(max_label, (graph_x-40, graph_y-10))
    title = label_font.render(f"Sales for '{dev_name}'", True, (0,255,255))
    surface.blit(title, (graph_x, graph_y-30))

# --- Main Loop ---
running = True
while running:
    screen.fill((30, 30, 30))
    draw_main_message(screen, main_message, font)
    if awaiting_name:
        prompt = "Game Name: " + user_input + "|"
    else:
        prompt = "Command: " + user_input + "|"
    prompt_surf = font.render(prompt, True, (0,255,0))
    screen.blit(prompt_surf, (20, HEIGHT - 40))
    status = f"Money: {money}   Days: {time_days}"
    status_surf = font.render(status, True, (255,255,0))
    screen.blit(status_surf, (WIDTH - 350, HEIGHT - 40))

    if developing:
        time_left = max(0, (dev_end_time - pygame.time.get_ticks()) // 1000)
        dev_msg = f"Developing '{dev_name}' ({dev_type}): {time_left} seconds left"
        dev_surf = font.render(dev_msg, True, (0,200,255))
        screen.blit(dev_surf, (20, HEIGHT - 80))
        if time_left == 0:
            finish_development()

    if show_graph:
        draw_graph(screen, buyers_history)
        now = pygame.time.get_ticks()
        elapsed = (now - graph_last_update) / 1000

        if elapsed >= graph_update_interval:
            update_graph()
            graph_last_update = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_RETURN:
                if awaiting_name:
                    if user_input.strip():
                        start_development(user_input.strip(), pending_dev_type)
                        user_input = ""
                elif not developing and not show_graph:
                    process_command(user_input)
                    user_input = ""
            else:
                if event.unicode.isprintable():
                    user_input += event.unicode

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
