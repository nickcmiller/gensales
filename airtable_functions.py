import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#Define api_key
api_key = os.environ.get('AIRTABLE_API_KEY')

def get_base_id(base_name, api_key=api_key):
    # Make the GET request to retrieve the list of bases
    url = 'https://api.airtable.com/v0/meta/bases'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)

    # Make GET request to Airtable API endpoint for bases
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    base_url = 'https://api.airtable.com/v0/meta/bases'
    base_response = requests.get(base_url, headers=headers)

    # Parse response JSON to retrieve base ID
    base_id = None
    for base in base_response.json()['bases']:
        if base['name'] == base_name:
            base_id = base['id']
            break

    if base_id is None:
        raise ValueError(f"No base found with name '{base_name}'")
        
    #Return base ID
    return(base_id)
    
def create_table(base_id, table_name, table_description, fields, api_key=api_key):

    # Set headers for the POST request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Define data for the POST request
    data = {
        'name': table_name,
        'description': table_description,
        'fields': fields
    }

    # Set the URL for the POST request
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code)

    # Return the response
    return response.json()