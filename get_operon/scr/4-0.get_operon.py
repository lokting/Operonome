#warning: search the first localtag in every sheet，attention for if the first localtag-last localtag  first localtag-second localtag situatation exists.

#only for chromosome operon

import openpyxl as xl


input_pearson_num_txt = r"tmp_output/gene_PCC.txt"
input_excel_path = r"tmp_output/gff.xlsx" 
output_operon_gene = r'output/operon-gene.xlsx'
chr_list_file = r'input/chr_list.txt'

def read_list_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]
    
#chromosome sheetID
chr_list = read_list_from_file(chr_list_file)

#{localtag1-localtag2:pearson_num}
pearson_num_dict = {}
with open(input_pearson_num_txt) as pearson_num:
    for i in pearson_num:
        line = i.split("\t")
        localtag_count = line[0]
        pearson_num_count = line[1]
        pearson_num_dict[localtag_count] = pearson_num_count

inter_localtag_list_small = []
inter_localtag_dict = {}
operon_num = 1
workbook = xl.load_workbook(input_excel_path)
# for sheet_name in workbook.sheetnames:
for sheet_name in chr_list:
    worksheet = workbook[sheet_name]
    num = 1
    finial = worksheet.max_row #sheet number
    while num<finial:
        operon = "openon_" + str(operon_num)
        num = num + 1

        if num == finial:
            cell_last_localtag = worksheet["E"+str(num)]
            last_localtag = cell_last_localtag.value
            cell_next_localtag = worksheet["E"+str(2)]
            next_localtag = cell_next_localtag.value
            inter_localtag = last_localtag + "-" + next_localtag
            pearson_num_inter = float(pearson_num_dict[inter_localtag]) #获得PCC(float)
            cell_intergap = worksheet["G"+str(num)]
            intergap = int(cell_intergap.value) #get intergene distance（int）
        else:
            cell_last_localtag = worksheet["E"+str(num)]
            last_localtag = cell_last_localtag.value
            cell_next_localtag = worksheet["E"+str(num + 1)]
            next_localtag = cell_next_localtag.value
            inter_localtag = last_localtag + "-" + next_localtag
            pearson_num_inter = float(pearson_num_dict[inter_localtag]) #获得PCC(float)
            cell_intergap = worksheet["G"+str(num)]
            intergap = int(cell_intergap.value) #get intergene distance（int）


        #PCC=nan indicates psuedo gene,no relations
        if pearson_num_inter == "nan": 
            #get operon gene organization ,no repeat, keep the gene order
            localtag_new_list = []
            if inter_localtag_list_small != []:
                for localtag_new in inter_localtag_list_small:
                    if localtag_new not in localtag_new_list:
                        localtag_new_list.append(localtag_new)
                inter_localtag_dict[operon] = localtag_new_list
            localtag_new_list = []
            inter_localtag_list_small = []
            operon_num = operon_num + 1
        #if satisfy one of the conditon,we consider the two genes have relations
        elif (intergap <= 10) or (intergap <= 50 and pearson_num_inter > 0.5)or (intergap <= 100 and pearson_num_inter > 0.6)or (intergap <= 200 and pearson_num_inter > 0.7)or (intergap <= 500 and pearson_num_inter > 0.8):
            inter_localtag_list_small.append(last_localtag)
            inter_localtag_list_small.append(next_localtag)
            #last localtag
            if num == finial:
                 #get operon gene organization ,no repeat, keep the gene order
                localtag_new_list = []
                if inter_localtag_list_small != []:
                    for localtag_new in inter_localtag_list_small:
                        if localtag_new not in localtag_new_list:
                            localtag_new_list.append(localtag_new)
                    inter_localtag_dict[operon] = localtag_new_list
                localtag_new_list = []
                inter_localtag_list_small = []
                operon_num = operon_num + 1
        #the two genes dont have relations
        else:
             #get operon gene organization ,no repeat, keep the gene order
            localtag_new_list = []
            if inter_localtag_list_small != []:
                for localtag_new in inter_localtag_list_small:
                    if localtag_new not in localtag_new_list:
                        localtag_new_list.append(localtag_new)
                inter_localtag_dict[operon] = localtag_new_list
            localtag_new_list = []
            inter_localtag_list_small = []
            operon_num = operon_num + 1


#get localtag has been grouped
localtag_many_list = []
localtag_output_list = []
for key_1,value_1 in inter_localtag_dict.items():
    localtag_output_list.append(value_1)
    localtag_many_list.extend(value_1)

#get all localtag in excel file
localtag_all_list = []
workbook = xl.load_workbook(input_excel_path)
# for sheet_name in workbook.sheetnames:
for sheet_name in chr_list :
    worksheet = workbook[sheet_name]
    num = 1
    finial = worksheet.max_row 
    while num<finial:
        num = num + 1
        cell_localtag = worksheet["E"+str(num)]
        localtag = cell_localtag.value
        localtag_all_list.append(localtag)
print("localtag_all_list")
print(len(localtag_all_list))

single_localtag_list = list( set(localtag_all_list) - set(localtag_many_list) )

localtag_output_list.extend(single_localtag_list)
print("localtag_output_list")
print(len(localtag_output_list))

str_new = ","
workbook_excel = xl.Workbook()
workbook_excel.create_sheet("Sheet")
worksheeet_excel = workbook_excel["Sheet"]
worksheeet_excel.append(["operon","localtag"])
operon_num_new = 1
for localtag_output in localtag_output_list:
    operon_name_new = "operon_" + str(operon_num_new)
    if type(localtag_output) == list:
        localtag_output_new = str_new.join(localtag_output)
    else:
        localtag_output_new = localtag_output
    worksheeet_excel.append([operon_name_new,localtag_output_new])
    operon_num_new = operon_num_new + 1        
workbook_excel.save(output_operon_gene)



