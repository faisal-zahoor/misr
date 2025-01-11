import frappe
import json

@frappe.whitelist()
def fetch_time_logs(doc=None):
    doc = json.loads(doc) or doc
    if not doc:
        return
    
    supplier = doc.get("supplier")
    start_date = doc.get("custom_start_date")
    end_date = doc.get("custom_end_date")

    timesheets = frappe.get_all(
        "Timesheet",
        {
            "custom_supplier": supplier,
            "start_date": ["<=", end_date],
            "end_date": [">=", start_date],
            "custom_purchase_invoice": "",
            "status": "Submitted"
        },
        ["name", "total_hours", "total_costing_amount"]
    )

    return timesheets


def on_submit(doc, method=None):
    for row in doc.custom_time_log:
        ts_doc = frappe.get_doc("Timesheet", row.time_sheet)
        ts_doc.db_set("custom_purchase_invoice", doc.name)
        ts_doc.db_set("status", "Payslip")