import re   # Import the regular expressions (regex) module
import sys  # Import the system module

# Define a regular expression to match the information we want to extract
 # This regex is looking for specific pieces of information within each GenBank record
 # Specifically, it's looking for the accession number, organism name, country location, and sequence data
 # The (?P<group_name>...) syntax defines a named capturing group in the regex
regex = re.compile(r'^ACCESSION\s+(?P<accession>\w+).*\n'
                   r'^ORGANISM\s+(?P<organism>.+?)\s*\n'
                   r'^COUNTRY\s+(?P<country>.+?)\s*\n'
                   r'^ORIGIN\s+(?P<sequence>[a-zA-Z\s]+)\n//\n',
                   re.MULTILINE | re.DOTALL)

# Read in the GenBank file
 # This line reads the contents of the file specified in the command line argument into a variable called gb_data
 # sys.argv is a list that contains the command line arguments passed to the script
 # The [1] index specifies the second item in the list, which should be the path to the GenBank file
with open(sys.argv[1], 'r') as infile:
    gb_data = infile.read()

# Search for matches using the regular expression
 # This line searches the contents of the gb_data variable for matches to the regex pattern
 # finditer() returns an iterator that yields match objects, which contain the matched text and group data
matches = regex.finditer(gb_data)

# Write out the extracted information to a new file
 # This loop iterates over each match object yielded by the regex search
 # For each match, it extracts the accession number, organism name, country location, and sequence data using the named capturing groups in the regex
 # It then prints out these values separated by tabs
 # for match in matches:
with open('extracted_gb_info.txt', 'w') as outfile:
    for match in matches:
        accession = match.group('accession')
        organism = match.group('organism')
        country = match.group('country')
        sequence = match.group('sequence').replace(' ', '').replace('\n', '')
        outfile.write(f'{accession}\t{organism}\t{country}\t{sequence}\n')
