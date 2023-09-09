
# helpers.py
# contains helper methods

import os
import shutil
import re
import time
from datetime import datetime
from constants.constants import IMG_PATH, ERROR404_IMG_PATH, DEFAULT_FONT
from modules.applogger import AppLogger
# import subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from typing import Callable, Iterable


log = AppLogger('HELPERS').getlogger()


# def add_timestamp(imgpath: str) -> tuple[str,bool]:
#     """
#     Add the timestamp to images
#     """
#     # 20230902_152601.jpg -> 20230902_152601
#     tstamp = imgpath.split('.')[0]
#     # 20230902_152601 -> 2023-09-02 15:26:01
#     tstamp = datetime.strptime(tstamp, '%Y%m%d_%H%M%S%f').strftime('%Y-%m-%d %H:%M:%S:%f')
#     # ffmpeg requires escaping special characters
#     tstamp = tstamp.replace(':','\:')

#     tmp_imgpath = os.path.join(IMG_PATH, f"{imgpath.split('.jpg')[0]}_tmp.jpg")
#     imgpath = os.path.join(IMG_PATH, imgpath)
    
#     # ffmpeg filter
#     filter = f"drawtext=text='{tstamp}': x=5: y=5: fontcolor=yellow: fontsize=12: shadowcolor=black: shadowx=1: shadowy=1: box=1: boxcolor=black@0.8: boxborderw=5"

#     # ffmpeg arguments
#     ffmpeg_cmd = [
#         "ffmpeg",
#         "-i", imgpath,
#         "-vf", filter,
#         tmp_imgpath,
#         "-loglevel", "error"
#     ]
#     try:
#         # add timestampt to image
#         subprocess.run(ffmpeg_cmd, check=True)
#         # remove original image file
#         os.remove(imgpath)
#         # rename new image filename (with timestamp) 
#         # to original filename
#         os.rename(tmp_imgpath, imgpath)

#     except Exception as ex:
#         log.error(f'Error adding timestamp: {ex.__class__.__name__} - {str(ex)}')
#         return (imgpath, False)
    
#     return (imgpath, True)


def add_timestamp(imgpath: str) -> tuple[str,bool]:
    """
    Adds timestamp to an image
    """
    
    try:

        # 20230902_152601.jpg -> 20230902_152601
        tstamp = imgpath.split('.')[0]
        # 20230902_152601 -> 2023-09-02 15:26:01
        tstamp = datetime.strptime(tstamp, '%Y%m%d_%H%M%S%f').strftime('%Y-%m-%d %H:%M:%S:%f')

        img = Image.open(os.path.join(IMG_PATH,imgpath))
        imgdraw = ImageDraw.Draw(img)
        font = ImageFont.truetype(DEFAULT_FONT, 14)
        imgdraw.text((5,5), tstamp, (0,255,0), font=font)
        img.save(os.path.join(IMG_PATH,imgpath))

    except Exception as ex:
        log.error(f'Error adding timestamp: {ex.__class__.__name__} - {str(ex)}')
        return (imgpath, False)
    
    return (imgpath, True)


def get_last_sortnum(dirname: str) -> int:
    """
    Return the latest sort number used for images 
    in an image directory
    Param:
        dirname     
    """
    sortnum_fpath = os.path.join(os.path.join(IMG_PATH, dirname), '.lastsortnum')
    if not os.path.exists(sortnum_fpath):
        with open(sortnum_fpath, 'w') as fh:
            fh.write('0')
        return 0
    
    lastsortnum = 0
    with open(sortnum_fpath, 'r') as fh:
        lastsortnum = int(fh.read())

    return lastsortnum


def set_last_sortnum(dirname: str, sortnum: int) -> None:
    """
    Sets the last sort number
    """
    sortnum_fpath = os.path.join(os.path.join(IMG_PATH, dirname), '.lastsortnum')
    with open(sortnum_fpath, 'w') as fh:
        fh.write(str(sortnum))


def get_unique_dates(imagefnames: list[str]) -> list[str]:
    """
    Returns list of unique dates found in list of image names
    Ex: 
    ['20230902_122322.jpg', '20230903_123322.jpg',...] 
    -> ['20230902', '20230903']
    """
    if not imagefnames:
        return []
    
    unique_dates: list[str] = []
    # extract unique dates found in image file names
    for img in imagefnames:
        # remove .jpg extension
        img_date = img.split('_')[0]
        if img_date not in unique_dates:
            unique_dates.append(img_date)

    return unique_dates


def create_dirs(dirnames: list[str]) -> None:
    """
    Creates multiple directories
    """
    for dirname in dirnames:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            log.debug(f'Created directory: {dirname}')
    

def assign_image_sequence(imgpaths: list[str]) -> list[tuple]:
    """
    Assigns sort number to image paths
    """ 
    def format_sequence(seq_no: int):
        """ Returns formatted sequence number """
        seqno_frmtd = str(seq_no)
        if len(seqno_frmtd) < 6:
            seqno_frmtd = f"{'0'*(6-len(seqno_frmtd))}{seq_no}"
        return seqno_frmtd

    last_sort_no = get_last_sortnum(dirname = imgpaths[0].split('_')[0])
    
    # remove .jpg extension
    imgpaths_sorted = [img.split('.')[0] for img in imgpaths]
    # sort filenames by the time
    imgpaths_sorted.sort(key=lambda img: img.split('_')[1])

    # [(original filename, filename with sequence),...]
    # ex: [(20230902_235317.jpg, 20230902_235317_000001.jpg),...]
    imgpaths_sorted = [(f"{img}.jpg", f"{img}_{format_sequence(seqno)}.jpg") 
                       for seqno,img in enumerate(imgpaths_sorted, start=last_sort_no)]
    
    set_last_sortnum(
        dirname = imgpaths[0].split('_')[0], 
        sortnum = last_sort_no + len(imgpaths)
    )

    return imgpaths_sorted


def rename_image(imgnames: tuple[str]) -> bool:
    """
    Renames an image

    Params:
        imgpaths: tuple[str] - (source, dest)
    """
    try:
        os.rename(
            os.path.join(IMG_PATH, imgnames[0]),
            os.path.join(IMG_PATH, imgnames[1])
        )
    except Exception as ex:
        log.error(f'[Rename Error]: {imgnames} Err: {ex.__class__.__name__} - {str(ex)}')
        return False
    return True


# def move_image(imgname: str) -> bool:
#     """
#     Moves image to its date directory
#     Ex: 20230903_122802_000001.jpg -> IMG_PATH/20230903_122802_000001.jpg 
#     """
#     try:
#         newpath = os.path.join(imgname.split('_')[0], imgname)
#         newpath = os.path.join(IMG_PATH, newpath)
#         shutil.move(
#             os.path.join(IMG_PATH, imgname),
#             newpath
#         )
#     except Exception as ex:
#         log.error(f'[Move Error]: {imgname} Err: {ex.__class__.__name__} - {str(ex)}')
#         return False
#     return True


def move_image(imgpath: tuple[str]) -> bool:
    """
    Moves image to its date directory

    Params:
        (org_img_path, sequenced_img_path)
        ex: (20230903_122802.jpg, 20230903_122802_000001.jpg)

    Moves 20230903_122802.jpg to 20230903/20230903_122802_000001.jpg 
    """
    try:
        # date directory
        newpath = os.path.join(imgpath[1].split('_')[0], imgpath[1])
        shutil.move(
            os.path.join(IMG_PATH, imgpath[0]), # 20230903_122802.jpg
            os.path.join(IMG_PATH, newpath) # 20230903/20230903_122802_000001.jpg 
        )
    except Exception as ex:
        log.error(f'[Move Error]: {imgpath} Err: {ex.__class__.__name__} - {str(ex)}')
        return False
    return True


def exec_multithread(func: Callable, items: Iterable, max_workers: int = 5) -> None:
    """
    Runs function with items as parameter in multiple threads
    """
    with ThreadPoolExecutor(max_workers) as exc:
        for itemno, runstat in enumerate(exc.map(func, items)):
            try:
                if not runstat:
                    log.debug(f'[Mutlithread Exec]: {func.__name__}({items[itemno]}) - Ret: {runstat}')
            except Exception as ex:
                log.error(f'[Mutlithread Exec]: {func.__name__}({items[itemno]}) - Err: {ex.__class__.__name__} - {str(ex)}')
    

def group_images() -> None:
    """
    Groups images based on their dates
    """
    # get list of all files/directories in image path
    # images = os.listdir(IMG_PATH)
    # keep only .jpg files
    # images = [img for img in images if img.endswith('.jpg')]

    # get list of all .jpg files in image path
    images = [img for img in os.listdir(IMG_PATH) if re.match(r'\d{8}_\d{12}.jpg', img)]
    log.debug(f'New images found: {len(images)}')
    if not images:
        return

    # contains list of unique dates found from
    # newly saved images
    unique_dates: list[str] = get_unique_dates(imagefnames = images)

    # create directories for dates found 
    # in image file names
    create_dirs(dirnames = [os.path.join(IMG_PATH, dt) for dt in unique_dates])

    # adding timestamp
    exec_multithread(func = add_timestamp, items = images, max_workers=2)
    
    # original image name and their sequenced image name
    # [('20230903_121501.jpg','20230903_121501_000011.jpg'),...]
    sequeced_imgs = assign_image_sequence(imgpaths = images)

    # # rename images with sequenced file names
    # # ex: 20230903_121501.jpg -> 20230903_121501_000011.jpg
    # exec_multithread(func = rename_image, items = sequeced_imgs, max_workers=2)

    # # list images which are sequenced
    # sequeced_imgs = [img for img in os.listdir(IMG_PATH) if re.match(r'\d{8}_\d{12}_\d{6}.jpg', img)]

    # move images to their appropriate date directories
    exec_multithread(func = move_image, items = sequeced_imgs, max_workers=2)


def remove_leading(text: str, char: str):
    """
    Removes leading char from text
    """
    if not all([text, char]):
        return 0
    
    if not text.startswith(char):
        return text
    
    return remove_leading(text[1:], char)


def get_images(imgdate: str, time_st: str, time_en: str) -> list:
    """
    Gets list of images based on the date filter specified

    Params:
        imgdate - Image date (yyyy-mm-dd)
        time_st - Start time (hh:mm)
        time_en - End time (hh:mm)
    """

    datedir = imgdate.replace('-','')
    # return 404 img if directory doesn't exist
    if not os.path.exists(os.path.join(IMG_PATH, datedir)):
        log.info(f'[imgdate: {imgdate} ({time_st} - {time_en})] No images found')
        return []
    
    t_st = int(remove_leading(time_st.replace(':',''),'0'))
    t_en = int(remove_leading(time_en.replace(':', ''), '0'))
    
    images = []
    try:
        # get images from the date dir
        for img in os.listdir(os.path.join(IMG_PATH, datedir)):
            if img.endswith('.jpg'):
                log.debug(f'Image: {img}')
                # get hh:min from image time
                img_time = int(remove_leading(img.split('_')[1][:4], '0'))
                if img_time >= t_st and img_time <= t_en:
                    images.append(img)
    except Exception as ex:
        log.error(f'[imgdate: {imgdate} ({time_st} - {time_en})] Error filtering image - {ex.__class__.__name__} - {str(ex)} ')
        return []
    
    if not images:
        log.info(f'[imgdate: {imgdate} ({time_st} - {time_en})] No images found')
        return []
    
    # sort images based on the sequence number
    images.sort(key=lambda imgf: imgf.replace('.jpg','').split('_')[-1])

    # IMG_PATH/20230903
    imgdirpath = os.path.join(IMG_PATH, datedir)
    images = [os.path.join(imgdirpath, img) for img in images]

    return images


def stream_images(images: list[str], delay: int = 0.2):
    """
    Streams list of images
    """
    if not images:
        return b''

    for img in images:

        imgdata = b''
        with open(img, 'rb') as imgfh:
            imgdata = imgfh.read()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+ imgdata + b'\r\n'
        )
        time.sleep(delay)


def get_err404_image():
    """
    Returns image for error 404
    """
    imgdata = b''
    with open(ERROR404_IMG_PATH, 'rb') as imgfh:
        imgdata = imgfh.read()
        # imgdata = b'--frame\r\nContent-Type: image/png\r\n\r\n'+ imgdata + b'\r\n'
        
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'+ imgdata + b'\r\n'
    )