from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.category import Category


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self, business_id: int) -> list[Category]:
        stmt = (
            select(Category)
            .where(Category.business_id == business_id)
            .order_by(Category.name.asc())
        )
        return list(self.session.scalars(stmt).all())

    def get_by_id(self, category_id: int) -> Category | None:
        return self.session.get(Category, category_id)

    def get_by_name(self, business_id: int, name: str) -> Category | None:
        stmt = select(Category).where(
            Category.business_id == business_id,
            Category.name == name,
        )
        return self.session.scalar(stmt)

    def create(self, **kwargs) -> Category:
        category = Category(**kwargs)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def update(self, category: Category, **kwargs) -> Category:
        for key, value in kwargs.items():
            setattr(category, key, value)
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        self.session.delete(category)
        self.session.commit()
