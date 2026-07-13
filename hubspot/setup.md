# HubSpot portal setup

This repo's skills assume a single HubSpot portal connected via a private
app token stored outside version control (see your team's secrets manager).

## Finding your portal ID

Your portal ID appears in the HubSpot URL after you log in — for example
`app.hubspot.com/contacts/21445566/objects/0-3/views/all/list` — and in
Settings → Account & Billing → Account Information.

Set it as an environment variable before running any skill in this repo:

```
export HUBSPOT_PORTAL_ID=<your-portal-id>
```

## Scopes the skills in this repo need

- `crm.objects.deals.read` — read deal records and stage history
- `crm.objects.contacts.read` — read contact records associated with deals
- `crm.pipelines.read` — read pipeline and stage definitions

## Local testing

Skills in `skills/` read the portal ID from the environment, not from a
hardcoded value, so the same skill code works against any portal — swap the
environment variable and it points at a different HubSpot account.
