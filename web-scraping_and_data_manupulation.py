# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import json
import pandas as pd

xhr_url = "https://www.desocialekaart.be/api/health-offers?rubrics=06.%20OPLEIDING%2C%20WERKLOOSHEID%20EN%20TEWERKSTELLING&page=0&size=1511&sort=RELEVANCE"

response = requests.get(xhr_url)

names = []
postal_codes = []
category_data = []



if response.status_code == 200:
    data = response.json()
    formatted_json = json.dumps(data, indent=4)
   
    for i in range(1511):
        company = data["_embedded"]["healthOfferProviderRepresentationList"][i]
        name = company["legalName"]["description"]
        
        
        if "addresses" in company and company["addresses"]:
            code = company["addresses"][0]["municipality"]["postalCode"]
        else:
            code = "N/A"
            
      
        categories = [activity["name"]["description"] for activity in company["activities"]]
            
        names.append(name)
        postal_codes.append(code)
        category_data.append(categories)
    
    df = pd.DataFrame({
        "Name": names,
        "Postal Code": postal_codes
    })
    
 
    unique_categories = set()

    for sublist in category_data:
        for category in sublist:
            unique_categories.add(category)
    
 
    for category in unique_categories:
        for i, categories in enumerate(category_data):
            df[category] = [1 if category in categories else 0 for categories in category_data]
            
    

   
    excel_file = "organization_data.xlsx"
    df.to_excel(excel_file, index=False, engine="openpyxl")

    print(f"Data has been collected and exported to {excel_file}.")
    
    
else:
    print(f"Request failed with status code: {response.status_code}")