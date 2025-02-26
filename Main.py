from pdf2image import convert_from_path
import pytesseract
from fpdf import FPDF
from unidecode import unidecode
import os

from tesseract_ocr import TesseractOCR

# Configurações iniciais
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\tesseract.exe'  # Altere conforme o caminho do Tesseract na sua máquina
input_pdf = r"C:\PDF\Entrada\export.pdf"  # Caminho do PDF de entrada
output_pdf = r"C:\PDF\Saida\output.pdf"  # Nome do PDF de saída
temp_image_folder = 'temp_images'  # Pasta temporária para salvar as imagens
ocr = TesseractOCR()  # Instancia a classe OCR

# Criar a pasta temporária para armazenar as imagens, se não existir
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
    # Salvar imagem temporária
    image_path = os.path.join(temp_image_folder, f'page_{i + 1}.jpeg')
    page_image.save(image_path, 'JPEG')

    # Aplicar OCR para extrair texto
    text, _ = ocr.read_text(image_path)  # Obtemos o texto e os dados detalhados

    # Processar texto para remover ou substituir caracteres incompatíveis
    text = unidecode(text)  # Remove acentos e normaliza caracteres especiais

    # Adicionar a página ao novo PDF
    pdf.add_page()
    pdf.set_font('Helvetica', size=0)
    pdf.multi_cell(0, 6, text)  # Ajusta automaticamente o texto em múltiplas linhas

# Salvar o PDF de saída
pdf.output(output_pdf)
print(f"PDF gerado com sucesso: {output_pdf}")

# Limpar arquivos temporários
print("Limpando arquivos temporários...")
for file in os.listdir(temp_image_folder):
    os.remove(os.path.join(temp_image_folder, file))
os.rmdir(temp_image_folder)

print("Processo concluído.")