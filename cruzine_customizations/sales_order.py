import frappe

@frappe.whitelist()
def get_shipping_rules(doctype, txt, searchfield, start, page_len, filters):
	qe = ' and cmt.city_master="'+filters['city']+'"'
	address = frappe.db.sql(""" 
        select 
            sr.name 
        from 
            `tabShipping Rule` as sr,
            `tabCity Master Table` as cmt
        where 
            sr.name = cmt.parent 
            %s
        group by
            sr.name
    """%qe)
	return address