from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, func
from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property

class Base(DeclarativeBase):
    pass

class Person(Base):
    __tablename__ = "persons"
    
    wca_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    
    results: Mapped[list["Result"]] = relationship(back_populates="person")
    
    country_id: Mapped[str] = mapped_column(ForeignKey("countries.id"))
    country: Mapped["Country"] = relationship(back_populates="people")
    

class Competition(Base):
    __tablename__ = "competitions"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    
    results: Mapped[list["Result"]] = relationship(back_populates="competition")
    year: Mapped[int]
    month: Mapped[int]
    day: Mapped[int]
    
    @hybrid_property
    def start_date(self) -> date:
        return date(self.year, self.month, self.day)

    @start_date.expression
    def start_date(cls):
        return func.printf("%04d-%02d-%02d", cls.year, cls.month, cls.day)

class Result(Base):
    __tablename__ = "results"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[str] = mapped_column(ForeignKey("persons.wca_id"))
    competition_id: Mapped[str] = mapped_column(ForeignKey("competitions.id"))
    
    best: Mapped[int]
    average: Mapped[int | None]
    
    person: Mapped[Person] = relationship(back_populates="results")
    competition: Mapped[Competition] = relationship(back_populates="results")
    
    round_type_id: Mapped[str] = mapped_column(ForeignKey("round_types.id"))
    round_type: Mapped["RoundType"] = relationship()
    event_id: Mapped[str] = mapped_column(ForeignKey("events.id"))

class Country(Base):
    __tablename__= "countries"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    
    people: Mapped[list["Person"]] = relationship(back_populates="country")

class Event(Base):
    __tablename__ = "events"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

class RoundType(Base):
    __tablename__ = "round_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    rank: Mapped[int]
    final: Mapped[int]
    name: Mapped[str]
    cell_name: Mapped[str]