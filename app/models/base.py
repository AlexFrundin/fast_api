from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.schema import Table
import re


@as_declarative()
class Base:
   @declared_attr
   def __tablename__(cls):
      pattern = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
      return pattern.sub(r'_\1', cls.__name__).lower()
   
   @hybrid_property
   def objects(self) -> Table:
      return self.__table__
   

metadata = Base.metadata

