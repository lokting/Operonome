#提取core operonome
import openpyxl as xl 
import os 
import csv

def get_localtag_list(localtag_str):
    return localtag_str.split(",") if "," in localtag_str else [localtag_str]

def get_operon_localtag_dict(excel_path):
    operon_dict = {}
    workbook = xl.load_workbook(excel_path)
    worksheet = workbook["Sheet"]
    for row in worksheet.iter_rows(min_row=2, values_only=True):  # 跳过标题行
        operon, localtag = row[0], row[1]
        operon_dict[operon] = get_localtag_list(localtag)
    return operon_dict

def load_strain_data(operon_dir, strains):
    strain_operons = {}
    for strain in strains:
        excel_path = os.path.join(operon_dir, f"{strain}_operon-gene.xlsx")
        operon_dict = get_operon_localtag_dict(excel_path)
        strain_operons[strain] = operon_dict
    return strain_operons

def load_gene_clusters(CG_file):
    gene_to_cluster = {}
    cluster_to_genes = {}
    with open(CG_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        headers = next(reader)  # 读取表头
        strains = headers  # 表头即为菌株名称
        gene_to_cluster = {strain: {} for strain in strains}
        cluster_id = 1  # 动态生成簇编号
        for row in reader:
            genes = row
            cluster_to_genes[cluster_id] = {}
            for i, strain in enumerate(strains):
                gene = genes[i].strip()
                if gene:
                    gene_to_cluster[strain][gene] = cluster_id
                    cluster_to_genes[cluster_id][strain] = gene
            cluster_id += 1  # 编号递增
    return strains, gene_to_cluster, cluster_to_genes

def find_core_operons(strain_operons, gene_to_cluster, strains):
    # 存储每个菌株的operon signature
    strain_signatures = {strain: {} for strain in strains}
    
    for strain in strains:
        for operon, genes in strain_operons[strain].items():
            cluster_ids = []
            valid = True
            for gene in genes:
                if gene in gene_to_cluster[strain]:
                    cluster_ids.append(gene_to_cluster[strain][gene])
                else:
                    valid = False
                    break
            if valid:
                signature = tuple(sorted(cluster_ids))
                if signature not in strain_signatures[strain]:
                    strain_signatures[strain][signature] = []
                strain_signatures[strain][signature].append(operon)
    
    # 收集所有可能的signature
    all_signatures = set()
    for strain in strains:
        all_signatures.update(strain_signatures[strain].keys())
    
    # 筛选存在于所有菌株中的signature
    core_signatures = []
    for sig in all_signatures:
        if all(sig in strain_signatures[strain] for strain in strains):
            core_signatures.append(sig)
    
    # 构建核心operonome
    core_operons = []
    for sig in core_signatures:
        operon_group = {}
        for strain in strains:
            operon_group[strain] = strain_signatures[strain][sig]
        core_operons.append(operon_group)
    
    return core_operons

def main():
    # 配置路径
    operon_dir= r"input/operon_file"
    CG_file = r"input/CG_ALL.txt"
    output_file = r"output/core_operonome.txt" 
    
    # 加载数据
    strains, gene_to_cluster, _ = load_gene_clusters(CG_file)
    strain_operons = load_strain_data(operon_dir, strains)
    
    # 查找核心operon
    core_operons = find_core_operons(strain_operons, gene_to_cluster, strains)
    
    # 写入输出文件
    # with open(output_file, 'w') as f:
    #     writer = csv.writer(f, delimiter='\t')
    #     header = ["Signature"] + [f"{strain}_operons" for strain in strains]
    #     writer.writerow(header)
        
    #     for group in core_operons:
    #         signature = next(iter(group.values()))[0]  # 获取第一个菌株的签名
    #         row = [",".join(signature)]
    #         for strain in strains:
    #             operons = ",".join([f"{strain}---{op}" for op in group[strain]])
    #             row.append(operons)
    #         writer.writerow(row)

    # 写入输出文件（去掉Signature列）
    with open(output_file, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        header = [f"{strain}_operons" for strain in strains]  # 只写菌株的operon列
        writer.writerow(header)
        
        for group in core_operons:
            row = []
            for strain in strains:
                operons = ",".join([f"{strain}---{op}" for op in group[strain]])
                row.append(operons)
            writer.writerow(row)

if __name__ == "__main__":
    main()