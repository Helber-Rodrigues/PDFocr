from pdf2image import convert_from_path
import pytesseract
from fpdf import FPDF
from unidecode import unidecode
import os

# Configurações iniciais
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Ajuste conforme necessário
input_pdf = r"C:\PDF\Entrada\export.pdf"  # Caminho do PDF de entrada
output_pdf = r"C:\PDF\Saida\output.pdf"  # Caminho do PDF de saída
temp_image_folder = 'temp_images'  # Pasta temporária para armazenar as imagens

# Criar a pasta temporária para armazenar as imagens
if not os.path.exists(temp_image_folder):
    os.makedirs(temp_image_folder)

# Converter cada página do PDF em imagem
print("Convertendo as páginas do PDF para imagens...")
pages = convert_from_path(input_pdf, dpi=300, output_folder=temp_image_folder, fmt='jpeg')

# Inicializar o PDF para saída
pdf = FPDF()

# Processar cada página
print("Aplicando OCR nas imagens e gerando o novo PDF...")
for i, page_image in enumerate(pages):
    # Salvar a imagem temporária
    image_path = os.path.join(temp_image_folder, f'page_{i + 1}.jpeg')
    page_image.save(image_path, 'JPEG')

    # Aplicar OCR para extrair texto
    text = pytesseract.image_to_string(image_path, lang='por')
    text = unidecode(text)  # Normalizar caracteres especiais

    # Adicionar uma nova página ao PDF
    pdf.add_page()

    # Adicionar a imagem como fundo da página
    pdf.image(image_path, x=0, y=0, w=210, h=297)  # Ajuste para A4 (210x297 mm)

    # Adicionar o texto extraído sobre a imagem
    pdf.set_font('Helvetica', size=12)
    pdf.set_text_color(0, 0, 0)  # Cor preta
    pdf.set_xy(10, 10)  # Posição inicial (10mm de margem superior e esquerda)
    pdf.multi_cell(190, 10, text)  # Largura ajustada (210 - 2x10mm)

# Salvar o PDF de saída
pdf.output(output_pdf)
print(f"PDF gerado com sucesso: {output_pdf}")

# Limpar os arquivos temporários
print("Limpando arquivos temporários...")
for file in os.listdir(temp_image_folder):
    os.remove(os.path.join(temp_image_folder, file))
os.rmdir(temp_image_folder)

print("Processo concluído.")