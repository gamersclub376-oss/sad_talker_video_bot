import os

print("📦 Installing SadTalker dependencies...")

# Install Python packages
os.system("pip install --upgrade pip")
os.system("pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu118")

# Clone SadTalker if not present
if not os.path.exists("/content/SadTalker"):
    os.system("git clone https://github.com/OpenTalker/SadTalker.git /content/SadTalker")

# Install SadTalker requirements
os.system("pip install -r /content/SadTalker/requirements.txt")

# Fix torchvision bug
os.system("sed -i 's/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/' /content/SadTalker/src/utils/face_enhancer.py")

# Download default character & music
os.system("wget -q https://raw.githubusercontent.com/yourusername/free-assets/main/semi_realistic_face.jpg -O /content/character.jpg")
os.system("wget -q https://raw.githubusercontent.com/yourusername/free-assets/main/bg_music.mp3 -O /content/bg_music.mp3")

print("✅ SadTalker setup complete.")
