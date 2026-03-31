import os
from Bio import SeqIO
from Bio.SeqFeature import FeatureLocation
import openpyxl as xl

gbff_dir = r"input/genome_gbff/"
gbff_files = [f for f in os.listdir(gbff_dir) if f.endswith(".gbff")]
gbff_file = os.path.join(gbff_dir, gbff_files[0])
excel_path = r"tmp_output/gbff_function.xlsx"

records = SeqIO.parse(gbff_file, "genbank")

workbook = xl.Workbook()
sheet = workbook.active
sheet.title = "Sheet1"
sheet.append(["locus_tag", "product","translation",  "protein_id", "gene", "location_start","location_end","Strand","pseudo"])

for record in records:
    for feature in record.features:
        if feature.type == "CDS":

            information_list = []

            gene = feature.qualifiers.get("gene", [""])[0]
            product = feature.qualifiers.get("product", [""])[0]
            locus_tag = feature.qualifiers.get("locus_tag", [""])[0]
            protein_id = feature.qualifiers.get("protein_id", [""])[0]
            translation = feature.qualifiers.get("translation", [""])[0]
            pseudo = feature.qualifiers.get("pseudo", "0")[0]


            location = feature.location
            # start = location.start.position + 1
            start = location.start + 1
            # end = location.end.position
            end = location.end
            
            if location.strand == 1 :
                strand = "+"
            elif location.strand == -1:
                strand = "-"

            if pseudo == "":
                pseudo_output = True
            elif pseudo == "0":
                pseudo_output = False

            # print("location:", location)
            # print("gene:", gene)
            # print("locus_tag:", locus_tag)
            # print("product:", product)
            # print("protein_id:", protein_id)
            # print("translation:", translation)

            information_list.append(locus_tag)
            information_list.append(product)
            information_list.append(translation)
            information_list.append(protein_id)
            information_list.append(gene)
            information_list.append(str(start))
            information_list.append(str(end))
            information_list.append(str(strand))
            information_list.append(str(pseudo_output))
            sheet.append(information_list)

workbook.save(excel_path)

