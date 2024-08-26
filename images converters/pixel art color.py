import pygame as pg
import pygame.gfxdraw
import numpy as np
import cv2
from tkinter import filedialog

class Converter:
    def __init__(self, color_lvl = 8, pixel_size = 8):
        self.path = filedialog.askopenfilename()
        
        if not self.path or not self.path.endswith(('.png', '.jpg', '.jpeg')):
            raise ValueError("Please select a valid file.")

        pg.init()
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.PIXEL_SIZE = pixel_size
        self.surface = pg.display.set_mode(self.RES)
        pg.display.set_caption(f"ASCII Color Converter - {self.path}")
        self.clock = pg.time.Clock()
        self.COLOR_LVL = color_lvl

        self.PALETTE, self.COLOR_COEFF = self.create_palette()

        self.draw()

    def draw_converted_image(self):
        color_indices = self.image // self.COLOR_COEFF
        
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                color = tuple(color_indices[x, y])
                if sum(color):
                    color = self.PALETTE[color]
                    pygame.gfxdraw.box(self.surface, (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE), color)

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True) # Create a list with all the possible RGB values
        color_palette = np.array([[r, g, b] for r in colors for g in colors for b in colors]) # Create a 3D array with all the possible RGB values
        palette = {}
        color_coeff = int(color_coeff) # Get the color coefficient
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color

        return palette, color_coeff

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_img = cv2.transpose(self.cv2_image)
        color_image = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2RGB)
        return color_image
    
    def draw_cv2_image(self): # Resize the cv2 image so it fits the screen
        resized_cv2_image = cv2.resize(self.cv2_image, (480, 720), interpolation = cv2.INTER_AREA)
        cv2.imshow("img", resized_cv2_image)

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()

    def save_image(self):
        # Save the Pygame surface directly to an image file
        pg.image.save(self.surface, filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]))

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    quit()

                if event.type == pg.KEYDOWN:
                    self.save_image()
            
            pg.display.flip()
            self.clock.tick()

if __name__ == "__main__":
    Converter().run()