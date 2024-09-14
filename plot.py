import pandas as pd
import plotly.graph_objects as go
import time
from disp_manager import Display
from PIL import Image
from datetime import timedelta

d = Display()

# Define the margin as a percentage (e.g., 10%)
X_AXIS_MARGIN_PERCENT = 10 / 100  # 10%

# Define font sizes
TITLE_FONT_SIZE = 45
AXIS_TITLE_FONT_SIZE = 15
TICK_LABEL_FONT_SIZE = 30

def resize_image_to_display(image_path, output_path):
    # Open the image
    img = Image.open(image_path)

    # Resize the image to the display size (240x135)
    img_resized = img.resize((240, 135), Image.Resampling.LANCZOS)

    # Save the resized image
    img_resized.save(output_path)


def wait(sec: float = 4):
    time.sleep(sec)


def plot_scatter(df, scaled=True, last_n_hours=None, smoothing=0):
    # Convert 'Timestamp' to datetime if it's not already
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Filter data for the last 'n' hours if specified
    if last_n_hours is not None:
        time_threshold = df['Timestamp'].max() - timedelta(hours=last_n_hours)
        df = df[df['Timestamp'] >= time_threshold]

    # Calculate dynamic range for temperature and moisture
    temp_min = df['Temp'].min()
    temp_max = df['Temp'].max()
    moist_min = df['Moist'].min()
    moist_max = df['Moist'].max()

    # Calculate the margin based on the percentage
    temp_range = temp_max - temp_min
    moist_range = moist_max - moist_min
    temp_margin = temp_range * X_AXIS_MARGIN_PERCENT
    moist_margin = moist_range * X_AXIS_MARGIN_PERCENT

    # Apply the margin to the axis limits
    temp_min -= temp_margin
    temp_max += temp_margin
    moist_min -= moist_margin
    moist_max += moist_margin

    # Ensure values don't go below 0
    temp_min = max(temp_min, 0)
    moist_min = max(moist_min, 0)

    # Create the base figure
    fig = go.Figure()

    # Define line shape based on smoothing parameter
    line_shape = 'linear'
    if smoothing == 1:
        line_shape = 'spline'
    elif smoothing == 2:
        line_shape = 'spline'

    if scaled:
        # Add the first trace (Moisture Level on the left y-axis)
        fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Moist'],
                                 mode='lines', name='Moisture Level',
                                 yaxis='y1', line_shape=line_shape))

        # Add the second trace (Temperature on the right y-axis)
        fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Temp'],
                                 mode='lines', name='Temperature (°C)',
                                 yaxis='y2', line_shape=line_shape))

        # Update layout for two y-axes with dynamic ranges
        fig.update_layout(
            title=f'Temperature and Moisture Level Over {last_n_hours} Hours' if last_n_hours else 'Temperature and Moisture Level Over Time',
            title_font=dict(size=TITLE_FONT_SIZE),

            xaxis_title_font=dict(size=AXIS_TITLE_FONT_SIZE),
            xaxis_tickfont=dict(size=TICK_LABEL_FONT_SIZE),

            # Left y-axis (Moisture Level)
            yaxis=dict(
                range=[moist_min, min(moist_max, 100)],  # Moisture max limited to 100%
                titlefont=dict(size=AXIS_TITLE_FONT_SIZE, color='royalblue'),
                tickfont=dict(size=TICK_LABEL_FONT_SIZE, color='royalblue')
            ),

            # Right y-axis (Temperature)
            yaxis2=dict(
                range=[temp_min, temp_max],  # Use dynamic range for temperature
                titlefont=dict(size=AXIS_TITLE_FONT_SIZE, color='orangered'),
                tickfont=dict(size=TICK_LABEL_FONT_SIZE, color='orangered'),
                overlaying='y',  # Overlay it on the same plot
                side='right'  # Display it on the right side
            ),

            # Hide the legend
            showlegend=False
        )
    else:
        # Add the first trace (Temperature)
        fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Temp'], mode='lines', name='Temp', line_shape=line_shape))

        # Add the second trace (Moisture Level)
        fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Moist'], mode='lines', name='Moist', line_shape=line_shape))

        # Update layout (optional, for better appearance)
        fig.update_layout(
            title=f'Temperature and Moisture Level Over {last_n_hours} Hours' if last_n_hours else 'Temperature and Moisture Level Over Time',
            title_font=dict(size=TITLE_FONT_SIZE),
            xaxis_title='Timestamp',
            xaxis_title_font=dict(size=AXIS_TITLE_FONT_SIZE),
            xaxis_tickfont=dict(size=TICK_LABEL_FONT_SIZE),
            yaxis_title='Value',
            yaxis_title_font=dict(size=AXIS_TITLE_FONT_SIZE),
            yaxis_tickfont=dict(size=TICK_LABEL_FONT_SIZE),

            # Hide the legend
            showlegend=False
        )

    # Set the figure size to 5x the display size (1200x675)
    fig.update_layout(width=1200, height=675)

    fig.show()

    # Save the figure as a high-resolution image
    fig.write_image("plot_scaled_large.png")

    # Resize the image to the display size
    resize_image_to_display("plot_scaled_large.png", "plot_scaled.png")

    # Show the image on the display
    show_on_display("plot_scaled.png")



def show_on_display(image_path):
    # Open the image
    image = Image.open(image_path)

    # Display it using the Display class
    d.disp.ShowImage(image.convert("RGB"))


def main():
    df = pd.read_csv("garden_data_cleaned.csv")

    # Call plot_scatter with the last 12 hours of data, dynamic axis scaling, and smoothing level 2
    plot_scatter(df, scaled=True, last_n_hours=12, smoothing=2)
    wait(10)


if __name__ == "__main__":
    main()
