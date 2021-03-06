#!/usr/bin/env python
"""
A simple parser for the NCBI gene info format.

Version 1.0
"""
from __future__ import with_statement
from collections import namedtuple
import gzip
from datetime import datetime

__author__  = "Uli Koehler"
__license__ = "Apache License v2.0"

#Initialized GeneInfo named tuple. Note: namedtuple is immutable
geneInfoFields = ["tax_id", "gene_id", "symbol", "locus_tag", "synonyms", "db_xrefs", "chromosome", "map_location", "description", "type_of_gene", "symbol_from_nomenclature_authority", "full_name_from_nomenclature_authority", "nomenclature_status", "other_designations", "modification_date"]
GeneInfo = namedtuple("GeneInfo", geneInfoFields)

def parseDBXrefs(xrefs):
    """Parse a DB xref string like HGNC:5|MIM:138670 to a dictionary"""
    #Split by |, split results by :. Create a dict (python 2.6 compatible way).
    if xrefs == "-": return {}
    return dict([(xrefParts[0], xrefParts[2])
                for xrefParts in (xref.partition(":")
                  for xref in xrefs.split("|"))])

def parseNCBIGeneInfo(filename):
    """
    A NCBI gene info format parser.
    Yields objects that contain info about a single gene.
    
    Supports transparent gzip decompression
    """
    #Parse with transparent decompression
    openFunc = gzip.open if filename.endswith(".gz") else open
    with openFunc(filename) as infile:
        for line in infile:
            if line.startswith("#"): continue
            parts = line.strip().split("\t")
            #If this fails, the format is not standard-compatible
            assert len(parts) == len(geneInfoFields)
            #Normalize data
            normalizedInfo = {
                "tax_id": int(parts[0]),
                "gene_id": int(parts[1]),
                "symbol": parts[2],
                "locus_tag": None if parts[3] == "-" else parts[3],
                "synonyms": [] if parts[4] == "-" else parts[4].split("|"),
                "db_xrefs": parseDBXrefs(parts[5]),
                "chromosome": parts[6],
                "map_location": parts[7],
                "description": parts[8],
                "type_of_gene": parts[9],
                "symbol_from_nomenclature_authority": None if parts[10] == "-" else parts[10],
                "full_name_from_nomenclature_authority": None if parts[11] == "-" else parts[11],
                "nomenclature_status": None if parts[12] == "-" else parts[12],
                "other_designations": None if parts[13] == "-" else parts[13],
                "modification_date": datetime.strptime(parts[14], "%Y%m%d")
            }
            #Alternatively, you can emit the dictionary here, if you need mutability:
            #    yield normalizedInfo
            yield GeneInfo(**normalizedInfo)
            

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("geneinfo_file", help="The NCBI GeneInfo input file (.gz allowed)")
    parser.add_argument("--print-records", action="store_true", help="Print all GeneInfo objects, not only")
    args = parser.parse_args()
    #Execute the parser
    recordCount = 0
    for geneInfo in parseNCBIGeneInfo(args.geneinfo_file):
        if args.print_records: print geneInfo
        #Access records like this: my_gene_id = geneInfo.gene_id
        recordCount += 1
    print "Total records: %d" % recordCount
        