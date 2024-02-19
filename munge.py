import urllib.request
import pandas
import json

emea_url = "https://www.bloomberg.com/markets/api/comparison/geographic-indices?name=emea&type=region"
json_file_path = "./data/emea.json"

# Add headers to the request to avoid "Are you a robot?" page
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

# Download the URL and save it to a file
req = urllib.request.Request(emea_url, headers=headers)
with urllib.request.urlopen(req) as response, open(json_file_path, "wb") as file:
    file.write(response.read())
    print(f"Downloaded {emea_url} to {json_file_path}")

# Open the file and read the contents
stock_list = []
with open(json_file_path, "r") as file:
    # Load the JSON data into a Python object
    data = file.read()
    data_json = json.loads(data)
    # Loop through the list of dictionaries and add them to the stock_list
    for contry_stock in data_json:
        stock_list.extend(contry_stock["fieldDataCollection"])
    print(f"Loaded {len(stock_list)} stock records")

# Convert the list of dictionaries to a pandas DataFrame
df = pandas.DataFrame(stock_list)
# Drop the columns we don't need
df.drop(columns=["lastUpdateEpoch", "lastUpdateTime",
        "lastUpdateISO", "userTimeZone"], inplace=True)
# Save the DataFrame to a CSV file
df.to_csv("./data/clean_data.csv", index=False)
print(f"Saved {len(df)} records to clean_data.csv")
