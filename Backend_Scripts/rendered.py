import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

def pdf_to_image(pdf_path, page_number, dpi):
    # Open the PDF file
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        
        # Convert the specified page to an image
        images = convert_from_path(pdf_path, dpi=dpi, first_page=page_number, last_page=page_number)
        
        # Get the path to the static/Images directory
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reader', 'static', 'Images')
        os.makedirs(static_dir, exist_ok=True)
        
        # Save the image in the static/Images directory
        image_path = os.path.join(static_dir, f"{page_number}.png")
        images[0].save(image_path, 'PNG')
        
        # Return the relative path from the static directory
        return os.path.relpath(image_path, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))