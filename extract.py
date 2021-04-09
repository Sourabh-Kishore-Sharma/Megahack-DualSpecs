#!/usr/bin/env python3

import pdfplumber
import pikepdf

import pandas as pd

import os
import re

import transform

def stmt_extract(file,cols):
    df=pd.DataFrame()
    data=[]
    with pdfplumber.open(file) as pdf:
        pages = pdf.pages
        for page in pages:
            for table in page.extract_tables():
                for row in table:
                    if bool(re.search(pattern,str(row[0]))):
                        row = ['0' if i == '' else i for i in row]
                        row = list(filter(None,row))
                        data.append(row)
        df = df.append(pd.DataFrame(data,columns=cols))
    return df


def rm_pwd(file,pwd):
    pdf = pikepdf.open(file,password = pwd)
    name = "nopwd"+str(file)
    pdf.save(name)
    return name


if __name__ == "__main__":
    pdf = input("File Name: ")
    global pattern
    if "yes" in pdf.lower():
        choice = "yes"
    elif "icici" in pdf.lower():
        choice = "icici"
    else:
        choice = input("Bank - ICICI/Yes : ").lower().strip()


    if choice == "icici":
        pattern = "[0-9]{1,4}$"
        cols = ["SrNo.","Value_Date","Transaction_Date","Cheque_Number",
                    "Description","Debit","Credit","Balance"]
    else:
        pattern = "[0-9]{2} \w* [0-9]{4}$"
        cols = ["Transaction_Date","Value_Date","Cheque_Number",
                "Description","Debit","Credit","Balance"]


    res = input("Is your PDF password protected? y/n : ").lower()
    if res == "n":
        try:
            df = stmt_extract(pdf,cols)
        except Exception as e:
            print(e)
            print("Incorrect password or corrupted file.")
            exit()
    else:
        pwd = input("Password: ")
        file = rm_pwd(pdf,pwd)
        df = stmt_extract(file,cols)

    #print(df)
    out = str(choice)+".csv"
    df.to_csv(out,index=False)
    print("Bank statements was successfully extracted!!")
    transform.bank(out,choice)
