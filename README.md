					      

					         PROBLEM STATEMENT

In this project, we consider the PhonePe Pulse data that is available in a GitHub repository, clone this GitHub repository in Python, extract the data, perform data analysis on the extracted data, and display the output in Streamlit app.

					         TECHNOLOGIES USED

Python, MySQL, Streamlit, GitHub Cloning, and Geo-visualization.

					            APPROACH

1. Here we consider Transaction data and User data of three categories - Aggregated, Map, and Top (Districts and PINCODES). We clone the GitHub repository in Python to access the files.
2. Then we store the obtained data in a Pandas Data frame and save each data frame as a CSV file.
3. Then this data is migrated to SQL where data analysis is performed using the SQL query commands.
4. We performed the analysis separately for Aggregated, Map, Top(Districts), and Top(PINCODE). There are dropdown boxes in each category corresponding to SQL queries and the output is displayed via bar graphs, pie charts, and geo-visualization (for some queries we have displayed the table too).

						       INSTRUCTIONS

1. First run the Phone_Pulse_data.py file to obtain the Transaction and User data of each category mentioned above to obtain the Data Frames. In this code, we save the Data Frames as CSV files (If you're using Jupyter Notebook, go to the terminal and type 'python PhonePe_Pulse_data.py' and then press enter to execute this file).
2. Then, run the PhonePe_pulse.py file by giving the command in the terminal as 'streamlit run PhonePe_pulse.py'. This will lead to the Streamlit App where the output will be displayed.
  

