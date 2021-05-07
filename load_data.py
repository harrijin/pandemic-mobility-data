import csv, requests, os

api_url = "http://localhost:5013/create"
columns_to_keep = ['sub_region_1', 'sub_region_2', 'date', 'retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline']
counter = 0

for file in os.listdir('data'):
    with open('data/' + file, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        table = list()
        for row in csv_reader:
            # sub_region_1 is state, sub_region_2 is county
            filtered_row = dict()
            for column in columns_to_keep:
                filtered_row[column] = row[column]
            table.append(filtered_row)
            counter += 1
            print("adding row number {}".format(counter))
        print("sending post request")
        r = requests.post(api_url, json=filtered_row)
        print(r.text)
print("done")