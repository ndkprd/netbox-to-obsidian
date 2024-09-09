import requests
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os
import yaml

# Load environment from the .env file
load_dotenv()

# Load configuration from the YAML file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Netbox needed variable
netbox_api_token = os.getenv('NETBOX_API_TOKEN')
netbox_base_url =  os.getenv('NETBOX_URL')
# Set up the headers with the API token
headers = {
    "Authorization": f"Token {netbox_api_token}"
}

# Setup the Jinja2 environment and load the template
env = Environment(loader=FileSystemLoader('templates'))

# Loop through each configured Netbox endpoints
for item in config['config']:
    netbox_endpoint = item['netbox_endpoint']
    obsidian_template = item['obsidian_template']
    obsidian_folder = item['obsidian_folder']

    # Construct the full API URL
    netbox_api_url = f"{netbox_base_url}{netbox_endpoint}"
    
    # Perform the GET request and save the response into a variable
    response = requests.get(netbox_api_url, headers=headers)

    # Check if the request was successful and store the content in a variable
    if response.status_code == 200:
        print(f"Collected the data from Netbox successfully from {netbox_endpoint}.")
        response_data = response.json().get('results', [])  # Assign the var with the value of 'results' dict item
        
        if response_data:
            for data_item in response_data:
                # Load the appropriate template.
                template = env.get_template(obsidian_template)
                # Render the template with the json data for each item.
                rendered_template = template.render(data_item)
                
                # Define the filename.
                if "device-types" in netbox_endpoint:
                    filename = f"{obsidian_folder}/{data_item['model']}.md"
                else:
                    filename = f"{obsidian_folder}/{data_item['name']}.md"

                # Save the rendered template into a file
                with open(filename, 'w') as f:
                    f.write(rendered_template)
                print(f"Template save to {filename}")
    else:
        print(f"Request failed with status code {response.status_code}")
