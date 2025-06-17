from app.db.session import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class DietPlan(Base):
    __tablename__ = "diet_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan = Column(String, nullable=False)

    user = relationship("User")
