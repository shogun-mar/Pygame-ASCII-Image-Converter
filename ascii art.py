import pygame as pg
import cv2

class Converter:
    def __init__(self, path = "img/gato2.jpg", font_size = 10):
        pg.init()
        self.path = path
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.ASCII_CHARS = '.",:;!~+-xmo*#W&8@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Courier', font_size, bold = True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

    def draw_converted_image(self):
        char_indices = self.image // self.ASCII_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[x, y]
                if char_index:
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_img = cv2.transpose(self.cv2_image)
        return cv2.cvtColor(transposed_img , cv2.COLOR_BGR2GRAY)
    
    def draw_cv2_image(self): # Resize the cv2 image so it fits the screen
        resized_cv2_image = cv2.resize(self.cv2_image, (480, 720), interpolation = cv2.INTER_AREA)
        cv2.imshow("img", resized_cv2_image)

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()

    def save_image_pg(self):
        # Save the Pygame surface directly to an image file
        pg.image.save(self.surface, 'output/img/converted_image.png')

    # def save_image_cv(self):
    #     pygame_img = pg.surfarray.array3d(self.surface)
    #     cv2_img = cv2.transpose(pygame_img)
    #     cv2.imwrite('output/img/converted_image.jpg', cv2_img)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                if event.type == pg.KEYDOWN:
                    self.save_image()
            
            self.draw()
            pg.display.set_caption(f"{self.clock.get_fps()}")
            pg.display.flip()
            self.clock.tick()

if __name__ == "__main__":
    Converter().run()