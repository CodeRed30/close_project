import csv

from closeio_api import Client
import secrets

api_key = secrets.API_KEY
api = Client(api_key)


def data_download():
    resp = api.get("lead")
    return resp["data"]


def state_count():
    for lead in lead_dict:
        if lead["addresses"]:
            state = lead["addresses"][0]["state"]
            if state not in state_tally.keys():
                state_tally[state] = {}
                state_tally[state]["companies"] = {}
                state_tally[state]["count"] = 1
            else:
                state_tally[state]["count"] += 1


def get_revenue():
    for lead in lead_dict:
        if lead["addresses"]:
            state = lead["addresses"][0]["state"]
            if lead["custom"]:
                revenue = lead["custom"].get("custom company revenue")
                if not revenue:
                    revenue = None
                company = lead.get("name")
                if revenue:
                    revenue = float(revenue[1:].replace(",", ""))
                    state_tally[state]["companies"][company] = revenue
                    if "total_revenue" not in state_tally[state].keys():
                        state_tally[state]["total_revenue"] = revenue
                    else:
                        state_tally[state]["total_revenue"] += revenue
                else:
                    state_tally[state]["companies"][company] = revenue


def clean_revenues(revenues):
    clean_revenues = {}
    for k, v in revenues.items():
        if v is not None:
            clean_revenues.update({f"{k}": v})
    return clean_revenues


def most_revenue():
    for state in state_tally:
        revenues = state_tally[state]["companies"]
        # Remove none's for calculation
        clean_revenues_dict = clean_revenues(revenues)
        largest_rev = max(clean_revenues_dict, key=revenues.get)
        state_tally[state]["most_revenue"] = largest_rev


def get_median():
    for state in state_tally:
        revenues = state_tally.get(state).get("companies")
        # Remove none's for calculation
        clean_revenues_dict = clean_revenues(revenues)
        sorted_companies = sorted(clean_revenues_dict.items(), key=lambda x: x[1])
        count = len(sorted_companies)
        if (count % 2) == 0:
            val1 = sorted_companies[int((count / 2) - 1)][1]
            val2 = sorted_companies[int(count / 2)][1]
            median = (val1 + val2) / 2
        else:
            median = sorted_companies[int(count / 2)][1]
        state_tally[state]["median_revenue"] = median

def generate_csv():
    # name of csv file
    filename = "state_download.csv"
    # field names
    fields = [
        "US State",
        "Total number of leads",
        "The lead with most revenue",
        "Total revenue",
        "Median revenue",
    ]
    # data rows of csv file
    rows = []
    for state in state_tally:
        state_row = [state]
        state_row.append(state_tally.get(state).get("count"))
        state_row.append(state_tally.get(state).get("most_revenue"))
        state_row.append('$' + str(state_tally.get(state).get("total_revenue")))
        state_row.append('$' + str(state_tally.get(state).get("median_revenue")))
        rows.append(state_row)

    with open(filename, "w") as csvfile:
        filewriter = csv.writer(
            csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        # writing the fields
        filewriter.writerow(fields)

        # writing the data rows
        filewriter.writerows(rows)

#To run the script
lead_dict = data_download()
state_tally = {}
state_count()
get_revenue()
most_revenue()
get_median()
generate_csv()