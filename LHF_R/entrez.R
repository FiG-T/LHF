### Project LHF - Attempting to use E-Utilities & Entrez 

#  After unsuccessful attempts to download the required GenBank files and sequences from
#  the NCBI website interface I have decided to try and use the API (known as Entrez)... 

install.packages("rentrez")
library(rentrez)

#  NCBI default is 3 requests per second - this may result in large requests taking a long
#  time to process.  This can be improved to 10 requests per second once you register for 
#  a (personal) API key (available once you sign up for an NCBI account). 

set_entrez_key("f5ff2d14bbc152047694a55253157602b507")
  # set the key for each session

entrez_dbs()
  # list all available databases

entrez_db_searchable("nucleotide")
  # list which features you can include in your search (here for the nucleotide database)

mtDNA_search <- entrez_search(
  db = "nucleotide",
  term = "(mitochondria[All Fields] OR mitochondrion[All Fields])
  AND Homo sapiens[porgn] AND (15400[SLEN] : 17000[SLEN])"
  )

mitomap_search <- entrez_search(
  db = "nucleotide",
  term = "(00000015400[SLEN] : 00000016600[SLEN]) AND Homo[Organism] AND mitochondrion
  [FILT] NOT ((Homo sapiens subsp. 'Denisova'[Organism] OR Homo sp. Altai[All Fields]) 
  OR (Homo sapiens subsp. 'Denisova'[Organism] OR Denisova hominin[All Fields]) OR
  neanderthalensis[All Fields] OR heidelbergensis[All Fields] OR consensus[All Fields] 
  OR (ancient[All Fields] AND (Homo sapiens[Organism] OR human[All Fields]) AND remains
  [All Fields])) AND (15400[SLEN] : 17000[SLEN])"
)
  
mtDNA_search$ids

mtDNA_summary <- entrez_summary(
  db = "nucleotide", 
  id = mtDNA_search$ids
  )
mtDNA_summary
extract_from_esummary(mtDNA_summary, "moltype")
