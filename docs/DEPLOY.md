# Deploying PACK AI to Modal (the service behind SWIS)

PACK AI runs as a Modal app named **pack-ai**. Its main endpoint, `api`, serves SWIS. Users are signed
in by SWIS through Azure SSO, so PACK AI needs no sign-in of its own. These steps need your accounts,
so you run them. No secret ever goes into chat or the repository.

**Where it runs:** Modal workspace **`yuttana858`**, environment **`SWIS`**. Callers use the proxy token named **SWIS AI** from that workspace. The expected address is `https://yuttana858-swis--pack-ai.modal.run`; Modal prints the exact address when you deploy, so use that one if it differs.

---

## 1. Log in to Modal on your computer

```bash
pip install modal
```

```bash
python3 -m modal setup
```

This opens your browser. Sign in, and select workspace **yuttana858**. Then make `SWIS` the default environment for your commands:

```bash
modal config set-environment SWIS
```

## 2. Give GitHub Actions a deploy token

1. In the Modal dashboard, open workspace **yuttana858** and go to **Settings → API Tokens → New token**. Name it `github-actions-deploy`. Copy the token id and secret.
2. In GitHub, open **yuttana858/SW_Pack_AI → Settings → Secrets and variables → Actions → New repository secret**. Create:
   - `MODAL_TOKEN_ID`: the token id
   - `MODAL_TOKEN_SECRET`: the token secret

## 3. Create the two Modal secrets (your computer)

**PACK AI service settings.** This generates the service key on your machine and prints it once. Store it in SWIS's server-side secrets, because SWIS sends it as `X-Service-Key`.

Mac or Linux:

```bash
KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))"); echo "PACKAI_SERVICE_KEY for SWIS: $KEY"; modal secret create --env SWIS pack-ai-api SWPACK_ENV=production SWPACK_AUTH_MODE=proxy PACKAI_SERVICE_KEY=$KEY SWPACK_ASSISTANT_NAME=SWIS
```

Windows PowerShell:

```powershell
$KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"; Write-Output "PACKAI_SERVICE_KEY for SWIS: $KEY"; modal secret create --env SWIS pack-ai-api SWPACK_ENV=production SWPACK_AUTH_MODE=proxy PACKAI_SERVICE_KEY=$KEY SWPACK_ASSISTANT_NAME=SWIS
```

**Claude API key.** Until you have one, use the placeholder `none`. The service then answers in search-only mode.

```bash
modal secret create --env SWIS anthropic ANTHROPIC_API_KEY=none
```

When you have a key, replace it with:

```bash
modal secret create --env SWIS anthropic ANTHROPIC_API_KEY=<your-key> --force
```

**Check:** in the Modal dashboard, environment **SWIS**, you should see **Secrets → pack-ai-api** and **anthropic**.

## 4. Deploy

In GitHub, go to **Actions → deploy-modal → Run workflow**: branch `main`, Modal environment `SWIS` (the default). The workflow:
1. Runs every check.
2. Builds the knowledge release into the `pack-ai-kb` Volume.
3. Runs the retrieval eval.
4. Deploys the app.

At the end of the deploy step, the log prints the endpoint address:
- **SWIS API:** expected `https://yuttana858-swis--pack-ai.modal.run`
- **MCP endpoint (optional, for Claude clients):** expected `https://yuttana858-swis--pack-ai-mcp-http.modal.run/mcp`

Re-run the workflow after any change you want live. Conversations are kept, because they live on the Volume.

## 5. The "SWIS AI" proxy token

Use the existing proxy token **SWIS AI** from workspace yuttana858. Whatever calls PACK AI sends its id (`wk-…`) and secret (`ws-…`) as the `Modal-Key` and `Modal-Secret` headers.

If the workspace uses role-based access, the token must be allowed for environment **SWIS**: in the dashboard, open **Settings → Proxy Auth Tokens → SWIS AI**, or run `modal workspace proxy-tokens allow`.

## 6. Test from a terminal

Replace the values in angle brackets (`<…>`):

```bash
curl -sS https://yuttana858-swis--pack-ai.modal.run/api/me -H "Modal-Key: <wk-…>" -H "Modal-Secret: <ws-…>" -H "X-Service-Key: <service key>" -H "X-User-Id: test-user" -H "X-User-Roles: engineer"
```

The expected reply contains `"name": "test-user"` and the roles. Then follow the ask examples in `docs/SWIS-INTEGRATION.md`.

---

## Optional: the PACK AI page later

`webapp/static/` is a complete chat page: citations, sources, feedback and a review queue. It can become the "fully functional harness". It would sign users in with Azure SSO directly, and `webapp/auth.py` already verifies Entra ID tokens (see `docs/IDENTITY-SETUP.md`). Or it can sit inside SWIS's front end. The GitHub sign-in code (`webapp/github_auth.py`) stays in the repository but is not used.
