The repository contain 4 files:
projectcc.py
Euro.json
dolar.json
report.pdf

# Currency converter for CLP (Chilean peso), USD (US Dolar) & EUR (Euro)

#### Description: The project consists in converting an amount of any of these 3 currencies: euro, us dolar or peso (chilean) to any of the 3 currencies for a specific given date. Print the result and save it to a pdf file.
Steps to achieve the objective of printing and saving a pdf file of the desire currency conversion:
1. Input date: provide the date from which value of currency is to be used to make conversion. Format of the date should be YYYY-MM-DD. For validation of dates, the "re" library is used and “if statement” to validate if date is in a range of dates within the year. A “while true” is used in conjunction with “re” and “if statement” to prompt the user until the correct date is given. 
2. Find value in json file for the date provided: after taking the validated date, the program will check first if already exists the json file with the currency values, if not a new version with recent data is downloaded using requests and api of https://api.sbif.cl (chilean authority that regulate financial institutions) for Euro and Dolar. If the file fails to be downloaded or if no value is found for the date provided by the user, the program exits via sys.exit and a message is displays that inform the problem. Second, after validation of the existence of the json file with refreshed data, the program try to find the value associated to the date and return the value of dolar and euro. If the value is not found the program exits via sys.exit and display a message that inform the problem. 
3. Convert the currency amount to the desire currency. After the value for the currency is found, the variable dolar and euro is used to make the convertion according to the parameters given of date, year, currency from which to "convert from" and currency to "convert to". The result is returned in a variable to be display in the console as print and also to be used to save as pdf file. 
4. Print to pdf. fpdf2 is used to display the result of the converted values to pdf. 
The repository contain 4 files:
projectcc.py
Euro.json
dolar.json
report.pdf
