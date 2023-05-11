"""pyturo.py
A python script for generating QR code images that can be used
for turorientering.
"""

import argparse
import qrcode

def create_qrcode(data: str, file_name: str):
    """Function generating QR code image from function arguments."""
    qr_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr_code.add_data(data)
    qr_code.make(fit=True)

    img = qr_code.make_image(fill_color="black", back_color="white")

    if not file_name.endswith(".png"):
        file_name += ".png"

    type(img)  # qrcode.image.pil.PilImage
    img.save(file_name)

def parse_csv_file(csv_file: str):
    """Function generating QR code images from data in CSV file."""
    with open(csv_file, encoding="utf-8") as file:
        for line in file:
            post_info = line.split(',')
            if post_info[1] == "Navn":
                # This is the file content heading
                continue
            create_qrcode(data=post_info[4], file_name=post_info[1].lower())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate QR-codes for tur-O')

    parser.add_argument(
        '-u', '--url', type=str, help='URL for post', required=False,
    )
    parser.add_argument(
        '-f', '--file_name', type=str, help='File name of the generated image', required=False,
    )
    parser.add_argument(
        '-c', '--csv_file', type=str, help='CSV file with tur-o post information', required=False,
    )

    args = parser.parse_args()

    if args.csv_file:
        parse_csv_file(csv_file=args.csv_file)
    else:
        create_qrcode(data=args.url, file_name=args.file_name)
