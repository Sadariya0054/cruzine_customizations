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
                frappe.db.rollback()
                
                balance = flt(minimum_criteria) - flt(advance_paid)
                owner = frappe.db.get_value("Sales Order", row.against_sales_order, "owner")
                
                message = "Your Order <b>{0}</b> has been Packed. Kindly Clear the Outstanding Payment {1}.".format(
                row.against_sales_order, balance)
                notification_doc = {
                    "type": "Alert",
                    "document_type": doc.doctype,
                    "document_name": doc.name,
                    "subject": message,
                    "from_user": doc.modified_by or doc.owner,
                    "email_content": message,
                }
                enqueue_create_notification(owner, notification_doc)
                subject = "Outstanding | {0} Sales Order | {1} Customer".format(row.against_sales_order, doc.customer)
                email_message = """
Dear <b>{0}</b>
<br><br>
Your Order has been Packed. Please clear your outstanding <b>&#8377; {1}</b> of Sales Order.
<br><br>
Do share the Payment Receipt or Screenshot on previous Mail Conversation of Sales Order once the Payment is done.
<br><br>
Regards,
<br>
Cruzine Team
""".format(owner, balance)
                frappe.sendmail(
                    recipients=owner,
                    subject=subject,
                    message=email_message,
                    reference_doctype=doc.doctype,
                    reference_name=doc.name,
                    cc=["supplychainsr.cruzine@gmail.com", "dhrumil@cruzine.in"]
                )
                frappe.db.commit()
                frappe.throw("Row: {0} <b>{1}</b> is against Sales Order <b>{2}</b> Payment is Pending <b>{3}</b> . Kindly send E-Mail to Sales Team for Clear Outstanding.".format(
                    row.idx, row.item_name, row.against_sales_order, balance))


def before_insert(doc, method): 
    customer = frappe.get_doc("Customer", doc.customer)
    for row in customer.custom_performance_indicator:
        doc.append("custom_performance_indicator",{"performance_indicator": row.performance_indicator})