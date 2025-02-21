# Sky Colour Gradient Image Generator

This Python script generates a series of 24 images representing sky colour gradients for each hour of the day. Each image features a gradient transitioning from a specified sky colour to a monochrome shade, with a name overlaid in a contrasting colour. This project was inspired by [@dame.is](https://bsky.app/profile/dame.is)'s blog post ['How I made an automated dynamic avatar for my Bluesky profile'](https://dame.is/blog/how-i-made-an-automated-dynamic-avatar-for-my-bluesky-profile).

While primarily designed for generating banner images, the script also supports creating profile images and custom-sized images.

## Features

- **Sky Colour Interpolation**: Smooth transitions between sky colours at different times of the day based on hourly RGB values.
- **Monochrome Fade**: Each image has a gradient that fades into a monochrome shade derived from the average RGB value of the sky colour.
- **Image Generation**: Automatically generates 24 images (one for each hour) if they do not already exist in the output folder.
- **Text Overlay**: Displays the project's name in a contrasting colour overlaid at the centre of each image.
- **Custom Image Sizes**: Supports generating images with user-defined width and height.

## Requirements

Ensure the following Python packages are installed:

- `json`
- `numpy`
- `PIL` (Pillow)

You can install the necessary packages using pip:

```bash
pip install -r requirements.txt
```

## Configuration

The script reads configuration settings from a JSON file located at `./config/generation.json`. This file should have the following structure:

```json
{
  "sky_colours": {
    "0": [10, 10, 40],
    "1": [12, 12, 45],
    "2": [15, 15, 50],
    "3": [18, 18, 55],
    "4": [20, 20, 60],
    "5": [50, 40, 100],
    "6": [100, 80, 150],
    "7": [110, 90, 170],
    "8": [120, 100, 190],
    "9": [135, 206, 235],
    "10": [90, 150, 200],
    "11": [80, 140, 190],
    "12": [70, 130, 180],
    "13": [80, 140, 190],
    "14": [90, 150, 200],
    "15": [135, 206, 235],
    "16": [180, 140, 50],
    "17": [220, 150, 25],
    "18": [255, 165, 0],
    "19": [160, 80, 10],
    "20": [139, 69, 19],
    "21": [50, 30, 15],
    "22": [20, 20, 60],
    "23": [10, 10, 40]
  },
  "name": "Project Name"
}
```

### Configuration Fields

- `sky_colours`: A dictionary mapping hours (as strings) to RGB values representing the sky colour at each hour.
- `name`: The name to be displayed on each image.

## Usage

1. Ensure the configuration file is correctly set up as described above.
2. Place the script in your desired directory.
3. Run the script using Python:

   ```bash
   python src/generator.py (--profile | --banner | --custom -w WIDTH -H HEIGHT)
   ```

   - `--profile` (`-p`) generates a **profile** image (400x400).
   - `--banner` (`-b`) generates a **banner** image (1500x500).
   - `--custom` (`-c`) allows specifying a custom width (`-w`) and height (`-H`).

   The script will generate 24 images (one for each hour) in the `./src/<profile_pics|banners|custom_wxh>` directory, if they don't already exist. Images will be named `00.png` through `23.png`, corresponding to each hour of the day.

## Notes

- The script checks if the output directory exists and creates it if necessary.
- It checks if each image already exists before attempting to regenerate it.
- The script uses a specific font located at `./config/fonts/madecarvingsoft.ttf`. Ensure this font file is available or adjust the path as needed.
- Images are generated with a gradient fading to a monochrome shade based on the average RGB value of the sky colour.

## License

This project is licensed under the MIT License.
