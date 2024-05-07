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
        "Sales Order": [
            dict(fieldname='customer_city',
                label='Customer City',
                fieldtype='Data',
                fetch_from = 'customer_address.customer_city',
                insert_after='address_display'
            ),
            dict(fieldname='customer_shipping_city',
                label='Customer Shipping City',
                fieldtype='Data',
                fetch_from = 'shipping_address_name.customer_city',
                insert_after='shipping_address'
            ),
        ],
        "Customer": [
            dict(fieldname='customer_city',
                label='Customer City',
                fieldtype='Link',
                options='City Master',
                insert_after='customer_type',
                allow_in_quick_entry=True
            ),
        ],
        "Address": [
            dict(fieldname='customer_city',
                label='Customer City',
                fieldtype='Link',
                options='City Master',
                insert_after='city'
            ),
        ],
         "Shipping Rule": [
            dict(fieldname='city_master_table',
                label='City Master Table',
                fieldtype='Table MultiSelect',
                options='City Master Table',
                insert_after='countries'
            ),
            dict(fieldname='incoterm_master_table',
                label='Incoterm Master Table',
                fieldtype='Table MultiSelect',
                options='Incoterm Master Table',
                insert_after='city_master_table'
            ),
        ]

    }
    try:
        create_custom_fields(custom_fields)
    except:
        print("Exception while createing customfield")
        frappe.error_log()