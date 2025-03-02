# Superior Colliculus Neuronal Subtype Analysis

## Overview
This repository implements a comprehensive gene expression analysis pipeline for neuronal subtypes in the **Superior Colliculus**. The project applies advanced bioinformatics techniques to categorize neuronal clusters, analyze differentially expressed genes, and identify correlations across timepoints.

## Features
- **Neuronal Subtype Identification:** Dotplots for excitatory, inhibitory, and mixed neuronal classification.
- **Gene Expression Analysis:** Identification of **differentially expressed genes (DEGs)** across multiple timepoints.
- **Cluster Relationship Mapping:** UMAP projections, dendrogram analysis, and harmony-based cluster integrations.
- **Sankey Plot Analysis:** Visualization of neuronal cluster evolution over time.
- **Superior Colliculus Layer Correlation:** Statistical analysis to determine gene expression specificity to anatomical layers.
- **Neurodevelopmental Disorder Associations:** Expression analysis of genes linked to **Schizophrenia** and **Autism**.

---

## Project Workflow

### **1. Data Processing & Preprocessing**
- Raw gene expression data is preprocessed: **filtering, normalization, log-transform, and batch effect correction**.
- High-variance genes are selected to enhance clustering accuracy.

### **2. Quick Run vs. Full Run**
- **Quick Run:** Uses pre-saved results for faster execution.
- **Full Run:** Executes all functions from scratch (may take over an hour).

### **3. Cluster & Gene Analysis**
- **Timepoint UMAPs:** Visualizes cellular clustering at different stages.
- **Differential Expression:** Identifies highly expressed genes in each cluster.
- **Gene Filtering:** Assigns neuronal subtypes and ranks genes by expression.

### **4. Advanced Analyses**
- **Cluster Distinction:** Categorizes clusters into *True Distinct, Relative Distinct, and Non-Distinct*.
- **Correlated Unique Genes:** Tracks unique gene overlap across timepoints.
- **Harmony Integration:** Aligns clusters across time for **temporal correlation analysis**.
- **Sankey Plots:** Maps lineage progression of clusters.

### **5. Statistical & Hypothesis Testing**
- **Superior Colliculus Layer Correlation:** Compares gene expression in specific layers.
- **Schizophrenia & Autism Gene Analysis:** Identifies cluster-specific gene expression patterns.

---

## **Visualization Examples**
### **Timepoint UMAP**
![Timepoint UMAP](![image](https://github.com/user-attachments/assets/444f481d-820f-4099-9b51-e1fb395b5fb5)
)
### **Differential Gene Expression Analysis**
![Differential_Analysis](![image](https://github.com/user-attachments/assets/277eee90-e23f-4de0-8304-c9281749069b)
)
### **Dot Plot for Differentially Express Neuronal Genes**
![DEG Plot](![image](https://github.com/user-attachments/assets/6d16bd28-309c-4998-8235-328d5cd62b1d))

### **Sankey Diagram of Cluster Correlations**
![Sankey Plot](![image](https://github.com/user-attachments/assets/559a5f4f-2aa9-4ef1-a553-870b13108610))

### **Clustural Relation Dendograms**
![Dendogram_Plot](![image](https://github.com/user-attachments/assets/e548580e-b462-4b08-b631-5d991d1aa44b)
)

### **DotPlot Triangle: Shared Genes between Clustural Neighbors**
![Dotplot_Triangle](![image](https://github.com/user-attachments/assets/e0b802a2-45c0-47f7-8f17-556b8c3c164a)
)
### **Harmony Timeseries Plots**
![Harmony_Timeplot](![image](https://github.com/user-attachments/assets/a23fa845-e0df-4ea7-aeff-a3f5ebe7a703))

### **P-Value Hypothesis Testing of Layer-specific Cluster Correlations**
![Hypothesis_Testing](![image](https://github.com/user-attachments/assets/851444a0-143d-4e91-82b4-ed3415de0e5c)
)

---

## **File Structure**
```
📂 Superior_Colliculus_Project
│── 📂 Permanent_Results              # Permanent results from analysis
│── 📂 Testing_Results           # Temporary tssting for test implementation
│── 📂 All_Programs         # Custom functions for analysis
```

---

## **How to Run**
1. **Clone the repository**  
   ```bash
   git clone https://github.com/koushikparakulam/Superior_Colliculus_Project.git
   cd Superior_Colliculus_Project
   ```

2. **Install dependencies**  

```
  !pip install 'matplotlib == 3.6'
  !pip install 'scanpy == 1.9.1'
```

3. **Set Quick Run or Full Run**  
   - Modify the `Quick_Run` parameter in `MAIN_Load_Output.ipynb`:
     - `True`: Loads pre-saved results for quick testing.
     - `False`: Runs all computations from scratch.

4. **Run the main analysis script**  
   ```bash
   python MAIN_Load_Output.ipynb
   ```

---

## **Data Sources**
- **Allen Brain Atlas API:** Layer-specific gene expression.
- **Panther Ontology:** Functional gene classification.
- **Custom Pre-Processed Data:** Includes normalized gene expression matrices.

---

## **Acknowledgments**
Special thanks to the **Bioinformatics & Computational Neuroscience team @FeildheimLabs** for their insights and support in developing this project.
