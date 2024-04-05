from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
from Backend_Scripts.additional import pdf_to_image  
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
    return render_template('main.html', books=books_df.to_dict('records'), books_name = books_df['Name'].tolist())

# Route to render reader.html with book IDc
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

        last_page_image_path = str(pdf_to_image(book_path, int(last_page), 150))
        return render_template('reader.html', book_id=book_id, last_page_image=last_page_image_path, last_page=last_page, book_name=book_name, book_author=book_author)
    else:
        return "Book not found"
    

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    return render_template('add_book.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', books=books_df.to_dict('records'), books_name = books_df['Name'].tolist())






@app.route('/reset', methods=['POST'])
def reset_page():
    # Retrieve the book_id from the form submission
    book_id = request.form.get('book_id')
    
    if book_id:
        # Add code here to reset the page
        # For example:
        # Reset the last page to the initial page
        initial_page = 1
        books_df.loc[books_df['ID'] == book_id, 'Last_page'] = initial_page
        
        # Redirect to the reader route with the book ID
        return redirect(f"/reader/{book_id}/undefined")
    else:
        # Handle the case when book_id is not provided
        return "Book ID not provided"
    
@app.route('/fullscreen', methods=['POST'])
def fullscreen():
    # Retrieve the book_id from the form data
    book_id = request.form.get('book_id')
    path = books_df.loc[books_df['ID'] == book_id].iloc[0]['Path']
    page_number = books_df.loc[books_df['ID'] == book_id].iloc[0]['Last_page']

    # Ensure that the book_id is not None
    if book_id is not None:        
        # Send the PDF file to the browser for display
        url = f"{path}#page={page_number}"
        return send_file(path, mimetype='application/pdf', as_attachment=False)
    else:
        # Handle the case when book_id is not provided
        return "Book ID not provided"
    

@app.route('/gotopage', methods=['POST'])
def gotopage():
    page = request.form.get('page')
    print(page)
    book_id = request.form.get('book_id')
    if page == 1:
        page = "undefined"

    return redirect(f"/reader/{book_id}/{page}")
    


if __name__ == '__main__':
    app.run(debug=True)
