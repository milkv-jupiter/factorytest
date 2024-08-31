from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer, QObject
from PIL.ImageQt import ImageQt
import os
import qrcode

def get_product_name():
    path = '/proc/device-tree/model'
    if os.path.exists(path):
        with open(path, 'r') as f:
            model = f.readline().strip(b'\0x00'.decode())
            return model.replace('spacemit', '').replace('board', '').strip()

def create_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    qt_image = ImageQt(img).convertToFormat(QImage.Format_RGB32)
    return QPixmap.fromImage(qt_image)

