import pandas as pd
import plotly.graph_objects as go
import time
from disp_manager import Display
from PIL import Image

d = Display()

def wait(sec: float = 4):
    time.sleep(sec)

def plot_unscaled(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Temp'], mode='lines', name='Temp'))
    fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Moist'], mode='lines', name='Moist'))

    fig.update_layout(title='Temperature and Moisture Level Over Time',
                      xaxis_title='Timestamp',
                      yaxis_title='Value',
                      legend_title='Legend')

    # Save the figure as a PNG file
    fig.write_image("plot_unscaled.png")

    # Show the figure on the LCD display
    show_on_display("plot_unscaled.png")

def plot_scaled(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Moist'], mode='lines', name='Moisture Level', yaxis='y1'))
    fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Temp'], mode='lines', name='Temperature (°C)', yaxis='y2'))

    fig.update_layout(
        title='Temperature and Moisture Level Over Time',
        xaxis_title='Timestamp',
        yaxis=dict(title='Moisture Level (%)', range=[0, 100], titlefont=dict(color='#1f77b4'), tickfont=dict(color='#1f77b4')),
        yaxis2=dict(title='Temperature (°C)', range=[0, 40], titlefont=dict(color='#ff7f0e'), tickfont=dict(color='#ff7f0e'),
                    overlaying='y', side='right'),
        legend_title='Legend'
    )

    # Save the figure as a PNG file
    fig.write_image("plot_scaled.png")

    # Show the figure on the LCD display
    show_on_display("plot_scaled.png")

def show_on_display(image_path):
    # Open the image
    image = Image.open(image_path)

    # Display it using the Display class
    d.disp.ShowImage(image.convert("RGB"))

def main():
    df = pd.read_csv("garden_data_cleaned.csv")

    plot_unscaled(df)
    wait()

    plot_scaled(df)
    wait()

if __name__ == "__main__":
    main()
