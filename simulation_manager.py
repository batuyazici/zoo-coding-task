from animal import Animal, Predator
from hunter import Hunter
from spatial_hash import SpatialHash
import random


class SimulationManager:
    """
    (EN)
    The simulation progresses through steps such as updating entity positions,
    checking for interactions, and generating new animals as a result of these interactions.
    (TR)
    Simülasyon, objelerin konumlarının güncellenmesi, etkileşimlerin kontrol edilmesi
    ve bu etkileşimler sonucunda yeni hayvanların üretilmesi gibi adımlarla ilerlemektedir.

    Attributes:
        (EN)
        entities (list): A collection of all entities participating in the simulation.
        spatial_hash (SpatialHash): SpatialHash instance to be used in the simulation.
        (TR)
        entities (list): Simülasyona katılan tüm objelerin bir listesi.
        spatial_hash (SpatialHash): Simülasyonda kullanılacak SpatialHash örneği.

    Methods:
        (EN)
        create_entity(): Creates an entity with specified characteristics.
        initialize_entities(): Initializes a predefined set of entities for the simulation.
        move_entities(): Moves entities based on their attributes and updates their positions in the spatial hash.
        check_interactions(): Checks for and handles interactions between entities, such as hunting or mating.
        handle_hunting(): Processes hunting interactions for predators and hunters.
        handle_reproduction(): Manages the reproduction process for animal entities.
        update_entities(): Updates the entity list based on the outcomes of interactions.
        run(): Executes the simulation loop, updating entities and checking for interactions until a stop condition is met.
        (TR)
        create_entity(): Belirtilen özelliklere sahip bir obje oluşturur (Aslan, Tavuk, Avcı vb.)
        initialize_entities(): Simülasyon için önceden tanımlanmış bir obje listesi başlatır.
        move_entities(): Objeleri özelliklerine göre taşır ve konumlarını spatial hash'ta günceller.
        check_interactions(): Avlanma veya meydana gelme gibi varlıklar arasındaki etkileşimleri kontrol eder ve yönetir.
        handle_hunting(): Yırtıcı hayvanlar ve avcılar için avlanma etkileşimlerini işler.
        handle_reproduction(): Hayvan varlıkları için üreme sürecini yönetir.
        update_entities(): Etkileşimlerin sonuçlarına göre obje listesini günceller.
        run(): Bir durdurma koşulu (1000 birim adım) karşılanana kadar varlıkları güncelleyerek ve etkileşimleri kontrol ederek
        simülasyon döngüsünü yürütür.
    """

    def __init__(self):
        self.entities = []
        self.spatial_hash = SpatialHash()
        self.initialize_entities()

    @staticmethod
    def create_entity(entity_type, gender, position, speed, hunt_range=None, prey_types=None):
        if entity_type == 'Hunter':
            return Hunter(position, hunt_range)
        elif entity_type in ['Wolf', 'Lion']:
            return Predator(entity_type, gender, position, speed, hunt_range, prey_types)
        else:
            return Animal(entity_type, gender, position, speed)

    def initialize_entities(self):
        self.entities = []

        animal_specs = [
            ("Sheep", 30, 2),
            ("Cow", 10, 2),
            ("Chicken", 10, 1),
            ("Rooster", 10, 1)
        ]
        predator_specs = [
            ("Wolf", 10, 3, ["Sheep", "Chicken", "Rooster"], 4),
            ("Lion", 8, 4, ["Cow", "Sheep"], 5)
        ]

        # Initialize Animals
        for spec in animal_specs:
            entity_type, total_count, speed = spec
            for i in range(total_count):  # spec[1] is the total count
                position = (random.randint(0, 499), random.randint(0, 499))
                gender = "Male" if i < total_count / 2 else "Female"
                self.entities.append(self.create_entity(entity_type, gender, position, speed))

        # Initialize Predators
        for spec in predator_specs:
            entity_type, total_count, speed, prey_types, hunt_range = spec
            for i in range(total_count):
                position = (random.randint(0, 499), random.randint(0, 499))
                gender = "Male" if i < total_count / 2 else "Female"
                self.entities.append(self.create_entity(entity_type, gender, position, speed, hunt_range, prey_types))

        self.entities.append(
            self.create_entity('Hunter', None, (random.randint(0, 499), random.randint(0, 499)), 1, hunt_range=8))

    def move_entities(self):
        for entity in self.entities:
            if entity.alive:
                entity.move()
                self.spatial_hash.insert(entity)

    def check_interactions(self):
        newborn_entities = []

        for entity in self.entities:
            if not entity.alive:
                continue

            if isinstance(entity, (Hunter, Predator)):
                self.handle_hunting(entity)
            elif isinstance(entity, Animal) and entity.can_reproduce:
                newborn_entities += self.handle_reproduction(entity)

        return newborn_entities

    def handle_hunting(self, entity):
        targets = self.spatial_hash.query(entity.position, entity.hunt_range)
        for target in targets:
            if entity != target and entity.can_hunt(target):
                target.alive = False

    def handle_reproduction(self, entity):
        newborn_entities = []
        partners = self.spatial_hash.query(entity.position, 3)
        for partner in partners:
            if (entity != partner and entity.can_reproduce_with(partner) and
                    partner.can_reproduce and entity.distance_to(partner) <= 3):
                new_position = ((entity.position[0] + partner.position[0]) // 2,
                                (entity.position[1] + partner.position[1]) // 2)
                offspring = Animal(entity.entity_type, random.choice(["Male", "Female"]),
                                   new_position, entity.speed)
                offspring.can_reproduce = False
                newborn_entities.append(offspring)
                entity.can_reproduce = False
                partner.can_reproduce = False

        return newborn_entities

    def update_entities(self, newborn_entities):
        self.entities.extend(newborn_entities)
        self.entities = [entity for entity in self.entities if entity.alive]
        for entity in self.entities:
            if isinstance(entity, Animal):
                entity.can_reproduce = True

    def run(self, cell_size=10, total_movement_units=1000):
        self.spatial_hash = SpatialHash(cell_size)
        movement_units = 0
        print(f"Simulation start with {len(self.entities)} entities remaining.")
        while movement_units < total_movement_units:
            self.spatial_hash.clear()
            self.move_entities()
            movement_units += sum(entity.speed for entity in self.entities if entity.alive)

            newborn_entities = self.check_interactions()
            self.update_entities(newborn_entities)

        print(f"Simulation ended with {len(self.entities)} entities remaining.")
