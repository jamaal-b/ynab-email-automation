#!/usr/bin/env python3
"""
YNAB Email Automation
Main application script with scheduler
"""

import os
import sys
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

from ynab_client import YNABClient, YNABDataProcessor
from email_sender import EmailSender
from report_generator import ReportGenerator


# Load environment variables
load_dotenv()


class YNABEmailAutomation:
    def __init__(self):
        # Initialize YNAB client
        api_token = os.getenv("YNAB_API_TOKEN")
        budget_id = os.getenv("YNAB_BUDGET_ID", "default")
        
        if not api_token:
            raise ValueError("YNAB_API_TOKEN not found in .env file")
        
        self.client = YNABClient(api_token, budget_id)
        self.processor = YNABDataProcessor(self.client)
        
        # Initialize email sender
        self.email_sender = EmailSender(
            smtp_server=os.getenv("SMTP_SERVER"),
            smtp_port=int(os.getenv("SMTP_PORT", 587)),
            username=os.getenv("SMTP_USERNAME"),
            password=os.getenv("SMTP_PASSWORD"),
            from_email=os.getenv("EMAIL_FROM")
        )
        
        self.to_email = os.getenv("EMAIL_TO")
        self.threshold = int(os.getenv("CATEGORY_SPENT_THRESHOLD", 80))
        
        # Initialize report generator
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.report_gen = ReportGenerator(template_dir)
    
    def send_daily_alert(self):
        """Send daily alert email"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running daily alert...")
        
        try:
            # Get uncategorized transactions
            uncategorized = self.processor.get_uncategorized_transactions()
            
            # Get category status
            category_status = self.processor.get_category_status(self.threshold)
            
            # Generate email
            html_content = self.report_gen.generate_daily_alert(
                uncategorized_transactions=uncategorized,
                category_status=category_status,
                threshold=self.threshold
            )
            
            # Send email
            subject = f"Daily Budget Alert - {datetime.now().strftime('%B %d, %Y')}"
            self.email_sender.send_email(
                to_email=self.to_email,
                subject=subject,
                html_content=html_content
            )
            
            print(f"  ✓ Daily alert sent successfully")
            
        except Exception as e:
            print(f"  ✗ Error sending daily alert: {str(e)}")
    
    def send_weekly_recap(self):
        """Send weekly recap email"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running weekly recap...")
        
        try:
            # Get last week's transactions
            transactions = self.processor.get_last_week_transactions()
            
            # Aggregate by category
            category_spending = self.processor.aggregate_by_category(transactions)
            
            # Get upcoming scheduled transactions
            upcoming = self.processor.get_upcoming_scheduled_transactions(days_ahead=14)
            
            # Get category status
            category_status = self.processor.get_category_status(self.threshold)
            
            # Generate email
            html_content = self.report_gen.generate_weekly_recap(
                transactions=transactions,
                category_spending=category_spending,
                upcoming_scheduled=upcoming,
                category_status=category_status
            )
            
            # Send email
            subject = f"Weekly Budget Recap - {datetime.now().strftime('%B %d, %Y')}"
            self.email_sender.send_email(
                to_email=self.to_email,
                subject=subject,
                html_content=html_content
            )
            
            print(f"  ✓ Weekly recap sent successfully")
            
        except Exception as e:
            print(f"  ✗ Error sending weekly recap: {str(e)}")
    
    def send_monthly_recap(self):
        """Send monthly recap email"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running monthly recap...")
        
        try:
            # Get last month's transactions
            transactions = self.processor.get_last_month_transactions()
            
            # Aggregate by category
            category_spending = self.processor.aggregate_by_category(transactions)
            
            # Get recurring transactions this month
            recurring = self.processor.get_recurring_scheduled_this_month()
            
            # Get month name
            last_month = datetime.now().replace(day=1) - __import__('datetime').timedelta(days=1)
            month_name = last_month.strftime("%B %Y")
            
            # Generate email
            html_content = self.report_gen.generate_monthly_recap(
                transactions=transactions,
                category_spending=category_spending,
                recurring_this_month=recurring,
                month_name=month_name
            )
            
            # Send email
            subject = f"Monthly Budget Report - {month_name}"
            self.email_sender.send_email(
                to_email=self.to_email,
                subject=subject,
                html_content=html_content
            )
            
            print(f"  ✓ Monthly recap sent successfully")
            
        except Exception as e:
            print(f"  ✗ Error sending monthly recap: {str(e)}")
    
    def run_scheduler(self):
        """Run the scheduler"""
        print("=" * 60)
        print("YNAB Email Automation Started")
        print("=" * 60)
        print(f"Daily alerts:   Every day at 7:30 AM")
        print(f"Weekly recap:   Mondays at 8:00 AM")
        print(f"Monthly recap:  1st of month at 8:00 AM")
        print(f"Alert threshold: {self.threshold}%")
        print("=" * 60)
        print("\nScheduler running... Press Ctrl+C to stop\n")
        
        # Schedule jobs
        schedule.every().day.at("07:30").do(self.send_daily_alert)
        schedule.every().monday.at("08:00").do(self.send_weekly_recap)
        schedule.every().day.at("08:00").do(self._check_monthly_recap)
        
        # Run indefinitely
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _check_monthly_recap(self):
        """Check if today is the 1st of the month and send recap"""
        if datetime.now().day == 1:
            self.send_monthly_recap()


def main():
    """Main entry point"""
    try:
        automation = YNABEmailAutomation()
        
        # Check command line arguments for manual execution
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            if command == "daily":
                automation.send_daily_alert()
            elif command == "weekly":
                automation.send_weekly_recap()
            elif command == "monthly":
                automation.send_monthly_recap()
            elif command == "test":
                print("Testing all reports...")
                automation.send_daily_alert()
                automation.send_weekly_recap()
                automation.send_monthly_recap()
            else:
                print("Usage: python main.py [daily|weekly|monthly|test]")
                print("  Or run without arguments to start scheduler")
        else:
            # Start scheduler
            automation.run_scheduler()
    
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
