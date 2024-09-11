from bs4 import BeautifulSoup
import pandas as pd
import os

# Initialize data dictionary
d = {'Clinic_Name': [], 'Phone_num': [], 'Address_text': [], 'Add_link': [], 'website_link': []}

# Loop over all HTML files in the "listings" directory
for file in os.listdir("listings"):
    try:
        with open(f"listings/{file}", 'r', encoding='utf-8') as f:
            html_doc = f.read()
        
        # Parse the HTML file
        soup = BeautifulSoup(html_doc, "html.parser")

        # Get clinic name (assuming it's in <h3> tag)
        Clinic_Name = soup.find("h3").get_text(strip=True)

        # Get phone number (assuming it's within elements with class "MuiButton-label")
        button_tag = soup.find('button', class_='ButtonPhone')
        if button_tag:
            phone_span = button_tag.find('span', class_='MuiButton-label')
            phone_number = phone_span.get_text(strip=True)
            
        else:
            phone_number="Not Available"

        # Get website link (if it exists)
        w = soup.find('a', class_="ButtonWebsite")
        if w and w.has_attr('href'):
            website_link = w['href']
        else:
            website_link = "Not available"

        # Get address and address link (assuming the first <a> tag has the address link)
        a_tag = soup.find('a')
        if a_tag and a_tag.has_attr('href'):
            add_link = "https://www.yellowpages.com.au/"+a_tag['href']
            address_text = a_tag.get_text(strip=True)
          
        else:
            add_link = "Not available"
            address_text = "Not available"
       
       # Append the data to the dictionary
        d['Clinic_Name'].append(Clinic_Name)
        d['Phone_num'].append(phone_number)
        d['Address_text'].append(address_text)
        d['Add_link'].append(add_link)
        d['website_link'].append(website_link)

    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Create a DataFrame and export to Excel
df = pd.DataFrame(data=d)
df.to_excel("data.xlsx", index=False)
print("Data has been successfully exported to data.xlsx")
