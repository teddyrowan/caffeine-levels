import glob
from PIL import Image

# filepaths
fp_in = "./screens/gif/*blood.png"
fp_out = "./screens/image.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
#img, *imgs = [Image.open(f) for f in glob.glob(fp_in)]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=200, loop=0)