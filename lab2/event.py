class Event:
    def __init__(self, id, idDay, name, time, mandatory):
        self.id = id
        self.name = name
        self.time = time
        self.mandatory = mandatory
        self.idDay = idDay