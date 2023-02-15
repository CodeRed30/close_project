from closeio_api import Client
import secrets
import datetime

api_key = secrets.API_KEY
api = Client(api_key)

# Enter dates here - please use YYYY-MM-DD format
start_date = '2021-01-01'
end_date = '2022-11-01'

#Ger data from Close
def data_download():
    resp = api.get("lead")
    return resp["data"]

data = data_download()

def create_date(date):
    if date:
        if 'T' in date:
            output = date.split('T')
            date = output[0]
        clean_date = datetime.date(*map(int, date.split('-')))
    return clean_date

# Collect all created date for each compny so dont have to iterate over whole data set
def get_date_data():
    dates = {}
    for each in data:
        name = each.get("name")
        date = each.get("custom.cf_gJ0SOVrxeQv67JLSSHYFp2HaMaRYW5ocQ2I2rcD9dpI")
        if date:
            date = create_date(date)
            dates[name] = date
    return dates

date_data = get_date_data()

def date_selector(start_date, end_date):
    selected_dates = []
    # Turn into date objects
    try:
        start_date_obj = create_date(start_date)
        end_date_obj = create_date(end_date)
    except Exception as e:
        print(e)
    for name, date in date_data.items():
        if start_date_obj <= date and end_date_obj >= date:
            selected_dates.append((name, date))
    return selected_dates

companies = date_selector(start_date=start_date, end_date=end_date)

def return_leads():
    successful_leads = []
    for company in companies:
        for lead in data:
            if company[0] == lead.get('name'):
                successful_leads.append(lead)
    print('The following companies were created within the date range supplied:')
    for lead in successful_leads:
        print(f'Name: {company[0]}')
        print(f'Date Founded: {company[1]}')
        if lead.get('contacts'):
            print(f'Contact Name: {lead.get("contacts")[0].get("name")}')
            print(f'Contact Phone: {lead.get("contacts")[0].get("phones")[0].get("phone_formatted")}')
            print(f'Contact Email: {lead.get("contacts")[0].get("emails")[0].get("email")}')
        print('----')

return_leads()
