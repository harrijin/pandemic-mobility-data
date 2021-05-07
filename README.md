# pandemic-mobility-data

This repository contains the source code for a front-end API for a subset of Google's [COVID-19 Mobility Report](https://www.google.com/covid19/mobility/). The subset contains only data for the United States, and contains data from 2/15/2020 to 4/30/2021. From Google's [overview](https://support.google.com/covid19-mobility/answer/9824897?hl=en&ref_topic=9822927):

> The data shows how visitors to (or time spent in) categorized places change compared to our baseline days. A baseline day represents a normal value for that day of the week. The baseline day is the median value from the 5‑week period Jan 3 – Feb 6, 2020.
>
>For each region-category, the baseline isn’t a single value—it’s 7 individual values. The same number of visitors on 2 different days of the week, result in different percentage changes. 
>
>To help you track week-to-week changes, the baseline days never change. These baseline days also don't account for seasonality. For example, visitors to parks typically increase as the weather improves.

The files in this repository can be used to build three separate Docker containers: a [front-end Flask API](), a [Redis database](), and a [Python worker node](). These three Docker containers can then be deployed using either the provided `docker-compose` file or Kubernetes configuration files.

The worker node generates a downloadable graph that shows changes in mobility due to the COVID-19 Pandemic. This graph can be customized to different date ranges, locations (county, statewide, or nationwide), and travel-type (Retail/Recreation, Grocery/Pharmacy, Parks, Public Transit, Workplaces, and Residential Areas).

![Example Image](./examples/example.png)

## Deployment Instructions

### Docker-compose

To deploy the API using `docker-compose`, navigate into the root directory of this repository and run the following:

```
make compose-up
```

### Kubernetes

Do the following to deploy the API to a Kubernetes cluster. 

## Using the API