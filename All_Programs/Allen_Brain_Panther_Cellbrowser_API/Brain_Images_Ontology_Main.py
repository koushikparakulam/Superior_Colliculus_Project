import os
import shutil
import time
from Panther_API_Genology_Ontology import PantherAPI
from Atlas_API_Genes_to_Images import Get_Allen_Brain_Section_Images
from Atlas_API_Genes_to_Images import Get_Allen_Exp_ID_Timepoint
from Atlas_API_Genes_to_Images import Ontology_Files_Parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller as chromedriver


def User_Params(timepoint_options, analysis_options):
    all_timepoints_atlas_translated = []
    timepoint_input = ''
    analysis = []
    while (True):
        timepoint_input = input(
            '\rPlease Provide Timepoint(s) Needed to be Analyzed (E18.5, P4, P14, E11.5, E13.5, E15.5, P28) ')
        if not timepoint_input:
            all_timepoints_atlas_translated = ['E18.5', 'P4', 'P14']
            break
        elif timepoint_input:
            for time_opt in timepoint_options:
                if time_opt in timepoint_input:
                    all_timepoints_atlas_translated.append(time_opt)

            if all_timepoints_atlas_translated:
                break
            else:
                print('\rTimepoints provided were not valid', end='')
                time.sleep(1)
                continue

    while (True):
        analysis_input = input('Which Analysis Would You Like to Be Performed (Allen, Panther, Cellbrowser) ')
        if not analysis_input:
            analysis = analysis_options
            break
        else:
            for anal_opt in analysis_options:
                if anal_opt in analysis_input:
                    analysis.append(anal_opt)
            if analysis:
                break
            else:
                print('\rAnalysis options provided were not valid', end='')
                time.sleep(1)
                continue
    return analysis, all_timepoints_atlas_translated

def Cell_Browser_Image(gene_directory, time_point, gene):
    url = "https://koushikparakulam.github.io/"+time_point+"_CellBrowser/?ds="+time_point+"_Neuronal_Results&gene="+gene
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    driver.get(url)
    time.sleep(2)
    width = 1350
    height = 800
    driver.set_window_size(width, height)
    driver.save_screenshot(gene_directory+"/"+time_point+"_"+gene+".png")
    driver.quit()


def Variant_Set(skipped_genes_set, curr_timepoint, set_of_genes, curr_dir, all_cell_browser_timepoints_translated, analysis):
    print('Working on Timepoint: ' + curr_timepoint + '\n')
    for x, gene in enumerate(set_of_genes):
        if 'Allen' in analysis:
            print('\rExtracting Images For: ' + gene + '\t' + str(x + 1) + ':' + str(len(set_of_genes)), end='')
            exp_skip = Get_Allen_Exp_ID_Timepoint(skipped_genes_set, gene, curr_timepoint)
            experiment_age = exp_skip[0]
            skipped_genes_set = exp_skip[1]
        else:
            experiment_age = (1,2,3)
            skipped_genes_set = set()
        if len(experiment_age) == 0:
            continue
        else:
            if 'Allen' in analysis:
                gene_dir_skip = Get_Allen_Brain_Section_Images(skipped_genes_set, gene, experiment_age[0], curr_dir)
                gene_directory = gene_dir_skip[0]
                skipped_genes_set = gene_dir_skip[1]
            else:
                gene_directory = curr_dir + '/' + gene
                if not os.path.exists(gene_directory):
                    os.mkdir(gene_directory)
            if len(gene_directory) == 0:
                continue
            else:
                if 'Panther' in analysis:
                    gene_description_directory = gene_directory + '/Ontologies_For_' + gene + '.txt'
                    open_gene_description_directory = open(gene_description_directory, "a")
                    new_Panther_API = PantherAPI(open_gene_description_directory, gene)
                    new_Panther_API.Gene_Ontology_Maker()
                    new_Panther_API.Ontology_File_Writer()
                    open_gene_description_directory.close()
                if curr_timepoint in all_cell_browser_timepoints_translated:
                    cell_browser_time = all_cell_browser_timepoints_translated.get(curr_timepoint)
                    Cell_Browser_Image(gene_directory, cell_browser_time, gene)

    if len(skipped_genes_set) > 0:
        print('Re-trying timed out genes: '+str(skipped_genes_set))
        set_of_genes = skipped_genes_set
        skipped_genes_set = set()
        Variant_Set(skipped_genes_set, curr_timepoint, set_of_genes, curr_dir, all_cell_browser_timepoints_translated, analysis)


def main():
    chromedriver.install()
    start_time = time.time()
    timepoint_options = ['E18.5', 'P4', 'P14', 'E11.5', 'E13.5', 'E15.5', 'P28']
    non_browser_options = ['E11.5', 'E13.5', 'E15.5', 'P28']
    analysis_options = ['Allen', 'Panther', 'Cellbrowser']
    analysis, all_timepoints_atlas_translated = User_Params(timepoint_options, analysis_options)

    print('\n')
    non_cb = []
    print('Timepoints: ', str(all_timepoints_atlas_translated))
    for vals in all_timepoints_atlas_translated:
        if vals in non_browser_options:
            non_cb.append(vals)
    if non_cb:
        print('Cellbrowser imaging will be skipped for the following: ', str(non_cb))
    print('Analysis: ', str(analysis))

    print('\n')
    all_cell_browser_timepoints_translated = {'E18.5': 'p0', 'P4': 'p4_6', 'P14': 'p15'}
    brain_images_parent_dir = 'Brain_Images_Organized_By_Genes'
    skipped_genes_set = set()

    # Deletes all folders/files present in Brain_Images and remakes new directory
    if os.path.exists(brain_images_parent_dir):
        shutil.rmtree(brain_images_parent_dir)
    os.mkdir(brain_images_parent_dir)

    for curr_timepoint in all_timepoints_atlas_translated:
        set_of_genes = set()
        genes_dir = "Genes/All_Genes.txt"
        set_of_genes = set_of_genes.union(Ontology_Files_Parser(genes_dir))
        curr_dir = brain_images_parent_dir + '/' + curr_timepoint
        os.mkdir(curr_dir)
        Variant_Set(skipped_genes_set, curr_timepoint, set_of_genes, curr_dir, all_cell_browser_timepoints_translated, analysis)
        print('\n')


    # Deletes all empty files and folders in the brain_images_parent_directory
    walk = list(os.walk(brain_images_parent_dir))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            shutil.rmtree(path)
    end_time = time.time() - start_time
    float_minutes = end_time/60
    decimal = float_minutes - int(float_minutes)
    seconds = 60*decimal
    minutes = int(float_minutes)
    print('Time Elapsed: '+str(minutes)+' minutes '+str(seconds)+' seconds')


if __name__ == '__main__':
    main()