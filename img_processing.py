from io import BytesIO
from zipfile import ZipFile
from config import IMG_PATH, IMG_COMPRESS_PATH, IMG_QUALITY
from PIL import Image
from hurry.filesize import size
import requests
from logger import log
from fastapi import Response
import os


def create_directory(path):
    folder_exist = os.path.exists(path)
    if not folder_exist:
        os.makedirs(path, exist_ok=False)
        log.info(
            f"New folder added: {path}")


def get_file_size(file_path):
    size_ = os.path.getsize(file_path)
    return size(size_)


def image_optimizer(fname, estate_id):
    try:
        fat_img = Image.open('/var/www/store-v2/storage/app/public/cdn/images/'+fname)
        ###
        # create_directory(IMG_COMPRESS_PATH + estate_id)
        slim_img_filename = '/var/www/store-v2/storage/app/public/cdn/images/tiny-images-plus/'+fname
        fat_img.resize(100, 100)
        fat_img.save(slim_img_filename, optimize=True,
                     quality=IMG_QUALITY)  # 95 => 50% , 90 => 30%
    except Exception as e:
        log.error(f"Exception msg: {e}")
        return None
    else:
        log.info(
            f"Image ( {fat_img.filename} ) from {get_file_size(fat_img.filename)} to {get_file_size(slim_img_filename)}")
        return True

############################## download stuff ###################################


def get_files_directory(folder_path):
    files = os.listdir(folder_path)
    files = [folder_path + f for f in files]
    return files


def zip_folder(folder_path):
    zip_subdir = "download"
    zip_filename = f"{zip_subdir}.zip"

    filenames = get_files_directory(folder_path)

    # Open StringIO to grab in-memory ZIP contents
    s = BytesIO()

    # The zip compressor
    zf = ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        _, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(
        s.getvalue(), media_type="application/x-zip-compressed")
    resp.headers["Content-Disposition"] = 'attachment; filename=%s' % zip_filename

    return resp


#######################################################################


def save_img_from_cdn(cdn_, filename):
    response = requests.get(cdn_)
    file = open(IMG_PATH + filename, "wb")
    file.write(response.content)
    file.close()

#save_img_from_cdn("https://i.imgur.com/cG4nUs2.jpeg", "cG4nUs2.jpeg")

#foo = foo.resize((160, 300), Image.ANTIALIAS)
#foo.save("path\\to\\save\\image_scaled.jpg", quality=95)
#foo.save("path\\to\\save\\image_scaled_opt.jpg", optimize=True, quality=95)
