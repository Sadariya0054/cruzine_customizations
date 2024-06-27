frappe.ui.form.on("Delivery Note", {
    refresh: (frm) => {
		if (frm.doc.docstatus == 0 && !frm.doc.__islocal) {
            if (frm.doc.__onload && frm.doc.__onload.has_unpacked_items) {
                
                this.frm.add_custom_button(
                    __("Create Bulk Packing Slip"),
                    function () {
                        // frappe.model.open_mapped_doc({
                        //     method: "cruzine_customizations.delivery_note.bulk_packing_slip",
                        //     frm: me.frm,
                        // });
                        let data = []
                        cur_frm.doc.items.forEach(element => {
                            data.push({"item": element.item_code, qty: element.actual_qty - element.packed_qty })
                        });
                        let d = new frappe.ui.Dialog({
                            title: 'Bulk Packing Slip',
                            fields: [
                                {
                                    label: 'Number of Packing Slip',
                                    fieldname: 'number_of_packing_slip',
                                    fieldtype: 'Int'
                                },
                                {
                                    label: 'Incriment of Package',
                                    fieldname: 'package_incriment',
                                    fieldtype: 'Int'
                                },
                                {
                                    fieldname: "packing_item_table",
                                    fieldtype: "Table",
                                    label: __("Packing Item"),
                                    in_place_edit: true,
                                    data: data,
                                    cannot_add_rows: false,
                                    get_data: () => {
                                        
                                        return data;
                                    },
                                    fields: [
                                        {
                                            fieldtype: "Link",
                                            options: "Item",
                                            fieldname: "item",
                                            label: __("Item"),
                                            in_list_view: 1,
                                        },
                                        {
                                            fieldtype: "Int",
                                            fieldname: "qty",
                                            label: __("Qty"),
                                            in_list_view: 1,
                                        }
                                    ],
                                }
                            ],
                            size: 'small', // small, large, extra-large 
                            primary_action_label: 'Submit',
                            primary_action(values) {
                                console.log(values);
                                values['doc']= cur_frm.doc.name
                                // d.hide();
                                frappe.call({
                                    method: "cruzine_customizations.delivery_note.bulk_packing_slip",
                                    args: values,
                                    freeze: true,
                                    callback: function (r) {
                                        
                                        d.hide();
                                    }
                                });
                            }
                        });
                        
                        d.show();
                    },
                    __("Create")
                );
            }
        }
    },
})