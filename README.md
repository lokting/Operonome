# Operonome-NeighborCoE

NeighborCoE is a Python-based toolkit for bacterial operon analysis, including:
1. operon identification from genome annotation and count data,
2. core operonome identification across strains, and
3. pan-operonome network construction.

## Overview

This repository currently contains two modules:

- **Operon/Core Operonome module**: identifies operons from genome annotation and count data, and further defines the core operonome across strains.
- **PanOperonome module**: constructs pan-operonome networks from strain-level operon annotations and pan-genome / homologous-gene relationships.

## Repository structure

```text
Operonome/
├── get_operon/
│   └── scr/
│       ├── 0.gbff_to_excel.py
│       ├── 1.gff_to_excel.py
│       ├── 2.count_file.py
│       ├── 3.get_intergenegap.py
│       ├── 4-0.get_operon.py
│       ├── 4-1.get_operon_function.py
│       └── 5.get_core_operonome.py
├── PanOperonome/
│   └── src/
│       ├── stage_0_input.py
│       ├── stage_1_preprocess.py
│       ├── stage_2_popgid.py
│       └── stage_3_network.py
├── images/
├── README.md
└── requirement.txt
