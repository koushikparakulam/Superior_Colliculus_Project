import requests
import json
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class PantherAPI:
    # Initializes all shared dictionaries, variables and values used by the method GeneConstruct
    def __init__(self, open_gene_description_directory, gene):
        self.open_gene_description_directory = open_gene_description_directory
        self.gene = gene
        self.Gene_Ontology_Function_GOterm_Genes = {}

    def Gene_Ontology_Packer(self, name_id):
        function_goterm = name_id['name'] + '\t' + name_id['id']
        if self.gene not in self.Gene_Ontology_Function_GOterm_Genes:
            self.Gene_Ontology_Function_GOterm_Genes[self.gene] = [function_goterm]
        else:
            ontology_list = self.Gene_Ontology_Function_GOterm_Genes.get(self.gene)
            ontology_list.append(function_goterm)
            self.Gene_Ontology_Function_GOterm_Genes[self.gene] = ontology_list

    def Gene_Ontology_Unpacker(self, go_term_packets):
        if isinstance(go_term_packets, list):
            for go_terms in go_term_packets:
                if 'annotation_list' in go_terms:
                    if 'annotation' in go_terms['annotation_list']:
                        packet = go_terms['annotation_list']['annotation']
                        if isinstance(packet, list):
                            for name_id in packet:
                                self.Gene_Ontology_Packer(name_id)
                        elif isinstance(packet, dict):
                            self.Gene_Ontology_Packer(packet)
        else:
            if 'annotation_list' in go_term_packets:
                if 'annotation' in go_term_packets['annotation_list']:
                    packet = go_term_packets['annotation_list']['annotation']
                    if isinstance(packet, list):
                        for name_id in packet:
                            self.Gene_Ontology_Packer(name_id)
                    elif isinstance(packet, dict):
                        self.Gene_Ontology_Packer(packet)

    def Gene_Ontology_Maker(self):
        # Might need to add a while to wait for connection security for valid response
        Post_Request = "http://pantherdb.org/services/oai/pantherdb/geneinfo"
        response = ''
        error = False
        try:
            response = requests.post(Post_Request,
                                     data={'organism': 10090, 'geneInputList': [self.gene],
                                           'class': 'biological process'})
            response.raise_for_status()
        except Exception as err:
            print(err)
            error = True
        if not error:
            Panther_Go_Dict = response.json()
            if 'mapped_genes' in Panther_Go_Dict['search'].keys():
                gene_dict_list = Panther_Go_Dict['search']['mapped_genes']['gene']
                if isinstance(gene_dict_list, list):
                    for gene_dict in gene_dict_list:
                        if 'annotation_type_list' in gene_dict:
                            if 'annotation_data_type' in gene_dict['annotation_type_list']:
                                go_term_packets = gene_dict['annotation_type_list']['annotation_data_type']
                                self.Gene_Ontology_Unpacker(go_term_packets)
                else:
                    if 'annotation_type_list' in gene_dict_list:
                        if 'annotation_data_type' in gene_dict_list['annotation_type_list']:
                            go_term_packets = gene_dict_list['annotation_type_list']['annotation_data_type']
                            self.Gene_Ontology_Unpacker(go_term_packets)
        return error

    def Ontology_File_Writer(self):
        molecular_biological_cellular = {}
        protein_class = {}
        pathway = {}
        ontology_list = self.Gene_Ontology_Function_GOterm_Genes.get(self.gene)
        for ontology_term in ontology_list:
            term = ontology_term.split('\t')[1]
            # Pathway ontologies
            if 'P0' in term:
                if self.gene not in pathway:
                    pathway[self.gene] = [ontology_term]
                else:
                    pathway_list = pathway.get(self.gene)
                    pathway_list.append(ontology_term)
                    pathway[self.gene] = pathway_list
            # Protein Class Ontologies
            elif 'PC' in term:
                if self.gene not in protein_class:
                    protein_class[self.gene] = [ontology_term]
                else:
                    protein_class_list = protein_class.get(self.gene)
                    protein_class_list.append(ontology_term)
                    protein_class[self.gene] = protein_class_list
            # molecular/biological/cellular Class Ontologies
            else:
                if self.gene not in molecular_biological_cellular:
                    molecular_biological_cellular[self.gene] = [ontology_term]
                else:
                    molecular_biological_cellular_list = molecular_biological_cellular.get(self.gene)
                    molecular_biological_cellular_list.append(ontology_term)
                    molecular_biological_cellular[self.gene] = molecular_biological_cellular_list

        # Write Molecular/Biological/Cellular Ontology
        self.open_gene_description_directory.write('Molecular/Biological/Cellular Ontology Terms: \n\n')
        if molecular_biological_cellular:
            for ontology in molecular_biological_cellular.get(self.gene):
                self.open_gene_description_directory.write(ontology+'\n')
        else:
            self.open_gene_description_directory.write('NO Molecular/Biological/Cellular ONTOLOGY TERMS\n')
        self.open_gene_description_directory.write('\n\n')

        # Write Protein Ontology
        self.open_gene_description_directory.write('Protein Ontology Terms: \n\n')
        if protein_class:
            for ontology in protein_class.get(self.gene):
                self.open_gene_description_directory.write(ontology + '\n')
        else:
            self.open_gene_description_directory.write('NO Protein ONTOLOGY TERMS\n')
        self.open_gene_description_directory.write('\n\n')

        # Write Pathway Ontology
        self.open_gene_description_directory.write('Pathway Ontology Terms: \n\n')
        if pathway:
            for ontology in pathway.get(self.gene):
                self.open_gene_description_directory.write(ontology + '\n')
        else:
            self.open_gene_description_directory.write('NO Pathway ONTOLOGY TERMS\n')
        self.open_gene_description_directory.write('\n\n')