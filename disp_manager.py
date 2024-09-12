import os
import sys
import time
import logging
from PIL import Image, ImageDraw, ImageFont


class MockLCD:
    def __init__(self):
        self.width = 240
        self.height = 240
        self.image = Image.new("RGB", (self.width, self.height), "WHITE")
        self.draw = ImageDraw.Draw(self.image)

    def Init(self):
        print("Mock display initialized.")

    def clear(self):
        self.image = Image.new("RGB", (self.width, self.height), "WHITE")
        self.draw = ImageDraw.Draw(self.image)

    def bl_DutyCycle(self, duty):
        """
        Set the backlight brightness.
        """
        if 0 <= duty <= 100:
            # Assuming you are using PWM to control the backlight
            self.pwm.set_pwm(self.BL_pin, 0, int(duty * 4095 / 100))
        else:
            logging.warning("Duty cycle should be between 0 and 100.")

    def ShowImage(self, image):
        image.show()  # Using PIL's built-in image viewer

    def module_exit(self):
        print("Mock display cleanup completed.")


# Check the platform and import accordingly
if sys.platform == "win32":
    LCD = MockLCD
else:
    import spidev as SPI
    from lib import LCD_1inch14


    class LCD(LCD_1inch14.LCD_1inch14):
        pass

# Define the paths to the fonts
FONT_PATH = "./Font/Font00.ttf"
FONT_PATH2 = "./Font/Font02.ttf"


# Function to print text with emojis
def print_text(draw):
    try:
        Font1 = ImageFont.truetype(FONT_PATH, 30)
        Font2 = ImageFont.truetype(FONT_PATH, 25)
        Font3 = ImageFont.truetype(FONT_PATH2, 25)

        # Draw text with emojis
        draw.text((1, 45), u'Test here 😀', font=Font2, fill="BLACK")
        draw.text((90, 82), u'0123456789', font=Font2, fill="RED")
        draw.text((00, 85), u'你好微雪', font=Font3, fill="BLUE")
    except Exception as e:
        logging.error(f"Error printing text: {e}")


# Function to print a plot
def print_plot(draw):
    try:
        # Example plot
        draw.rectangle((1, 1, 2, 2), fill="BLACK")
        draw.rectangle((1, 7, 3, 10), fill="BLACK")
        draw.rectangle((1, 13, 4, 17), fill="BLACK")
        draw.rectangle((1, 19, 5, 24), fill="BLACK")

        draw.line([(20, 1), (50, 31)], fill="RED", width=1)
        draw.line([(50, 1), (20, 31)], fill="RED", width=1)
        draw.line([(90, 17), (122, 17)], fill="RED", width=1)
        draw.line([(106, 1), (106, 33)], fill="RED", width=1)

        draw.rectangle([(20, 1), (50, 31)], fill="WHITE", outline="BLUE")
        draw.rectangle([(55, 1), (85, 31)], fill="BLUE")

        draw.arc((90, 1, 122, 33), 0, 360, fill=(0, 255, 0))
        draw.ellipse((125, 1, 158, 33), fill=(0, 255, 0))
    except Exception as e:
        logging.error(f"Error printing plot: {e}")


def main():
    logging.basicConfig(level=logging.DEBUG)
    try:
        # Initialize LCD display
        if sys.platform == "win32":
            disp = LCD()
        else:
            RST = 27
            DC = 25
            BL = 18
            bus = 0
            device = 0
            disp = LCD(spi=SPI.SpiDev(bus, device), spi_freq=10000000, rst=RST, dc=DC, bl=BL)

        # Initialize and clear the display
        if sys.platform != "win32":
            disp.Init()
        image = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image)

        print_plot(draw)
        print_text(draw)
        disp.ShowImage(image)

        time.sleep(60)
        logging.info("Displaying image")

        # Load and show a static image
        if not sys.platform == "win32":
            image = Image.open('./pic/LCD_1inch14.jpg')
            disp.ShowImage(image)
            time.sleep(30)

        if not sys.platform == "win32":
            disp.module_exit()
            logging.info("Quit")
    except Exception as e:
        logging.error(f"Error in main: {e}")


if __name__ == "__main__":
    main()
