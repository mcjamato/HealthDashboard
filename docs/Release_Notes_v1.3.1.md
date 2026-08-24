# Version 1.3.1 - Client Role Navigation

Version 1.3.1 separates the client experience from the administrator
experience.

Administrators retain access to the complete application.

Client users see only:

## Customer Dashboards
- Exercise Dashboard
- Health Dashboard
- Mental Wellness Dashboard
- Nutrition Dashboard

## Customer Data
- Exercise Entry
- Health Entry
- Mental Wellness Entry
- Nutrition Entry
- Blood Work
- Change Password

A client login is linked to one `client_id` in the `users` table. The client
does not receive a customer selector and cannot switch to another client.

The application also performs an authorization check after navigation selection,
so hiding a menu item is not the only access control.
