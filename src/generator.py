import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
import argparse

# Load sky colours, name, and timezone from generation.json
with open("./config/generation.json", "r") as file:
    config = json.load(file)
    sky_colours = config["sky_colours"]
    name = config["name"]

# Function to interpolate RGB values between given key times
def interpolate_colour(hour):
    hours = sorted(map(int, sky_colours.keys()))
    for i in range(len(hours) - 1):
        if hours[i] <= hour <= hours[i + 1]:
            t = (hour - hours[i]) / (hours[i + 1] - hours[i])
            c1, c2 = np.array(sky_colours[str(hours[i])]), np.array(
                sky_colours[str(hours[i + 1])]
            )
            return tuple((1 - t) * c1 + t * c2)
    return sky_colours[str(hour)]  # Exact match case

# Argument parser for image type
parser = argparse.ArgumentParser(description="Generate profile images or banners.")
parser.add_argument("--type", choices=["profile", "banner"], required=True, help="Choose to generate 'profile' (400x400) or 'banner' (1500x500) images.")
args = parser.parse_args()

# Set dimensions based on type
if args.type == "profile":
    width, height = 400, 400
    output_folder = "./src/profile_pics"
elif args.type == "banner":
    width, height = 1500, 500
    output_folder = "./src/banners"

font_size = 50
font_path = "./config/fonts/madecarvingsoft.woff2"  # Adjust if needed

# Check and create the folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Check if images need to be generated
images_to_generate = []
for hour in range(24):
    image_path = f"{output_folder}/{str(hour).zfill(2)}.png"
    if not os.path.exists(image_path):
        images_to_generate.append(hour)

# Generate images
for hour in images_to_generate:
    colour = interpolate_colour(hour)
    average_colour = np.mean(colour)
    monochrome_colour = (int(average_colour), int(average_colour), int(average_colour))
    fade_ratio = 0.3
    gradient_height = int(height * fade_ratio)

    # Create gradient
    gradient = np.vstack([
        np.full((height - gradient_height, width, 3), colour, dtype=np.uint8),
        np.linspace(colour, monochrome_colour, gradient_height).astype(np.uint8).reshape(gradient_height, 1, 3).repeat(width, axis=1)
    ])

    img = Image.fromarray(gradient)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Position text
    text_colour = (255 - int(colour[0]), 255 - int(colour[1]), 255 - int(colour[2]), 150)  # Semi-transparent text
    if args.type == "profile":
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)
    else: 
        position = (20, 20)  # Top-left for banners
    
    draw.text(position, name, fill=text_colour, font=font)
    
    # Add grain effect
    noise = np.random.normal(0, 25, (height, width, 3)).astype(np.uint8)
    noise_img = Image.fromarray(noise, mode="RGB")
    img = Image.blend(img, noise_img, alpha=0.1)  # Blend in noise slightly
    
    # Save image
    image_path = f"{output_folder}/{str(hour).zfill(2)}.png"
    img.save(image_path)

print(f"{args.type.capitalize()} images generated successfully.")