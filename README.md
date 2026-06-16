# ŠkolaOnline Služba

Fetches your `služba` (duty) from ŠkolaOnline and sends it to a Discord webhook every Monday morning.

## How it works

A GitHub Actions workflow runs every Monday at 05:30 UTC. It logs into ŠkolaOnline, scrapes the current week's duty from the calendar page, and posts it to a Discord channel via a webhook.

## Setup

### 1. Fork / clone this repository

### 2. Set up GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add these repository secrets:

| Secret | Description |
|---|---|
| `EMAIL` | Your ŠkolaOnline login email |
| `PASS` | Your ŠkolaOnline login password |
| `DC_WEBHOOK_URL` | Discord webhook URL (see below) |

### 3. Create a Discord webhook

1. Open your Discord server's settings
2. Go to **Integrations → Webhooks**
3. Create a new webhook, choose the channel, and copy the URL
4. Add it as the `DC_WEBHOOK_URL` secret

### 4. Run it manually (optional)

Go to **Actions → Služba → Run workflow** to trigger it on-demand without waiting for the scheduled time.

## Schedule

The workflow runs automatically every Monday at `05:30 UTC` (`cron: '30 5 * * 1'`). Edit `.github/workflows/sluzba.yml` to change the schedule.
