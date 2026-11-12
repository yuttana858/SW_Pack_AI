# Deploying PACK AI to Modal (workspace "SWIS") with GitHub sign-in

App address once deployed: **https://swis--pack-ai.modal.run**

These steps need your accounts, so you run them. No secret ever needs to be pasted into chat or
committed to the repository.

**Two GitHub logins:**
- **Logging into Modal** with GitHub is how *you* administer the workspace.
- **"Sign in with GitHub" on PACK AI** is how *engineers* use the app.

Both use the same GitHub identities, so engineers need nothing new.

---

## 1. Create the Modal workspace and log in (your computer)

```bash
pip install modal
```

```bash
python3 -m modal setup
```

This opens your browser. Sign in with GitHub, and create (or pick) the workspace **swis**. The token is saved on your computer.

## 2. Give GitHub Actions a deploy token

1. In the Modal dashboard, open the **swis** workspace and go to **Settings → API Tokens → New token**. Name it `github-actions-deploy`.
2. In GitHub, open the repository and go to **Settings → Secrets and variables → Actions → New repository secret**. Add two secrets:
   - `MODAL_TOKEN_ID`: the token id
   - `MODAL_TOKEN_SECRET`: the token secret
3. Optional: under **Settings → Environments**, create `production` and require a reviewer before deploys.

## 3. Register the "Sign in with GitHub" app

In GitHub, go to your **organization → Settings → Developer settings → OAuth Apps → New OAuth App**:

| Field | Value |
|---|---|
| Application name | PACK AI |
| Homepage URL | `https://swis--pack-ai.modal.run` |
| Authorization callback URL | `https://swis--pack-ai.modal.run/auth/github/callback` |

The web function is labelled `pack-ai`, so its address is `https://<workspace>--pack-ai.modal.run`. Modal prints the real URL on the first deploy; if it differs (for example, a different workspace name), update both fields here and `SWPACK_PUBLIC_URL` in step 4.

After creating the app, copy the **Client ID**, then **Generate a new client secret** and copy it.

## 4. Create the Modal secrets (your computer)

First the web app secret. Fill in your GitHub organization name and the two values from step 3:

```bash
modal secret create pack-ai-web SWPACK_ENV=production SWPACK_AUTH_MODE=github SWPACK_GITHUB_ORG=<your-github-org> GITHUB_CLIENT_ID=<client-id> GITHUB_CLIENT_SECRET=<client-secret> SWPACK_SESSION_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))") SWPACK_PUBLIC_URL=https://swis--pack-ai.modal.run
```

Then the Claude API key. Until you have a key, use the placeholder `none`, which keeps the app in search-only mode:

```bash
modal secret create anthropic ANTHROPIC_API_KEY=none
```

When you have a key, replace it with:

```bash
modal secret create anthropic ANTHROPIC_API_KEY=<your-key> --force
```

## 5. Deploy

In GitHub, go to **Actions → deploy-modal → Run workflow**. The workflow:
1. Runs every check.
2. Builds the knowledge release into the `pack-ai-kb` Volume.
3. Runs the retrieval eval.
4. Deploys:
   - the web app (`web`)
   - the MCP endpoint (`mcp_http`)
   - the `ask`, `build_index` and `retrieval_eval` functions

Re-run it after any change you want live. Engineers' conversations are kept, because they live on the Volume.

## 6. Sign in

Open `https://swis--pack-ai.modal.run` and choose **Sign in with GitHub**.
- **Who can sign in:** every active member of your organization gets the **engineer** role.
- **Who is refused:** non-members, and invitations not yet accepted.

## 7. Later: roles and plants through GitHub teams

Create teams in your GitHub organization and map them in `webapp/auth.yaml`:

| Team (example) | Effect |
|---|---|
| `swpack-stewards` | role steward: can decide on any correction (already mapped) |
| `plant-dallas` | plant `dallas` (add under `team_plants`) |

Commit the change and re-run the deploy workflow. Team changes take effect at an engineer's next sign-in; sessions last 8 hours.

## Notes

- **MCP endpoint (`mcp_http`):** protected by Modal proxy auth. To let a Claude client use it, create a proxy auth token in the Modal dashboard.
- **Single container:** the web app runs as one container because conversations are stored in SQLite on the Volume. Postgres (phase C4) lifts this.
- **Rotating the GitHub client secret:** generate a new one in the OAuth App, re-create `pack-ai-web` with `--force`, and re-run the deploy.
