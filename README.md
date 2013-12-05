consumer_net_data_import
========================

####Description

Parse consumer info CSV files and output three edge lists that can be plotted in Gepi.

####Synopsis

          usage: cndi.py [-h] -s STEP_TO_RUN
          Create consumer networks
          Arguments:
             -h, --help            show this help message and exit
             -s STEP_TO_RUN, --step_to_run STEP_TO_RUN
                        Step to run: all or "1", "2", "3", "1,2", etc.



####Detailed description

The objective of this test is create 3 different “networks” in order to compare how consumers’ behaviors are reflected by 3 different data sets. The resulting networks will have nodes that each represent a distinct brand and the link (weight) between these nodes will indicate that there is at least one person who uses/interacts with both of these brands. The strength of the link will reflect the number of people connecting the brands.  

The three data sets are: 

 1. OneView Simmons Data where consumers are asked to recall what brands they use/purchase (there are a total of 1471 brands/products in this dataset.  Each product is associated with a website – you can find the mapping in BrandWebsites.csv).  The dataset for this task is called ExperianBrands.csv.
   - One file with about 1471 brands (as columns) and nearly 980 different people (as rows). A 1 at the intersection indicates that the person has identified as having used that brand, a 0 indicates they do not use the brand. 
   - Here a link between two brands is formed when at least one person indicates having used both brands. So if I used both Amazon and Google, then Amazon and Google would be connected.  The weight on the link between Amazon and Google would be the number of people that indicated purchasing both Amazon and Google.

 2. comScore click-through data for brand websites.  The data set for this task is in ComScoreDatapt1.csv, ComScoreDatapt2.csv, and ComScoreDatapt3.csv
   - this data has clicks on different websites by user ids.
   - Here a link between two brands is formed when at least one person clicks on two brands. So if I clicked on both Amazon and Google, then Amazon and Google would be connected.  The weight on the link between Amazon and Google would be the number of people that clicked on both Amazon and Google.


 3. comScore purchase data for the same websites as in (2)
   - Web-wide visitation and transaction behavior based on a random sample from a cross-section of more than 2 million Internet users in the United States
   - The comScore click-through and purchase data are in three large files (this is only because the files are quite large and we thought it would be easier to manage in three separate files) and this data is not sorted by user or brand, so purchases and clicks are distributed across the three files – you will need to combine them using your scripts
   - The unique panel identifier is Machine ID, and information on the user’s session and purchase behavior on each domain is given in additional column, as well as some demographic information (which at this point is not necessary for the creation of the network). A transaction is indicated by a 1 in the column titled tran_flag.
   - Here we want to know the connections between brand websites based on people that purchased from those websites.  So two websites are connected if people purchased things from the two websites.  So if I purchased (as indicated by the tran_flag) on both Amazon.com and Target.com then Amazon and Target.com would be connected.  The weight on the link would be the total number of people that purchased from both Amazon.com and Target.com.

Eventually, we want to plot these networks using Gephi (a free publicly available graphing software—download and install it), but need to format the data in an acceptable format for this program. The format is something called an edge list.  Your scripts should create edge lists of brands for each of the three files. 

The end result for each of the three files, should be in the following format:

     BrandNamei, BrandNamej, n
 - Where the BrandNames are two different brands, i,j, and n is the number of people that connect the two brands. 
There is a filename BrandWebsites.csv that makes the mapping between brandnames in dataset one and the brandnames in datasets 2 and 3.   

For now use the brandnames in column 2 of the csv file with the website names for each brand.

Deliverables: 
 - 1) you should provide a script/scripts that take in as input files in the format of 1, 2, and 3 filetypes above and spit out the comma separated edge list.  The script(s) should be documented and tested against the data.
 - 2) You should deliver three edge list files
 - 3) you should plot the three network plots in Gephi to show that the resulting files with the current data works.  Provide 3 plots – one for each data set.
 


####Problems:

 - NUL (```\000```) bytes error while reading from csv file (maybe because input file is encoded in utf-16 instead of utf-8)

   Solution: use ```tr``` to remove NUL bytes from file:
   
                tr < 6006061aba57f4d8.csv -d '\000' > 6006061aba57f4d8_nonul.csv
