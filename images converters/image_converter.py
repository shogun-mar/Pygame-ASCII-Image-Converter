import pygame as pg
import cv2
from tkinter import filedialog

class ImageConverter:
    def __init__(self) -> None:
        self.path = filedialog.askopenfilename()
        
        if not self.path or not self.path.endswith(('.png', '.jpg', '.jpeg')):
            raise ValueError("Please select a valid file.")

        pg.init()
        try:
            self.image = self.get_image()
            self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
            self.surface = pg.display.set_mode(self.RES)
        except AttributeError:
            pass
        
        self.clock = pg.time.Clock()
    
    def draw_cv2_image(self):
        cv2.imshow("img", self.cv2_image)

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

                if event.type == pg.KEYDOWN and event.key == pg.K_s:
                    self.save_image()
            
            pg.display.flip()
            self.clock.tick(60) # Limit the frame rate to 60 FPS so CPU usage is reduced