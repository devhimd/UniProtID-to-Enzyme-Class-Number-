# Importing the library
import requests
# Extracting the EC Number from the rhea database
def fetch_ec_numbers(uniprot_id):
	url= "https://www.rhea-db.org/rhea?"
	parameters = {
  		"query":f"uniprot:{uniprot_id}",
  		"columns":"ec",
  		"format":'tsv',
  		"limit":10,
	}
	response = requests.get(url,params=parameters)
	if response.status_code == 200:
    		ec_numbers = response.text.split("\n")
    		ec_numbers = [ec.replace("EC:", "") for ec in ec_numbers if ec]
    		return ec_numbers
	else:
    		print(f"Failed to fetch data for {uniprot_id}. Status code: {response.status_code}")
    		return []
# Text File as Input where it consists of the UniProtID
input_file = "uniprot_ids.txt"
with open(input_file, "r") as file:
	uniprot_ids = [line.strip() for line in file.readlines()]
# Fetch EC numbers for each UniProtID
results = {}
for uniprot_id in uniprot_ids:
	ec_numbers = fetch_ec_numbers(uniprot_id)
	results[uniprot_id] = ec_numbers
# Categorisizing the Enzyme Classes
def categorize_ec(ec_numbers):
    categories = set()
    if not ec_numbers:
        return ["NA"]
    for ec_number in ec_numbers:
        if ec_number.startswith('1'):
            categories.add("Oxidoreductase")
        if ec_number.startswith('2'):
            categories.add("Transferases")
        if ec_number.startswith('3'):
            categories.add("Hydrolases")
        if ec_number.startswith('4'):
            categories.add("Lyases")
        if ec_number.startswith('5'):
            categories.add("Isomerases")
        if ec_number.startswith('6'):
            categories.add("Ligases")
        if ec_number.startswith('7'):
            categories.add("Translocases")
    if not categories:
        return ["NA"]
    return list(categories)
    if len(categories) > 1:
        return list(categories)
    elif len(categories) == 1:
        return list(categories)[0]  # Return the single category
# Write the Results to a CSV File
output_file = "EC_Numbers_Output.csv"
with open(output_file, "w") as file:
    file.write("UniProt ID,EC Numbers, EC Categories\n")
    for uniprot_id, ec_numbers in results.items():
    	ec_categories = categorize_ec(ec_numbers)
    	file.write(f"{uniprot_id},{','.join(ec_numbers)},{','.join(ec_categories)}\n")
print(f"Output saved to {output_file}")
