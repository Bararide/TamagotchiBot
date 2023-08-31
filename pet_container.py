class Pet:
    def __init__(self, owner, animal, pet_name, latitude = None, longitude = None, health = 100) -> None:
        self.pet_name = pet_name
        self.animal = animal
        self.health = health
        self.owner = owner
        self.latitude = latitude
        self.longitude = longitude

    def __init__(self) -> None:
        self.latitude = None
        self.longitude = None

    def return_pet_list(self) -> list:
        return [self.animal, self.pet_name]