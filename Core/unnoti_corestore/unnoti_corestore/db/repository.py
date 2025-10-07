from sqlalchemy.orm import Session

class GenericRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def list(self):
        return self.db.query(self.model).all()

    def get(self, id_):
        return self.db.query(self.model).get(id_)

    def create(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj):
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj):
        self.db.delete(obj)
        self.db.commit()
        return True