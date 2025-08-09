import tkinter as tk
import random

# Game settings
WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 20
SPEED = 100  # milliseconds

# Colors
BG_COLOR = "honeydew"
SNAKE_COLOR = "olivedrab"
FOOD_COLOR = "tomato"
TEXT_COLOR = "saddlebrown"

# Directions
DIRECTIONS = {
    "Up": (0, -SNAKE_SIZE),
    "Down": (0, SNAKE_SIZE),
    "Left": (-SNAKE_SIZE, 0),
    "Right": (SNAKE_SIZE, 0)
}

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game 🐍")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        self.root.bind("<Key>", self.change_direction)
        self.setup_game()

    def setup_game(self):
        self.running = False
        self.direction = None
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.score = 0

        self.canvas.delete("all")
        self.squares = []

        # Score text
        self.score_text = self.canvas.create_text(WIDTH // 2, 20, text=f"Score: {self.score}",
                                                  font=("Arial", 14), fill=TEXT_COLOR)

        # Food
        self.food = self.random_food()
        self.food_item = self.canvas.create_oval(
            self.food[0], self.food[1],
            self.food[0] + SNAKE_SIZE, self.food[1] + SNAKE_SIZE,
            fill=FOOD_COLOR
        )

        # Snake
        for x, y in self.snake:
            square = self.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE,
                                                  fill=SNAKE_COLOR)
            self.squares.append(square)

        # Instruction
        self.start_text = self.canvas.create_text(WIDTH // 2, HEIGHT // 2,
                                                  text="Press an arrow key to start",
                                                  font=("Arial", 16), fill=TEXT_COLOR)

    def change_direction(self, event):
        key = event.keysym
        if key in DIRECTIONS:
            # Prevent reverse movement
            if self.direction:
                opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
                if key == opposite.get(self.direction):
                    return
            self.direction = key

            if not self.running:
                self.running = True
                self.canvas.delete(self.start_text)
                self.move_snake()

    def move_snake(self):
        if not self.running or not self.direction:
            return

        dx, dy = DIRECTIONS[self.direction]
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        # Check collision
        if (new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            self.end_game()
            return

        self.snake.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            self.food = self.random_food()
            self.canvas.coords(self.food_item,
                               self.food[0], self.food[1],
                               self.food[0] + SNAKE_SIZE, self.food[1] + SNAKE_SIZE)
        else:
            self.snake.pop()

        # Redraw snake
        for square in self.squares:
            self.canvas.delete(square)
        self.squares = []
        for x, y in self.snake:
            square = self.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE,
                                                  fill=SNAKE_COLOR)
            self.squares.append(square)

        self.root.after(SPEED, self.move_snake)

    def random_food(self):
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        return (x, y)

    def end_game(self):
        self.running = False
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 30,
                                text="Game Over!", font=("Arial", 24, "bold"), fill=TEXT_COLOR)
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2,
                                text=f"Final Score: {self.score}", font=("Arial", 16), fill=TEXT_COLOR)

        # Buttons
        play_btn = tk.Button(self.root, text="Play Again", font=("Arial", 12),
                             command=self.setup_game, bg="lightgreen")
        quit_btn = tk.Button(self.root, text="Quit", font=("Arial", 12),
                             command=self.root.quit, bg="salmon", fg="white")
        self.canvas.create_window(WIDTH // 2 - 60, HEIGHT // 2 + 40, window=play_btn)
        self.canvas.create_window(WIDTH // 2 + 60, HEIGHT // 2 + 40, window=quit_btn)

# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

