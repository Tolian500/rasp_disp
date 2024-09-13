import os
import sys
import time
import logging
import platform

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
        self.Font2 = ImageFont.truetype("./Font/Font00.ttf", 25)
        self.Font3 = ImageFont.truetype("./Font/Font02.ttf", 25)
        self.Font4 = ImageFont.truetype("./Font/Font03.ttf", 25)
        self.Font5 = ImageFont.truetype("./Font/Font03.ttf", 25)

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
            self.height = 240
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

    def show_text(self, content:str):
        image2 = Image.new("RGB", (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image2)
        draw.text((1, 1), content, font=self.Font2, fill="BLACK")
        draw.text((1, 30), content, font=self.Font3, fill="BLACK")
        draw.text((1, 60), content, font=self.Font4, fill="BLACK")
        self.disp.ShowImage(image2)

# Main script execution
if __name__ == "__main__":
    try:
        muscot = Muscot()
        muscot.show_text("Hello Here")

        # muscot.draw_test()
        muscot.wait()
        muscot.wait()
        muscot.wait()

        # muscot.image_test()
        # muscot.wait()
        # muscot.bright_test()
        # muscot.wait()
    except IOError as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("User interrupted. Exiting...")
