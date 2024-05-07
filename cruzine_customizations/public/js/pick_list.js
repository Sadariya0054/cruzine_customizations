frappe.ui.form.on("Pick List", {
    refresh: (frm) => {
		frm.trigger("add_get_items_button");
    },
    add_get_items_button: (frm) => {
		setTimeout(() => {
            frm.remove_custom_button('Get Items');
        }, 10);
		let purpose = frm.doc.purpose;
		if (purpose != "Delivery" || frm.doc.docstatus !== 0) return;
		let get_query_filters = {
			docstatus: 1,
			per_delivered: ["<", 100],
			status: ["!=", ""],
			customer: frm.doc.customer,
		};
		frm.get_items_btn = frm.add_custom_button(__("Get Validated Items"), () => {
			erpnext.utils.map_current_doc({
				method: "erpnext.selling.doctype.sales_order.sales_order.create_pick_list",
				source_doctype: "Sales Order",
				target: frm,
				setters: {
					company: frm.doc.company,
					customer: frm.doc.customer,
				},
				date_field: "transaction_date",
				get_query_filters: get_query_filters,
				get_query_method: "cruzine_customizations.server_scripts.pick_list.get_query_method"
			});
		});
	},
})