from sqlalchemy import Column,DateTime,String,Integer

from app.db.base_class import Base



class Members(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30),  index=True)
    card_id =Column(String(30), index = True)
    finger_id = Column(String(20), index = True)
    phone = Column(String(30), index = True)
    finger_data =Column(String(5000), index=True)
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result