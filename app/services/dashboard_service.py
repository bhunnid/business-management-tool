from datetime import datetime, time

from sqlalchemy import func, select

from app.database.models.expense import Expense
from app.database.models.product import Product
from app.database.models.sale import Sale
from app.database.session import SessionLocal


class DashboardService:
    def get_summary(self, business_id: int) -> dict:
        today_start = datetime.combine(datetime.now().date(), time.min)

        with SessionLocal() as session:
            sales_total = session.scalar(
                select(func.coalesce(func.sum(Sale.total), 0.0)).where(
                    Sale.business_id == business_id,
                    Sale.created_at >= today_start,
                )
            ) or 0.0

            transaction_count = session.scalar(
                select(func.count(Sale.id)).where(
                    Sale.business_id == business_id,
                    Sale.created_at >= today_start,
                )
            ) or 0

            expenses_total = session.scalar(
                select(func.coalesce(func.sum(Expense.amount), 0.0)).where(
                    Expense.business_id == business_id,
                    Expense.created_at >= today_start,
                )
            ) or 0.0

            low_stock_count = session.scalar(
                select(func.count(Product.id)).where(
                    Product.business_id == business_id,
                    Product.active == True,
                    Product.quantity_in_stock <= Product.reorder_level,
                )
            ) or 0

        return {
            "sales_total": float(sales_total),
            "transaction_count": int(transaction_count),
            "expenses_total": float(expenses_total),
            "estimated_balance": float(sales_total) - float(expenses_total),
            "low_stock_count": int(low_stock_count),
        }
