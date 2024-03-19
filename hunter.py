from entity import Entity
"""
    Attributes:
        hunt_range (int): (EN) The maximum distance within which the hunter can identify and attack targets. 
                               Which is 8 defined on the project definition.
                          (TR) Avcının hedefleri tespit edip saldırabileceği maksimum mesafe.
                               Proje tanımında tanımlanan 8'dir.

    Methods:
        can_hunt(entity): (EN) Determines whether a given entity falls within the hunter's hunt range and is alive. 
                          (TR) Belirli bir objenin avcının av menziline girip girmediğini ve hayatta olup olmadığını belirler.
                          
"""

class Hunter(Entity):
    def __init__(self, position, hunt_range=8):
        super().__init__("Hunter", position, 1)
        self.hunt_range = hunt_range

    def can_hunt(self, entity):
        if self is not entity and entity.alive:
            return self.distance_to(entity) <= self.hunt_range
        return False