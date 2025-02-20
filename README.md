# Sky Colour Gradient Image Generator

This Python script generates a series of 24 images representing sky colour gradients at each hour of the day. Each image features a gradient transitioning from a specified sky colour to a monochrome shade, with a name overlaid in a contrasting colour. It is inspired by [@dame.is](https://bsky.app/profile/dame.is)'s blog post ['How I made an automated dynamic avatar for my Bluesky profile'](https://dame.is/blog/how-i-made-an-automated-dynamic-avatar-for-my-bluesky-profile). It is meant for the banner image rather than the profile photo because I prefer it.

## Features

- **Sky Colour Interpolation**: Smooth transitions between sky colours at different times of the day, based on hourly RGB values.
- **Monochrome Fade**: Each image has a gradient fading into a monochrome shade derived from the average RGB value.
- **Image Generation**: Automatically generates 24 images (one for each hour) if they do not already exist.
- **Text Overlay**: Displays the project's name in a contrasting colour over each image.

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

The script reads configuration settings from a JSON file located at `./config/generation.json`. This file should contain the following structure:

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

- `sky_colours`: A dictionary mapping hours (as strings) to RGB values representing the sky colour at that hour.
- `name`: The name to be displayed on each image.

## Usage

1. Ensure the configuration file is correctly set up as described above.
2. Place the script in the desired directory.
3. Run the script using Python:

   ```bash
   python src/generator.py
   ```

The script will generate 24 images in the `./src/blobs` directory, each named `00.png` through `23.png`, corresponding to each hour of the day, if they don't already exist.

## Notes

- The script checks if the output directory exists and creates it if necessary.
- It checks if each image already exists before attempting to regenerate it.
- The script uses a specific font located at `./config/fonts/madecarvingsoft.woff2`. Ensure this font file is available or adjust the path as needed.
- Images are generated with a gradient fading to a monochrome shade based on the average RGB value of the sky colour.

## License

This project is licensed under the MIT License.
