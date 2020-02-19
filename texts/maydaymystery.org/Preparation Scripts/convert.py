import os
from PIL import Image

gif_files = []
# r=root, d=directories, f = files
for r, d, f in os.walk('.'):
    for filename in f:
        ext = filename.split(os.path.extsep)[-1]
        if ext.lower() == 'gif':
            gif_files.append(filename)

def split_last(str_in, sep, first=False):
    separated = str_in.split(sep)
    if first:
        end = sep.join(separated[1:])
        first = separated[0]
        return first, end
    else:
        start = sep.join(separated[:-1])
        last = separated[-1]
        return start, last

def to_jpg(image_path):
    name, ext = split_last(image_path, os.path.extsep)
    if ext.lower in ['jpg', 'jpeg']:
        raise ValueError('Already a JPAG image!')
    img = Image.open(image_path).convert('RGBA')
    new_img = Image.new('RGBA', img.size, 'WHITE')
    new_img.paste(img, (0,0), img)
    new_image_path = name + '.jpg'
    print('{} => {}'.format(image_path, new_image_path))
    new_img.convert('RGB').save(new_image_path)

    

def main():
    for f in gif_files:
        to_jpg(f)
        os.remove(f)
