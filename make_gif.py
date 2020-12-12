import glob
from PIL import Image

# filepaths
fp_in = "./screens/gif/*blood.png"
fp_out = "./screens/image.gif"

img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=125, loop=0)