from fastapi import APIRouter
import requests
from config.logging_config import logger
from external_api.gs_api import GoogleSheetsAPI

router = APIRouter()


@router.post("/intake")
async def intake():
    logger.info(f"*** API GHL: Intake")
    
    gs = GoogleSheetsAPI()
    new_intake = gs.read_all_data()
    if new_intake:
        logger.info(f"New Intake - ({new_intake})")
        
        # iterate through new contacts
        for intake_contact in new_intake:
            logger.info(f"Intake Contact - ({intake_contact})")
            
            # send new intake contact to Make
            response = requests.post(
                url="https://hook.us1.make.com/qnslfetwxho7xs01q4h9mgs2l6ufumy6",
                json={"contact": intake_contact}
            )
            if response.status_code == 200:
                logger.info("Intake Contact sent to Make")
        
    else:
        logger.warning("No New Intake")
    
    # clear worksheet
    gs.clear_worksheet()
    return {
        "intake": new_intake
    }
