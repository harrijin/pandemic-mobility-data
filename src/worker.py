from redis_helper import q, update_job_status, get_job, get_data_point, add_image
import datetime
import matplotlib.pyplot as plt

@q.worker
def execute_job(jid):
    job = get_job(jid)
    job_info = {key.decode('utf-8'): value.decode('utf-8') for key, value in job.items()}
    update_job_status(jid, "in progress")
    # generate date range
    # default start and end dates based on start and end dates of dataset
    start_date = datetime.date(2020, 2, 15)
    end_date = datetime.date(2021, 4, 30)
    if job_info["start_date"]:
        start_date = datetime.datetime.strptime(job_info["start_date"], '%Y-%m-%d').date()
    if job_info["end_date"]:
        end_date = datetime.datetime.strptime(job_info["end_date"], '%Y-%m-%d').date()
    day_delta = datetime.timedelta(days=1)
    # loop over date range
    dates_list = list()
    categories_string = job_info["interested_categories"]
    categories = categories_string.strip('][').split(', ')
    all_data = list() # list of tuples where each tuple will match the index of the desired categories
    for i in range((end_date-start_date).days):
        date = start_date + i*day_delta
        dates_list.append(date)
        state = job_info["sub_region_1"].title()
        county = job_info["sub_region_2"].title()
        if state == "Usa":
            state = ""
        key = state +"_"+county+"_"+date.strftime('%Y-%m-%d')
        row = get_data_point(key)
        if len(row) == 0:
            continue
        data_point = tuple(row[category.strip("'")] for category in categories)
        all_data.append(data_point)

    generate_plot(dates_list, all_data, location_name(job_info["sub_region_1"], job_info["sub_region_2"]), categories)
    # save plot file
    with open('output_img.png', 'rb') as f:
        img = f.read()
        add_image(jid, img)

    update_job_status(jid, "done")
    
def human_readable_categories(category):
    if category == 'retail_and_recreation_percent_change_from_baseline':
        return "Retail and Recreation"
    if category == 'grocery_and_pharmacy_percent_change_from_baseline':
        return "Grocery and Pharmacy"
    if category == 'parks_percent_change_from_baseline':
        return "Parks"
    if category == 'transit_stations_percent_change_from_baseline':
        return "Public Transit"
    if category == 'workplaces_percent_change_from_baseline':
        return "Workplaces"
    if category == 'residential_percent_change_from_baseline':
        return "Residential Area"
    return "invalid category"
    
def generate_plot(dates, all_data, location, categories):
    for i in range(len(categories)):
        data = [float(data_point[i]) for data_point in all_data]
        plt.plot(dates, data, '-o', label = human_readable_categories(categories[i].strip("'")))
    plt.plot(dates, [0 for i in range(len(dates))], color='black', linewidth='4', label="Baseline")
    plt.xlabel('Date')
    plt.ylabel('Percent change from baseline')
    plt.title("Mobility data for " + location.title())
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.gcf().set_figwidth(10)
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.grid(b=True,which='both')
    # plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
    plt.savefig("output_img.png")
    plt.clf()
    plt.cla()
    
def location_name(sub_region_1, sub_region_2):
    if not sub_region_1 and not sub_region_2:
        return "United States"
    if not sub_region_2:
        return sub_region_1
    return sub_region_2 + ", " + sub_region_1

execute_job()