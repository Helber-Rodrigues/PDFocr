from PIL import ImageFont, Image, ImageDraw
from pytesseract import Output
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Ajuste conforme o caminho do Tesseract

class TesseractOCR:
    def __init__(self):
        # Configuração para o Tesseract
        self.config_pytesseract = '--tessdata-dir assets/tessdata -l por --oem 3 --psm 3'
        self.font = r'../assets/font/calibri.ttf'  # Ajuste para o caminho da fonte desejada

    def read_text(self, img_path):
        """
        Extrai texto de uma imagem usando Tesseract OCR.
        """
        text, data = self.__get_text_from_img(img_path)
        return text, data

    def annotate_image(self, img_path, output_path):
        """
        Extrai texto de uma imagem e desenha caixas delimitadoras em torno do texto detectado.
        """
        text, data = self.__get_text_from_img(img_path)

        # Carregar a imagem usando PIL para anotar
        img = Image.open(img_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font, size=20) if self.font else None

        # Desenhar caixas delimitadoras
        for i in range(len(data['text'])):
            if data['text'][i].strip():  # Ignorar caixas vazias
                x, y, w, h = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
                draw.text((x, y - 20), data['text'][i], fill="blue", font=font)

        # Salvar a imagem anotada
        img.save(output_path)
        print(f"Imagem anotada salva em: {output_path}")

    def __get_text_from_img(self, img_path):
        """
        Função privada para processar a imagem e extrair texto com dados detalhados.
        """
        # Carregar a imagem usando OpenCV
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"A imagem {img_path} não foi encontrada ou não é válida.")

        # Converter para escala de cinza para melhorar a detecção
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Aplicar OCR
        data = pytesseract.image_to_data(gray, config=self.config_pytesseract, output_type=Output.DICT)
        text = pytesseract.image_to_string(gray, config=self.config_pytesseract)

        return text, data