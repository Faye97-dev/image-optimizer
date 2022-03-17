DEBUG = True


# database config
DB_CONFIG = {
    'host': '',
    'database': '',
    'user': '',
    'password': '',
}

# images folder absolutes path end with '/'
ROOT_DIR='/var/www/appraisal-API/storage/app/public/images/'
IMG_COMPRESS_PATH = ROOT_DIR + 'tiny-images/'
RESIZED_PATH = ROOT_DIR + 'tiny-images-plus-2/'
LOGS_PATH = './logs/'


# preprocessing config
IMG_WIDTH = 200  # unused !
IMG_HEIGHT = 150  # unused !
IMG_QUALITY = 40
