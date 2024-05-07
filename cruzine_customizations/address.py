import frappe

def before_insert(doc, method):
    if not doc.customer_city:
        for row in doc.links:
            if row.link_doctype == "Customer" and row.link_name:
                customer_city = frappe.db.get_value("Customer", row.link_name, "customer_city")
                if customer_city:
                     doc.customer_city = customer_city
            