import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Edge WebDriver
driver = webdriver.Edge()

# Search parameters
search1 = "health"
search2 = "clinic"
location1 = "queensland"
location2 = "Australia"

# Open the webpage
url = f"https://www.yellowpages.com.au/search/listings?clue={search1}+{search2}&locationClue={location1}%2C+{location2}&lat=&lon="
driver.get(url)

# Create a directory for saving HTML files
os.makedirs('listings', exist_ok=True)

listing_counter = 1  # Counter for naming HTML files

while True:
    try:
        # Wait until FreeListing elements are present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "FreeListing"))
        )

        # Find all FreeListing elements on the current page
        free_listings = driver.find_elements(By.CLASS_NAME, "FreeListing")
        print(f"Number of listings on this page: {len(free_listings)}")

        # Extract and save HTML content of each FreeListing box
        for listing in free_listings:
            # Get HTML content of the listing
            listing_html = listing.get_attribute('outerHTML')
            
            # Define the filename
            filename = f'listings/listing_{listing_counter}.html'
            
            # Save HTML content to file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(listing_html)
            
            # Increment counter
            listing_counter += 1

        # Attempt to click the next page button
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Next'))  # Adjust selector as needed
            )
            next_button.click()
        except Exception as e:
            print("No more pages or unable to click 'Next' button:", e)
            break

    except Exception as e:
        print(f"Error: {e}")
        break


driver.quit()
