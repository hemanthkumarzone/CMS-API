import xmlrpc.client

ODOO_URL = "http://localhost:8069"
ODOO_DB = "portfolio_odoo"
ODOO_USERNAME = "chejarladhanalakshmi18@gmail.com"
ODOO_PASSWORD = "Admin@123"


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
