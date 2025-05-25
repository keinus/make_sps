"""이미지 해상도 모듈"""
from PIL import Image


def get_image_details(file_path) -> tuple[tuple[int, int], int]:
    """이미지 파일의 해상도와 색상 비트를 반환합니다.
    이 함수는 주어진 파일 경로를 통해 이미지의 해상도와 색상 비트를 가져옵니다.
    PIL(Pillow) 라이브러리를 사용하여 이미지를 열고, 이미지의 크기(size)를 통해
    해상도를 추출합니다. 이미지의 모드(mode)를 확인하여 해당 모드에 맞는
    비트 수(bits per pixel)를 매핑한 후 반환합니다.

    Args:
        file_path (str): 이미지 파일 경로

    Returns:
        tuple: (해상도, 색상 비트) 형식의 튜플.
               이미지 파일이 아니거나 오류 발생 시 None을 반환합니다.
    """
    with Image.open(file_path) as img:
        width, height = img.size
        resolution = (width, height)

        # 색상 비트 확인
        mode_to_bpp = {
            '1': 1,
            'L': 8,
            'P': 8,
            'RGB': 24,
            'RGBA': 32,
            'CMYK': 32,
            'YCbCr': 24,
            'I': 32,
            'F': 32
        }
        color_bits = mode_to_bpp.get(img.mode, None)
        color_bits = color_bits if color_bits is not None else 0

        return resolution, color_bits
