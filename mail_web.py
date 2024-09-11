from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options
chrome_options = Options()

# Set up the Chrome WebDriver with ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the Temp-Mail website
driver.get("https://temp-mail.org/")

# Wait to ensure the page loads fully
wait = WebDriverWait(driver, 30)

# Function to find the "Copy" button
def find_copy_button():
    try:
        return wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='tm-body']/div[1]/div/div/div[2]/div[1]/form/div[1]/div/button[2]")))
    except Exception as e:
        print(f"Copy button not found: {e}")
        return None

# Function to check if email field is populated
def is_email_filled():
    try:
        email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"mail\"]")))
        return email_field.get_attribute('value') != ''
    except Exception as e:
        print(f"Email field not found or error checking: {e}")
        return False

# Step 1: Wait for the email field to be populated
email_filled = False
timeout = 30  # Timeout for waiting
start_time = time.time()
while time.time() - start_time < timeout:
    if is_email_filled():
        email_filled = True
        break
    print("Waiting for email field to be populated...")
    time.sleep(5)  # Wait before checking again

if email_filled:
    # Step 2: Try to locate and click the "Copy" button
    copy_button = find_copy_button()
    if copy_button:
        print("Found the Copy button.")
        copy_button.click()  # Click the button to copy the email address
        print("Clicked the Copy button.")
    else:
        print("Copy button not found.")
else:
    print("Email field is not populated within the timeout period.")

# Close the browser session after use
time.sleep(5)  # Give some time to verify the action
driver.quit()
