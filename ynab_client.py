"""
YNAB API Client
Handles all interactions with the YNAB API
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class YNABClient:
    def __init__(self, api_token: str, budget_id: str = "default"):
        self.api_token = api_token
        self.budget_id = budget_id
        self.base_url = "https://api.ynab.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a request to the YNAB API"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()["data"]
    
    def get_budget_id(self) -> str:
        """Get the actual budget ID if using 'default'"""
        if self.budget_id != "default":
            return self.budget_id
        
        data = self._make_request("budgets")
        return data["budgets"][0]["id"]
    
    def get_accounts(self) -> List[Dict]:
        """Get all accounts"""
        budget_id = self.get_budget_id()
        data = self._make_request(f"budgets/{budget_id}/accounts")
        return data["accounts"]
    
    def get_transactions(
        self, 
        since_date: Optional[str] = None,
        account_id: Optional[str] = None
    ) -> List[Dict]:
        """Get transactions, optionally filtered by date and account"""
        budget_id = self.get_budget_id()
        params = {}
        if since_date:
            params["since_date"] = since_date
        
        endpoint = f"budgets/{budget_id}/transactions"
        if account_id:
            endpoint = f"budgets/{budget_id}/accounts/{account_id}/transactions"
        
        data = self._make_request(endpoint, params)
        return data["transactions"]
    
    def get_scheduled_transactions(self) -> List[Dict]:
        """Get all scheduled transactions"""
        budget_id = self.get_budget_id()
        data = self._make_request(f"budgets/{budget_id}/scheduled_transactions")
        return data["scheduled_transactions"]
    
    def get_month_budget(self, month: Optional[str] = None) -> Dict:
        """
        Get budget data for a specific month
        month format: YYYY-MM-DD (uses first day of month)
        """
        budget_id = self.get_budget_id()
        if not month:
            month = datetime.now().strftime("%Y-%m-01")
        
        data = self._make_request(f"budgets/{budget_id}/months/{month}")
        return data["month"]
    
    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        budget_id = self.get_budget_id()
        data = self._make_request(f"budgets/{budget_id}/categories")
        return data["category_groups"]


class YNABDataProcessor:
    """Process YNAB data for email reports"""
    
    def __init__(self, client: YNABClient):
        self.client = client
    
    def get_last_week_transactions(self) -> List[Dict]:
        """Get transactions from the last 7 days, excluding transfers, reconciliations, and inflows"""
        since_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        transactions = self.client.get_transactions(since_date=since_date)
        
        # Filter out scheduled transactions, transfers, reconciliations, and inflows
        actual_transactions = []
        for t in transactions:
            # Skip scheduled transactions
            if t.get("scheduled_transaction_id"):
                continue
            
            # Skip transfers between accounts
            if t.get('transfer_account_id'):
                continue
            
            # Skip reconciliation adjustments - safely handle None values
            payee_name = t.get('payee_name') or ''
            if 'reconciliation' in payee_name.lower() or 'balance adjustment' in payee_name.lower():
                continue
            
            # Skip inflows (income going to Ready to Assign) - safely handle None values
            cat_name = t.get('category_name') or ''
            if 'inflow' in cat_name.lower() or 'ready to assign' in cat_name.lower():
                continue
            
            actual_transactions.append(t)
        
        actual_transactions.sort(key=lambda x: x["date"], reverse=True)
        return actual_transactions
    
    def get_last_month_transactions(self) -> List[Dict]:
        """Get transactions from the previous month, excluding transfers, reconciliations, and inflows"""
        today = datetime.now()
        first_of_this_month = today.replace(day=1)
        last_month = first_of_this_month - timedelta(days=1)
        first_of_last_month = last_month.replace(day=1)
        
        since_date = first_of_last_month.strftime("%Y-%m-%d")
        transactions = self.client.get_transactions(since_date=since_date)
        
        # Filter to only last month, excluding transfers, reconciliations, and inflows
        last_month_str = last_month.strftime("%Y-%m")
        last_month_transactions = []
        for t in transactions:
            # Only include transactions from last month
            if not t["date"].startswith(last_month_str):
                continue
            
            # Skip scheduled transactions
            if t.get("scheduled_transaction_id"):
                continue
            
            # Skip transfers between accounts
            if t.get('transfer_account_id'):
                continue
            
            # Skip reconciliation adjustments - safely handle None values
            payee_name = t.get('payee_name') or ''
            if 'reconciliation' in payee_name.lower() or 'balance adjustment' in payee_name.lower():
                continue
            
            # Skip inflows (income) - safely handle None values
            cat_name = t.get('category_name') or ''
            if 'inflow' in cat_name.lower() or 'ready to assign' in cat_name.lower():
                continue
            
            last_month_transactions.append(t)
        
        return last_month_transactions
    
    def get_upcoming_scheduled_transactions(self, days_ahead: int = 30) -> List[Dict]:
        """Get scheduled transactions in the next N days"""
        scheduled = self.client.get_scheduled_transactions()
        today = datetime.now().date()
        future_date = today + timedelta(days=days_ahead)
        
        upcoming = []
        for st in scheduled:
            next_date = st.get("date_next")
            if next_date:
                next_date_obj = datetime.strptime(next_date, "%Y-%m-%d").date()
                if today <= next_date_obj <= future_date:
                    upcoming.append(st)
        
        upcoming.sort(key=lambda x: x["date_next"])
        return upcoming
    
    def get_uncategorized_transactions(self) -> List[Dict]:
        """Get transactions that haven't been categorized, excluding transfers and inflows"""
        # Get recent transactions (last 30 days)
        since_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        transactions = self.client.get_transactions(since_date=since_date)
        
        # YNAB uses a null or specific category for uncategorized
        # Also exclude transfers and inflows
        uncategorized = []
        for t in transactions:
            # Skip transfers between accounts
            if t.get('transfer_account_id'):
                continue
            
            # Skip reconciliations - safely handle None values
            payee_name = t.get('payee_name') or ''
            if 'reconciliation' in payee_name.lower() or 'balance adjustment' in payee_name.lower():
                continue
            
            # Skip inflows (we don't need to categorize income) - safely handle None values
            cat_name = t.get('category_name') or ''
            if 'inflow' in cat_name.lower() or 'ready to assign' in cat_name.lower():
                continue
            
            # Check if uncategorized
            if not t.get("category_id") or t.get("category_name") == "Uncategorized":
                uncategorized.append(t)
        
        return uncategorized
    
    def get_category_status(self, threshold_percent: int = 80) -> Dict:
        """
        Get categories that are over budget or close to the threshold
        Returns dict with 'overspent', 'warning', and 'underfunded' lists
        """
        month_data = self.client.get_month_budget()
        categories = month_data.get("categories", [])
        
        result = {
            "overspent": [],
            "warning": [],  # Close to limit
            "underfunded": []
        }
        
        for cat in categories:
            budgeted = cat.get("budgeted", 0) / 1000  # Convert from milliunits
            activity = abs(cat.get("activity", 0)) / 1000  # Activity is negative for spending
            balance = cat.get("balance", 0) / 1000
            name = cat.get("name") or "Unknown"
            
            # Skip "Inflow: Ready to Assign" - this is income, not a spending category - safely handle None
            if 'inflow' in name.lower() or 'ready to assign' in name.lower():
                continue
            
            # Skip categories with no budget
            if budgeted == 0:
                continue
            
            percent_used = (activity / budgeted * 100) if budgeted > 0 else 0
            
            if balance < 0:
                result["overspent"].append({
                    "name": name,
                    "budgeted": budgeted,
                    "activity": activity,
                    "balance": balance,
                    "percent_used": percent_used
                })
            elif percent_used >= threshold_percent:
                result["warning"].append({
                    "name": name,
                    "budgeted": budgeted,
                    "activity": activity,
                    "balance": balance,
                    "percent_used": percent_used
                })
            elif balance > budgeted * 2:  # More than double the monthly budget available
                result["underfunded"].append({
                    "name": name,
                    "budgeted": budgeted,
                    "activity": activity,
                    "balance": balance
                })
        
        return result
    
    def aggregate_by_category(self, transactions: List[Dict]) -> Dict[str, Dict]:
        """Aggregate transactions by category, excluding transfers, reconciliations, and inflows
        
        For split transactions, this method expands the subtransactions so each category
        gets counted individually instead of lumping everything under 'Split'
        """
        category_totals = {}
        
        for t in transactions:
            # Skip transfers between accounts
            if t.get('transfer_account_id'):
                continue
            
            # Skip reconciliation adjustments - safely handle None values
            payee_name = t.get('payee_name') or ''
            if 'reconciliation' in payee_name.lower() or 'balance adjustment' in payee_name.lower():
                continue
            
            # Handle split transactions by processing subtransactions individually
            subtransactions = t.get('subtransactions', [])
            if subtransactions:
                # This is a split transaction - process each subtransaction separately
                for sub in subtransactions:
                    # Skip inflows in subtransactions too
                    sub_cat_name = sub.get('category_name') or 'Uncategorized'
                    if 'inflow' in sub_cat_name.lower() or 'ready to assign' in sub_cat_name.lower():
                        continue
                    
                    # Get the amount from the subtransaction
                    # REMOVED abs() to keep the sign (negative for spending, positive for returns)
                    sub_amount = sub.get('amount', 0) / 1000
                    
                    # Add to the appropriate category
                    if sub_cat_name not in category_totals:
                        category_totals[sub_cat_name] = {
                            "total": 0,
                            "count": 0,
                            "transactions": []
                        }
                    
                    # SUBTRACT the amount:
                    # Spending (-100) -> becomes +100 towards total spent
                    # Return (+100)   -> becomes -100 towards total spent
                    category_totals[sub_cat_name]["total"] -= sub_amount
                    category_totals[sub_cat_name]["count"] += 1
                    # Store the parent transaction but note it was from a split
                    category_totals[sub_cat_name]["transactions"].append(t)
                
                # Skip processing the parent transaction since we handled the subtransactions
                continue
            
            # For non-split transactions, process normally
            # Skip inflows (income going to Ready to Assign) - safely handle None values
            cat_name = t.get('category_name') or 'Uncategorized'
            if 'inflow' in cat_name.lower() or 'ready to assign' in cat_name.lower():
                continue
            
            # REMOVED abs() here as well
            amount = t.get('amount', 0) / 1000  # Convert from milliunits
            
            if cat_name not in category_totals:
                category_totals[cat_name] = {
                    "total": 0,
                    "count": 0,
                    "transactions": []
                }
            
            # SUBTRACT the amount
            category_totals[cat_name]["total"] -= amount
            category_totals[cat_name]["count"] += 1
            category_totals[cat_name]["transactions"].append(t)
        
        return category_totals
    
    def get_recurring_scheduled_this_month(self) -> List[Dict]:
        """Get recurring scheduled transactions for the current month"""
        scheduled = self.client.get_scheduled_transactions()
        today = datetime.now()
        this_month = today.strftime("%Y-%m")
        
        recurring_this_month = []
        for st in scheduled:
            frequency = st.get("frequency", "")
            next_date = st.get("date_next", "")
            
            # Check if it's recurring and occurs this month
            if frequency and frequency != "never" and next_date.startswith(this_month):
                recurring_this_month.append(st)
        
        recurring_this_month.sort(key=lambda x: x["date_next"])
        return recurring_this_month
