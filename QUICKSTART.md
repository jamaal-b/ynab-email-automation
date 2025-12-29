# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Get Your YNAB Token
1. Go to https://app.ynab.com/settings/developer
2. Click "New Token"
3. Give it a name (e.g., "Email Automation")
4. Copy the token

### Step 2: Setup Email (Gmail Example)
1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Create an App Password for "Mail"
4. Copy the 16-character password

### Step 3: Configure the Application

#### Option A: Use Setup Script (Easiest)
```bash
./setup.sh
```
Follow the prompts to enter your credentials.

#### Option B: Manual Configuration
1. Copy the example config:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in:
   - `YNAB_API_TOKEN` - Your YNAB token from Step 1
   - `SMTP_USERNAME` - Your email address
   - `SMTP_PASSWORD` - Your App Password from Step 2
   - `EMAIL_FROM` - Your email address
   - `EMAIL_TO` - Where to send reports (can be same)
   - `TIMEZONE` - Your timezone (e.g., America/New_York)

### Step 4: Test It!
```bash
# Test all three email types
python main.py test
```

Check your email - you should receive 3 test emails!

### Step 5: Deploy on Unraid

#### If you have Docker Compose:
```bash
docker-compose up -d
```

#### Using Unraid Docker UI:
1. Copy project to `/mnt/user/appdata/ynab-emailer/`
2. In Unraid Docker tab, click "Add Container"
3. Configure:
   - Name: `ynab-emailer`
   - Repository: Build from `/mnt/user/appdata/ynab-emailer/Dockerfile`
   - Add environment variables from your `.env` file
4. Start container

### Step 6: Verify It's Running
```bash
# Check logs
docker-compose logs -f

# Or if using Docker directly
docker logs -f ynab-emailer
```

You should see:
```
YNAB Email Automation Started
Daily alerts:   Every day at 7:30 AM
Weekly recap:   Mondays at 8:00 AM
Monthly recap:  1st of month at 8:00 AM
Scheduler running...
```

## 📧 What You'll Receive

### Daily (7:30 AM)
- Any uncategorized transactions
- Categories close to their limit (80%+)
- Overspent categories

### Weekly (Monday 8:00 AM)
- Last week's spending by category
- Upcoming scheduled transactions
- Budget status

### Monthly (1st at 8:00 AM)
- Previous month's complete analysis
- Top spending categories
- Recurring transactions
- Monthly statistics

## 🔧 Customization

### Change Alert Threshold
In `.env`:
```env
CATEGORY_SPENT_THRESHOLD=90  # Alert at 90% instead of 80%
```

### Change Schedule Times
Edit `main.py` lines with `schedule.every()`:
```python
schedule.every().day.at("06:00").do(self.send_daily_alert)  # 6 AM
schedule.every().friday.at("17:00").do(self.send_weekly_recap)  # Friday 5 PM
```

### Customize Email Design
Edit HTML templates in `templates/` folder:
- `daily_alert.html`
- `weekly_recap.html`
- `monthly_recap.html`

## ❓ Troubleshooting

### Emails Not Arriving
1. Check spam/junk folder
2. Verify email credentials in `.env`
3. For Gmail, confirm you're using an App Password
4. Check logs: `docker-compose logs -f`

### YNAB Connection Issues
1. Verify token is correct
2. Check you have access to the budget
3. Token may need regenerating at https://app.ynab.com/settings/developer

### Wrong Timezone
1. Update `TIMEZONE` in `.env`
2. Update `TZ` in `docker-compose.yml`
3. Restart: `docker-compose restart`
4. Find your timezone: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## 💡 Tips

- **Test before deploying**: Always run `python main.py test` first
- **Check logs regularly**: Especially the first few days
- **Secure your .env**: Contains sensitive credentials
- **Keep it updated**: Occasionally pull latest updates

## 📞 Need Help?

1. Check the full README.md
2. Review error messages in logs
3. Verify all prerequisites are met
4. Test individual components (YNAB API, email sending)

## Next Steps

Once everything is working:
1. Set it and forget it! 🎉
2. Check your emails at scheduled times
3. Adjust thresholds and schedules to your preference
4. Customize templates to match your style

Enjoy your automated YNAB budget reports! 📊
