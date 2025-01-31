import tkinter as tk
from tkinter import messagebox
import random
import json

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Snake Game")
        self.master.geometry("600x600")
        self.master.resizable(False, False)
        
        # Game configuration
        self.width = 500
        self.height = 400
        self.cell_size = 20
        self.speed = 100
        self.high_score = 0
        self.load_high_score()
        
        # Colors
        self.bg_color = "#2E2E2E"
        self.snake_color = "#4CAF50"
        self.food_color = "#FF5252"
        self.text_color = "#FFFFFF"
        
        # Create start screen
        self.create_start_screen()
        
    def load_high_score(self):
        try:
            with open("highscore.json", "r") as f:
                self.high_score = json.load(f).get("high_score", 0)
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        with open("highscore.json", "w") as f:
            json.dump({"high_score": self.high_score}, f)

    def create_start_screen(self):
        self.start_frame = tk.Frame(self.master, bg=self.bg_color)
        self.start_frame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(self.start_frame, text="SNAKE GAME", font=("Arial", 32, "bold"), 
                        bg=self.bg_color, fg=self.text_color)
        title.pack(pady=50)
        
        speed_frame = tk.Frame(self.start_frame, bg=self.bg_color)
        speed_frame.pack(pady=30)
        
        tk.Button(speed_frame, text="Normal Speed", font=("Arial", 14), width=15,
                 command=lambda: self.start_game(150), bg="#2196F3", fg="white").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(speed_frame, text="Medium Speed", font=("Arial", 14), width=15,
                 command=lambda: self.start_game(100), bg="#FF9800", fg="white").grid(row=0, column=1, padx=10, pady=10)
        tk.Button(speed_frame, text="High Speed", font=("Arial", 14), width=15,
                 command=lambda: self.start_game(60), bg="#E91E63", fg="white").grid(row=0, column=2, padx=10, pady=10)
        
        high_score_label = tk.Label(self.start_frame, text=f"High Score: {self.high_score}", 
                                   font=("Arial", 14), bg=self.bg_color, fg=self.text_color)
        high_score_label.pack(pady=20)
        
        self.master.bind("<Return>", lambda e: self.start_game(150))

    def start_game(self, speed):
        self.speed = speed
        self.start_frame.pack_forget()
        self.initialize_game()
        
    def initialize_game(self):
        # Game variables
        self.direction = "Right"
        self.snake = [(10, 10), (10, 9), (10, 8)]
        self.food = None
        self.score = 0
        self.game_over = False
        
        # Create game canvas
        self.game_frame = tk.Frame(self.master, bg=self.bg_color)
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.game_frame, width=self.width, height=self.height, 
                               bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Score display
        self.score_label = tk.Label(self.game_frame, text=f"Score: {self.score}   High Score: {self.high_score}", 
                                   font=("Arial", 14), bg=self.bg_color, fg=self.text_color)
        self.score_label.pack()
        
        # Generate first food
        self.create_food()
        self.draw()
        
        # Controls
        self.master.bind("<KeyPress>", self.change_direction)
        self.master.bind("<space>", self.restart_game)
        
        self.run_game()

    def create_food(self):
        while True:
            x = random.randint(0, (self.width//self.cell_size)-1)
            y = random.randint(0, (self.height//self.cell_size)-1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def draw(self):
        self.canvas.delete(tk.ALL)
        
        # Draw snake
        for x, y in self.snake:
            self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size,
                                        (x+1)*self.cell_size, (y+1)*self.cell_size,
                                        fill=self.snake_color, outline="")
        
        # Draw food
        if self.food:
            x, y = self.food
            self.canvas.create_oval(x*self.cell_size, y*self.cell_size,
                                   (x+1)*self.cell_size, (y+1)*self.cell_size,
                                   fill=self.food_color, outline="")

    def move(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        
        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 1, head_y)
        
        # Check collision with walls
        if (new_head[0] < 0 or new_head[0] >= self.width//self.cell_size or
            new_head[1] < 0 or new_head[1] >= self.height//self.cell_size):
            self.game_over = True
        
        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
        
        if not self.game_over:
            self.snake.insert(0, new_head)
            
            # Check if food is eaten
            if new_head == self.food:
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                self.score_label.config(text=f"Score: {self.score}   High Score: {self.high_score}")
                self.create_food()
            else:
                self.snake.pop()
            
            self.draw()
        else:
            self.show_game_over()

    def run_game(self):
        if not self.game_over:
            self.move()
            self.master.after(self.speed, self.run_game)

    def change_direction(self, event):
        key = event.keysym
        if (key == "Up" and self.direction != "Down" or
            key == "Down" and self.direction != "Up" or
            key == "Left" and self.direction != "Right" or
            key == "Right" and self.direction != "Left"):
            self.direction = key

    def show_game_over(self):
        self.canvas.create_text(self.width/2, self.height/2, text="GAME OVER", 
                               font=("Arial", 32, "bold"), fill=self.text_color)
        self.canvas.create_text(self.width/2, self.height/2 + 40, 
                               text="Press SPACE to restart or ESC to quit",
                               font=("Arial", 14), fill=self.text_color)
        self.master.bind("<Escape>", self.return_to_menu)

    def restart_game(self, event=None):
        self.game_frame.pack_forget()
        self.initialize_game()

    def return_to_menu(self, event=None):
        self.game_frame.pack_forget()
        self.create_start_screen()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()