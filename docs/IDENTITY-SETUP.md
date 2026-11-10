# Connecting your identity provider (sign-in)

> **Current choice: GitHub sign-in.** Every active member of the company GitHub organization signs in as a packaging engineer; GitHub teams grant steward/plant roles. Setup steps are in `docs/DEPLOY.md`. The OIDC instructions below remain for a later move to Entra ID, Okta or Google Workspace.

SW Pack AI signs engineers in with **OpenID Connect**, which works with Microsoft Entra ID (Azure AD),
Okta, Google Workspace, Auth0 and Keycloak. The page uses the Authorization Code flow with PKCE (no
client secret in the browser). The API verifies every token's signature, issuer, audience and expiry.

## 1. Register the application with your provider

| Setting | Value |
|---|---|
| Application type | Single-page application (SPA), public client |
| Redirect URI | `https://<your-app-host>/` |
| Logout redirect URI | `https://<your-app-host>/` |
| Scopes | `openid profile email` (plus an API scope if your provider issues access tokens per API) |
| Token claims | Include the user's **groups** in the token (Entra: "groups claim"; Okta: groups claim filter) |

## 2. Create groups for roles and plants

| Group (example) | Maps to |
|---|---|
| SWPack-Engineers | role `engineer`: ask questions, send corrections |
| SWPack-Stewards | role `steward`: decide on any correction |
| SWPack-PlantAdmin-Dallas | role `plant-admin`: decide on Dallas corrections |
| SWPack-Plant-Dallas | plant `dallas`: sees Dallas data first, can select Dallas |

Everyone who signs in is at least a `viewer` (read-only).

## 3. Fill in `webapp/auth.yaml`

Copy `webapp/auth.example.yaml` to `webapp/auth.yaml` and fill in:
- the issuer, audience and client id
- the claim names
- the group → role mapping
- the group → plant mapping

Plant ids must match the `plant_id` values in `data/plants/<plant>/plant.yaml`.

## 4. Run in production mode

Set:
- `SWPACK_ENV=production`
- `SWPACK_AUTH_MODE=oidc`
- `SWPACK_AUTH_CONFIG=<path to auth.yaml>`

On Modal these go in the `swpack-web` secret. Developer sign-in is refused when `SWPACK_ENV=production`.

## What we need from you

1. Which provider you use.
2. Who can register an app in it.
3. The groups (or the people) for engineers, stewards, plant admins and each plant.
