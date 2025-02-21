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
            return tuple((1 - t) * c1 + t * c2) + (255,)
    
    return tuple(sky_colours[str(hour)]) + (255,)

def create_gradient(hour, width, height):
    """Generate gradient with fade effect and appropriate RGBA handling."""
    colour = interpolate_colour(hour)
    
    average_colour = np.mean(colour[:3])
    fade_ratio = 0.1 + (0.5 - 0.1) * (1 - average_colour / 255)
    gradient_height = int(height * fade_ratio)
    
    monochrome_colour = (int(average_colour), int(average_colour), int(average_colour), 255)
    
    gradient_rgb = np.vstack([
        np.full((height - gradient_height, width, 3), colour[:3], dtype=np.uint8),
        np.linspace(colour[:3], monochrome_colour[:3], gradient_height)
        .astype(np.uint8)
        .reshape(gradient_height, 1, 3)
        .repeat(width, axis=1),
    ])
    
    alpha_channel = np.full((gradient_rgb.shape[0], gradient_rgb.shape[1], 1), 255, dtype=np.uint8)
    gradient_rgba = np.concatenate((gradient_rgb, alpha_channel), axis=2)
    return gradient_rgba

def get_available_folder(base_folder):
    """Check if the folder already exists, and if so, create a new folder with a counter."""
    counter = 1
    folder = base_folder
    while os.path.exists(folder):
        folder = f"{base_folder}_{counter}"
        counter += 1
    return folder

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

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate profile images or banners.")
parser.add_argument(
    "-p", "--profile", action="store_true", help="Generate profile image (400x400)."
)
parser.add_argument(
    "-b", "--banner", action="store_true", help="Generate banner image (1500x500)."
)
parser.add_argument(
    "-c", "--custom", action="store_true", help="Generate custom image with custom width and height."
)
parser.add_argument("-w", "--width", type=int, help="Custom image width (required with -c).")
parser.add_argument("-H", "--height", type=int, help="Custom image height (required with -c).")
args = parser.parse_args()

# Set image dimensions based on the flags
if args.profile:
    width, height = 400, 400
    output_folder = "./src/profile_pics"
elif args.banner:
    width, height = 1500, 500
    output_folder = "./src/banners"
elif args.custom:
    if not args.width or not args.height:
        print("Error: Custom dimensions (-w and -H) are required with the -c flag.")
        exit(1)
    width, height = args.width, args.height
    output_folder = f"./src/custom_{width}x{height}"
else:
    print("Error: You must specify either -p, -b, or -c.")
    exit(1)

# Define font path
font_path = "./config/fonts/madecarvingsoft.ttf"

# Create output folder
output_folder = get_available_folder(output_folder)
os.makedirs(output_folder)

# Determine which hours need image generation
images_to_generate = []
for hour in range(24):
    image_path = f"{output_folder}/{str(hour).zfill(2)}.png"
    if not os.path.exists(image_path):
        images_to_generate.append(hour)

# Generate images for the specified hours
for hour in images_to_generate:
    # Create gradient
    gradient = create_gradient(hour, width, height)
    # Create image from gradient array
    img = Image.fromarray(gradient, 'RGBA')
    draw = ImageDraw.Draw(img)
    
    # Text color calculation (adjusting based on background)
    text_colour = (
        min(255, int(255 - gradient[0][0][0] * 1.2)),
        min(255, int(255 - gradient[0][0][1] * 1.2)),
        min(255, int(255 - gradient[0][0][2] * 1.2)),
        255,  # Full opacity for text
    )
    
    # Calculate text placement, font size, and draw text
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
    
    # Ensure text fits within padding and margins
    position_x = max(position_x, horizontal_padding)
    position_y = max(position_y, vertical_padding)
    min_bottom_margin = 20
    max_position_y = height - text_height - min_bottom_margin
    position_y = min(position_y, max_position_y - text_height)
    
    # Add text to image
    text_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((position_x, position_y), name, font=font, fill=text_colour)
    img = Image.alpha_composite(img, text_img)
    
    # Optionally add noise to image
    noise = np.random.normal(0, 25, (height, width, 3)).astype(np.uint8)
    noise_img = Image.fromarray(noise, mode="RGB")
    img = Image.blend(img.convert("RGB"), noise_img, alpha=0.1)
    
    # Save the generated image
    image_path = f"{output_folder}/{str(hour).zfill(2)}.png"
    img.save(image_path)

# Print success message
print(f"Images generated successfully.")
print(f"Images saved to: {output_folder}")