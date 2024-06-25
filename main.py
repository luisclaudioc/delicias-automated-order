import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import re

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Connect to the file
sheet_id = "1Yhvejuf-ACahA32eQ4iBLtKyI-jD_87ZLokrpjBhPWY"
stock = client.open_by_key(sheet_id)

# Get client and client sheet
stores = {
    "1": "Empório Mais Brasil",
    "2": "Armazém Atlântico",
    "3": "By Brasil",
    "4": "Mescla Café",
    "5": "Receita Inusitada",
}
print("Enter one of the following client numbers:")
for attr, val in stores.items():    
    print(attr + ") " + val)
store = input()

# Filling function
def fill_sheet(string):
    order_line = re.search(r"([0-9]+)([a-zA-Z áíã]+)", string)
    quant = order_line.group(1)
    product = re.sub(r"^\s+|\s+$", "", order_line.group(2))
    product_index = product_list.index(product) + 1
    client_sheet.update_cell(product_index, column, quant)

# Client validator
if store in stores:
    # Enter client sheet
    client_sheet = stock.worksheet(stores[store])
    # Get products list
    product_list = list(map(lambda x: x.lower(), client_sheet.col_values(3)))
    # Get today date and fill it
    today = datetime.now().strftime("%d/%m")
    column = len(client_sheet.row_values(1)) + 1
    client_sheet.update_cell(1, column, today)
    # Read order and update
    order = open("order.txt", "r").read()
    order_array = order.split("\n")
    for element in order_array: fill_sheet(element)
    print("Process complete")

# Client not found
else: 
    print("Client not recognized")
    
