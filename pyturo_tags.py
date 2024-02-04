# https://pypi.org/project/collective.documentgenerator/
# https://appyframe.work/19

import sys
import argparse
import csv
import qrcode

from pathlib import Path
from appy.pod.renderer import Renderer

class Post:
    def __init__(self, route, name, code, uri, description):
        self.route = route
        self.name = name
        self.code = code
        self.uri = uri
        self.description = description
    def get_qr_file_name(self):
        """Return file name for QR image"""
        return self.name.lower() + ".png"
    def get_qr_file(self):
        """Create file object for QR image file"""
        qr_file = Path(self.get_qr_file_name())
        if not qr_file.exists():
            print("File does not exist!")
            self.create_qr_image()
        return qr_file
    def create_qr_image(self):
        """Create QR image from self.uri and save to file"""
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr_code.add_data(self.uri)
        qr_code.make(fit=True)

        img = qr_code.make_image(fill_color="black", back_color="white")

        type(img)  # qrcode.image.pil.PilImage
        img.save(self.get_qr_file_name())
        return img

def read_posts_from_file(file_path):
    """Read post info from file and return as array of Post objects
       CSV: Tur,Navn,Kode,Poeng,QR,Beskrivelse"""
    post_array = []
    with open(file_path, 'r', encoding="utf-8") as csvfile:
        postreader = csv.DictReader(csvfile, delimiter=',')
        for row in postreader:
            post = Post(
                route=row['Tur'],
                name=row['Navn'],
                code=row['Kode'],
                uri=row['QR'],
                description=row['Beskrivelse']
            )
            post_array.append(post)
    return post_array


def _main():
    parser = argparse.ArgumentParser(description='Generate QR-codes for tur-O')

    parser.add_argument(
        '-c', '--csvfile', type=str, help='CSV file with tur-o post information', required=True,
    )

    args = parser.parse_args()

    posts = read_posts_from_file(args.csvfile)

    for post in posts:
        post.create_qr_image()

    pod_context =  {'read_posts_from_file': read_posts_from_file,
                    'posts': posts}

    tag_doc_name = Path(args.csvfile).with_suffix('.odt').name

    renderer = Renderer('turo_tags_template.odt', pod_context, tag_doc_name, overwriteExisting=True)
    renderer.run()

if __name__ == "__main__":
    sys.exit(_main())
