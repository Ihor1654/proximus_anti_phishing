from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# declarative base class
Base = declarative_base()

# an example mapping using the base
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    company = Column(String)
    business_unit = Column(String)
    team = Column(String)
    role =  Column(String)
    email = Column(String)
    linkedin = Column(String)

class Themes(Base):
    __tablename__ = 'themes'

    id = Column(Integer, primary_key=True)
    name  = Column(String)
    theme  = Column(String)
    theme_creator = Column(String)
    fake_link = Column(String)
    fake_sender = Column(String)
    system_instructions = Column(String)
    grounding_text= Column(String)
    output_composition = Column(String)
    generation_config = Column(String)

class Campaigns(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    name  = Column(String)
    theme_id  = Column(Integer, ForeignKey('themes.id'))
    campaign_creator = Column(String)
    targets = Column(String)
    start_date = Column(String)
    end_date = Column(String)

# create an engine
engine = create_engine('sqlite:///Proximus.db')
print(type(engine))
# Create database following parameters defined in `Base`. In our case, this contains the two tables 'Users' and 'Media'.
Base.metadata.create_all(engine)

# Database session
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Code to add a column
#session.execute(text("ALTER TABLE user ADD COLUMN linkedin TEXT"))

#code to update a record
# Your code
"""session.query(User).filter(User.id == '4').update({"linkedin" : "https://www.linkedin.com/in/vriveraq/"})
session.commit()"""


# Deleting a record
#session.query(User).filter(User.lastname == 'Van Belle').delete()
#session.commit()  # Commit the changes to the database


# Using `class User(Base)` to input new parameters into the table `user`
"""user_in_table = User(firstname = "Zelimkhan", 
                      lastname = "Jachichanov", 
                      company = "BeCode",
                      business_unit = "IT", 
                      team = "ARAI", 
                      role =  "Data Scientist Trainee",
                      email = "zelimkhanjachichanov@hotmail.com",
                      linkedin = "https://www.linkedin.com/in/zelimkhan-jachichanov/"

# Add and commit changes to table `user`
session.add(user_in_table)
session.commit()
print(user_in_table)
                      )
"""
"""

# Function to fetch a single record
def get_single_record(session, model, filter_condition):
    result = session.query(model).filter(filter_condition).first()
    return result

# Create a session
with SessionLocal() as session:
    # Assuming you want to fetch the user with ID 1
    result = get_single_record(session, User, User.id == 1)

    if result:
        print(f"Quote: {result.quote_quotation}")
        
    else:
        print("Quote not found.")
"""
# in case you want to close the connection in this notebook
session.close()