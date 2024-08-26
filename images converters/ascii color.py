import pygame as pg
import numpy as np
import cv2
from image_converter import ImageConverter

class ASCIIColorConverter(ImageConverter):
    def __init__(self, font_size = 10, color_lvl = 8):
        super().__init__()

        pg.display.set_caption(f"ASCII Color Converter - {self.path}")

        self.COLOR_LVL = color_lvl
        self.ASCII_CHARS = 'ixzao*#MW&8%B@$'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.SysFont('Courier', font_size, bold = True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

        # Need to be repeated here because this type of converter needs both the color and gray image
        self.color_image, self.gray_image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.color_image.shape[0], self.color_image.shape[1]
        self.surface = pg.display.set_mode(self.RES)

        self.draw()

    def draw_converted_image(self):
        char_indices = self.gray_image // self.ASCII_COEFF
        color_indices = self.color_image // self.COLOR_COEFF
        
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[x, y]
                if char_index:
                    char = self.ASCII_CHARS[char_index]
                    color = tuple(color_indices[x, y])
                    self.surface.blit(self.PALETTE[char][color], (x, y))

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True) # Create a list with all the possible RGB values
        color_palette = np.array([[r, g, b] for r in colors for g in colors for b in colors]) # Create a 3D array with all the possible RGB values
        palette = dict.fromkeys(self.ASCII_CHARS, None) # Create a dictionary with the ASCII characters as keys and None as values
        color_coeff = int(color_coeff) # Get the color coefficient
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                char_palette[color_key] = self.font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_img = cv2.transpose(self.cv2_image)
        color_image = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2GRAY)
        return color_image, gray_image

if __name__ == "__main__":
    converter = ASCIIColorConverter()
    converter.run()