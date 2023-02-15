# Take Home Project

## Assignment
Objective: To gain insight into your ability to learn unfamiliar APIs via written documentation and utilize that API to pull and manipulate data into a report via Python scripting.

### Part 1: Utilizing the Close API and Python
1. Register* with your email address at https://app.close.com/signup for a 14-day free trial. While on a free trial, you’ll have full access to all of the Close features, API included.
*If you’ve already registered and your trial has expired, send a message to support@close.com to extend it.
2. Generate a new Close API key as shown at https://help.close.com/docs/api-keys
3. Utilizing the Close API, write a Python script that:
a. imports companies & contacts from this CSV file to your Close organization 
i. one CSV row equals one contact
ii. company equals lead in Close (one lead can have multiple contacts) 
iii. group contacts into leads/companies by their lead/company name 
iv. discard any invalid data
b. finds all leads that were founded within a date range specified when running the script
c. segments the found leads above by US State and generates a CSV file that contains the
following columns:
i. the state name
ii. total number of leads in the state
iii. the lead with the most revenue in the state 
iv. total revenue of all leads in the state
v. the median revenue of all leads in the state
You can download a sample of the desired output of the script here.
Please be sure to include comments in your Python code to help the reviewer understand what each block of code does.
### Part 2: Uploading your script to GitHub and writing a README
Once your Python script from Part 1 is complete, upload your script to a new GitHub repository along
with a README.md file that:
A. Explains your script’s logic to someone that is not overly technical. How did you eliminate the invalid data? How did you find all the leads? How did you segment the leads by state and find the one with the most revenue?
B. Explains how to run the script, including any dependencies that must be downloaded for the script to run.

## Setup to run scripts
1. Git clone this repository
2. ```cd close```
3. ```python -m venv .venv```
4. ```.venv/bin/activate```
5. ```pip install -r requirements.txt```
6. Open  ```secrets.py``` and replace ```API_KEY``` with your API Key - more information to be found [here](https://help.close.com/docs/api-keys)

## Run script
In terminal run the following for each script: 
#### For Script A
```python script_a.py```
#### For Script B
```python script_b.py```
#### For Script C
```python script_c.py```

## Improvements
 - Give option of running Argparse to input csv filepaths and API keys instead of amending scripts
 - Make my code more DRY, I could use more functions or build a central library of useful functions for scripts
 - I spent the most time on this functionality ```if not any(company in d['name'] for d in clean_data):``` so my contacts could create new leads if they didnt already exist or be added to existing leads. 
 - More work with exceptions of the Close API responses.

## Challenges
 - With any assignment time is a major challenge as you can spend many hours, or days even refactoring 
 - Working with custom fields took some time to understand how they work with Close
 - Better validators than len() when uploading custom data
 - ```None``` data in script C - calculations around the count as just because the CRM does not have the data for a companies revenue it does not mean that the revenue is 0. Therefore in calculating the median do you include the None date - I chose not to, as it could majorly skew the data set and mislead those using the data.

 ## Explanations
 - If statements ensure data existed before handling it and putting it into the dict
 - Use of ```phonenumbers``` and ```email-validator``` to ensure that data is of the correct formatting and valid. As well as adding information to print statements to know what data is invalid
 
 ## Logic
 #### Script A
 - Company_import function is split by an if/else statement. If the company does not already exist as a lead, create a lead and then add the contact to that lead and fill all custom data and address information. Otherwise find the existing lead, generate a contact and add that to the list of contacts for that lead, then add or update any other data on that lead. 
 - Using external providers to validate phone and email addresses to strengthen the validation process
 - The terminal will return a list of emails or phone numbers that are not valid and explain in some more detail when available
 - Finally the terminal will update you when it is trying to update your Close database and when it is complete!

 #### Script B
 - The script takes two date inputs at line 9 and 10 and turns them into date time objects
 - It then creates a dictionary of the company name and custom founded dates to iterate and compare to the input and generates a list of companies 
 - Finally it takes that data and uses it to return contact information for the first contact of each successful lead
 - I would like to have more control over date validation of their chosen start and end dates, potentally an input which is then formatted by the script

 #### Sctipt C
 - This script has functions seperated by each column of the CSV it needs to generate. Once pulling all the relevant information from the Close CRM using the API connection, it will create a dictionary of data related to each state. 
 - This dictionary is then iterated over to generate the rows needed to create the CSV
 - This function is flexible to adapt to additonal states if the data includes it


 ## Questions
 If you have any further questions please contact Katrinaharradine at gmail dot com