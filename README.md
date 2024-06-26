# privue-demo

link to the demo page: https://privue-demo-wdxg3n5hvmu2gcv8ypw432.streamlit.app/  

In the first tab (Privatization Example), we will present the privatization technique SUE-LDP in action.  
You need to specify the limits of the range from which you want to privatize values- [Min value, Max value].  
Select the number of buckets (d). The range will be divided evenly into sub-sections, according to this parameter.  
Choose the privacy budget epsilon, which determines the algorithm's probabilities for selecting buckets where the value will be set to 1.  
Finally, select the value which you would like to privatize.  
Submit the parameters by pressing the button. A histogram will be displayed, which represents the perturbed result of the algorithm (a d-bit vector). Along with the histogram, a table shows which sub-section each index in the histogram represents (high probability candidates for the original value).  

In the second tab (File Privatization), we will provide the option to privatize a file of data using SUE-LDP.  
You are able to submit a file which may contain multiple values per user, instead of a single value.  
Select the number of values for each user.  
Submit a JSON file containing the data you want to privatize. Required format: File must be comprised of main JSON Objects - each represents a user (No limitations on user key name,  only that they are unique). Every user's object has nested JSON objects which represent timestamps (No limitations on timestamp key name, only that they are unique per user object). The numeric values for each timestamp are held in an array (consistent order for every timestamp). If a user doesn't have a record for a timestamp, it shouldn't appear in the user object. We provide an example file which you can download (3 values per user record).  
Choose the privacy budget epsilon. For each value (In the order they appear in the file records) specify the limits of the range [Min value, Max value] and the number of buckets (d), similarly to the previous tab.  
Submit the parameters by pressing the "Submit and privatize" button. A new button, named "Download privatized JSON output file", will be displayed, which will download the privatized file. This file will contain privatized records for each timestamp (an array of d-bit vectors) instead of the original ones.  

In the third tab (Estimation), after privatizing your file in the previous tab, you can upload it for estimation of the different values.  
Each value will be represented with:  
    &emsp;An "average" histogram - An estimation of the distribution of the actual data across all user records.  
    &emsp;Estimation of the average value (which was calculated using the "average" histogram).  
    &emsp;A table showing which sub-section each index in the histogram represents (to clarify sub-section distribution).  

There are example JSON files in the repo, which you can enter in tab 2 to view a possible privatization of the data within:  
1. input_1.json - data for 1000 users, across 7 timestamps, a single values recorded per timestamp. Distribution for the value Normal(750,100).  
2. input_2.json - data for 500 users, for 7 timestamps, 3 values recorded per timestamp. Distribution of each value:  
    &emsp;Value 1: Normal(67,1)  
    &emsp;Value 2: Normal(32,10)  
    &emsp;Value 3: Normal(49,40)  
Remember that the algorithm is probabilistic - 2 output files from the same example file can have different estimation results (which you can view in tab 3).  

To directly use the privue package used in the demo for privatization and estimation, install using `pip install privue`  
Package github repo: https://github.com/LiorDaSelior/privue
