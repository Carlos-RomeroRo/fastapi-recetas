from sqlalchemy.orm import Session
from fastapi import HTTPException

class BaseRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model
    
    def create(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def get_by_id(self, obj_id: int):
        obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} with id {obj_id} not found")
        return obj
    
    def get_all(self):
        return self.db.query(self.model).all()
    
    def delete(self, obj):
        self.db.delete(obj)
        self.db.commit()
    
    def update(self, obj):
        self.db.commit()
        self.db.refresh(obj)
        return obj
    