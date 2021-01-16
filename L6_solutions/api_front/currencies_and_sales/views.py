import logging

import pandas as pd
import requests
from django.shortcuts import render
from json2html import json2html

logging.basicConfig(level=logging.DEBUG)

BASE_URL = "http://127.0.0.1:5000"
BASE_URL_SALES = f"{BASE_URL}/sales"
BASE_URL_RATES = f"{BASE_URL}/rates/usd"
DATE_START = "2013-01-01"
DATE_END = "2014-12-31"


def get_endpoint(request, root_url, date_range=False):
    start = request.POST.get("start")

    if date_range:
        end = request.POST.get("end")
        return f"{root_url}/{start}/{end}", start, end
    return f"{root_url}/{start}", start


def get_error_msg(status_code):
    if status_code == 404:
        return f"No data found. Note that data is available only for date range {DATE_START} - {DATE_END}"
    if status_code == 400:
        return "End date cannot be earlier than start date."
    return "Unknown error occurred"


def get_html_table(data):
    return json2html.convert(data, table_attributes="class=\"table table-hover\"")


def get_data(endpoint):
    logging.info(f"Requesting data from {endpoint}")

    response = requests.get(endpoint)
    logging.info(response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def index(request):
    return render(request, "index.html")


def rates_single_date(request):
    context = {
        'title': "USD rates",
        'heading': "USD rate for single date"
    }

    if request.method == "POST":
        endpoint, desired_date = get_endpoint(request, BASE_URL_RATES)

        data = get_data(endpoint)
        if not type(data) is int:
            context["table"] = get_html_table(data)
            context["table_heading"] = f"USD rate from {desired_date}"
        else:
            context["error_msg"] = get_error_msg(data)

    return render(request, "single_date.html", context=context)


def rates_date_range(request):
    context = {
        'title': "USD rates",
        'heading': "USD rates from date range",
    }

    if request.method == "POST":
        endpoint, start_date, end_date = get_endpoint(request, BASE_URL_RATES, date_range=True)

        data = get_data(endpoint)
        if not type(data) is int:
            context["table"] = get_html_table(data)
            context["label"] = "USD rate"
            context["data"] = pd.DataFrame(data)['USD'].to_list()
            context["labels"] = pd.DataFrame(data)['effectiveDate'].to_list()
            context["table_heading"] = f"USD rates from {start_date} to {end_date}"

        else:
            context["error_msg"] = get_error_msg(data)

    return render(request, "date_range.html", context=context)


def sales_single_date(request):
    context = {
        'title': "Sales",
        'heading': "Single date sales",
    }

    if request.method == "POST":
        endpoint, desired_date = get_endpoint(request, BASE_URL_SALES)

        data = get_data(endpoint)
        if not type(data) is int:
            context["table"] = get_html_table(data)
            context["table_heading"] = f"Sales from {desired_date}"

        else:
            context["error_msg"] = get_error_msg(data)

    return render(request, "single_date.html", context=context)


def sales_date_range(request):
    context = {
        'title': "Sales",
        'heading': "Sales from date range",
        'available_currencies': ['USD', 'PLN']
    }
    if request.method == "POST":
        endpoint, start_date, end_date = get_endpoint(request, BASE_URL_SALES, date_range=True)
        ccy = request.POST.get("ccy")

        data = get_data(endpoint)
        if not type(data) is int:
            ccy_data = pd.DataFrame(data)[['DATE', ccy]]
            context["table"] = get_html_table(ccy_data.to_json(orient="records"))
            context["label"] = f"Sales in {ccy}"
            context["data"] = ccy_data[ccy].to_list()
            context["labels"] = ccy_data['DATE'].to_list()
            context["table_heading"] = f"Sales from {start_date} to {end_date} in {ccy}"

        else:
            context["error_msg"] = get_error_msg(data)

    return render(request, "date_range.html", context=context)
