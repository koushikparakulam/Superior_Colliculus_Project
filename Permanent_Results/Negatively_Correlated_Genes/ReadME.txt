Folder contains three correlated timepoint folders: p0_p4_6, p4_6_p10, p10_p15

Each folder contains Cluster Folders corresponding the the cluster with regards to the reference timepoint 

	-ex. p0 is the reference timepoint for the correlation p0_p4_6

Each Cluster Folder contains all the clustural relationships to the correlated timepoint BUT excludes any correlation where there are no Excitatory/Inhibitory negative genes

	-ex. p0_C6__p4/6_C1 has a correlation however, none of the genes within their correlation have (Slc17a6, Cacna2d1) or (Gad1, Gad2, Slc32a1)
	     
		- as such this correlation would be excluded in the dotplots as the genes within this correlation is not representative of being genes NOT expressed
		  by a Excitatory/Inhibitory cluster.



All dotplots within the Cluster Folders contain the correlated negatively expressed genes ordered by the highest negative expression between both timepoints


For a given dotplot the genes within them are genes where the cluster in question is NOT expressing it but at least one other cluster expresses it highly

These genes are coincided by the fact that the said cluster does not express (Slc17a6, Cacna2d1) or (Gad1, Gad2, Slc32a1) thus possibly showing a relationship
between genes not expressed in a given cluster and it not being Excitatory/Inhibitory


To find all correlations see the Negative Correlation Genes Ranking .txt file provided in the correlated timepoint folder

These correlations are ordered by the highest correlation which is a value given based on the 
	-quantity of genes correlated
		and 
	-the quality of correlated genes,
		i.e. the ratio of the average expression for a given gene in reference to the expression of the gene against all other clusters 
		     AND the correlated timepoint

	*Note that these correlation values are not as a percentage

These correlations can be seen as Excitatory/Inhibitory/Mixed based on the names