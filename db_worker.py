from sqlalchemy import create_engine, Column, Integer,Float, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from functools import wraps

Base = declarative_base()

user_group = Table(
    'user_group',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.group_id'), primary_key=True),
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,nullable=False)
    firstname = Column(String,nullable=False)
    lastname = Column(String,nullable=False)
    company = Column(String)
    business_unit = Column(String)
    team = Column(String)
    role = Column(String)
    email = Column(String,nullable=False)
    linkedin = Column(String)
    email_count = Column(Integer, default=0)
    email_opened= Column(Integer, default=0)
    link_clicked = Column(Integer, default=0)
    submited_data = Column(Integer, default=0)
    email_reported = Column(Integer, default=0)
    templates = relationship('Template', back_populates='user')
    groups = relationship('Group', secondary=user_group, back_populates='users')

class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)

    users = relationship('User', secondary=user_group, back_populates='groups')

class Template(Base):
    __tablename__ = 'templates'

    template_id = Column(Integer, primary_key=True)
    html_template = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='templates')

class Theme(Base):
    __tablename__ = 'themes'

    id = Column(Integer, primary_key=True)
    name = Column(String,unique=True)
    landing_page = Column(String)
    system_instruction = Column(String)
    structur_instruction = Column(String)
    prompt_template = Column(String)
    subject = Column(String)
    config_id = Column(Integer, ForeignKey('generative_config.id'))

    generative_config = relationship('GenerativeConfig', back_populates='themes')

class GenerativeConfig(Base):
    __tablename__ = 'generative_config'

    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    p = Column(Float)
    k = Column(Integer)
    max_output_tokens = Column(Integer)
    response_mime_type = Column(String)

    themes = relationship('Theme', back_populates='generative_config')

class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False,unique=True)
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    theme_id = Column(Integer, ForeignKey('themes.id'))

    group = relationship('Group')
    theme = relationship('Theme')

def db_operation(operation_type):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            session = self.Session()
            try:
                result = func(self, session, *args, **kwargs)
                if operation_type == "add":
                    session.add(result)
                    session.commit()
                    session.refresh(result)
                elif operation_type == "delete":
                    session.delete(result)
                    session.commit()
                return result
            except Exception as e:
                session.rollback()
                print(f"Error during {operation_type}: {e}")
            finally:
                session.close()
        return wrapper
    return decorator

class DBWorker:
    def __init__(self, db_path='data/db/Proximus_v2.db'):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    @db_operation("add")
    def add_record(self, session, model_class, **kwargs):
        return model_class(**kwargs)

    @db_operation("delete")
    def delete_record(self, session, model_class, **filters):
        return session.query(model_class).filter_by(**filters).first()

    @db_operation("get")
    def get_record(self, session, model_class, **filters):
        return session.query(model_class).filter_by(**filters).first()
    
    @db_operation("get")
    def get_records(self, session, model_class, **filters):
        return session.query(model_class).filter_by(**filters).all()
    
    @db_operation("add")
    def add_user_to_group(self, session, user_id, group_id):
        # Получаем пользователя по user_id
        user = session.query(User).filter_by(id=user_id).first()

        # Получаем группу по group_id
        group = session.query(Group).filter_by(group_id=group_id).first()

        if user and group:
            # Добавляем пользователя в группу
            group.users.append(user)

            # Возвращаем обновленную группу
            return group
        else:
            raise ValueError("User or Group not found")

