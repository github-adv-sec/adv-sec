def attendees_to_markdown(attendee_state):
    headers = ["Handle", "Invite Sent?", "Org Name", "Fork Errors"]
    rows = []
    for attendee in attendee_state:
        row = [
            attendee["handle"],
            "✅" if attendee["invited"] else "❌",
            f"[{attendee['org_name']}](https://github.com/{attendee['org_name']})"
            if attendee["org_name"] is not None
            else "",
            ", ".join(attendee["fork_errors"]) if attendee["fork_errors"] else "None",
        ]
        rows.append(row)
    table = f"| {' | '.join(headers)} |\n| {' | '.join(['---' for _ in headers])} |\n"
    for row in rows:
        table += f"| {' | '.join(row)} |\n"
    return table


complete = f"""
## Provisioning complete 🎉\n\n
REMINDER: These bootcamp environments are set to auto delete.  If they need to stick around, add the `bootcamp::hold` label.\n\n
"""

errored = f"""
## Provisioning errored 👎 \n\n
Additional information on this error is available in the Actions logs. 
"""

teardown_complete = f"""
## Teardown complete 🗑\n\n
I've successfully deleted the following orgs.  REMINDER: It takes 90 days for these org names to be available again.\n\n
"""
