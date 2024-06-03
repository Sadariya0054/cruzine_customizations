import frappe

def on_submit(doc, method):
    dn = doc.shipment_delivery_note[0].delivery_note
    so = frappe.db.get_value("Delivery Note Item", {"parent": dn}, "against_sales_order")
    if so:
        dnis = frappe.get_all("Delivery Note Item",{"against_sales_order": so}, "parent")
        delivery_notes = []
        for row in dnis:
            if row['parent'] not in delivery_notes:
                delivery_notes.append(row['parent'])
        charges = 0
        for dn in delivery_notes:
            shipmentsdn = frappe.get_all("Shipment Delivery Note",{"delivery_note":dn}, "parent")
            shipments = []
            for row in shipmentsdn:
                if row['parent'] not in shipments:
                    shipments.append(row['parent'])
            for shipment in shipments:
                custom_other_charges = frappe.db.get_value("Shipment", shipment,"custom_other_charges")
                if custom_other_charges:
                    charges += frappe.utils.flt(custom_other_charges)
                
                shipment_amount = frappe.db.get_value("Shipment", shipment,"shipment_amount")
                if shipment_amount:
                    charges += frappe.utils.flt(shipment_amount)
        frappe.db.set_value("Sales Order", so, "custom_shipping_charges", charges)
        so_doc = frappe.get_doc("Sales Order", so)
        gros_profit = 0
        for row in so_doc.items:
            gros_profit += row.gross_profit
        gros_profit -= charges
        profit_per = gros_profit * 100 / so_doc.total

        custom_net_profit = str(gros_profit) + " (" + str(profit_per) +" %)"
        frappe.db.set_value("Sales Order", so, "custom_net_profit", custom_net_profit)
        
        