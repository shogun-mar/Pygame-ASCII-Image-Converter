import pygame as pg
import cv2
from video_converter import VideoConverter

class ASCIIGreyscaleConverter(VideoConverter):
    def __init__(self, font_size = 10):
        super().__init__()
        
        pg.display.set_caption(f"ASCII Greyscale Converter - {self.path}")

        self.ASCII_CHARS = '.",:;!~+-xmo*#W&8@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Courier', font_size, bold = True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

    def draw_converted_image(self):
        self.image = self.get_image()
        char_indices = self.image // self.ASCII_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[x, y]
                if char_index:
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))

    def get_image(self):
        ret, self.cv2_image = self.capture.read()
        if not ret:
            exit()
        transposed_img = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2GRAY)
        return image

if __name__ == "__main__":
    converter = ASCIIGreyscaleConverter()
    converter.run()