import csv
import json

import secrets 

from closeio_api import Client

from email_validator import validate_email, EmailNotValidError
import phonenumbers

filename = 'CSE Take Home Project.csv'
clean_data = []
api_key = secrets.API_KEY
api = Client(api_key)

def phone_number_validator(name, phone, phones = []):
    try:
        phone_obj = phone.replace('-', '')
        phone_obj = phonenumbers.parse(phone_obj)
        if phonenumbers.is_possible_number(phone_obj):
            phones.append({'type': 'office', 'phone': phone})
        else: 
            print('The phone number is not valid')
            print(f"Please fix {name}'s phone number: {phone} and retry uploading\n---")
        return phones
    except Exception as errorMsg:
        print(str(errorMsg))
        print(f"Please fix {name}'s phone number: {phone} and retry uploading\n---")

def email_validator(name, email, emails = []):
    try:
        email_object = validate_email(email)
        clean_email = email_object.email
        emails.append({'type': 'office', 'email': email})
        return emails
    except EmailNotValidError as errorMsg:
        print(str(errorMsg))
        print(f"Please fix {name}'s email address: {email} and retry uploading\n---")


def email_uploader(name, csv_emails):
    email_list = csv_emails.split('\n')
    emails = []
    for email in email_list:
        emails = email_validator(name, email, emails)
    return emails

def phone_uploader(name, csv_phones):
    phone_list = csv_phones.split('\n')
    phones = []
    for phone in phone_list:
        phones = phone_number_validator(name, phone, phones)
    return phones

def trigger_upload():
    print('Data prepped and ready to upload')
    try:
        for lead in clean_data:
            api.post('lead', data=lead)
    except Exception as e: 
        print(f'{lead["name"]} did not upload to close, please review the data and try again')
        print(f'Error: {e}')

    count = len(clean_data)
    if count == 1:
        count = '1 lead'
    else: 
        count = f'{count} leads'
    print(f"{count} successfully uploaded to Close, please head to close.com to confirm")


def company_import():
    with open(filename, 'r') as csvfile:
        # Turn CSV into dictionary
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            # Conditionally generate a new company
            company = row['Company']
            if not any(company in d['name'] for d in clean_data):
                new_lead = {'name': row['Company']}
            
                # Generate Contact data 
                contact = {}
                if row['Contact Name']:
                    contact['name'] = row['Contact Name'].title()
                # Split emails
                if row['Contact Emails']:
                    emails = email_uploader(row['Contact Name'], row['Contact Emails'])
                    if emails:
                        contact['emails'] = emails
                # Split phone numbers
                if row['Contact Phones']:
                    phones = phone_uploader(row['Contact Name'], row['Contact Phones'])
                    if phones:
                        contact['phones'] = phones
                # Add contact to lead
                if contact:
                    new_lead['contacts'] = [contact]
                
                # Generate custom data
                custom = {}
                if row['custom.Company Founded']:
                    custom['custom company founded'] = row['custom.Company Founded']
                if row['custom.Company Revenue']:
                    custom['custom company revenue'] = row['custom.Company Revenue']
                if custom:
                    new_lead['custom'] = custom
                
                # Generate address data
                addresses = []
                if row['Company US State']:
                    addresses.append({'state': row['Company US State'], 'country':'US'})
                if addresses:
                    new_lead['addresses'] = addresses
                
                clean_data.append(new_lead)

            else:
                #add contact to an existing lead
                for lead in clean_data:
                    if lead['name'] == row['Company']:
                        # Generate Contact
                        contact = {}
                        if row['Contact Name']:
                            contact['name'] = row['Contact Name'].title()
                        # Split emails
                        if row['Contact Emails']:
                            emails = email_uploader(contact['name'], row['Contact Emails'])
                            if emails:
                                contact['emails'] = emails
                        # split phone numbers
                        if row['Contact Phones']:
                            phones = phone_uploader(row['Contact Name'], row['Contact Phones'])
                            if phones:
                                contact['phones'] = phones
                        # Add contact to contacts
                        if contact:
                            if 'contacts' in lead.keys():
                                lead['contacts'].append(contact)
                            else:
                                lead['contacts'] = [contact]
                        
                        # Custom data
                        # If nothing custom exists in lead
                        if not 'custom' in lead.keys():
                            custom = {}
                        
                        if row['custom.Company Founded']:
                            if not 'custom company founded' in lead['custom'].keys():
                                if len(custom) == 0: # need better validator
                                    custom['custom company founded'] = row['custom.Company Founded']
                                else: 
                                    lead['custom']['custom company founded'] = row['custom.Company Founded']
                        if row['custom.Company Revenue']:
                            if not 'custom company revenue' in lead['custom'].keys():
                                if len(custom) == 1: # need better validator
                                    custom['custom company revenue'] = row['custom.Company Revenue']
                                else:
                                    lead['custom']['custom company revenue'] = row['custom.Company Revenue']
                        if custom:
                            lead['custom'] = custom
                        
                        # Addresses data
                        if not 'addresses' in lead.keys():
                            addresses = []
                        if row['Company US State']:
                            if not 'state' in lead['addresses'][0].keys(): # better way to access keys inside address list
                                if len(addresses) == 0:
                                    addresses.append({'state': row['Company US State'], 'country':'US'})
                                else: 
                                    lead['addresses']['state'] = row['Company US State']
                                    lead['addresses']['country'] = 'US'
                        if addresses:
                            lead['addresses'] = addresses

    trigger_upload()

company_import()

