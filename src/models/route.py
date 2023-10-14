from ..database import database
from sqlalchemy import Column, String, DateTime, Float


class Route(database.Base):

    __tablename__ = 'route'

    id = Column(String, primary_key=True)
    flightId = Column(String)
    sourceAirportCode = Column(String)
    sourceCountry = Column(String)
    destinyAirportCode = Column(String)
    destinyCountry = Column(String)
    bagCost = Column(Float)
    plannedStartDate = Column(DateTime)
    plannedEndDate = Column(DateTime)
    createdAt = Column(DateTime)
    updateAt = Column(DateTime)

    def __init__(self, id, flightId, sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost, plannedStartDate, plannedEndDate, createdAt, updateAt):
        self.id = id
        self.flightId = flightId
        self.sourceAirportCode = sourceAirportCode
        self.sourceCountry = sourceCountry
        self.destinyAirportCode = destinyAirportCode
        self.destinyCountry = destinyCountry
        self.bagCost = bagCost
        self.plannedStartDate = plannedStartDate
        self.plannedEndDate = plannedEndDate
        self.createdAt = createdAt
        self.updateAt = updateAt