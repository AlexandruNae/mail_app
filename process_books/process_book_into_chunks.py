import os
import PyPDF2
from src.utils import title_to_alias

def split_pdf_into_txt(pdf_path, book_alias, book_title, char_limit=5000):
    # Create the main folder 'lecture' if not exist
    if not os.path.exists('../lectures'):
        os.makedirs('../lectures')

    # Create the book folder
    book_folder = f'../lectures/{book_alias}'
    if not os.path.exists(book_folder):
        os.makedirs(book_folder)

    # Read PDF
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

        char_buffer = ""
        file_count = 1

        for i in range(total_pages):
            # Get content of each page
            page = reader.pages[i]
            page_content = page.extract_text()
            page_content = page_content.replace(' -', '-')
            page_content = page_content.replace('-\n', '-')
            page_content = page_content.replace('  —', '\n—')

            char_buffer += page_content

            while len(char_buffer) >= char_limit:
                # # Generate folder for each part
                # part_folder = f'{book_folder}/{book_title}_{file_count}'
                # if not os.path.exists(part_folder):
                #     os.makedirs(part_folder)

                # Write the content to a txt file
                with open(f'{book_folder}/{book_alias}_{file_count}.txt', 'w', encoding='utf-8') as txt_file:
                    txt_file.write('\n' + char_buffer[:char_limit])

                # Update char_buffer and file_count
                char_buffer = char_buffer[char_limit:]
                file_count += 1

        # Handle any remaining text
        if char_buffer:
            # part_folder = f'{book_folder}/{book_alias}_{file_count}'
            # if not os.path.exists(part_folder):
            #     os.makedirs(part_folder)

            with open(f'{book_folder}/{book_alias}_{file_count}.txt', 'w', encoding='utf-8') as txt_file:
                txt_file.write(page_content)


if __name__ == "__main__":
    # Assume the current working directory is 'mail_app_scripts'
    # Construct the relative path to the PDF within the project directory
    pdf_relative_path = os.path.join('book_pdf', 'Harap_Alb_Ion_Creanga.pdf')

    # Get the absolute path of the current script (which is in 'mail_app_scripts')
    project_directory = os.path.dirname(os.path.abspath(__file__))

    # Combine the project directory with the relative path to get the full path to the PDF
    pdf_path = os.path.join(project_directory, pdf_relative_path)


    book_title = 'Harap-Alb'  # Replace with your book title
    book_alias = title_to_alias(book_title)

    split_pdf_into_txt(pdf_path, book_alias, book_title)