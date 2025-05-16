Role-specific passwords:
Executive: EXEC_PASS
Member: MEM_PASS

Dummy account credentials:
username, password: bgil, bgil
username, password: bloi, bloi


Admin credentials:
username: aDmIn
password: siadminni@123



Proposed Functionalities of each Role:
Admin Account:
1. A single, pre-created account within the system. The admin has unrestricted access to all system functionalities and user information.

Executive Accounts: Executives have broader access compared to regular members. They can:
1. Create accounts (but require confirmation from other executives before activation).
2. Confirm new registrations submitted through the registration form to prevent people not part of the organization from creating an account.
3. Update their own profile information and account details.
4. Limited ability to update profile information of other accounts.
5. Read the full information of all accounts as well as their information in the system.
6. Delete accounts if necessary. However, it requires confirmation from other executive accounts.
7. Request deletion of their own profile (requires executive confirmation).

Member Accounts: Members have more limited access. They can:
1. Create an account (but require confirmation from executives before activation).
2. Update only their own profile information and account details.
3. Read information from other members' profiles, but only limited details are visible.
4. Request deletion of their own profile (requires executive confirmation).



Proposed Tables:
1. account_status table (enum(active, pending, inactive), reason, accepted_by(this is user_id))
2. profiles table (dependent siya sa accounts, diri ibutang ang other info about sa user)
3. accounts table (add foreign key of account_status table)
4. creation_request (for handling the account creaction request)
5. deletion_request (for handling deletion request)

