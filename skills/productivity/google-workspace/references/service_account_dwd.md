# Service Account + Domain‑wide Delegation (summary)

When operating inside a Google Workspace (G Suite) domain, Service Accounts
with Domain‑wide Delegation (DWD) allow server-side processes to impersonate
users and call Google APIs on their behalf. This is the recommended pattern
for headless sync agents that must access Gmail, Calendar, Drive, and other
per-user resources without interactive consent flows.

When to use
- You are an Admin of a Google Workspace domain and can configure DWD in the
  Admin Console.
- You need unattended access (cron job every 5 minutes) and the service must
  operate on user mailboxes or calendars.

Key steps
1. Create Service Account in Google Cloud Console → IAM & Admin → Service Accounts
2. Enable "Enable G Suite Domain-wide Delegation" for the SA
3. Create JSON key (store at ~/.hermes/google_service_account.json with chmod 600)
4. Admin Console → Security → API controls → Manage domain-wide delegation → Add client_id and the required scopes
5. In code, create delegated credentials:

   from google.oauth2 import service_account
   from googleapiclient.discovery import build

   SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']
   creds = service_account.Credentials.from_service_account_file(
       '/home/thaieasyvps/.hermes/google_service_account.json', scopes=SCOPES)
   delegated = creds.with_subject('user@yourdomain.com')
   gmail = build('gmail', 'v1', credentials=delegated)

Scopes examples
- Gmail (read/send/modify): https://www.googleapis.com/auth/gmail.modify
- Calendar: https://www.googleapis.com/auth/calendar
- Drive: https://www.googleapis.com/auth/drive
- Sheets: https://www.googleapis.com/auth/spreadsheets
- Docs: https://www.googleapis.com/auth/documents
- People/Contacts: https://www.googleapis.com/auth/contacts.readonly

Security and pitfalls
- DWD grants wide access — configure minimal scopes and audit keys regularly
- Keys are powerful: store them with strict filesystem permissions and never commit them to git
- Admin must explicitly authorize the SA client ID for DWD — inability to impersonate shows as 403 errors

