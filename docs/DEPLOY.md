# Deploying SWIS (PACK AI) to Modal

PACK AI runs as a Modal app named **pack-ai** in workspace **`yuttana858`**, environment **`SWIS`**.

| Endpoint | Address (Modal prints the exact one on deploy) | Who uses it | Protection |
|---|---|---|---|
| `web`: the SWIS chat page and API | `https://yuttana858-swis--pack-ai.modal.run` | You in a browser; later other systems | Your login (single user for now; Azure SSO later). Service callers use the service key |
| `mcp_http`: knowledge tools for Claude clients (optional) | `https://yuttana858-swis--pack-ai-mcp-http.modal.run/mcp` | Claude Code / other Claude clients | The **SWIS AI** proxy token |

These steps need your accounts, so you run them on your computer. No secret ever goes into chat or the repository.

---

## 1. Log in to Modal

```bash
pip install modal
```

```bash
python3 -m modal setup
```

Sign in in the browser and select workspace **yuttana858**. Then make `SWIS` your default environment:

```bash
modal config set-environment SWIS
```

## 2. Give GitHub Actions a deploy token

1. In the Modal dashboard, open workspace **yuttana858** and go to **Settings → API Tokens → New token**. Name it `github-actions-deploy`.
2. In GitHub, open **yuttana858/SW_Pack_AI → Settings → Secrets and variables → Actions → New repository secret**. Create:
   - `MODAL_TOKEN_ID`: the token id
   - `MODAL_TOKEN_SECRET`: the token secret

## 3. Choose your SWIS password and create the secrets

**a. Make a password hash.** From the repository folder on your computer, run:

```bash
python3 -m webapp.passwords
```

Type a password of 12+ characters twice; nothing is shown. The command prints one line starting with `scrypt$…`. That's the **hash**, and only the hash goes to Modal. Copy the whole line.

**b. Create the web secret.** Replace `<your-username>` with the username you'll sign in with, and paste the hash between the **single quotes**. The quotes matter, because the hash contains `$` signs.

Mac or Linux:

```bash
modal secret create --env SWIS pack-ai-web SWPACK_ENV=production SWPACK_AUTH_MODE=password PACKAI_ADMIN_USER=<your-username> PACKAI_ADMIN_PASSWORD_HASH='<paste the scrypt$… line>' SWPACK_SESSION_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))") SWPACK_ASSISTANT_NAME=SWIS
```

Windows PowerShell:

```powershell
$S = python -c "import secrets; print(secrets.token_urlsafe(48))"; modal secret create --env SWIS pack-ai-web SWPACK_ENV=production SWPACK_AUTH_MODE=password PACKAI_ADMIN_USER=<your-username> PACKAI_ADMIN_PASSWORD_HASH='<paste the scrypt$… line>' SWPACK_SESSION_SECRET=$S SWPACK_ASSISTANT_NAME=SWIS
```

Optional extras you can add to the same command:
- `PACKAI_ADMIN_PLANTS=<plant-id>`: which plant data you see first. Leave it out for library data only.
- `PACKAI_SERVICE_KEY=<48+ random characters>`: lets another system call the API with `X-Service-Key` (see `docs/SWIS-INTEGRATION.md`).

**c. Claude API key.** Until you have one, use the placeholder `none`; SWIS then answers in search-only mode.

```bash
modal secret create --env SWIS anthropic ANTHROPIC_API_KEY=none
```

When you have a key, replace it with:

```bash
modal secret create --env SWIS anthropic ANTHROPIC_API_KEY=<your-key> --force
```

**Check:** in the Modal dashboard, environment **SWIS**, you should see **Secrets → pack-ai-web** and **anthropic**.

## 4. Deploy

In GitHub, go to **Actions → deploy-modal → Run workflow**: branch `main`, Modal environment `SWIS` (the default). The workflow:
1. Runs every check.
2. Builds the knowledge release into the `pack-ai-kb` Volume.
3. Runs the retrieval eval.
4. Deploys.

The last step's log prints the addresses. Re-run the workflow after any change you want live. Conversations are kept, because they live on the Volume.

## 5. Sign in

1. Open the `web` address (expected `https://yuttana858-swis--pack-ai.modal.run`).
2. Sign in with your username and password.
3. Ask a question, then a follow-up: SWIS keeps the conversation. Your conversations are listed on the left, and they're still there after a deploy.

**Notes:**
- **Sessions** last 8 hours.
- **Failed sign-ins:** after 5 in 15 minutes, that address is locked out for the rest of the 15 minutes.
- **Forgot the password:** repeat step 3a, re-create `pack-ai-web` with `--force` and the new hash, then re-run the deploy.

## 6. Optional: knowledge tools for Claude clients (MCP)

The `mcp_http` endpoint needs the **SWIS AI** proxy token. Clients send its id (`wk-…`) and secret (`ws-…`) as `Modal-Key` and `Modal-Secret` headers. If the workspace uses role-based access, allow the token for environment **SWIS** (**Settings → Proxy Auth Tokens → SWIS AI**).

---

## Later: Azure SSO

When your Azure SSO system is ready, switch the mode in the `pack-ai-web` secret:
- **The page signs users in with Entra ID itself:** `SWPACK_AUTH_MODE=oidc`, with `webapp/auth.yaml` filled in as described in `docs/IDENTITY-SETUP.md`.
- **Your SSO front end calls PACK AI and passes the user:** `SWPACK_AUTH_MODE=proxy` with the service key (`docs/SWIS-INTEGRATION.md`).

Conversations, the knowledge base and the page stay the same.
