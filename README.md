# YNAB Email Automation

Automated email reports for your YNAB budget with daily alerts, weekly recaps, and monthly summaries.

## Features

### 📧 Daily Alert (7:30 AM)
- Uncategorized transactions
- Categories near spending limit (80%+)
- Overspent categories

### 📊 Weekly Recap (Mondays at 8:00 AM)
- Last 7 days spending breakdown by category
- Upcoming scheduled transactions (next 2 weeks)
- Over/under funded categories

### 📈 Monthly Report (1st of month at 8:00 AM)
- Previous month's complete spending analysis
- Top spending categories
- Recurring transactions for current month
- Monthly statistics (avg per day, largest transaction, etc.)

## Prerequisites

1. **YNAB Personal Access Token**
   - Go to https://app.ynab.com/settings/developer
   - Click "New Token"
   - Give it a name and copy the token

2. **Email Account for Sending**
   - Gmail (recommended): Use an App Password
     - Enable 2FA on your Google account
     - Generate App Password: https://myaccount.google.com/apppasswords
   - Or use any SMTP server

## Setup Instructions

### Option 1: Docker (Recommended for Unraid)

1. **Clone or download this repository to your Unraid server**

2. **Create your `.env` file**
   ```bash
   cp .env.example .env
   nano .env  # or use your preferred editor
   ```

3. **Fill in your configuration in `.env`:**
   ```env
   # YNAB API Configuration
   YNAB_API_TOKEN=your_token_here
   YNAB_BUDGET_ID=default
   
   # Email Configuration (Gmail example)
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password_here
   EMAIL_FROM=your_email@gmail.com
   EMAIL_TO=your_email@gmail.com
   
   # Alert Thresholds
   CATEGORY_SPENT_THRESHOLD=80
   
   # Timezone
   TIMEZONE=America/New_York
   ```

4. **Update timezone in `docker-compose.yml`**
   ```yaml
   environment:
     - TZ=America/New_York  # Change to your timezone
   ```

5. **Build and run the container**
   ```bash
   docker-compose up -d
   ```

6. **View logs**
   ```bash
   docker-compose logs -f
   ```

### Option 2: Direct Python Installation

1. **Install Python 3.8+**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create and configure `.env`** (same as Docker step 2-3)

4. **Run the application**
   ```bash
   # Start scheduler (runs continuously)
   python main.py
   
   # Or test individual reports
   python main.py daily    # Test daily alert
   python main.py weekly   # Test weekly recap
   python main.py monthly  # Test monthly report
   python main.py test     # Test all three reports
   ```

## Unraid Setup

### Method 1: Using Community Applications (if available)

1. Install "Docker Compose Manager" from Community Applications
2. Copy your project folder to `/mnt/user/appdata/ynab-emailer/`
3. Configure `.env` file
4. Start the container using Docker Compose Manager

### Method 2: Manual Docker Setup

1. **Copy files to Unraid:**
   ```bash
   # Copy to appdata folder
   cp -r ynab-emailer /mnt/user/appdata/
   cd /mnt/user/appdata/ynab-emailer
   ```

2. **Configure `.env` file** (see above)

3. **Build and run:**
   ```bash
   docker-compose up -d
   ```

4. **Add to Unraid autostart** (optional):
   - Go to Docker tab in Unraid
   - Or add to `/boot/config/go` script:
   ```bash
   cd /mnt/user/appdata/ynab-emailer && docker-compose up -d
   ```

## Configuration Options

### Email Schedule
Edit `main.py` to change schedule times:
```python
schedule.every().day.at("07:30").do(self.send_daily_alert)
schedule.every().monday.at("08:00").do(self.send_weekly_recap)
```

### Alert Threshold
Change the percentage in `.env`:
```env
CATEGORY_SPENT_THRESHOLD=80  # Alert when 80% spent
```

### Timezone
Set your timezone in `.env` and `docker-compose.yml`:
- Find your timezone: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- Common examples: `America/New_York`, `America/Los_Angeles`, `America/Chicago`, `Europe/London`

## Testing

Before setting up the scheduler, test that everything works:

```bash
# Test all reports at once
python main.py test

# Or test individually
python main.py daily
python main.py weekly
python main.py monthly
```

This will send test emails immediately so you can verify:
- YNAB API connection works
- Email configuration is correct
- Email templates display properly

## Troubleshooting

### YNAB API Errors
- Verify your Personal Access Token is correct
- Check that you have access to the budget
- Token may need to be regenerated if expired

### Email Not Sending
- **Gmail**: Make sure you're using an App Password, not your regular password
- Check SMTP settings match your provider
- Verify firewall isn't blocking port 587
- Check spam/junk folder

### Scheduler Not Running
- Check Docker container logs: `docker-compose logs -f`
- Verify timezone is set correctly
- Times are in 24-hour format (e.g., "08:00" not "8:00 AM")

### Permission Issues (Unraid)
```bash
# Fix permissions on the directory
chmod -R 755 /mnt/user/appdata/ynab-emailer
chown -R nobody:users /mnt/user/appdata/ynab-emailer
```

## Customization

### Email Templates
The HTML email templates are in the `templates/` folder:
- `daily_alert.html` - Daily alert template
- `weekly_recap.html` - Weekly recap template
- `monthly_recap.html` - Monthly report template

You can edit these to customize the look and content of your emails.

### Adding More Reports
To add custom reports:
1. Create a new template in `templates/`
2. Add a method in `YNABDataProcessor` to gather the data
3. Add a generation method in `ReportGenerator`
4. Add a send method in `YNABEmailAutomation`
5. Schedule it in `run_scheduler()`

## Project Structure

```
ynab-emailer/
├── main.py                 # Main application & scheduler
├── ynab_client.py          # YNAB API client & data processor
├── email_sender.py         # Email sending functionality
├── report_generator.py     # Report generation with Jinja2
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── .env.example            # Example environment variables
├── .env                    # Your configuration (create this)
├── templates/              # Email templates
│   ├── daily_alert.html
│   ├── weekly_recap.html
│   └── monthly_recap.html
└── README.md               # This file
```

## Security Notes

- **Never commit `.env` file** - It contains sensitive credentials
- Store your `.env` file securely
- Use App Passwords for email, not your main password
- YNAB tokens have full access to your budget - keep them secure
- Consider using environment variables instead of `.env` for production

## Support

For issues with:
- **YNAB API**: Check https://api.ynab.com/
- **This script**: Review logs and troubleshooting section above
- **Docker/Unraid**: Check Unraid forums or Docker documentation

## License

This project is provided as-is for personal use.

## Acknowledgments

- YNAB API: https://api.ynab.com/
- Built with Python, Jinja2, and schedule library
