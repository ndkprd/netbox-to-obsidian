import requests
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os

# Load environment from the .env file
load_dotenv()

# Netbox needed variable
netbox_api_token = os.getenv('NETBOX_API_TOKEN')
netbox_api_url = f"{os.getenv('NETBOX_URL')}/api/dcim/devices/"
# Obsidian needed variable
obsidian_folder_device = os.getenv('OBSIDIAN_FOLDER_DEVICE')

# Set up the headers with the API token
headers = {
    "Authorization": f"Token {netbox_api_token}"
}

# Perform the GET request and save the response into a variable
response = requests.get(netbox_api_url, headers=headers)

# Check if the request was successful and store the content in a variable
if response.status_code == 200:
    print("Collected the data from Netbox successfully.")
    response_data = response.json().get('results', [])  # Assign the var with the value of 'results' dict item

    # print(response_data)
else:
    print(f"Request failed with status code {response.status_code}")
    response_data = None

# Setup the Jinja2 environment and load the template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('templates/device.md.j2')

# Loop through each item in response_data and render the file for each device.
if response_data:
    for device in response_data:
        # Render the template with the json data for each device.
        rendered_template = template.render(device)
        filename = f"{obsidian_folder_device}/{device['name']}.md"
        # Save the rendered template into a file
        with open(filename, 'w') as f:
            f.write(rendered_template)
        print(f"Template save to {filename}")
