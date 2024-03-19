import random


class Entity:
    """
        (TR) Her hayvanat bahçesindeki herhangi bir objenin türü, konumu, hızı ve canlı durumuyla karakterize edilir.
        (EN) Each entity is characterized by its type, position, speed, and alive status.

        Attributes:
            (EN)
            entity_type (str): The type of the entity, such as 'Animal', 'Predator', etc.
            position (tuple): The current position of the entity in the simulation environment as a tuple (x, y).
            speed (int): The maximum distance the entity can move in one simulation step.
            alive (bool): The living state of the entity. Entities are considered alive upon initialization and may
                          be marked as not alive as a result of simulation interactions.
            (TR)
            entity_type (str): 'Hayvan', 'Yırtıcı' vb. gibi varlığın türü.
            position (tuple): Objenin simülasyon ortamındaki bir tuple (x, y) olarak mevcut konumu.
            speed (int): Objenin bir simülasyon adımında hareket edebileceği maksimum mesafe.
            alive (bool): Objenin yaşam durumu. Varlıklar başlatıldıktan sonra canlı kabul edilir ve
                          simülasyon etkileşimlerinin bir sonucu olarak canlı değil olarak işaretlenebilir.

        Methods:
            move(boundary=(500, 500)): (TR) Verilen sınır kısıtlamaları dahilinde objenin rastgele hareketini simüle eder.
                                       (EN) Simulates random movement of the entity within the given boundary constraints.

            distance_to(other): (TR) Bu obje ile başka bir obje arasındaki Öklid mesafesini hesaplar.
                                (EN) Calculates the Euclidean distance between this entity and another entity.

    """

    def __init__(self, entity_type, position, speed):
        self.entity_type = entity_type
        self.position = position
        self.speed = speed
        self.alive = True

    def move(self, boundary=(500, 500)):
        dx = random.randint(-self.speed, self.speed)
        dy = random.randint(-self.speed, self.speed)
        new_x = min(max(0, self.position[0] + dx), boundary[0] - 1)
        new_y = min(max(0, self.position[1] + dy), boundary[1] - 1)
        self.position = (new_x, new_y)

    def distance_to(self, other):
        return ((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2) ** 0.5
