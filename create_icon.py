import os
import subprocess
from PIL import Image, ImageDraw

def create_rounded_corners(image, radius):
    # Create a mask with rounded corners
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
    
    # Apply the mask to the image
    output = Image.new('RGBA', image.size, (0, 0, 0, 0))
    output.paste(image, mask=mask)
    return output

def create_icns():
    try:
        # Create iconset directory
        iconset_dir = "src/assets/SG_One.iconset"
        os.makedirs(iconset_dir, exist_ok=True)
        
        # Load and process the logo
        logo_path = "src/assets/logo.png"
        if not os.path.exists(logo_path):
            print(f"Error: Logo file not found at {logo_path}")
            return
        
        # Open and process the logo
        logo = Image.open(logo_path)
        
        # Define icon sizes for macOS
        icon_sizes = {
            "icon_16x16.png": 16,
            "icon_16x16@2x.png": 32,
            "icon_32x32.png": 32,
            "icon_32x32@2x.png": 64,
            "icon_128x128.png": 128,
            "icon_128x128@2x.png": 256,
            "icon_256x256.png": 256,
            "icon_256x256@2x.png": 512,
            "icon_512x512.png": 512,
            "icon_512x512@2x.png": 1024
        }
        
        # Create icons for each size
        for name, size in icon_sizes.items():
            # Resize the logo
            resized = logo.resize((size, size), Image.Resampling.LANCZOS)
            
            # Add rounded corners (radius is 20% of the size)
            radius = int(size * 0.2)
            rounded = create_rounded_corners(resized, radius)
            
            # Save the icon
            icon_path = os.path.join(iconset_dir, name)
            rounded.save(icon_path, "PNG")
            print(f"Created icon: {icon_path}")
        
        # Convert iconset to icns using iconutil
        print("Converting iconset to icns...")
        
        # First, ensure we're in the correct directory
        current_dir = os.getcwd()
        os.chdir("src/assets")
        
        # Run iconutil
        result = subprocess.run(['iconutil', '-c', 'icns', 'SG_One.iconset'], 
                              capture_output=True, text=True)
        
        # Return to original directory
        os.chdir(current_dir)
        
        if result.returncode != 0:
            print(f"Error running iconutil: {result.stderr}")
            return
        
        # Check if the icns file was created
        icns_path = os.path.join("src/assets", "SG_One.icns")
        if not os.path.exists(icns_path):
            print("Error: iconutil did not create the icns file")
            return
        
        # Rename the icns file
        os.rename(icns_path, os.path.join("src/assets", "icon.icns"))
        print("Icon creation completed successfully!")
        
        # Clean up iconset directory
        subprocess.run(['rm', '-rf', iconset_dir])
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Clean up on error
        if os.path.exists(iconset_dir):
            subprocess.run(['rm', '-rf', iconset_dir])
        if os.path.exists(os.path.join("src/assets", "SG_One.icns")):
            os.remove(os.path.join("src/assets", "SG_One.icns"))

if __name__ == "__main__":
    create_icns() 