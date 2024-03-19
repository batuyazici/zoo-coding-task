from entity import Entity


class Animal(Entity):
    """
        (EN) The animal class, which is inherited from the entity class, also contains the reproduction and gender of that animal,
        and a method for the controls its reproduction with another object.
        (TR) Entity classından inherit edilen animal classında ek olarak o hayvanın reproducelaması ve cinsiyeti bulunur,
        bir methodda öteki objeyle reproducelamasını kontrol eder.

        Attributes:
            (EN)
            gender (str): The gender of the animal.
            can_reproduce (bool): Indicates whether the animal is currently capable of reproducing. This
                                  reset based on simulation rules after an animal reproduces.
             (TR)
             gender (str): Hayvanın cinsiyeti.
             can_reproduce (bool): Hayvanın şu anda üreme yeteneğine sahip olup olmadığını gösterir. Bu
                                  Bir hayvan çoğaldıktan sonra simülasyon kurallarına göre sıfırlanır.
        Methods:
            can_reproduce_with(other): (EN) Determines whether this animal can reproduce with another animal.
                                       (TR) Bu hayvanın başka bir hayvanla üreyip üreyemeyeceğini belirler.
    """
    def __init__(self, entity_type, gender, position, speed):
        super().__init__(entity_type, position, speed)
        self.gender = gender
        self.can_reproduce = True

    def can_reproduce_with(self, other):
        return (self.entity_type == other.entity_type and
                self.gender != other.gender and
                other.can_reproduce and  # Ensure both animals can reproduce
                self.distance_to(other) <= 3)  # Reproduction only if they're close enough


class Predator(Animal):
    def __init__(self, entity_type, gender, position, speed, hunt_range, prey_types):
        super().__init__(entity_type, gender, position, speed)
        self.hunt_range = hunt_range
        self.prey_types = prey_types

    def can_hunt(self, prey):
        return prey.entity_type in self.prey_types and self.distance_to(prey) <= self.hunt_range
