#!/bin/bash

echo "================================"
echo "YNAB Email Automation Setup"
echo "================================"
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Copy example file
cp .env.example .env
echo "✓ Created .env file from template"
echo ""

# Get YNAB token
echo "YNAB Configuration:"
echo "-------------------"
echo "Get your token from: https://app.ynab.com/settings/developer"
read -p "Enter your YNAB Personal Access Token: " ynab_token
sed -i "s/YNAB_API_TOKEN=.*/YNAB_API_TOKEN=$ynab_token/" .env
echo "✓ YNAB token configured"
echo ""

# Get email configuration
echo "Email Configuration:"
echo "-------------------"
echo "For Gmail:"
echo "  1. Enable 2FA on your Google account"
echo "  2. Generate App Password: https://myaccount.google.com/apppasswords"
echo ""
read -p "Enter your email address: " email_address
read -p "Enter your email password (or App Password): " -s email_password
echo ""

sed -i "s/SMTP_USERNAME=.*/SMTP_USERNAME=$email_address/" .env
sed -i "s/SMTP_PASSWORD=.*/SMTP_PASSWORD=$email_password/" .env
sed -i "s/EMAIL_FROM=.*/EMAIL_FROM=$email_address/" .env
sed -i "s/EMAIL_TO=.*/EMAIL_TO=$email_address/" .env
echo "✓ Email configured"
echo ""

# Get timezone
echo "Timezone Configuration:"
echo "----------------------"
echo "Find your timezone at: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
echo "Examples: America/New_York, America/Los_Angeles, America/Chicago, Europe/London"
read -p "Enter your timezone [America/New_York]: " timezone
timezone=${timezone:-America/New_York}
sed -i "s|TIMEZONE=.*|TIMEZONE=$timezone|" .env
sed -i "s|TZ=.*|TZ=$timezone|" docker-compose.yml
echo "✓ Timezone set to $timezone"
echo ""

# Get alert threshold
echo "Alert Threshold:"
echo "---------------"
read -p "Alert when category is X% spent [80]: " threshold
threshold=${threshold:-80}
sed -i "s/CATEGORY_SPENT_THRESHOLD=.*/CATEGORY_SPENT_THRESHOLD=$threshold/" .env
echo "✓ Threshold set to $threshold%"
echo ""

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Test the configuration:"
echo "   python main.py test"
echo ""
echo "2. Start with Docker:"
echo "   docker-compose up -d"
echo ""
echo "   Or run directly:"
echo "   python main.py"
echo ""
echo "3. View logs:"
echo "   docker-compose logs -f"
echo ""
echo "Your .env file has been created with your settings."
echo "Keep this file secure - it contains sensitive information!"
echo ""
