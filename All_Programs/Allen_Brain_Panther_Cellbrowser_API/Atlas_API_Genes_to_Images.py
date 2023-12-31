import requests
import xml.etree.ElementTree as ET
import urllib.request
import os
import glob
import time


def Ontology_Files_Parser(genes_dir):
    set_of_genes = set()
    with open(genes_dir) as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                gene_line = line.rstrip().lstrip()
                if len(gene_line.split()) > 1:
                    continue
                else:
                    set_of_genes.add(gene_line)
    return set_of_genes


def Get_Allen_Exp_ID_Timepoint(skipped_genes_set, gene, curr_timepoint):
    experiment_age = tuple()
    get_experiments_XML = "https://developingmouse.brain-map.org/api/v2/data/query.xml?criteria=model::SectionDataSet,rma::criteria,[failed$eq'false'],plane_of_section[name$eq'sagittal'], genes[acronym$eq'" +gene+"'],rma::include,specimen(donor(age))"
    response = ''
    skip = False
    try:
        response = requests.get(get_experiments_XML, timeout=None)
        response.raise_for_status()
    except Exception as e:

        print('\n')
        print('Timed out skipping Gene: '+gene+'\n')
        skipped_genes_set.add(gene)
        skip = True
    if not skip:
        xml_file = "/Users/koupa/PycharmProjects/pythonProject/Allen_Brain_Analysis/temporary.xml"
        with open(xml_file, 'w') as file:
            file.write(response.text)
            file.close()
        tree = ET.parse(xml_file)
        allen_xml_resp = tree.getroot()
        experiment_age_tupleList = []
        for response in allen_xml_resp:
            for section_data_set in response.findall('section-data-set'):
                experiment_id = section_data_set.find('id').text
                age_name = ''
                for specimen in section_data_set.findall('specimen'):
                    for donor in specimen.findall('donor'):
                        for age in donor.findall('age'):
                            age_name = age.find('name').text
                experiment_age_tupleList.append((experiment_id, age_name))
        os.remove(xml_file)
        for e_a in experiment_age_tupleList:
            if e_a[1] == curr_timepoint:
                experiment_age = e_a
                break
    exp_skip = (experiment_age,skipped_genes_set)
    return exp_skip


def Get_Allen_Brain_Section_Images(skipped_genes_set, gene, experiment, curr_dir):
    gene_directory = ''
    get_image_list = "https://developingmouse.brain-map.org/api/v2/data/query.xml?criteria=model::SectionImage,rma::criteria,[data_set_id$eq"+experiment+"]"
    response = ''
    skip = False
    try:
        response = requests.get(get_image_list, timeout=None)
        response.raise_for_status()
    except Exception as e:

        print('\n')
        skip = True
        print('Timeout Error skipping Image Collection for Gene: '+gene+'\n')
        skipped_genes_set.add(gene)
    if not skip:
        xml_file = "/Users/koupa/PycharmProjects/pythonProject/Allen_Brain_Analysis/temporary.xml"
        with open(xml_file, 'w') as file:
            file.write(response.text)
            file.close()
        tree = ET.parse(xml_file)
        allen_xml_resp = tree.getroot()
        all_image_ids = []
        for r in allen_xml_resp:
            for section_data_set in r.findall('section-image'):
                image_id = section_data_set.find('id').text
                all_image_ids.append(int(image_id))
        all_image_ids = sorted(all_image_ids, reverse=True)
        image_index = int(len(all_image_ids) / 2)
        os.remove(xml_file)
        gene_directory = curr_dir+'/'+gene
        if not os.path.exists(gene_directory):
            os.mkdir(gene_directory)
        else:
            files = glob.glob(gene_directory + '/*')
            for f in files:
                try:
                    os.remove(f)
                except PermissionError:
                    print('Permission Denied')
                    print('Gene involved: '+ gene)
                    continue
        for index in range(image_index-3, image_index+3):
            image_id = all_image_ids[index]
            get_images = 'http://api.brain-map.org/api/v2/image_download/' + str(image_id) + '?downsample=4&annotation=true'
            try:
                response = requests.get(get_images, timeout=None)
                response.raise_for_status()
            except Exception as e:
                print('\n')
                print('Timed out skipping Image for Gene: ' + gene + '\n')
                skipped_genes_set.add(gene)
                continue
            image_url = response.url
            path = gene_directory+'/'+gene+'_'+str(image_id)+'.jpg'

            # Image url retrive error handler
            url_request_recheck = True
            while url_request_recheck:
                with urllib.request.urlopen(image_url) as d, open(path, "wb") as opfile:
                    byte_data = d.read()
                    str_data = str(byte_data)
                    if 'Site unavailable' in str_data:
                        pass
                    else:
                        opfile.write(byte_data)
                        url_request_recheck = False

    gene_dir_skip = (gene_directory, skipped_genes_set)
    return gene_dir_skip


