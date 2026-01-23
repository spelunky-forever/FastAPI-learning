from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.base import Base, BaseType
from sqlalchemy import ForeignKey
from typing import Optional, TYPE_CHECKING
from model.user import User

if TYPE_CHECKING:
    from model.item import User

class Item(Base):
    __tablename__ = "Item"
    id:Mapped[BaseType.int_primary_key]
    name:Mapped[BaseType.str_50]
    price:Mapped[float]
    brand:Mapped[BaseType.str_30]
    description:Mapped[BaseType.optional_str_100]
    create_time:Mapped[BaseType.update_time]
    last_login:Mapped[BaseType.update_time]
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship("User", back_populates="items")

    def __init__(self,name:str, price:float, brand:str, description:Optional[str], user_id:int) -> None:
        self.name = name
        self.price = price
        self.brand = brand
        self.description = description
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"Item(id={self.id}, price={self.price}, brand={self.brand}, description={self.description}, user_id={self.user_id})"
    