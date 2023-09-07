import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and connect to Google Drive
def authenticate_gdrive():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("openprocedures-amba-9d8238b4597b.json", scope)
    client = gspread.authorize(creds)
    return client

# Save checklist results to Google Drive
def save_to_gdrive(checklist_results, completed_by, client):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = f"Restaurant Opening Procedure Checklist Results (Submitted on: {timestamp} by {completed_by}):\n\n"
    for section, results in checklist_results.items():
        content += f"{section}:\n"
        for item, result in zip(sections[section], results):
            content += f"{'[x]' if result else '[ ]'} {item}\n"
        content += "\n"

    # Write to Google Sheet
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/135KjN_wUu4gXv4_Ht9TaumflMXkThA2JRKFYrGeX_po/edit#gid=0')
    worksheet = spreadsheet.sheet1
    worksheet.append_row([timestamp, completed_by, content])


# Create a checkbox for each item in the checklist
def create_checklist():
    st.title('Restaurant Opening Procedure')
    
    sections = {
        "9:00 am - 9:10 am: Setting the Ambiance": [
            "Turn on lights",
            "Turn on music"
        ],
        "9:10 am - 9:20 am: Preliminary Food Preparations": [
            "Rinse and soak rice (this will continue passively)",
            "Open cooler lids and organize utensils"
        ],
        "9:20 am - 9:35 am: Grills and Fryers Setup": [
            "Activate fryers (assuming simultaneous activation)",
            "Heat grills (assuming simultaneous heating)",
            "Ignite gyro pilots",
            "Prepare gyro cone",
            "Prepare containers for falafel"
        ],
        "9:35 am - 9:50 am: Food Preparations": [
            "Assemble bread",
            "Position sauces",
            "Refill dips and toppings",
            "Stock cooler with meat and falafel"
        ],
        "9:50 am - 10:05 am: Cooking & Grilling": [
            "Cook meats and grill vegetables (assuming some simultaneous cooking)"
        ],
        "10:05 am - 10:20 am: Final Cooking & Preparations": [
            "Prepare fries (assuming some leftover)",
            "Set up gyro slicer and prepare storage",
            "Fill steamers with water",
            "Check on the rice that has been soaking/cooking"
        ],
        "10:20 am - 10:30 am: Final Touches": [
            "Activate the 'Open' sign",
            "Double-check everything, ensure everything is in place, and make any final adjustments"
        ]
    }

    checklist_results = {}
    for section, items in sections.items():
        st.subheader(section)
        checklist_results[section] = [st.checkbox(item) for item in items]

    return checklist_results, sections


client = authenticate_gdrive()
checklist_results, sections = create_checklist()
completed_by = st.text_input("Completed by:")

if st.button('Submit'):
    if completed_by:
        save_to_gdrive(checklist_results, completed_by, client)
        st.success("Checklist submitted and saved to Google Drive!")
    else:
        st.warning("Please provide your name in the 'Completed by' section.")
