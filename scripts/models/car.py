# Class to describe a car
class Car:
    def __init__(self, manufacturer, model, assembly_location, first_year_produced, last_year_produced, engine, transmission, weight):
        self.manufacturer = manufacturer
        self.model = model
        self.assembly_location = assembly_location
        self.first_year_produced = first_year_produced
        self.last_year_produced = last_year_produced
        self.engine = engine
        self.transmission = transmission
        self.weight = weight
