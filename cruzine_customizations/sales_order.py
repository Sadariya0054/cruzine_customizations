import frappe

@frappe.whitelist()
def get_shipping_rules(doctype, txt, searchfield, start, page_len, filters):
	qe = ' and cmt.city_master="'+filters.get('city')+ '"  and imt.incoterm="'+filters.get('incoterm')+'"'
	address = frappe.db.sql(""" 
        select 
            sr.name 
        from 
            `tabShipping Rule` as sr,
            `tabCity Master Table` as cmt,
			`tabIncoterm Master Table` as imt
        where 
            sr.name = cmt.parent 
			and sr.name = imt.parent   
            %s
        group by
            sr.name
    """%(qe))
	return address