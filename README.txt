-1st task is implemented in download_data.py, task1.py.
	-download_data.py takes a path to a folder as the argument, all files will be downloaded to that folder.
	-task1.py takes a path to a .csv file as the first argument and a date in 31/01/2017 format as the second optional argument.
	-I use pandas package to process a .csv document.
-2nd task is implemented in the MsdHW java project and in task2_2.py.
	-I use jsoup 1.11.3 library to automatically download files from the web.
	-I use apache commons net 3.6 library to work with ftp server.
	-StoreToLocalAndFTP in Main.java will download files to a local storage and to a ftp server.
	-task2_2.py takes a path to a folder that contains the dataset as the argument.
-Attachments
	-tmp/dem_reg_2016-2018.csv - contains all records of DEMENTIA_REGISTER_65_PLUS. 
	It was produced by dem_regions_by_date function in task2_2.py
	-tmp/dem_rev_vs_est_2107.csv - contains comparison of DEMENTIA_REGISTER_65_PLUS vs 
	DEMENTIA_ESTIMATE_65_PLUS by region by date. It was produced by dem_registered_vs_estimate function
	-tmp/by_regions.png was produced by plot_by_region function in task2_2.py. 
	-tmp/by_time.png was produced by plot_by_time function in task2_2.py.
	-tmp/deg_reg_vs_est.png was produced by plot_reg_vs_est function.