# Becoming Maximus - Ghost Blog on Render

This project contains the configuration and scripts to deploy and manage a Ghost blog named **"Becoming Maximus"** on Render.com.

## Deployment Instructions

1. **GitHub Repository**: Push these files to a new GitHub repository.
2. **Render Blueprint**: 
   - Log in to [Render.com](https://render.com).
   - Click **New +** and select **Blueprint**.
   - Connect your GitHub repository.
   - Render will detect the `render.yaml` file and set up the Web Service and Persistent Disk.
3. **Environment Variables**:
   - During setup (or after in the Render dashboard), set the `url` environment variable to your actual Render URL (e.g., `https://becoming-maximus.onrender.com`).
4. **Ghost Setup**:
   - Once deployed, visit `https://your-site.onrender.com/ghost` to create your admin account.
   - Go to **Settings > Integrations** and click **+ Add custom integration**.
   - Name it "OpenClaw Publisher".
   - Copy the **Admin API Key** and **API URL**.

## Configuration

Store your credentials in `~/.ghost/credentials.json`:

```json
{
  "admin_api_url": "https://your-site.onrender.com",
  "admin_api_key": "ID:SECRET"
}
```

## Publishing

Use the provided Python script to publish Markdown files:

```bash
./scripts/ghost-publish.py path/to/post.md --status published
```

The script handles:
- Frontmatter extraction (title, excerpt, tags).
- Markdown to HTML conversion.
- JWT authentication for the Ghost Admin API.
