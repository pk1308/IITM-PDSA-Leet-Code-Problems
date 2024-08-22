import os

import PyPDF2


def compress_pdf(input_path):
    with open(input_path, 'rb') as input_file:
        reader = PyPDF2.PdfFileReader(input_file)
        writer = PyPDF2.PdfFileWriter()

        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            page.compressContentStreams()  # Compress the content streams

            # Add the compressed page to the writer
            writer.addPage(page)
        output_path =  str(input_path)[:-3] + "cmp.pdf"
        # Write the compressed PDF to the output file
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        os.rename(output_file, input_path)

