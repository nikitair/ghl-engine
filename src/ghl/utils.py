from config.logging_config import logger
from external_api.gs_api import GoogleSheetsAPI


def prepare_contacts_to_create() -> list[dict]:
    gs = GoogleSheetsAPI()
    contacts = []
    
    raw_new_contacts = gs.read_all_data()
    if not raw_new_contacts:
        logger.warning(f"!No NEW Contacts found")
        return contacts
    
    for raw_contact in raw_new_contacts:
        logger.info(f"Processing raw Contact - ({raw_contact})")
        
        contact = {
            "business_name": raw_contact["Company name"],
            "first_name": raw_contact["First Name"],
            "last_name": raw_contact["Last Name"],
            # "phone": [raw_contact["Mobile phone 1"], raw_contact["Mobile phone 2"], raw_contact["Mobile phone 3"]],
            "email": raw_contact["Email"],
            "brokerage_phone_number": raw_contact["Brokerage phone"],
            "city": raw_contact["City"],
            "province": raw_contact["Province"],
            "postal_code": raw_contact["Postal Code"],
            "website": raw_contact["Website URL"],
            "linkedin": raw_contact["LinkedIn"],
            "brokerage": raw_contact["Address Line"]
        }