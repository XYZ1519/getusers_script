import requests
import csv

url = "https://api.{HERE}.amity.co/api/v3/users"  # Replace with your API endpoint
headers = {
    "accept": "application/json",
    "Authorization": "Bearer {INSERT TOKEN HERE}" # Please add the Bearer token obtained from POST /api/v3/sessions when using an Admin User. Please follow the details in the following link https://api-docs.amity.co/#/Session/post_api_v3_sessions
    }  

page_token = None    
has_more_pages = True
loop_count = 1
paging = None
next_page = None

# Create a CSV file and initialize the CSV writer
csv_filename = "users.csv"
csv_file = open(csv_filename, "w", newline="")
csv_writer = csv.writer(csv_file)

while has_more_pages:
    params = {'options[limit]':1,'options[token]': page_token} if page_token else {}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()

        users = data['users']
        if page_token is None:
            # Extract field names from the first page and write them as the CSV header
            field_names = list(users[0].keys())
            csv_writer.writerow(field_names)

        for user in users:
            # Write the data to the CSV file
            csv_writer.writerow(user.values())

        # Process the data from the current page
        print("====================================================================")

        print(loop_count)
        loop_count = loop_count+1
        paging = data.get('paging')
        print(paging)
        next_page = paging.get('next') if paging else None
        print(next_page)
        page_token = next_page if next_page else None
        print(page_token)
        has_more_pages = page_token is not None
        
    else:
        print("====================================================================")
        print(paging)
        print(loop_count)
        print(next_page)
        print(page_token)
        print('Error:', response.status_code)
        break

# Close the CSV file
csv_file.close()

print(f"Data saved to '{csv_filename}' successfully.")