from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import time

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

    def bl_DutyCycle(self, value):
        print(f"Backlight set to {value}%")

    def ShowImage(self, image):
        image.show()  # Using PIL's built-in image viewer

    def module_exit(self):
        print("Mock display cleanup completed.")

# Usage in your script
if __name__ == "__main__":
    try:
        # Use the mock class instead of the actual display class
        disp = MockLCD()
        disp.Init()
        disp.clear()
        disp.bl_DutyCycle(50)

        # Create blank image for drawing
        Font1 = ImageFont.truetype("./Font/Font00.ttf", 30)
        Font2 = ImageFont.truetype("./Font/Font00.ttf", 25)
        Font3 = ImageFont.truetype("./Font/Font02.ttf", 25)

        image2 = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image2)

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

        draw.text((1, 45), u'Hellow WaveShare', font=Font2, fill="BLACK")
        draw.text((90, 82), u'0123456789', font=Font2, fill="RED")
        draw.text((0, 85), u'你好微雪', font=Font3, fill="BLUE")
        disp.ShowImage(image2)

        time.sleep(2)

        image = Image.open('./pic/LCD_1inch14.jpg')
        disp.ShowImage(image)
        time.sleep(2)

        disp.module_exit()

    except IOError as e:
        print(e)
    except KeyboardInterrupt:
        disp.module_exit()
        print("quit:")
        exit()
