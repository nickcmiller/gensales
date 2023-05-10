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
    
def get_fields(base_id, table_name, api_key=api_key):
    try:
        # Make the API request to retrieve the table schema
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if there is an HTTP error
        response_json = response.json()
        tables = response_json['tables']

        for table in tables:
            if table['name'] == table_name:
                fields = table['fields']

        field_names = []
        for field in fields:
            field_names.append({
                'id': field['id'],
                'name': field['name'],
            })

        return field_names
    except requests.exceptions.RequestException as e:
        # Handle any HTTP errors or network-related errors
        print("Error: ", e)
        return []
    except KeyError as e:
        # Handle any errors related to missing or incorrect data keys
        print("Error: ", e)
        return []
    except Exception as e:
        # Handle any other unexpected errors
        print("Error: ", e)
        return []

def process_record(base_id, table_name, record, fields, process_field, api_key=api_key):
    try:
        
        record_id = record['id']
        record_name = record['fields']['Name']

        url = f"https://api.airtable.com/v0/{base_id}/{table_name}/{record_id}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        new_fields = {}
        
        #Iterate through every non-index field in the record
        for field in fields[1:]:
            field_key = field['name']
            field_value = process_field(field_key)
            new_fields[field_key]=field_value

        json_data = {
            "fields": new_fields
        }

        # Send the PATCH request to update the record's field
        response = requests.patch(url, headers=headers, json=json_data)
        response.raise_for_status()  # Raise an exception if there is an HTTP error

        # Check if the request was successful
        if response.status_code == 200:
            print(f"Record {record_name} updated successfully!")
        else:
            print("Error updating field. Error:", response.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any HTTP errors or network-related errors
        print("Error: ", e)
    except KeyError as e:
        # Handle any errors related to missing or incorrect data keys
        print("Error: ", e)
    except Exception as e:
        # Handle any other unexpected errors
        print("Error: ", e)

def iterate_through_records(base_id, table_name, fields, process_field, api_key=api_key):
    try:
        # Make the API request to get the first page of records
        url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
        headers = {"Authorization": f"Bearer {api_key}"}
        params = {"pageSize": 100, "fields":""} # Change the page size if needed
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception if there is an HTTP error
        response_json = response.json()
    
        # Iterate through the records on the first page
        for record in response_json["records"]:
            process_record(base_id, table_name, record, fields, process_field)
    
        # Check if there are more pages of records
        while "offset" in response_json:
            # Make the API request to get the next page of records
            params["offset"] = response_json["offset"]
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception if there is an HTTP error
            response_json = response.json()
    
            # Iterate through the records on the current page
            for record in response_json["records"]:
                process_record(base_id, table_name, record, fields, process_field)
    except requests.exceptions.RequestException as e:
        # Handle any HTTP errors or network-related errors
        print("Error: ", e)
    except KeyError as e:
        # Handle any errors related to missing or incorrect data keys
        print("Error: ", e)
    except Exception as e:
        # Handle any other unexpected errors
        print("Error: ", e)