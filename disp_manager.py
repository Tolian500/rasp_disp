import os
import sys
import time
import logging
import platform
import pygame
import sys

try:
    import spidev as SPI
    from lib import LCD_1inch14
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    # Mock imports for Windows testing
    from PIL import Image, ImageDraw, ImageFont

# Platform detection
IS_LINUX = platform.system() == "Linux"
IS_WINDOWS = platform.system() == "Windows"

logging.basicConfig(level=logging.DEBUG)

WAIT_SECONDS = 2


class Muscot:
    def __init__(self):
        # Raspberry Pi pin configuration:
        if IS_LINUX:
            self.RST = 27
            self.DC = 25
            self.BL = 18
            self.bus = 0
            self.device = 0

            logging.info("Initializing LCD on Raspberry Pi.")
            self.disp = LCD_1inch14.LCD_1inch14()  # Hardware SPI display
            self.disp.Init()
            self.disp.clear()
            self.disp.bl_DutyCycle(50)
        else:
            logging.info("Simulating LCD display on Windows.")
            self.disp = self.MockDisplay()

        # Initialize fonts
        self.Font1 = ImageFont.truetype("./Font/Font00.ttf", 30)
        self.Font2 = ImageFont.truetype("./Font/Font01.ttf", 25)
        self.Font3 = ImageFont.truetype("./Font/Font02.ttf", 25)
        self.Font4 = ImageFont.truetype("./Font/Font03.ttf", 20)
        self.Font5 = ImageFont.truetype("./Font/Font04.ttf", 20)

    def draw_test(self):
        image2 = Image.new("RGB", (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image2)

        logging.info("Drawing shapes and text")
        draw.rectangle((1, 1, 2, 2), fill="BLACK")
        draw.rectangle((1, 7, 3, 10), fill="BLACK")
        draw.rectangle((1, 13, 4, 17), fill="BLACK")
        draw.rectangle((1, 19, 5, 24), fill="BLACK")
        draw.line([(20, 1), (50, 31)], fill="RED", width=1)
        draw.rectangle([(20, 1), (50, 31)], fill="WHITE", outline="BLUE")
        draw.arc((90, 1, 122, 33), 0, 360, fill=(0, 255, 0))

        draw.text((1, 45), u'Test1 ✔️', font=self.Font2, fill="BLACK")
        draw.text((90, 82), u'Test2 🎉🎉', font=self.Font2, fill="RED")
        draw.text((0, 85), u'Test3 🤗⛱️', font=self.Font3, fill="BLUE")

        self.disp.ShowImage(image2)

    def image_test(self):
        logging.info("Displaying image.")
        image = Image.open('./pic/LCD_1inch14.jpg')
        self.disp.ShowImage(image)

    def bright_test(self):
        for x in range(0, 100):
            self.disp.bl_DutyCycle(x)
            time.sleep(0.2)
        self.disp.bl_DutyCycle(50)

    def wait(self, seconds=WAIT_SECONDS):
        time.sleep(seconds)

    def cleanup(self):
        logging.info("Exiting...")
        self.disp.module_exit()

    # Mock display class for Windows testing
    class MockDisplay:
        def __init__(self):
            self.width = 240
            self.height = 135
            self.backlight = 50

        def Init(self):
            logging.info("Mock display initialized.")

        def clear(self):
            logging.info("Mock display cleared.")

        def ShowImage(self, image):
            image.show()  # Show the image on the screen using PIL's viewer (Windows)

        def bl_DutyCycle(self, duty):
            logging.info(f"Mock backlight set to {duty}%.")

        def module_exit(self):
            logging.info("Mock display exiting.")

    def show_text(self, content: str, width=20, fill_char='+'):
        # Split the content by newline, justify each line, then rejoin
        justified_lines = [line.rjust(width, fill_char) for line in content.split('\n')]
        justified_text = '\n'.join(justified_lines)

        # Create a new image for drawing the justified text
        image2 = Image.new("RGB", (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image2)

        # Draw the justified text
        draw.text((1, 1), justified_text, font=self.Font5, fill="BLACK")
        self.disp.ShowImage(image2)

    def draw_moisture_bar(self,current_level):
        pygame.init()
        screen = pygame.display.set_mode((240, 240))
        clock = pygame.time.Clock()

        # Colors
        gray = (128, 128, 128)
        green_start = (144, 238, 144)
        green_end = (0, 128, 0)
        white = (255, 255, 255)

        # Bar dimensions
        bar_width = 20
        bar_height = 150
        bar_x = 50
        bar_y = 30

        # Draw background
        screen.fill((255, 255, 255))

        # Draw the gray background bar
        pygame.draw.rect(screen, gray, pygame.Rect(bar_x, bar_y, bar_width, bar_height))

        # Draw gradient
        for i in range(20, 40):
            color = [int(green_start[j] + (green_end[j] - green_start[j]) * (i - 20) / 20) for j in range(3)]
            pygame.draw.rect(screen, color,
                             pygame.Rect(bar_x, bar_y + bar_height * (100 - i) / 100, bar_width, bar_height / 100))

        # Draw the current level as a white dash
        pygame.draw.line(screen, white, (bar_x - 5, bar_y + bar_height - current_level * bar_height / 100),
                         (bar_x + bar_width + 5, bar_y + bar_height - current_level * bar_height / 100), 3)

        # Refresh the screen
        pygame.display.flip()

        # Keep the window open until closed
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(60)

    # Example usage:

    def show_moist(self, moisture_level):
        # Create a blank image
        image = Image.new("RGB", (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image)

        # Define bar dimensions
        bar_x = 30
        bar_y = 100
        bar_width = 180
        bar_height = 30
        fill_width = int((moisture_level / 100) * bar_width)  # Calculate the width based on the percentage

        # Draw the background of the bar
        draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], outline="BLACK", fill="WHITE")

        # Choose the color based on the moisture level
        if 20 <= moisture_level <= 40:
            fill_color = "GREEN"  # Optimal range
        elif moisture_level < 20:
            fill_color = "RED"  # Too dry
        else:
            fill_color = "BLUE"  # Too wet

        # Draw the filled part of the bar
        draw.rectangle([bar_x, bar_y, bar_x + fill_width, bar_y + bar_height], fill=fill_color)

        # Add percentage text
        draw.text((bar_x + bar_width + 10, bar_y), f"{moisture_level}%", font=self.Font3, fill="BLACK")

        # Display the image on the screen
        self.disp.ShowImage(image)


# Main script execution
if __name__ == "__main__":
    try:
        text = "Темп: 25^C\nВол: 54%\nДо поливу: 10 днів"
        muscot = Muscot()
        muscot.show_text(text)

        # muscot.draw_test()
        muscot.wait()
        muscot.show_moist(50)
        muscot.wait()
        muscot.draw_moisture_bar(25)

        # muscot.image_test()
        # muscot.wait()
        # muscot.bright_test()
        # muscot.wait()
    except IOError as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("User interrupted. Exiting...")
