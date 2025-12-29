"""
Report Generator
Creates email reports from YNAB data using Jinja2 templates
"""

from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
import os


class ReportGenerator:
    def __init__(self, template_dir: str):
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate_daily_alert(
        self,
        uncategorized_transactions: List[Dict],
        category_status: Dict,
        threshold: int
    ) -> str:
        """Generate daily alert email HTML"""
        template = self.env.get_template("daily_alert.html")
        
        return template.render(
            current_date=datetime.now().strftime("%A, %B %d, %Y"),
            uncategorized_transactions=uncategorized_transactions,
            uncategorized_count=len(uncategorized_transactions),
            category_status=category_status,
            threshold=threshold
        )
    
    def generate_weekly_recap(
        self,
        transactions: List[Dict],
        category_spending: Dict,
        upcoming_scheduled: List[Dict],
        category_status: Dict
    ) -> str:
        """Generate weekly recap email HTML"""
        template = self.env.get_template("weekly_recap.html")
        
        # Calculate week start/end
        today = datetime.now()
        week_start = (today - timedelta(days=7)).strftime("%B %d")
        week_end = today.strftime("%B %d, %Y")
        
        # Calculate total spent
        total_spent = sum(abs(t.get("amount", 0)) / 1000 for t in transactions)
        
        return template.render(
            week_start=week_start,
            week_end=week_end,
            total_spent=total_spent,
            transaction_count=len(transactions),
            category_spending=category_spending,
            upcoming_scheduled=upcoming_scheduled,
            category_status=category_status
        )
    
    def generate_monthly_recap(
        self,
        transactions: List[Dict],
        category_spending: Dict,
        recurring_this_month: List[Dict],
        month_name: str
    ) -> str:
        """Generate monthly recap email HTML"""
        template = self.env.get_template("monthly_recap.html")
        
        # Calculate statistics
        total_spent = sum(abs(t.get("amount", 0)) / 1000 for t in transactions)
        transaction_count = len(transactions)
        
        # Days in month
        last_month = datetime.now().replace(day=1) - timedelta(days=1)
        days_in_month = last_month.day
        
        avg_per_day = total_spent / days_in_month if days_in_month > 0 else 0
        avg_transaction = total_spent / transaction_count if transaction_count > 0 else 0
        
        # Find largest transaction
        largest_transaction = 0
        if transactions:
            largest_transaction = max(abs(t.get("amount", 0)) / 1000 for t in transactions)
        
        # Find most active day
        day_counts = defaultdict(int)
        for t in transactions:
            date = datetime.strptime(t["date"], "%Y-%m-%d")
            day_counts[date.strftime("%A")] += 1
        
        most_active_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else "N/A"
        
        # Top categories with percentages
        top_categories = []
        for cat_name, data in sorted(
            category_spending.items(), 
            key=lambda x: x[1]["total"], 
            reverse=True
        ):
            percentage = (data["total"] / total_spent * 100) if total_spent > 0 else 0
            top_categories.append((
                cat_name,
                {
                    **data,
                    "percentage": percentage
                }
            ))
        
        return template.render(
            month_name=month_name,
            total_spent=total_spent,
            transaction_count=transaction_count,
            avg_per_day=avg_per_day,
            avg_transaction=avg_transaction,
            largest_transaction=largest_transaction,
            most_active_day=most_active_day,
            categories_used=len(category_spending),
            top_categories=top_categories,
            recurring_this_month=recurring_this_month,
            comparison_last_month=None  # Could add this feature later
        )
