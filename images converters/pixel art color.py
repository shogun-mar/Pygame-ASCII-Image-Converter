import pygame as pg
import pygame.gfxdraw
import numpy as np
import cv2
from image_converter import ImageConverter

class ColorPixelArtConverter(ImageConverter):
    def __init__(self, color_lvl = 8, pixel_size = 8):
        super().__init__()

        self.PIXEL_SIZE = pixel_size
        pg.display.set_caption(f"ASCII Color Converter - {self.path}")
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

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_img = cv2.transpose(self.cv2_image)
        color_image = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2RGB)
        return color_image

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True) # Create a list with all the possible RGB values
        color_palette = np.array([[r, g, b] for r in colors for g in colors for b in colors]) # Create a 3D array with all the possible RGB values
        palette = {}
        color_coeff = int(color_coeff) # Get the color coefficient
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color

        return palette, color_coeff

if __name__ == "__main__":
    converter = ColorPixelArtConverter()
    converter.run()