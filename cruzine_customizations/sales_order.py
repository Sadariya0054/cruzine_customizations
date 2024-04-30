import frappe

@frappe.whitelist()
def get_shipping_rules(doctype, txt, searchfield, start, page_len, filters):
	qe = ' and cmt.city_master="'+filters['city']+'"'
	table = ""
	if filters.get('incoterm',''):
		qe = ' and sr.name = imt.parent and imt.incoterm="'+filters['incoterm']+'"'
		table = '''`tabCity Master Table` as cmt,
			`tabIncoterm Master Table` as imt'''
	else:
		table = '''`tabCity Master Table` as cmt'''
	address = frappe.db.sql(""" 
        select 
            sr.name 
        from 
            `tabShipping Rule` as sr,
            %s
        where 
            sr.name = cmt.parent 
            
            %s
        group by
            sr.name
    """%(table,qe))
	return address