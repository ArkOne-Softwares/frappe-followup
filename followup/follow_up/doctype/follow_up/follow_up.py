# Copyright (c) 2024, ArkOne Softwares and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, now_datetime


class FollowUp(Document):
    pass


def send_reminder(doc):
    # Get the assigned user and reminder message
    user = doc.user  # Field with the user to notify
    reminder_message = f"Reminder: You have a follow-up scheduled on {doc.date}."

    # Send system notification (real-time)
    frappe.publish_realtime(
        event="msgprint",
        message=reminder_message,
        user=user
    )

    # Mark the document as notified to avoid duplicate reminders
    doc.notified = 1
    doc.save()


def check_due_reminders():
    current_time = now_datetime()

    # Get follow-up records where date has passed and notifications haven't been sent
    follow_up_records = frappe.get_all(
        "Follow Up",
        filters={
            "date": ["<=", current_time],
            "notified": 0  # Ensure notification hasn't been sent yet
        },
        fields=["name", "user", "date"]
    )

    # Loop through records and send reminders
    for record in follow_up_records:
        follow_up_doc = frappe.get_doc("Follow Up", record['name'])
        send_reminder(follow_up_doc)
