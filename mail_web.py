#!/usr/bin/env python3  # Shebang for Unix-based platforms

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyperclip  # This library helps in accessing the clipboard
import os         # To handle file paths in a cross-platform manner

# Set up Chrome options
chrome_options = Options()

# Set up the Chrome WebDriver with ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the Temp-Mail website
driver.get("https://temp-mail.org/")

# Wait to ensure the page loads fully
wait = WebDriverWait(driver, 40)

# Function to find the "Copy" button
def find_copy_button():
    try:
        return wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='tm-body']/div[1]/div/div/div[2]/div[1]/form/div[1]/div/button[2]")))
    except Exception as e:
        print(f"Copy button not found: {e}")
        return None

# Function to check if the email field is populated
def is_email_filled():
    try:
        email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='mail']")))
        return email_field.get_attribute('value') != ''
    except Exception as e:
        print(f"Email field not found or error checking: {e}")
        return False

# Function to retrieve the email from the email field
def get_email():
    try:
        email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='mail']")))
        return email_field.get_attribute('value')
    except Exception as e:
        print(f"Error retrieving the email: {e}")
        return None

# Function to verify if the email is copied to clipboard
def is_email_copied_to_clipboard(expected_email):
    clipboard_content = pyperclip.paste()  # Get the current clipboard content
    return clipboard_content == expected_email

# Function to manually copy the email from the email field
def manually_copy_email_to_clipboard(email_text):
    try:
        pyperclip.copy(email_text)  # Copy email text to clipboard
        print(f"Email manually copied to clipboard: {email_text}")
    except Exception as e:
        print(f"Failed to manually copy email to clipboard: {e}")

# Function to check for new emails and fetch the OTP
def check_for_email_and_fetch_otp():
    try:
        # Wait for the inbox to load
        inbox_table = wait.until(EC.presence_of_element_located((By.ID, "tm-mailbox")))

        # Find the first email in the inbox (you might need to adjust the XPath depending on the page structure)
        first_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='tm-mailbox']/div[1]")))
        first_email.click()  # Open the first email

        # Wait for the email content to load
        email_body = wait.until(EC.visibility_of_element_located((By.ID, "tm-message-content")))

        # Extract OTP or relevant text (modify based on the structure of the email)
        otp_text = email_body.text
        print(f"Email content fetched: {otp_text}")

        # Save OTP or email content to a file in a platform-independent way
        script_dir = os.path.dirname(__file__)  # Absolute path of script directory
        file_path = os.path.join(script_dir, 'otp.txt')  # Platform-independent path
        with open(file_path, 'w') as file:
            file.write(otp_text)
        print(f"OTP/email content saved to {file_path}.")

    except Exception as e:
        print(f"Error while checking for or reading email: {e}")

# Step 1: Wait for the email field to be populated
email_filled = False
timeout = 30  # Timeout for waiting
start_time = time.time()
while time.time() - start_time < timeout:
    if is_email_filled():
        email_filled = True
        break
    print("Waiting for email field to be populated...")
    time.sleep(10)  # Wait before checking again

if email_filled:
    # Step 2: Retrieve the temporary email
    temp_email = get_email()
    if temp_email:
        print(f"Temporary email: {temp_email}")

        # Step 3: Keep trying to copy the email until it is successfully copied to the clipboard
        email_copied = False
        while not email_copied:
            # Try to find and click the "Copy" button
            copy_button = find_copy_button()
            if copy_button:
                print("Found the Copy button.")
                copy_button.click()  # Click the button to copy the email address
                print("Clicked the Copy button.")

                # Check if the email has been successfully copied to the clipboard
                time.sleep(10)  # Wait a moment before checking the clipboard
                if is_email_copied_to_clipboard(temp_email):
                    print("Email successfully copied to clipboard.")
                    email_copied = True
                else:
                    print("Email not copied to clipboard. Retrying...")
            else:
                # Fallback: Copy the email text directly from the email field
                print("Copy button not found. Falling back to manually copying the email from the text field.")
                manually_copy_email_to_clipboard(temp_email)

                # Verify if the email has been copied to the clipboard
                if is_email_copied_to_clipboard(temp_email):
                    print("Email manually copied to clipboard successfully.")
                    email_copied = True
                else:
                    print("Manual copy failed. Retrying...")
else:
    print("Email field is not populated within the timeout period.")

# Close the browser session after use
time.sleep(10)  # Give some time to verify the action
driver.quit()
