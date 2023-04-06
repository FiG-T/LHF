import sys
import re

if len(sys.argv) != 2:
    print("Usage: python extract_genbank_info.py input_file")
    sys.exit()

input_file = sys.argv[1]
output_file = "genbank_output.tsv"

with open(input_file, "r") as f:
    with open(output_file, "w") as out:
        out.write("Accession\tOrganism\tCountry\tHaplogroup\tSequence\n")
        accession = ""
        organism = ""
        country = ""
        haplogroup = ""
        sequence = ""
        in_features = False
        in_source = False
        for line in f:
            line = line.strip()
            if line.startswith("ACCESSION"):
                accession = line.split()[1]
            elif line.startswith("  ORGANISM") or line.startswith("ORGANISM"):
                organism = line.split("  ")[-1].strip()
            elif line.startswith("  /country") or line.startswith("country"):
                country = line.split("=")[-1].strip().strip('"')
            elif line.startswith("SOURCE"):
                in_source = True
            elif line.startswith("FEATURES"):
                in_features = True
            elif line.startswith("ORIGIN"):
                sequence_lines = []
                for next_line in f:
                    if next_line.startswith("//"):
                        break
                    sequence_lines.append(next_line.strip())
                sequence = ''.join(sequence_lines)
                sequence = re.sub(r'\d', '', sequence)
                out.write(accession + "\t" + organism + "\t" + country + "\t" + haplogroup + "\t" + sequence + "\n")
                accession = ""
                organism = ""
                country = ""
                haplogroup = ""
                sequence = ""
                in_features = False
            elif in_features and "/country=" in line:
                country = line.split("=")[-1].strip().strip('"')
            elif in_source and "/haplogroup=" in line:
                haplogroup = line.split("=")[-1].strip().strip('"')
            elif line.startswith("//"):
                in_source = False
        if accession:
            out.write(accession + "\t" + organism + "\t" + country + "\t" + haplogroup + "\t" + sequence + "\n")

print("Extraction complete. Results saved to " + output_file + ".")
