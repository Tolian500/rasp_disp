from disp_manager import Display
from plot import plot_scatter
import time
import pandas as pd


d = Display()


df = pd.read_csv("garden_data_cleaned.csv")
d.show_on_display(plot_scatter(df, scaled=True, last_n_hours=12, smoothing=2))
time.sleep(10)
d.show_text("Temp: 25°C")
time.sleep(10)
d.show_text("Moist: 55%")
time.sleep(10)
