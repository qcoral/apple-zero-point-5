import pygame
import random
import time
import sys
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

font = pygame.font.Font("C:/Users/Josh/Code/funkyterminal/Glass_TTY_VT220.ttf", 18)
font_big = pygame.font.SysFont("C:/Users/Josh/Code/funkyterminal/Glass_TTY_VT220.ttf", 32)

input = ""
output_lines = []
cursor_visible = True
cursor_timer = 0
command_history = []
history_index = -1

matrix_mode = {"active": False, "columns": None}
rickroll_mode = False
zelda_mode = False
party_mode = False
ascii_art_mode = False
secret_count = 0


MATRIX_CHARS = "01"
ZELDA_ART = [
    "   ▲   ",
    "  ▲ ▲  ",
    " ▲   ▲ ",
    "▲     ▲",
    "ZELDA!"
]

def print_output(text, color=WHITE):
    if isinstance(text, list):
        output_lines.extend([(line, color) for line in text])
    else:
        output_lines.append((text, color))
    if len(output_lines) > 20:
        del output_lines[:len(output_lines)-20]

def execute_command(command):
    global matrix_mode
    
    command = command.strip().lower()
    words = command.split()
    
    if not words:
        return
    
    cmd = words[0]
    args = words[1:]
    
    if cmd == "help":
        print_output([
            "Available commands:",
            "help - Show this message",
            "clear - Clear the screen",
            "echo - repeat text",
            "time - show current time",
            "date - show current date",
            "matrix - enter the Matrix",
            "zelda - It's dangerous to go alone",
            "exit - close the terminal",
            "neofetch - system info",
            "sudo - Super User Do",
            "rps - Rock, Paper, Scissors",
        ], GREEN)
        
    
    elif cmd == "clear":
        output_lines.clear()
    
    elif cmd == "echo":
        print_output(' '.join(args))
    
    elif cmd == "time":
        print_output(time.strftime("%H:%M:%S"))
    
    elif cmd == "date":
        print_output(time.strftime("%Y-%m-%d"))
    
    elif cmd == "matrix":
        matrix_mode["active"] = not matrix_mode["active"]
        if not matrix_mode["active"]:
            matrix_mode["columns"] = None
        print_output("You chose the red pill..." if matrix_mode["active"] else "Exiting Matrix mode", GREEN)
        
    elif cmd == "rps":
        try:
            Uinput = args[0].lower()
        except IndexError:
            print_output("Please include 'r', 'p', or 's'", RED)
            return
        TerminalInput = random.choice(['r', 'p', 's'])
        print_output(f"The computer chose: {TerminalInput}", YELLOW)
        if Uinput == TerminalInput:
            print_output("It's a tie!", WHITE)
        elif (Uinput == 'r' and TerminalInput == 's') or \
             (Uinput == 'p' and TerminalInput == 'r') or \
             (Uinput == 's' and TerminalInput == 'p'):
            print_output("You win!", GREEN)
        else:
            print_output("You lose!", RED)
        
    elif cmd == "guessthenumber":
        print_output("Guess the number between 1 and 100", YELLOW)
        Rnumber = random.randint(1, 100)
        attempts = 0
        while True:
            print_output("Enter your guess:", YELLOW)
            try:
                Uguess = int(input)
                attempts += 1
                if Uguess < Rnumber:
                    print_output("Too low!", WHITE)
                elif Uguess > Rnumber:
                    print_output("Too high!", WHITE)
                else:
                    print_output(f"Congratulations! You guessed the number {Rnumber} in {attempts} attempts.", GREEN)
                    break
            except ValueError:
                print_output("Please enter a valid number.", RED)

    elif cmd == "zelda":
        print_output(ZELDA_ART, YELLOW)
    
    
    elif cmd == "exit":
        pygame.quit()
        sys.exit()
    
    elif cmd == "neofetch":
        print_output([
            "H   H",
            "H   H    HQ OS v3.14",
            "H   H",
            "HHHHH    CPU: Python 3.x",
            "H   H    MEMORY: 512MB",
            "H   H    STORAGE: 5GB",
            "H   H"
        ], GREEN)
    elif cmd == "sudo":
        print_output("I'm sorry, Dave. I'm afraid I can't do that.", RED)



def initialize_terminal():
    messages = [
        "Welcome!",
        "Initializing HQ OS...",
        "HQ OS Terminal [Version 3.14]",
        "Type 'help' for available commands"
    ]
    
    for text in messages:
        print_output(text, GREEN)
        screen.fill(BLACK)
        y_pos = 10
        for line, color in output_lines[-20:]:
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (10, y_pos))
            y_pos += 20
        pygame.display.flip()
        time.sleep(1)

initialize_terminal()

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print_output(f"> {input}", GREEN)
                execute_command(input)
                command_history.append(input)
                history_index = len(command_history)
                input = ""
            
            elif event.key == pygame.K_BACKSPACE:
                input = input[:-1]
            
            elif event.key == pygame.K_UP:
                if command_history and history_index > 0:
                    history_index -= 1
                    input = command_history[history_index]
            
            elif event.key == pygame.K_DOWN:
                if command_history and history_index < len(command_history) - 1:
                    history_index += 1
                    input = command_history[history_index]
                elif command_history and history_index == len(command_history) - 1:
                    history_index = len(command_history)
                    input = ""
            
            else:
                input += event.unicode

    cursor_timer += dt
    if cursor_timer >= 0.5:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    if matrix_mode["active"]:
        if matrix_mode["columns"] is None:
            matrix_mode["columns"] = [random.randint(-HEIGHT, 0) for _ in range(WIDTH // 10)]
        for i in range(len(matrix_mode["columns"])):
            x = i * 10
            matrix_mode["columns"][i] += 10
            if matrix_mode["columns"][i] > HEIGHT:
                matrix_mode["columns"][i] = random.randint(-HEIGHT, 0)
            y = matrix_mode["columns"][i]
            char = random.choice(MATRIX_CHARS)
            color = (0, random.randint(100, 255), 0)
            text_surface = font.render(char, True, color)
            screen.blit(text_surface, (x, y))
            text_surface = font.render(char, True, color)
            screen.blit(text_surface, (x, y))

    y_pos = 10
    for line, color in output_lines[-20:]:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (10, y_pos))
        y_pos += 20

    prompt = "> " + input
    text_surface = font.render(prompt, True, GREEN)
    screen.blit(text_surface, (10, HEIGHT - 30))

    if cursor_visible:
        cursor_x = 10 + font.size(prompt)[0]
        pygame.draw.rect(screen, GREEN, (cursor_x, HEIGHT - 30, 10, 20))
    
    pygame.display.flip()
    screen.fill(BLACK)

pygame.quit()