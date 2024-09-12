from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO

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

        # Generate a plot
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        plt.figure(figsize=(2.4, 2.4), dpi=100)  # Set figure size and resolution
        plt.plot(x, y)
        plt.title("Sine Wave")

        # Save plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        plt.close()

        # Load image from BytesIO
        image = Image.open(buf)
        image = image.resize((disp.width, disp.height))  # Resize to fit display
        disp.ShowImage(image)

        input("Press Enter to continue...")

        disp.module_exit()

    except IOError as e:
        print(e)
    except KeyboardInterrupt:
        disp.module_exit()
        print("quit:")
        exit()
