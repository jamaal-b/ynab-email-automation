# YNAB Email Automation - Project Overview

## 📋 What I Built For You

A complete Python application that automatically sends you beautiful HTML email reports about your YNAB budget on a schedule you specified.

## 📧 Email Schedule

1. **Daily Alert** - Every day at 7:30 AM
   - Uncategorized transactions (with account details)
   - Categories at 80%+ spent
   - Overspent categories

2. **Weekly Recap** - Every Monday at 8:00 AM
   - Last 7 days spending breakdown by category
   - Next 2 weeks of scheduled transactions
   - Categories that are over/under funded

3. **Monthly Report** - 1st of each month at 8:00 AM
   - Previous month's complete spending analysis
   - Top 5 spending categories with percentages
   - Recurring transactions for current month
   - Statistics: largest transaction, most active day, etc.

## 🏗️ Project Structure

```
ynab-emailer/
├── main.py                    # Main app with scheduler
├── ynab_client.py             # YNAB API integration
├── email_sender.py            # Email sending via SMTP
├── report_generator.py        # Generates HTML emails from templates
├── requirements.txt           # Python dependencies
├── Dockerfile                 # For containerization
├── docker-compose.yml         # Easy Docker deployment
├── setup.sh                   # Interactive setup script
├── .env.example               # Configuration template
├── .gitignore                 # Git ignore rules
├── README.md                  # Full documentation
├── QUICKSTART.md              # 5-minute setup guide
└── templates/                 # HTML email templates
    ├── daily_alert.html       # Daily alert template
    ├── weekly_recap.html      # Weekly recap template
    └── monthly_recap.html     # Monthly report template
```

## 🎨 Features

### Professional HTML Emails
- Modern, clean design with gradients
- Mobile-responsive
- Color-coded alerts (red for overspent, yellow for warnings, green for good)
- Progress bars for category spending
- Summary cards with key metrics

### Smart Data Processing
- Automatically aggregates transactions by category
- Filters out scheduled transactions from regular spending
- Identifies uncategorized transactions
- Calculates spending percentages
- Tracks recurring scheduled transactions

### Flexible Deployment
- **Docker**: Run in a container (perfect for Unraid)
- **Direct Python**: Run as a Python script
- **Testing Mode**: Test emails before scheduling

### Easy Configuration
- Single `.env` file for all settings
- Interactive setup script
- Customizable alert thresholds
- Adjustable timezone support

## 🚀 Quick Setup (5 Steps)

1. **Get YNAB Token**: https://app.ynab.com/settings/developer
2. **Get Email App Password**: https://myaccount.google.com/apppasswords (for Gmail)
3. **Run Setup**: `./setup.sh` (or manually edit `.env`)
4. **Test**: `python main.py test`
5. **Deploy**: `docker-compose up -d`

See QUICKSTART.md for detailed instructions.

## 🔧 Configuration Options

### .env File
```env
YNAB_API_TOKEN=your_token
YNAB_BUDGET_ID=default
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=your_email@gmail.com
CATEGORY_SPENT_THRESHOLD=80
TIMEZONE=America/New_York
```

### Customization Points

1. **Schedule Times**: Edit `main.py`
2. **Alert Threshold**: Change in `.env` (default: 80%)
3. **Email Design**: Edit HTML files in `templates/`
4. **Data Processing**: Modify methods in `ynab_client.py`

## 🧪 Testing

```bash
# Test all three email types
python main.py test

# Test individually
python main.py daily
python main.py weekly
python main.py monthly

# Start scheduler
python main.py
```

## 📦 Dependencies

- **requests**: YNAB API communication
- **jinja2**: HTML template rendering
- **schedule**: Job scheduling
- **python-dotenv**: Environment variable management

All dependencies are in `requirements.txt` and will be installed automatically with Docker.

## 🐳 Docker Deployment (Unraid)

### Method 1: Docker Compose (Recommended)
```bash
cd /mnt/user/appdata/ynab-emailer
docker-compose up -d
```

### Method 2: Direct Docker
Build and run manually using the provided Dockerfile.

### Viewing Logs
```bash
docker-compose logs -f
# or
docker logs -f ynab-emailer
```

## 🎯 Why This Solution Works Well

1. **Python-based**: Reliable, well-supported libraries
2. **YNAB API**: Official API with comprehensive data access
3. **Containerized**: Easy to deploy, isolated, portable
4. **Scheduled**: Set it and forget it
5. **Secure**: Credentials in .env file, not hardcoded
6. **Tested**: Includes test mode for verification
7. **Documented**: Comprehensive README and Quick Start guide

## 🔒 Security Considerations

- Never commit `.env` file to version control
- Use email App Passwords, not main password
- YNAB token has full budget access - keep secure
- `.gitignore` configured to protect sensitive files
- Store `.env` securely on your Unraid server

## 📈 Future Enhancement Ideas

- Add graphs/charts using Chart.js or Plotly
- Compare spending to previous periods
- Add budget vs actual comparison
- Track progress toward savings goals
- SMS alerts for critical overspending
- Web dashboard interface
- Multiple budget support
- Custom report builder

## 🛠️ Technical Details

### YNAB API Integration
- Uses official YNAB REST API
- Supports all transaction types
- Handles scheduled transactions separately
- Retrieves category budgets and balances

### Email Sending
- SMTP protocol via Python's smtplib
- Supports TLS encryption
- HTML + text multipart messages
- Works with Gmail, Outlook, custom SMTP servers

### Scheduling
- Python `schedule` library
- Runs continuously in background
- Checks every minute for pending jobs
- Timezone-aware scheduling

### Template Engine
- Jinja2 for HTML generation
- Separates logic from presentation
- Easy to customize without touching Python code
- Supports variables, loops, conditionals

## 📚 Additional Resources

- YNAB API Docs: https://api.ynab.com/
- Python Schedule: https://schedule.readthedocs.io/
- Jinja2 Docs: https://jinja.palletsprojects.com/
- Docker Docs: https://docs.docker.com/

## ✅ What's Included

- ✅ Complete working application
- ✅ Professional HTML email templates
- ✅ Docker containerization for Unraid
- ✅ Interactive setup script
- ✅ Comprehensive documentation
- ✅ Testing capabilities
- ✅ Error handling and logging
- ✅ Security best practices

## 🎉 Ready to Use!

Everything is configured and ready to deploy. Just:
1. Add your credentials to `.env`
2. Test it works
3. Deploy to your Unraid server
4. Enjoy automated budget reports!

---

**Created**: December 2024
**Language**: Python 3.11+
**License**: Personal Use
**Deployment**: Docker on Unraid NAS
