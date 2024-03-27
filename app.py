from flask import Flask, render_template, request, jsonify
import pandas as pd
from Backend_Scripts.rendered import pdf_to_image   
from Backend_Scripts.Basic_Logic import Library
import os

app = Flask(__name__)

# Assuming you have your DataFrame named 'books_df'
books_df = pd.read_pickle('Server/New_Library.lib')
IMAGE_DIR = os.path.join("static", "Images")

# Route to render main.html
@app.route('/')
def index():
    # Render main.html with books data
    return render_template('main.html', books=books_df.to_dict('records'))

# Route to render reader.html with book ID
@app.route('/reader/<book_id>')
@app.route('/reader/<book_id>/<last_page>')
def reader(book_id, last_page=None):
    book_row = books_df[books_df['ID'] == book_id]
    if not book_row.empty:
        book_path = book_row.iloc[0]['Path']
        book_name = book_row.iloc[0]['Name']
        book_author = book_row.iloc[0]['Author']
        if last_page == "undefined":
            last_page = book_row.iloc[0]['Last_page']  # Use last page from .lib file if not provided in URL

        books_df.loc[books_df['ID'] == book_id, 'Last_page'] = last_page
        pd.to_pickle(books_df, "Server/New_Library.lib")
        print(books_df)

        print(last_page)
        last_page_image_path = str(pdf_to_image(book_path, int(last_page), 150))
        print(f"Path to Image: {last_page_image_path}")
        return render_template('reader.html', book_id=book_id, last_page_image=last_page_image_path, last_page=last_page, book_name=book_name, book_author=book_author)
    else:
        return "Book not found"


if __name__ == '__main__':
    app.run(debug=True)
