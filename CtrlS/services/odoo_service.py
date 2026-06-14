import os
from dotenv import load_dotenv

load_dotenv()
import xmlrpc.client

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")


def test_odoo_connection():
    try:
        common = xmlrpc.client.ServerProxy(
            f"{ODOO_URL}/xmlrpc/2/common"
        )

        uid = common.authenticate(
            ODOO_DB,
            ODOO_USERNAME,
            ODOO_PASSWORD,
            {}
        )

        if uid:
            return {
                "success": True,
                "uid": uid
            }

        return {
            "success": False,
            "message": "Authentication failed"
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
def get_odoo_connection():

    common = xmlrpc.client.ServerProxy(
        f"{ODOO_URL}/xmlrpc/2/common"
    )

    uid = common.authenticate(
        ODOO_DB,
        ODOO_USERNAME,
        ODOO_PASSWORD,
        {}
    )

    models = xmlrpc.client.ServerProxy(
        f"{ODOO_URL}/xmlrpc/2/object"
    )

    return uid, models


def create_crm_lead(
    name,
    email,
    phone=None,
    company=None,
    description=None
):

    uid, models = get_odoo_connection()

    lead_id = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "crm.lead",
        "create",
        [{
            "name": name,
            "contact_name": name,
            "email_from": email,
            "phone": phone or "",
            "partner_name": company or "",
            "description": description or "",
        }]
    )

    return lead_id   
