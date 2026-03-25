from app.database.models.category import Category
from app.database.repositories.category_repo import CategoryRepository
from app.database.session import SessionLocal


class CategoryService:
    def list_categories(self, business_id: int) -> list[Category]:
        with SessionLocal() as session:
            repo = CategoryRepository(session)
            return repo.list_all(business_id)

    def create_category(self, business_id: int, name: str) -> Category:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Category name is required.")

        with SessionLocal() as session:
            repo = CategoryRepository(session)
            existing = repo.get_by_name(business_id, clean_name)
            if existing is not None:
                raise ValueError("Category already exists.")

            return repo.create(
                business_id=business_id,
                name=clean_name,
            )

    def update_category(self, category_id: int, business_id: int, name: str) -> Category:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Category name is required.")

        with SessionLocal() as session:
            repo = CategoryRepository(session)
            category = repo.get_by_id(category_id)
            if category is None:
                raise ValueError("Category not found.")

            existing = repo.get_by_name(business_id, clean_name)
            if existing is not None and existing.id != category_id:
                raise ValueError("Another category with that name already exists.")

            return repo.update(category, name=clean_name)

    def delete_category(self, category_id: int) -> None:
        with SessionLocal() as session:
            repo = CategoryRepository(session)
            category = repo.get_by_id(category_id)
            if category is None:
                raise ValueError("Category not found.")
            repo.delete(category)
