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
fans = 0
main_message = "Welcome to Game Dev Simulation!"
user_input = ""

# Input states
awaiting_name = False
awaiting_price = False
pending_dev_type = None
pending_dev_name = ""

game_costs = {"small": 100, "medium": 500, "big": 1000}
game_times = {"small": 30, "medium": 60, "big": 120} 
game_days = {"small": 7, "medium": 21, "big": 60}
price_ranges = {"small": (5, 50), "medium": (10, 100), "big": (20, 200)}

# Development state
developing = False
dev_type = None
dev_name = ""
dev_price = 0
dev_end_time = 0

# Graph/sales state
show_graph = False
graph_update_interval = 10 
graph_total_time = 60  
graph_last_update = 0
sales_start_time = 0
buyers = 0
buyers_history = []
buyers_max = 0

# Random event state
event_messages = [
    ("Your game was featured on a popular website! Sales spike!", 1.5, 0),
    ("A famous streamer played your game! Fans surge!", 1.3, 10),
    ("A bug was discovered in your game. Sales slow down.", 0.7, -5),
    ("A competitor released a similar game. Sales dip.", 0.8, -2),
    ("Your game received great reviews! Sales increase.", 1.2, 5),
]
last_event_time = 0
event_interval = 10 
current_event_msg = ""
event_display_time = 0  

def set_main_message(message):
    global main_message
    main_message = message

def process_command(cmd):
    global money, time_days, developing, dev_type, dev_end_time, awaiting_name, pending_dev_type, awaiting_price
    cmd = cmd.strip()
    if developing or awaiting_name or awaiting_price or show_graph:
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
        set_main_message(f"Money: {money} | Days: {time_days} | Fans: {fans}")
    elif cmd.lower() == "help":
        set_main_message("Commands: develop [small|medium|big], status, help, quit")
    elif cmd.lower() == "quit":
        pygame.quit()
        sys.exit()
    else:
        set_main_message("Unknown command. Type 'help' for options.")

def start_development(name, size, price):
    global money, developing, dev_type, dev_name, dev_price, dev_end_time
    global buyers, buyers_history, buyers_max, show_graph, graph_last_update
    cost = game_costs[size]
    money -= cost
    developing = True
    dev_type = size
    dev_name = name
    dev_price = price
    dev_end_time = pygame.time.get_ticks() + game_times[size] * 1000  # ms
    set_main_message(f"Started developing '{dev_name}' ({dev_type}) at ${dev_price}! It will take {game_times[size]} seconds.")
    show_graph = False
    buyers = -cost
    buyers_history = [buyers]
    buyers_max = 0
    graph_last_update = pygame.time.get_ticks()

def finish_development():
    global developing, dev_type, time_days, show_graph, graph_last_update, sales_start_time, last_event_time
    days = game_days[dev_type]
    time_days += days
    set_main_message(f"Development finished for '{dev_name}'! Now tracking sales for 60 seconds...")
    developing = False
    show_graph = True
    graph_last_update = pygame.time.get_ticks()
    sales_start_time = pygame.time.get_ticks()
    last_event_time = sales_start_time

def update_graph():
    global buyers, buyers_history, buyers_max, show_graph, graph_last_update, money, fans
    min_price, max_price = price_ranges[dev_type]
    if dev_price > 150:
        increase = 0 
    else:
        base = {"small": 20, "medium": 50, "big": 100}[dev_type]
        price_factor = max(0.1, 1.5 - ((dev_price - min_price) / (max_price - min_price)))
        fan_factor = 1 + (fans / 200)
        increase = int(random.randint(1, base) * price_factor * fan_factor)
    buyers += increase
    buyers_history.append(buyers)
    buyers_max = max(buyers_max, buyers)
    if len(buyers_history) > graph_total_time // graph_update_interval + 1:
        show_graph = False
        total_buyers = max(0, buyers)
        total_profit = total_buyers * dev_price
        set_main_message(f"Sales finished for '{dev_name}'. Buyers: {total_buyers}. Profit: ${total_profit}")
        money += total_profit
        if total_buyers > 0:
            gained = random.randint(5, 20) + total_buyers // 50
            fans_gained = min(gained, total_buyers // 2)
            fans += fans_gained
            set_main_message(main_message + f" | Gained {fans_gained} fans!")
        else:
            fans_lost = random.randint(0, 5)
            fans = max(0, fans - fans_lost)
            if fans_lost:
                set_main_message(main_message + f" | Lost {fans_lost} fans.")

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

def draw_graph(surface, buyers_history, time_left, event_msg=None):
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
    title = label_font.render(f"Sales for '{dev_name}' @ ${dev_price}", True, (0,255,255))
    surface.blit(title, (graph_x, graph_y-30))
    timer_text = label_font.render(f"Sales time left: {time_left}s", True, (255,255,255))
    surface.blit(timer_text, (graph_x, graph_y+graph_h+10))
    if event_msg:
        event_surf = label_font.render(event_msg, True, (255, 200, 0))
        surface.blit(event_surf, (graph_x, graph_y+graph_h+40))

# --- Main Loop ---
running = True
while running:
    screen.fill((30, 30, 30))
    draw_main_message(screen, main_message, font)
    if awaiting_name:
        prompt = "Game Name: " + user_input + "|"
    elif awaiting_price:
        minp, maxp = price_ranges[pending_dev_type]
        prompt = f"Set price for '{pending_dev_name}' (${minp}-{maxp}): {user_input}|"
    else:
        prompt = "Command: " + user_input + "|"
    prompt_surf = font.render(prompt, True, (0,255,0))
    screen.blit(prompt_surf, (20, HEIGHT - 40))
    status = f"Money: {money}   Days: {time_days}   Fans: {fans}"
    status_surf = font.render(status, True, (255,255,0))
    screen.blit(status_surf, (WIDTH - 400, HEIGHT - 40))
    if developing:
        time_left = max(0, (dev_end_time - pygame.time.get_ticks()) // 1000)
        dev_msg = f"Developing '{dev_name}' ({dev_type}): {time_left} seconds left"
        dev_surf = font.render(dev_msg, True, (0,200,255))
        screen.blit(dev_surf, (20, HEIGHT - 80))
        if time_left == 0:
            finish_development()

    if show_graph:
        now = pygame.time.get_ticks()
        sales_elapsed = (now - sales_start_time) // 1000
        time_left = max(0, graph_total_time - sales_elapsed)
        draw_graph(screen, buyers_history, time_left, current_event_msg if event_display_time > now else None)

        if now - last_event_time > event_interval * 1000 and time_left > 0:
            if random.random() < 0.5:  
                msg, sales_factor, fan_delta = random.choice(event_messages)
                current_event_msg = msg
                event_display_time = now + 4000  
                set_main_message(main_message + " | " + msg)

                if len(buyers_history) > 1:
                    delta = buyers_history[-1] - buyers_history[-2]
                    buyers_history[-1] += int(delta * (sales_factor - 1))
                    buyers = buyers_history[-1]
                    if fan_delta != 0:
                        fans = max(0, fans + fan_delta)
            last_event_time = now

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
                        pending_dev_name = user_input.strip()
                        set_main_message(f"Set a price for '{pending_dev_name}' (suggested range: ${price_ranges[pending_dev_type][0]}-${price_ranges[pending_dev_type][1]}):")
                        user_input = ""
                        awaiting_name = False
                        awaiting_price = True
                elif awaiting_price:
                    try:
                        price = int(user_input.strip())
                        minp, maxp = price_ranges[pending_dev_type]
                        if not (minp <= price <= maxp):
                            set_main_message(f"Price must be between ${minp} and ${maxp}.")
                        else:
                            start_development(pending_dev_name, pending_dev_type, price)
                            user_input = ""
                            awaiting_price = False
                    except ValueError:
                        set_main_message("Please enter a valid number for the price.")
                elif not developing and not show_graph:
                    process_command(user_input)
                    user_input = ""
            else:
                if event.unicode.isprintable():
                    user_input += event.unicode

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
