# shallExtractor
Reads in a natural-language document containing requirements. Spits out a CSV Requirements Matrix by extracting every line with a 'shall', 'should', 'must' or 'will' in it, arranged with section headings. 

# Prerequisites

`pip install 'PyPDF2<3.0'`

Any version after 3.0 will throw an error.


# Usage

`python script_name.py input_file.pdf output_file.csv --search-word shall`



