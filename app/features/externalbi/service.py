from sqlalchemy import func
from sqlalchemy.orm import Session

from app.features.contactus.service import ContactUsSortField
from app.features.externalbi.dto import ExternalBiDto
from app.features.order.model import Order
from app.features.order_type.model import OrderType
from app.utils.response import PaginatedResponse, Pagination, ResponseBiModel
from app.utils.sort import SortOrder


def find_bi_email(db: Session):

    query = (
        db.query(
            Order.email.label("email"),
            func.count(Order.id).label("total"),
        )
        .filter(Order.email.isnot(None))
        .group_by(Order.email)
        .order_by(Order.email)
    )

    data = query.all()

    return ResponseBiModel(
        message="success",
        data=[
            {
                "email": row.email,
                "total": row.total,
            }
            for row in data
        ],
    )

def find_bi_total_type(db: Session):

    query = (
        db.query(
            OrderType.id.label("order_type_id"),
            OrderType.type_name.label("order_type_name"),
            func.count(Order.id).label("total"),
        )
        .outerjoin(Order, Order.order_type_id == OrderType.id)
        .group_by(OrderType.id, OrderType.type_name)
        .order_by(OrderType.id)
    )

    data = query.all()

    return ResponseBiModel(
        message="success",
        data=[
            {
                "order_type_id": row.order_type_id,
                "order_type_name": row.order_type_name,
                "total": row.total,
            }
            for row in data
        ],
    )

def find_bi_total_status(db: Session):

    query = (
        db.query(
            Order.payment_status.label("status"),
            func.count(Order.id).label("total"),
        )
        .group_by(Order.payment_status)
        .order_by(Order.payment_status)
    )

    data = query.all()

    return ResponseBiModel(
        message="success",
        data=[
            {
                "status": row.status,
                "total": row.total,
            }
            for row in data
        ],
    )