frappe.ui.form.on("Purchase Invoice", {
	refresh: function (frm, dt, dn) {
        if(frm.doc.docstatus == 0){
            frm.add_custom_button("Fetch Timelogs", () => {
                frappe.call({
                    method: "misr.events.purchase_invoice.fetch_time_logs",
                    args: {
                        doc: frm.doc
                    },
                    callback(r){
                        if(r.message) {
                            let hours = 0
                            let amount = 0
                            frm.doc.custom_time_log = []
                            for (const row of r.message) {
                                const new_row = frm.add_child("custom_time_log");

                                const cdt = new_row.doctype
                                const cdn = new_row.name
                                
                                frappe.model.set_value(cdt, cdn, "time_sheet", row.name)
                                frappe.model.set_value(cdt, cdn, "working_hours", row.total_hours)
                                hours += row.total_hours
                                amount += row.total_costing_amount
                            }

                            frappe.model.set_value(dt, dn, "custom_total_hours", hours)
                            frappe.model.set_value(dt, dn, "custom_total_amount", amount)

                            frm.refresh_field("custom_time_log")
                        }
                    }
                })
            })
        }
    }
})