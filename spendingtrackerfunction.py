import json
import boto3
from collections import defaultdict
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SpendingTrackingTable")
budget_table = dynamodb.Table("budgetTrackingTable")

def lambda_handler(event, context):
    try:
        method = event.get("httpMethod", "GET")

        # 🔹 Handle POST: Add a new expense
        if method == "POST":
            body = json.loads(event["body"])
            item = body.get("item")
            price = float(body.get("price", 0))
            category = body.get("category", "Other")
            date = body.get("date", datetime.today().strftime("%Y-%m-%d"))

            if not item or price <= 0:
                return {
                    "statusCode": 400,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": json.dumps({"error": "Invalid item or price"})
                }

            # Save expense in DynamoDB
            table.put_item(Item={
                "date": date,
                "item": item,
                "price": str(price),
                "category": category
            })

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                },
                "body": json.dumps({"message": "Expense added successfully!"})
            }

        # 🔹 Handle GET: Dashboard logic (your existing code)
        response = table.scan()
        items = response.get("Items", [])

        budget_response = budget_table.scan()
        budget_items = budget_response.get("Items", [])

        current_budget = 0
        if budget_items:
            for item in budget_items:
                if "actual-budget" in item:
                    try:
                        current_budget = float(item["actual-budget"])
                        break
                    except (ValueError, TypeError):
                        pass

        spending_data = defaultdict(float)
        item_spending = defaultdict(float)
        monthly_spending = defaultdict(float)
        category_spending = defaultdict(float)
        highest_spent_item = {"item": None, "amount": 0}
        total_spent = 0

        for entry in items:
            date = entry["date"]
            item = entry["item"]
            price = float(entry["price"])
            category = entry.get("category", "Other")

            spending_data[date] += price
            item_spending[item] += price
            category_spending[category] += price

            month = date[:7]
            monthly_spending[month] += price

            if price > highest_spent_item["amount"]:
                highest_spent_item = {"item": item, "amount": price}

            total_spent += price

        top_5_items = sorted(item_spending.items(), key=lambda x: x[1], reverse=True)[:5]
        top_5_items = [{"item": item, "amount": amount} for item, amount in top_5_items]

        highest_category = max(category_spending.items(), key=lambda x: x[1], default=("None", 0))
        highest_spending_category = {
            "category": highest_category[0],
            "amount": highest_category[1]
        }

        category_breakdown = [{"category": cat, "amount": amount} for cat, amount in category_spending.items()]

        today = datetime.today()
        current_month = today.strftime("%Y-%m")
        days_passed = today.day
        days_in_month = (datetime(today.year, today.month % 12 + 1, 1) - datetime(today.year, today.month, 1)).days
        total_spent_current_month = monthly_spending.get(current_month, 0)
        projected_cost = (total_spent_current_month / days_passed) * days_in_month if days_passed > 0 else 0

        budget_remaining = current_budget - total_spent_current_month
        budget_percentage = (total_spent_current_month / current_budget) * 100 if current_budget > 0 else 0

        spending_trend = "steady"
        daily_spending_rate = total_spent_current_month / days_passed if days_passed > 0 else 0

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "spending_data": dict(spending_data),
                "highest_spent_item": highest_spent_item,
                "top_5_items": top_5_items,
                "monthly_spending": dict(monthly_spending),
                "projected_cost": projected_cost,
                "current_budget": current_budget,
                "budget_remaining": budget_remaining,
                "budget_percentage": budget_percentage,
                "highest_spending_category": highest_spending_category,
                "category_breakdown": category_breakdown,
                "spending_trend": spending_trend,
                "daily_spending_rate": daily_spending_rate,
                "total_spent": total_spent
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
