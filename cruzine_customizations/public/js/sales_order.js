frappe.ui.form.on("Sales Order", {
    refresh: (frm) => {
		frm.set_query("shipping_rule", function (frm) {
            return {
                query: "cruzine_customizations.sales_order.get_shipping_rules",
                filters: {
                    city: frm.customer_shipping_city || frm.customer_city,
                },
            };
        });
    },
})