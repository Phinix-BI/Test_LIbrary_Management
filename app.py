from flask import Flask, render_template, request, jsonify
import pandas as pd
from Backend_Scripts.rendered import pdf_to_image   
from Backend_Scripts.Basic_Logic import Library
import os

app = Flask(__name__)

# Assuming you have your DataFrame named 'books_df'
books_df = pd.read_pickle('Server/New_Library.lib')
IMAGE_DIR = os.path.join("static", "Images")

# def get_last_page_image(id, page):
#     book_path = books_df.loc[books_df['ID'] == id, 'Path'].iloc[0]
#     pdf_to_image(book_path, page, 150)
#     last_page_image_path = os.path.join(IMAGE_DIR, f"{page}.png")
#     return last_page_image_path


# Route to render main.html
@app.route('/')
def index():
    # Render main.html with books data
    return render_template('main.html', books=books_df.to_dict('records'))

# Route to render reader.html with book ID
@app.route('/reader/<book_id>')
def reader(book_id):
    book_row = books_df[books_df['ID'] == book_id]
    if not book_row.empty:
        last_page = book_row.iloc[0]['Last_page']
        book_path = book_row.iloc[0]['Path']
        last_page_image_path = str(pdf_to_image(book_path, last_page, 150))
        print(f"Path to Image: {last_page_image_path}")
        return render_template('reader.html', book_id=book_id, last_page_image=last_page_image_path)
    else:
        return "Book not found"


if __name__ == '__main__':
    app.run(debug=True)
