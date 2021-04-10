#!/usr/bin/env python3

import pandas as pd
import re
import datetime


global food
food = ["zomato","swiggy","tea","breads","vadapav","burger"]
global UPI
UPI = ["amazon","google","paytm","bharatpe"]
global travel_accommodate
travel_accommodate = ["ola","uber","irctc","rent"]
global bill
bill = ["jio","prepaid","bill","credit card"]
global entertainment
entertainment = ["bookmyshow","tunes"]
global salary
salary = ["salary","reward","cashback"]


global regex
regex = food + UPI + travel_accommodate + bill + entertainment + salary


def yes_bank(file,name):
    df = pd.read_csv(file)
    description = df["Description"]

    df["Payment_Area"] = "Others"
    for i,des in enumerate(df["Description"]):
        for pattern in regex:
            if bool(re.search(pattern,des,re.IGNORECASE)):
                df.at[i,"Payment_Area"] = pattern

    df["Payment_Type"] = "Others"
    for i,des in enumerate(df["Description"]):
        type = des.split("/")[0]
        df.at[i,"Payment_Type"] = type

    df["From"] = "Others"
    for i,des in enumerate(df["Description"]):
        try:
            sender = des.split("/")[2].split(":")[1]
            df.at[i,"From"] = sender
        except:
            continue

    df["To"] = "Others"
    for i,des in enumerate(df["Description"]):
        try:
            receiver = des.split("To:")[1].split("/")[0]
            df.at[i,"To"] = receiver
        except:
            continue

    df["Class"] = "Others"

    for i,des in enumerate(df["Payment_Area"]):
        if des in food:
            df.at[i,"Class"] = "Food"
        if des in UPI:
            df.at[i,"Class"] = "UPI Payment"
        if des in travel_accommodate:
            df.at[i,"Class"] = "Travel/Accommodations"
        if des in bill:
            df.at[i,"Class"] = "Bill"
        if des in entertainment:
            df.at[i,"Class"] = "Entertainment"
        if des in salary:
            df.at[i,"Class"] = "Salary"

    df = df.drop(["Value_Date","Cheque_Number","Description"],axis=1)
    df["Transaction_Date"] = df["Transaction_Date"].apply(lambda x: datetime.datetime.strptime(x,"%d %b %Y").strftime("%d/%m/%Y"))
    df.to_csv("yes.csv",index=False)
    print("CSV file was tranformed/classified successfully!!")

def icici_bank(file,name):
    df = pd.read_csv(file)
    description = df["Description"]

    df["Payment_Area"] = "Others"
    for i,des in enumerate(df["Description"]):
        for pattern in regex:
            if bool(re.search(pattern,des,re.IGNORECASE)):
                df.at[i,"Payment_Area"] = pattern

    df["Payment_Type"] = "Others"
    for i,des in enumerate(df["Description"]):
        type = des.split("/")[0]
        df.at[i,"Payment_Type"] = type

    df["To"] = "Others"
    df["Remarks"] = None


    for i,des in enumerate(df["Description"]):
        info = des.split("/")
        if len(info) == 5:
            df.at[i,"Payment_Type"] = info[0]
            df.at[i,"Remarks"] = info[2]
            df.at[i,"To"] = info[3]

    df["Class"] = "Others"

    for i,des in enumerate(df["Payment_Area"]):
        if des in food:
            df.at[i,"Class"] = "Food"
        if des in UPI:
            df.at[i,"Class"] = "UPI Payment"
        if des in travel_accommodate:
            df.at[i,"Class"] = "Travel/Accommodations"
        if des in bill:
            df.at[i,"Class"] = "Bill"
        if des in entertainment:
            df.at[i,"Class"] = "Entertainment"
        if des in salary:
            df.at[i,"Class"] = "Salary"

    df = df.drop(["Value_Date","Cheque_Number","Description"],axis=1)
    df.to_csv("icici.csv",index=False)

def bank(file,name):
    if name == "yes":
        yes_bank(file,name)
    else:
        icici_bank(file,name)

if __name__ == "__main__":
    file = input("File Name: ")
    name = input("Bank Name: ")
    bank(file,name)
