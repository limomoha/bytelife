import pygame
import sys
import time
import base64
import json
import pyperclip
import random
import copy # For deep copying attributes
from ByteLife import LifeEngineNone
# --- CONFIG ---
icon_image = pygame.image.load("costume1.png")
pygame.display.set_icon(icon_image)
WIDTH, HEIGHT = 1100, 750
SIDEBAR_WIDTH = 320
CONSOLE_HEIGHT = 200
FPS = 30
console_scroll = 0
friends_scroll = 0
SCROLL_SPEED = 20

# Colors
BG, SIDEBAR, CONSOLE_BG = (240, 240, 240), (30, 30, 35), (10, 10, 10)
TEXT_G, GOLD, WHITE, MODAL_BG = (0, 255, 65), (218, 165, 32), (255, 255, 255), (45, 45, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("ByteLife")
font = pygame.font.SysFont("Courier", 16)
bold_f = pygame.font.SysFont("Arial", 20, bold=True)

# Engine Init (Triggers your secret 'random bob mcdonald' logic)
sim = LifeEngineNone("random bob mcdonald")

# --- GLOBAL STATE FOR COPYING ---
last_confirmed_action = None 
icon_image = icon_image.convert_alpha()
class ConfirmationModal:
    def __init__(self):
        self.active = False
        self.target_func = None
        self.action_name = ""
        # 1. Decide how big you want it
        new_width = 600
        new_height = 250 # Or whatever your height was

        # 2. Define the position from scratch
        # This centers it horizontally (WIDTH) and vertically (HEIGHT)
        x_pos = (WIDTH // 2) - (new_width // 2)
        y_pos = (HEIGHT // 2) - (new_height // 2)

        # 3. NOW create the rect
        self.rect = pygame.Rect(x_pos, y_pos, new_width, new_height)
        # Position buttons relative to the new wide rect
        btn_w, btn_h = 120, 50
        padding = 40

        # Left button
        self.yes_btn = pygame.Rect(self.rect.x + padding, 
                                    self.rect.y + self.rect.height - btn_h - 20, 
                                    btn_w, btn_h)

        # Right button (calculates position based on the new width)
        self.no_btn = pygame.Rect(self.rect.right - btn_w - padding, 
                                self.rect.y + self.rect.height - btn_h - 20, 
                                btn_w, btn_h)

    def trigger(self, action_name, func):
        self.action_name = action_name
        self.target_func = func
        self.active = True

    def draw(self, surface):
        if not self.active: return
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0,0))

        # 1. Draw the wider background
        pygame.draw.rect(surface, MODAL_BG, self.rect, border_radius=15)
        pygame.draw.rect(surface, GOLD, self.rect, 3, border_radius=15)
        title_surf = bold_f.render("CONFIRM ACTION", True, GOLD)
        # Formula: (Rect X) + (Rect Width / 2) - (Text Width / 2)
        title_x = self.rect.x + (self.rect.width // 2) - (title_surf.get_width() // 2)
        surface.blit(title_surf, (title_x, self.rect.y + 20))

        # 3. Process Text (Now supports longer names since the box is wider)
        surface.blit(font.render(f"Process: {self.action_name[:43]}...", True, WHITE), (self.rect.x + 40, self.rect.y + 70))
        surface.blit(font.render("Focus resets if you switch buttons.", True, (150, 150, 150)), (self.rect.x + 40, self.rect.y + 100))

        # 4. Draw Buttons (Assuming they were moved in __init__)
        pygame.draw.rect(surface, (50, 180, 50), self.yes_btn, border_radius=8)
        pygame.draw.rect(surface, (180, 50, 50), self.no_btn, border_radius=8)

        # Center labels inside buttons
        surface.blit(bold_f.render("RUN", True, WHITE), (self.yes_btn.centerx - 20, self.yes_btn.y + 12))
        surface.blit(bold_f.render("EXIT", True, WHITE), (self.no_btn.centerx - 25, self.no_btn.y + 12))

    def check_click(self, pos):
        global last_confirmed_action
        if self.yes_btn.collidepoint(pos):
            last_confirmed_action = self.action_name
            self.target_func()
            self.active = False
            return True
        if self.no_btn.collidepoint(pos):
            self.active = False
            return True
        return False

class Button:
    def __init__(self, text, x, y, w, h, func):
        self.text, self.rect, self.func = text, pygame.Rect(x, y, w, h), func

    def draw(self, surface):
        is_focused = (self.text == last_confirmed_action)
        color = (180, 220, 255) if is_focused else (220, 220, 220)
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2 if not is_focused else 4, border_radius=5)
        
        display = self.text if len(self.text) < 18 else self.text[:15] + "..."
        txt_surf = font.render(display, True, (0, 0, 0))
        surface.blit(txt_surf, (self.rect.x + 15, self.rect.y + 12))

# --- SPECIAL SYSTEM FUNCTIONS ---
def clone_sim():
    global cloned_data
    try:
        # 1. Start with the full dictionary of attributes
        full_dict = sim.__dict__.copy()
        
        # 2. DELETE the stuff JSON can't handle (the functions and methods)
        # We also clear 'printed' to keep the save code short
        keys_to_remove = ['functions', 'printed']
        
        clean_dict = {k: v for k, v in full_dict.items() if k not in keys_to_remove}

        # 3. Stringify the CLEAN data only
        json_str = json.dumps(clean_dict)
        
        # 4. Scramble to Base64 and push to clipboard
        b64_str = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
        b64_str = base64.b64encode(b64_str.encode("utf-8")).decode("utf-8")
        pyperclip.copy(b64_str)
        
        sim.printed += "\n[SYSTEM] ATTRIBUTES SERIALIZED & COPIED!"
        print("Success! Your stats are in the clipboard.")

    except Exception as e:
        print(f"JSON Error: {e}")
        sim.printed += f"\n[ERROR] Serialization failed: {e}"


def restore_sim():
    global sim, last_confirmed_action
    try:
        # 1. Get from clipboard
        raw_data = pyperclip.paste()
        
        # 2. Base64 -> JSON String
        json_str = base64.b64decode(raw_data).decode("utf-8")
        json_str = base64.b64decode(json_str).decode("utf-8")
        
        # 3. JSON -> Dictionary
        data_dict = json.loads(json_str)
        
        # 4. UPDATE the existing sim object with new attributes
        # This keeps the class methods intact while changing the numbers/stats
        sim.__dict__.update(data_dict)
        
        # 5. Reset UI State
        last_confirmed_action = None
        sim.is_alive = True # Force resurrection
        sim.printed += "\n[SYSTEM] TIME REWOUND: DATA RESTORED FROM CLIPBOARD."
        
    except Exception as e:
        sim.printed += "\n[ERROR] Clipboard does not contain a valid Bob."

# Setup Action Buttons
buttons = []
modal = ConfirmationModal()
startX, startY = SIDEBAR_WIDTH + 20, 40
for i, (name, func) in enumerate(sim.functions.items()):
    col, row = i // 10, i % 10
    buttons.append(Button(name, startX + (col * 220), startY + (row * 50), 200, 40, func))

# System Buttons (Save/Load)
save_btn = Button("CREATE CLONE (BACKUP)", 20, 550, 280, 45, clone_sim)
load_btn = Button("RESTORE FROM CLONE", 20, 610, 280, 45, restore_sim)

# Trackers
last_money, current_age = sim.money, sim.age
show_summary, summary_timer, yearly_profit = False, 0, 0

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if modal.active:
                modal.check_click(event.pos)
            else:
                # 1. ALWAYS check System Buttons (Save/Load) even if dead
                if save_btn.rect.collidepoint(event.pos):
                    modal.trigger(save_btn.text, save_btn.func)
                elif load_btn.rect.collidepoint(event.pos):
                    modal.trigger(load_btn.text, load_btn.func)
                
                # 2. ONLY check Action Buttons if ALIVE
                elif sim.is_alive:
                    for b in buttons:
                        if b.rect.collidepoint(event.pos):
                            if b.text == last_confirmed_action:
                                b.func()
                            else:
                                modal.trigger(b.text, b.func)
        elif event.type == pygame.VIDEORESIZE:
            # Update the screen size with the new dimensions from the event
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            # You may also need to update game elements (e.g., scale surfaces, reposition objects) here


    # --- DRAWING ---
    # (Sidebars, Console, and Buttons as usual...)
    for b in buttons: b.draw(screen)
    save_btn.draw(screen)
    load_btn.draw(screen)

    # 3. The Death Screen should NOT cover the System Buttons
    if not sim.is_alive:
        # Create a smaller overlay or one that leaves the sidebar clear
        overlay = pygame.Surface((WIDTH - SIDEBAR_WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (SIDEBAR_WIDTH, 0)) # Only covers the action area
        
        death_txt = bold_f.render("GAME OVER - CHARACTER DECEASED", True, (255, 0, 0))
        hint_txt = font.render("Use 'RESTORE' in the sidebar to rewind time", True, WHITE)
        screen.blit(death_txt, (SIDEBAR_WIDTH + 150, HEIGHT // 2 - 20))
        screen.blit(hint_txt, (SIDEBAR_WIDTH + 170, HEIGHT // 2 + 20))

    modal.draw(screen) # Always draw modal on the very top

    # Detect Age Up
    if sim.age > current_age:
        yearly_profit = sim.money - last_money
        show_summary, summary_timer = True, pygame.time.get_ticks()
        current_age, last_money = sim.age, sim.money

    # Sidebar
    pygame.draw.rect(screen, SIDEBAR, (0, 0, SIDEBAR_WIDTH, HEIGHT))
    # 1. Start with your core stats
    stats = [
        f"ID: {sim.name.upper()}", 
        f"AGE: {sim.age}", 
        f"CASH: ${int(sim.money):,}", 
        f"HAPPY: {sim.happiness}%",
        "--- FRIENDS ---" # A header to separate them
    ]

    # 2. Add each friend as a NEW entry in the list
    # This forces them to be drawn on separate lines in your render loop
    for friend_name in list(sim.dictionary.keys()):
        stats.append(f"• {friend_name}")
    for i, s in enumerate(stats):
        screen.blit(bold_f.render(s, True, WHITE), (20, 40 + (i * 45)))
    
    # Draw System Buttons
    save_btn.draw(screen)
    load_btn.draw(screen)

    # Console
    c_rect = (SIDEBAR_WIDTH + 20, HEIGHT - CONSOLE_HEIGHT - 20, WIDTH - SIDEBAR_WIDTH - 40, CONSOLE_HEIGHT)
    pygame.draw.rect(screen, CONSOLE_BG, c_rect, border_radius=10)
    lines = sim.printed.split('\n')[-10:]
    for i, line in enumerate(lines):
        screen.blit(font.render(f"> {line}", True, TEXT_G), (c_rect[0] + 20, c_rect[1] + 20 + (i * 18)))

    # Action Buttons
    for b in buttons: b.draw(screen)
    modal.draw(screen)

    if show_summary:
        pop = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 60, 300, 120)
        pygame.draw.rect(screen, (40, 40, 45), pop, border_radius=15)
        p_color = (0, 255, 0) if yearly_profit >= 0 else (255, 0, 0)
        screen.blit(bold_f.render(f"YEAR RECAP", True, GOLD), (pop.x+80, pop.y+20))
        screen.blit(font.render(f"Net: ${int(yearly_profit):,}", True, p_color), (pop.x+80, pop.y+60))
        if pygame.time.get_ticks() - summary_timer > 1500: show_summary = False

    if not sim.is_alive:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((0,0,0,180))
        screen.blit(overlay, (0,0)); screen.blit(bold_f.render("GAME OVER", True, (255,0,0)), (WIDTH//2-50, HEIGHT//2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()