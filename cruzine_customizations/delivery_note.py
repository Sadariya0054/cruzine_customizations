import frappe
from frappe.utils import flt

def on_submit(doc, method):
    for row in doc.items:
        if row.against_sales_order:
            payment_schedule = frappe.get_all("Payment Schedule",{"parent": row.against_sales_order }, ["payment_term"])
            final_percentage = 0
            for row2 in payment_schedule:
                term_type = frappe.db.get_value("Payment Term", row2.payment_term, "term_type")
                percentage = 0
                if term_type == "Before Dispatch":
                    percentage = frappe.db.get_value("Payment Term", row2.payment_term, "invoice_portion")
                if term_type == "On Dispatch":
                    percentage = frappe.db.get_value("Payment Term", row2.payment_term, "invoice_portion")
                final_percentage = final_percentage + flt(percentage)        
            rounded_total = frappe.db.get_value("Sales Order", row.against_sales_order, "rounded_total")
            advance_paid = frappe.db.get_value("Sales Order", row.against_sales_order, "advance_paid")
            minimum_criteria = flt(rounded_total) * flt(final_percentage) / 100
            if minimum_criteria > flt(advance_paid):
                frappe.throw("Row:{0} has item against Sales Order {1} which dont have enough {2} advance payment ".format(
                    row.idx, row.against_sales_order, minimum_criteria))