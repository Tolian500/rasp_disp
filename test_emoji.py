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
        Font = ImageFont.load_default()

        image = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image)

        # Draw text with emojis
        text = "Hello World! 😊🌍"
        draw.text((10, 10), text, font=Font, fill="BLACK")
        disp.ShowImage(image)

        input("Press Enter to continue...")

        disp.module_exit()

    except IOError as e:
        print(e)
    except KeyboardInterrupt:
        disp.module_exit()
        print("quit:")
        exit()
