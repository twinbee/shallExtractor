import csv
import PyPDF2
import re
import argparse

def extract_paragraphs_with_word(input_file, output_file, word='shall'):
    pdf_text = ""
    with open(input_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()

    sections = re.split(r'\n(?=\d+\.\s)', pdf_text)  # Split into sections based on section numbering

    rows = []
    for section in sections:
        lines = section.strip().split('\n')
        section_num = lines[0].split('.')[0]
        section_desc = ' '.join(lines[0].split('.')[1:]).strip()
        sentences = [line for line in lines[1:] if word in line.lower()]
        for sentence in sentences:
            rows.append([section_num, section_desc, sentence.strip()])

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Section Number', 'Section Description', 'Sentence with "{}"'.format(word)])
        for row in rows:
            csvwriter.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract sentences containing a specific word from a PDF file and save them in a CSV file.')
    parser.add_argument('input_pdf', help='Path to the input PDF file')
    parser.add_argument('output_csv', nargs='?', help='Path to the output CSV file. If not specified, the name of the PDF file with .csv extension will be used.')

    args = parser.parse_args()
    input_pdf_path = args.input_pdf
    output_csv_path = args.output_csv or (input_pdf_path[:-4] + '.csv')

    extract_paragraphs_with_word(input_pdf_path, output_csv_path)

