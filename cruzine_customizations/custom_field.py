from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import frappe

def setup_custom_fields():
    custom_fields = {
        "Payment Term": [
            dict(fieldname='term_type',
                label='Term Type',
                fieldtype='Select',
                options='\nBefore Dispatch\nOn Dispatch\nOther',
                mandatory=1,
                insert_after='due_date_based_on'
            ),
        ],
    }
    try:
        create_custom_fields(custom_fields)
    except:
        print("Exception while createing customfield")
        frappe.error_log()