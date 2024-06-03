import frappe

def capitalize(sentence):
    return (' ').join(map(lambda word: word[0].upper() + word[1:], sentence.split(' ')))


def validate(doc, method):
    doc.customer_name = capitalize(doc.customer_name)
    if doc.custom_verification != doc.get_doc_before_save().custom_verification:
        sos = frappe.get_all("Sales Order",{"customer": doc.name})
        for so in sos:
            frappe.db.set_value("Sales Order", so['name'], 
                "custom_customer_verification_status",  doc.custom_verification)