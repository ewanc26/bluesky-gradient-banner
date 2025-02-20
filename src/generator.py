import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import argparse

# Load configuration settings from JSON file
with open("./config/generation.json", "r") as file:
    config = json.load(file)
    sky_colours = config["sky_colours"]
    name = config["name"]

def interpolate_colour(hour):
    """Interpolate sky colour based on the given hour."""
    hours = sorted(map(int, sky_colours.keys()))
    
    for i in range(len(hours) - 1):
        if hours[i] <= hour <= hours[i + 1]:
            t = (hour - hours[i]) / (hours[i + 1] - hours[i])
            c1, c2 = np.array(sky_colours[str(hours[i])]), np.array(sky_colours[str(hours[i + 1])])
            return tuple((1 - t) * c1 + t * c2)
    
    return sky_colours[str(hour)]

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate profile images or banners.")
parser.add_argument(
    "--type",
    choices=["profile", "banner"],
    required=True,
    help="Choose to generate 'profile' (400x400) or 'banner' (1500x500) images.",
)
args = parser.parse_args()

# Set image dimensions based on type
if args.type == "profile":
    width, height = 400, 400
    output_folder = "./src/profile_pics"
elif args.type == "banner":
    width, height = 1500, 500
    output_folder = "./src/banners"

# Define font path
font_path = "./config/fonts/madecarvingsoft.ttf"

def get_available_folder(base_folder):
    """Check if the folder already exists, and if so, create a new folder with a counter."""
    counter = 1
    folder = base_folder
    while os.path.exists(folder):
        folder = f"{base_folder}_{counter}"
        counter += 1
    return folder

# Create the output folder if it doesn't exist
output_folder = get_available_folder(output_folder)
os.makedirs(output_folder)

# Determine which hours need image generation
images_to_generate = []
for hour in range(24):
    image_path = f"{output_folder}/{str(hour).zfill(2)}.png"
    if not os.path.exists(image_path):
        images_to_generate.append(hour)

def get_max_font_size(draw, text, font_path, max_width, max_height):
    """Calculate the maximum font size that fits within the image dimensions."""
    font_size = 1
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    
    while text_width <= max_width and text_height <= max_height:
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    
    return font_size - 1

# Generate images for the specified hours
for hour in images_to_generate:
    colour = interpolate_colour(hour)
    
    # Calculate text colour based on the background colour
    text_colour = (
        min(255, int(255 - colour[0] * 1.2)),
        min(255, int(255 - colour[1] * 1.2)),
        min(255, int(255 - colour[2] * 1.2)),
        200,
    )
    
    # Calculate fade ratio and create gradient
    average_colour = np.mean(colour)
    fade_ratio = 0.1 + (0.5 - 0.1) * (1 - average_colour / 255)
    gradient_height = int(height * fade_ratio)
    monochrome_colour = (int(average_colour), int(average_colour), int(average_colour))
    
    gradient = np.vstack(
        [
            np.full((height - gradient_height, width, 3), colour, dtype=np.uint8),
            np.linspace(colour, monochrome_colour, gradient_height)
            .astype(np.uint8)
            .reshape(gradient_height, 1, 3)
            .repeat(width, axis=1),
        ]
    )
    
    # Create image with gradient
    img = Image.fromarray(gradient)
    draw = ImageDraw.Draw(img)
    
    # Calculate text placement
    horizontal_padding = width * 0.1
    usable_width = width - 2 * horizontal_padding
    vertical_padding = height * 0.1
    usable_height = height - 2 * vertical_padding
    font_size = get_max_font_size(draw, name, font_path, usable_width, usable_height)
    font = ImageFont.truetype(font_path, font_size)
    
    # Get text bounding box and position
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position_x = (width - text_width) // 2
    position_y = (height - text_height) // 2
    
    # Ensure text is within padding and margins
    position_x = max(position_x, horizontal_padding)
    position_y = max(position_y, vertical_padding)
    min_bottom_margin = 20
    max_position_y = height - text_height - min_bottom_margin
    position_y = min(position_y, max_position_y - text_height)
    
    # Add text to image
    text_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((position_x, position_y), name, font=font, fill=text_colour)
    img = Image.alpha_composite(img.convert("RGBA"), text_img)
    
    # Add noise to the image
    noise = np.random.normal(0, 25, (height, width, 3)).astype(np.uint8)
    noise_img = Image.fromarray(noise, mode="RGB")
    img = Image.blend(img.convert("RGB"), noise_img, alpha=0.1)
    
    # Save the generated image
    image_path = f"{output_folder}/{str(hour).zfill(2)}.png"
    img.save(image_path)

# Print success message
print(f"{args.type.capitalize()} images generated successfully.")
print(f"Images saved to: {output_folder}")