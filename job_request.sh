#!/bin/bash
URL="https://isp-proxy.tacc.utexas.edu/harrijin"
PURPLE='\033[1;35m'
NO_COLOR='\033[0m'

echo 'Welcome to the Pandemic Mobility API!'
echo -e -n "This dataset is a subset of Google's COVID-19 Mobility Report Data and contains aggregate data for all of the US, individual states, and individual counties. See ${PURPLE}README.md${NO_COLOR} for more information. "
echo 'This script allows you to easily submit a job request with the desired parameters. The job will create downloadable graphs with the desired parameters. '
echo -e -n "Enter the full ${PURPLE}state name${NO_COLOR}, not case sensitive. Enter USA if you want aggregate country data: " 
read state_name
echo -e -n "Enter the full ${PURPLE}county name${NO_COLOR}, not case sensitive (include county or parish or borough at the end). If you want aggregate data for the entire state, leave blank: " 
read county_name
echo -e -n "Enter the desired ${PURPLE}start date${NO_COLOR} in the form ${PURPLE}YYYY-MM-DD${NO_COLOR} (include leading zeroes). Leave blank for default start date (2020-02-15): " 
read start_date
echo -e -n "Enter the desired ${PURPLE}end date${NO_COLOR} in the form ${PURPLE}YYYY-MM-DD${NO_COLOR} (include leading zeroes). Leave blank for default end date (2021-04-30): " 
read end_date
categories=""
echo -e -n "Do you want a graph of ${PURPLE}Retail and Recreation${NO_COLOR} data [y/n] (default: No)? " 
read yn
case $yn in
    [Yy]* ) categories+='"retail_and_recreation_percent_change_from_baseline",';;
    [Nn]* ) :;;
esac
echo -e -n "Do you want a graph of ${PURPLE}Grocery and Pharmacy${NO_COLOR} data [y/n] (default: No)? " 
read yn
case $yn in
    [Yy]* ) categories+='"grocery_and_pharmacy_percent_change_from_baseline",';;
    [Nn]* ) :;;
esac
echo -e -n "Do you want a graph of ${PURPLE}Park${NO_COLOR} data [y/n] (default: No)? " 
read yn
case $yn in
    [Yy]* ) categories+='"parks_percent_change_from_baseline",';;
    [Nn]* ) :;;
esac
echo -e -n "Do you want a graph of ${PURPLE}Public Transit${NO_COLOR} data [y/n] (default: No)? " 
read yn
case $yn in
    [Yy]* ) categories+='"transit_stations_percent_change_from_baseline",';;
    [Nn]* ) :;;
esac
echo -e -n "Do you want a graph of ${PURPLE}Workplace${NO_COLOR} data [y/n] (default: No)? " 
read yn
case $yn in
    [Yy]* ) categories+='"workplaces_percent_change_from_baseline",';;
    [Nn]* ) :;;
esac
echo -e -n "Do you want a graph of ${PURPLE}Residential${NO_COLOR} data [y/n] (default: No)? " 
read yn
case $yn in
    [Yy]* ) categories+='"residential_percent_change_from_baseline",';;
    [Nn]* ) :;;
esac
categories=${categories%?}
command="wget --post-data='{\"sub_region_1\": \"$state_name\", \"sub_region_2\": \"$county_name\", \"start_date\": \"$start_date\", \"end_date\": \"$end_date\", \"interested_categories\": [$categories]}' $URL/new_job --no-check-certificate -q"
echo -e "Running command: ${PURPLE}$command${NO_COLOR}"
eval $command
jid=$(cat new_job | jq -r '.id')
rm new_job
echo ""
echo -e "Your job id is ${PURPLE}$jid${NO_COLOR}"
echo "To check the status of your job, run the following command:"
echo -e "${PURPLE}wget --no-check-certificate $URL/job/$jid -q -O -${NO_COLOR}"
echo "Once the status of your job is 'done', download your image using the following command:"
echo -e "${PURPLE}wget --no-check-certificate $URL/download/$jid --output-document=output.png${NO_COLOR}"
