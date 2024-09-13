import os
import sys
import time
import logging
import platform
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


class Display:
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
        self.Font5 = ImageFont.truetype("./Font/Font04.ttf", 22)
        self.Font6 = ImageFont.truetype("./Font/OrbitronM.ttf", 22)
        self.Font7 = ImageFont.truetype("./Font/OrbitronSB.ttf", 18)

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

    def blick(self, sec: float):
        self.disp.bl_DutyCycle(0)
        time.sleep(sec)
        self.disp.bl_DutyCycle(50)
        time.sleep(sec * 2)
        self.disp.bl_DutyCycle(0)
        time.sleep(sec)
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

    def show_text(self, content: str, width=5, fill_char='+', color="BLACK"):
        # Split the content by newline, justify each line, then rejoin
        justified_lines = [line.rjust(width, fill_char) for line in content.split('\n')]
        justified_text = '\n'.join(justified_lines)

        # Create a new image for drawing the justified text
        image2 = Image.new("RGB", (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image2)

        # Draw the justified text
        draw.text((1, 1), justified_text, font=self.Font5, fill=color)
        self.disp.ShowImage(image2)

    def draw_moisture_bar(self, current_level):
        # Define margins
        top_margin = 10
        bottom_margin = 10

        # Set up dimensions and positions for the bar
        bar_width = 20
        bar_height = 200
        image_width = self.disp.width
        image_height = bar_height + top_margin + bottom_margin
        bar_x = (image_width - bar_width) // 2  # Center horizontally
        bar_y = top_margin  # Start position vertically with top margin

        # Create a new blank image with adjusted height
        image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 255))  # Use RGBA for transparency
        draw = ImageDraw.Draw(image)

        # Draw the background of the moisture bar with a gradient from light brown to light blue
        self.draw_gradient(draw, bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                           start_color=(22, 98, 125),
                           end_color=(125, 140, 139))  # Light brown to light blue (210, 180, 140)

        # Optimal range (20% - 40%) with green lines
        good_top = bar_y + (100 - 40) * bar_height // 100
        good_bot = bar_y + (100 - 20) * bar_height // 100
        draw.line([bar_x - 5, good_top, bar_x + bar_width + 5, good_top], fill="WHITE", width=1)
        draw.line([bar_x - 5, good_bot, bar_x + bar_width + 5, good_bot], fill="WHITE", width=1)

        # Draw the current level as a white dash
        current_level_y = bar_y + (100 - current_level) * bar_height // 100
        draw.line([bar_x - 5, current_level_y, bar_x + bar_width + 5, current_level_y], fill=(169, 191, 4), width=3)

        # Show the image
        self.disp.ShowImage(image.convert("RGB"))  # Convert to RGB before showing on display

    def draw_gradient(self, draw, x1, y1, x2, y2, start_color, end_color):
        # Calculate the height of the gradient
        height = y2 - y1

        # Draw the gradient by filling rectangles with varying colors
        for i in range(height):
            # Calculate the color for this position
            r = int(start_color[0] + (end_color[0] - start_color[0]) * i / height)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * i / height)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * i / height)
            color = (r, g, b)

            # Draw a horizontal line with the calculated color
            draw.line([(x1, y1 + i), (x2, y1 + i)], fill=color)

            # Example usage:

    def show_hor_bar(self, moisture_level):
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

    def show_moisture_with_text(self, current_level, text):
        # Create a new blank image with the screen size
        image = Image.new("RGBA", (240, 135), (39, 39, 39, 39))
        draw = ImageDraw.Draw(image)

        # Define margins and dimensions
        top_margin = 5
        bottom_margin = 5
        bar_width = 20
        bar_height = 125
        image_width = 240
        image_height = 135

        # Move the bar 30 pixels to the right from the center
        bar_x = (image_width - bar_width) // 2 + 100
        bar_y = top_margin  # Start position vertically with top margin

        # Draw the background of the moisture bar with a gradient from light brown to light blue
        self.draw_gradient(draw, bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                           start_color=(22, 98, 125),
                           end_color=(125, 140, 139))  # Light brown to light blue

        # Optimal range (20% - 40%) with green lines
        good_top = bar_y + (100 - 40) * bar_height // 100
        good_bot = bar_y + (100 - 20) * bar_height // 100
        draw.line([bar_x - 0, good_top, bar_x + bar_width + 0, good_top], fill="WHITE", width=2)
        draw.line([bar_x - 0, good_bot, bar_x + bar_width + 0, good_bot], fill="WHITE", width=2)

        # Draw the current level as a white dash
        current_level_y = bar_y + (100 - current_level) * bar_height // 100
        draw.line([bar_x - 15, current_level_y, bar_x + bar_width + 0, current_level_y], fill=(169, 191, 4), width=3)

        # Draw the text at the bottom of the screen
        text_position = (10, 10)
        draw.text(text_position, text, font=self.Font7, fill="WHITE")

        # Show the image
        self.disp.ShowImage(image.convert("RGB"))  # Convert to RGB before showing on display




# Main script execution
if __name__ == "__main__":
    try:
        curent_moist = 50
        muscot = Display()
        # muscot.show_text(f"Current moist: {curent_moist}")
        # muscot.draw_moisture_bar(curent_moist)
        muscot.show_moisture_with_text(35, f"Status: Too wet\nTemp: 20°C \nMoist:  {curent_moist}%\nNext water:\nIn 2 Hours")
        time.sleep(10)

    except IOError as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("User interrupted. Exiting...")
