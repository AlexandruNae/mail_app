import os
import PyPDF2


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

            char_buffer += page_content

            while len(char_buffer) >= char_limit:
                # # Generate folder for each part
                # part_folder = f'{book_folder}/{book_alias}_{file_count}'
                # if not os.path.exists(part_folder):
                #     os.makedirs(part_folder)

                # Write the content to a txt file
                with open(f'{book_folder}/{book_alias}_{file_count}.txt', 'w', encoding='utf-8') as txt_file:
                    txt_file.write(char_buffer[:char_limit])

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
    pdf_path = 'C:\\Users\\alexn\\PycharmProjects\\mail_app_scripts\\process_books\\book_pdf\\Harap_Alb_Ion_Creanga.pdf'  # Replace with your PDF path
    book_alias = 'harap_alb'  # Replace with your book alias
    book_title = 'Harap-Alb'  # Replace with your book title

    split_pdf_into_txt(pdf_path, book_alias, book_title)