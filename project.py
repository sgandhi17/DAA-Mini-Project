import tkinter as tk
from collections import deque
import random

class SnakeGame:
    def _init_(self, master):
        self.master = master
        self.master.title('Snake Game')

        # Game canvas
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg='black')
        self.canvas.pack()

        # Score label, positioned at the top right corner
        self.score_label = tk.Label(self.master, text="Score: 0", font=('Helvetica', 14))
        self.score_label.place(x=300, y=10)

        # Control buttons with changed colors
        self.restart_button = tk.Button(self.master, text="Restart", bg='blue', fg='white', command=self.restart_game)
        self.restart_button.pack(side='left')

        self.pause_button = tk.Button(self.master, text="Pause", bg='red', fg='white', command=self.toggle_pause)
        self.pause_button.pack(side='right')

        self.color_button = tk.Button(self.master, text="Change Color", bg='green', fg='white', command=self.change_color)
        self.color_button.pack(side='bottom')

        self.snake = deque([(20, 20), (20, 30), (20, 40)])
        self.food = self.random_food_position()
        self.direction = 'Down'
        self.score = 0
        self.paused = False
        self.snake_color = 'green'
        self.initial_speed = 100  # Initial speed in milliseconds
        self.speed = self.initial_speed

        self.game_running = True
        self.draw_snake()
        self.place_food()
        self.master.bind("<KeyPress>", self.change_direction)
        
        self.run_game()

    def run_game(self):
        if self.game_running and not self.paused:
            self.move_snake()
            self.check_collisions()
        self.master.after(self.speed, self.run_game)

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in list(self.snake)[:-1]:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0]+10, segment[1]+10, fill=self.snake_color, tag="snake")
        
        # Draw the snake head in a different color
        head_x, head_y = self.snake[-1]
        self.canvas.create_rectangle(head_x, head_y, head_x+10, head_y+10, fill='blue', tag="snake")

    def place_food(self):
        self.canvas.delete("food")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0]+10, self.food[1]+10, fill='red', tag="food")

    def random_food_position(self):
        return (random.randint(0, 39) * 10, random.randint(0, 39) * 10)

    def move_snake(self):
        head_x, head_y = self.snake[-1]
        if self.direction == 'Up':
            new_head = (head_x, head_y - 10)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 10)
        elif self.direction == 'Left':
            new_head = (head_x - 10, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 10,head_y)
        
        self.snake.append(new_head)
        if new_head == self.food:
            self.food = self.random_food_position()
            self.score += 1
            self.speed = max(10, self.speed - 5)  # Increase speed, but not too fast
            self.score_label.config(text=f"Score: {self.score}")
            self.place_food()
        else:
            self.snake.popleft()
        
        self.draw_snake()

    def change_direction(self, event):
        new_direction = event.keysym
        valid_directions = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if new_direction in valid_directions and valid_directions[new_direction] != self.direction:
            self.direction = new_direction

    def check_collisions(self):
        head_x, head_y = self.snake[-1]
        if head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400:
            self.game_over()
        
        # Check if the snake collides with itself
        for segment in list(self.snake)[:-1]:
            if segment == (head_x, head_y):
                self.game_over()
                
    def game_over(self):
        self.game_running = False
        self.pause_button.config(state='disabled')
        self.canvas.create_text(200, 200, text="Game Over", fill="white", font=('Helvetica', 24))

    def restart_game(self):
        # Reset the game state, including speed
        self.snake = deque([(20, 20), (20, 30), (20, 40)])
        self.food = self.random_food_position()
        self.direction = 'Down'
        self.score = 0
        self.initial_speed = 100
        self.speed = self.initial_speed  # Ensure the speed starts from the initial pace
        self.score_label.config(text="Score: 0")
        self.snake_color = 'green'
        self.game_running = True
        self.paused = False
        self.pause_button.config(state='normal')
        self.canvas.delete("all")
        self.draw_snake()
        self.place_food()
        self.run_game()

    def toggle_pause(self):
        if not self.game_running:
            return
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")

    def change_color(self):
        colors = ['green', 'yellow', 'purple', 'orange']
        current_color_index = colors.index(self.snake_color)
        new_color_index = (current_color_index + 1) % len(colors)
        self.snake_color = colors[new_color_index]
        self.draw_snake()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()