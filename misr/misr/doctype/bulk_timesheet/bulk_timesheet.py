# Copyright (c) 2025, NexTash and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_days, add_to_date, cstr

class BulkTimesheet(Document):
	def validate(self):
		# Get data from the submitted document
		start_date = getdate(self.start_date)
		total_hours = self.hours
		rate_per_hour = self.ratehour
		employee = self.employee
		project = self.project
		customer = self.customer

		# Initialize variables
		remaining_hours = total_hours
		current_date = start_date

		# Create Timesheet
		timesheet = frappe.get_doc({
			"doctype": "Timesheet",
			"employee": employee,
			"customer": customer,
			"parent_project": project,
			"start_date": start_date,
			"time_logs": []  # Initialize an empty time_logs list
		})

		# Allocate hours to timelogs
		while remaining_hours > 0:
			hours_for_day = min(remaining_hours, 9)  # Allocate up to 9 hours per day
			timesheet.append("time_logs", {
				"from_time": cstr(add_to_date(current_date, hours=8)),  # 08:00 AM
				"hours": hours_for_day,
				"billing_rate": rate_per_hour,
				"costing_rate": rate_per_hour,
				"is_billable": 1,  # Assuming billable by default
				"project": project,
				"activity_type": "Execution"  # Change if needed
			})
			remaining_hours -= hours_for_day
			current_date = add_days(current_date, 1)  # Move to the next day

		# Save and Submit Timesheet
		timesheet.save()
		frappe.msgprint(f"Timesheet {timesheet.name} created successfully.")
