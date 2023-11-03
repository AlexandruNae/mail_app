import os
import PyPDF2
from src.utils import title_to_alias

import fitz  # PyMuPDF
from src.utils import title_to_alias


def normalize_page_content(page_content, min_words_per_line=3):
    lines = page_content.split('\n')
    normalized_lines = []
    current_line = ''

    for line in lines:
        line = line
        if line.startswith('–'):  # Dacă linia începe cu "–", o tratăm ca un început de linie nouă
            if current_line:  # Dacă avem text în current_line, îl adăugăm la rezultat
                normalized_lines.append(current_line)
                current_line = line  # Începem o nouă linie cu textul curent
            else:
                normalized_lines.append(line)  # Dacă current_line e gol, pur și simplu adăugăm linia
        else:
            words = line.split()
            # Concatenăm cu linia curentă doar dacă nu va deveni prea lungă
            if len(words) < min_words_per_line and (len(current_line.split()) + len(words) <= min_words_per_line):
                current_line += (' ' if current_line else '') + line
            else:  # Dacă linia e suficient de lungă, o tratăm ca o linie separată
                if current_line:  # Dacă current_line are conținut, îl adăugăm la rezultat
                    normalized_lines.append(current_line)
                current_line = line

    # Adăugăm orice conținut rămas în current_line
    if current_line:
        normalized_lines.append(current_line)

    return '\n'.join(normalized_lines)


def split_pdf_into_txt(pdf_path, book_alias, book_title, char_limit=8000):
    # Create the main folder 'lectures' if not exist
    if not os.path.exists('../lectures'):
        os.makedirs('../lectures')

    # Create the book folder
    book_folder = f'../lectures/{book_alias}'
    if not os.path.exists(book_folder):
        os.makedirs(book_folder)

    # Open PDF
    with fitz.open(pdf_path) as pdf:
        char_buffer = ""
        file_count = 1

        for page in pdf:
            # Get content of each page
            page_content = page.get_text()

            # Normalize the content of the page
            page_content = normalize_page_content(page_content)

            char_buffer += page_content

            # Check if the buffer exceeds the character limit and split accordingly
            while len(char_buffer) >= char_limit:
                split_index = char_buffer.rfind('\n', 0, char_limit)
                if split_index == -1:
                    split_index = char_limit

                # Write the content to a txt file
                with open(f'{book_folder}/{book_alias}_{file_count}.txt', 'w', encoding='utf-8') as txt_file:
                    txt_file.write(char_buffer[:split_index])

                # Update char_buffer and file_count
                char_buffer = char_buffer[split_index:]
                file_count += 1

        # Handle any remaining text
        if char_buffer.strip():
            with open(f'{book_folder}/{book_alias}_{file_count}.txt', 'w', encoding='utf-8') as txt_file:
                txt_file.write(char_buffer)

if __name__ == "__main__":
    # Assume the current working directory is 'mail_app_scripts'
    # Construct the relative path to the PDF within the project directory
    pdf_relative_path = os.path.join('book_pdf', 'Moromeții_I.pdf')

    # Get the absolute path of the current script (which is in 'mail_app_scripts')
    project_directory = os.path.dirname(os.path.abspath(__file__))

    # Combine the project directory with the relative path to get the full path to the PDF
    pdf_path = os.path.join(project_directory, pdf_relative_path)


    book_title = 'Moromeții I'  # Replace with your book title
    book_alias = title_to_alias(book_title)

    split_pdf_into_txt(pdf_path, book_alias, book_title)