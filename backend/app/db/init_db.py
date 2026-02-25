from .session import engine
from .base import Base

def init_db():
    import app.models.user
    import app.models.transaction
    import app.models.category
    
    Base.metadata.create_all(bind=engine)
