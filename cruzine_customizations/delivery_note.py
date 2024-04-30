import frappe
from frappe.utils import flt
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification

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
                balance = flt(minimum_criteria) - flt(advance_paid)
                owner = frappe.db.get_value("Sales Order", row.against_sales_order, "owner")
                message = "Row: {0} <b>{1}</b> is against Sales Order <b>{2}</b> Payment is Pending <b>{3}</b> . Please followup customer.".format(
                    row.idx, row.item_name, row.against_sales_order, balance)
                frappe.db.rollback()
                notification_doc = {
                    "type": "Alert",
                    "document_type": doc.doctype,
                    "document_name": doc.name,
                    "subject": message,
                    "from_user": doc.modified_by or doc.owner,
                    "email_content": message,
                }
                enqueue_create_notification(owner, notification_doc)
                frappe.sendmail(
                    recipients=frappe.db.get_value("User", doc.owner, "email") or doc.owner,
                    subject=subject,
                    message=message,
                    reference_doctype=doc.doctype,
                    reference_name=doc.name,
                )
                frappe.db.commit()
                frappe.throw("Row: {0} <b>{1}</b> is against Sales Order <b>{2}</b> Payment is Pending <b>{3}</b> . Kindly send E-Mail to Sales Team for Clear Outstanding.".format(
                    row.idx, row.item_name, row.against_sales_order, balance))