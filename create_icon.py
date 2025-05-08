import os
from PIL import Image, ImageDraw

def create_rounded_corners(image, radius):
    """Create rounded corners for the image"""
    # Create a mask with rounded corners
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
    
    # Apply the mask to the image
    output = Image.new('RGBA', image.size, (0, 0, 0, 0))
    output.paste(image, mask=mask)
    return output

def create_icns():
    """Create macOS .icns file from logo with rounded corners"""
    # Create iconset directory
    iconset_dir = "src/assets/logo.iconset"
    if not os.path.exists(iconset_dir):
        os.makedirs(iconset_dir)
    
    # Load the logo
    logo_path = "src/assets/logo.png"
    if not os.path.exists(logo_path):
        print("Error: Logo file not found!")
        return
    
    # Open and resize logo for different sizes
    img = Image.open(logo_path)
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    # Generate all required sizes
    for size in sizes:
        # Regular size
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        # Add rounded corners (radius is 20% of the size)
        radius = int(size * 0.2)
        rounded = create_rounded_corners(resized, radius)
        rounded.save(f"{iconset_dir}/icon_{size}x{size}.png")
        
        # @2x size
        if size * 2 <= 1024:
            resized = img.resize((size*2, size*2), Image.Resampling.LANCZOS)
            radius = int(size * 2 * 0.2)
            rounded = create_rounded_corners(resized, radius)
            rounded.save(f"{iconset_dir}/icon_{size}x{size}@2x.png")
    
    # Convert iconset to icns
    os.system(f"iconutil -c icns {iconset_dir}")
    
    # Clean up iconset directory
    os.system(f"rm -rf {iconset_dir}")
    
    print("Icon file created successfully!")

if __name__ == "__main__":
    create_icns() 