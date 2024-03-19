
class SpatialHash:
    """
    (EN) Implements a spatial hashing mechanism to efficiently manage and query entities based on their positions
    within a simulated environment. Spatial hashing divides the space into a grid of cells, with each cell
    containing entities that fall within its bounds.
    (TR) Objeler simüle edilmiş bir ortamdaki konumlarına göre verimli bir şekilde yönetmek ve nerede olduğunu bulmak için spatial hashing uygulanır.
    Spatial hashing, alanı bir ızgaraya böler ve ızgaradaki her hücre kendi sınırları dahilindeki objeler, içerir.

    Attributes:
        (EN)
        cell_size (int): The size of each cell in the spatial hash grid.
        buckets (dict): A dictionary mapping grid cell keys to lists of entities within those cells. Each key
                        represents a cell's coordinates in the grid.
        (TR)
        cell_size (int): Spatial Hash Grid'teki her bir kısmın boyutu.
        buckets (dict): Dictionary hücre anahtarlarını bu hücrelerdeki varlıkların listelerine eşleyen bir method.
                        Her key, gridteki bir hücrenin koordinatlarını temsil eder.

    Methods:
        (EN)
        get_key(position): Calculates and returns the key for the cell corresponding to a given position in the
                           spatial hash grid.
        insert(entity): Adds an entity to the appropriate cell based on its position. If the cell does not
                        already exist in the buckets dictionary, it is created.
        query(position, query_range): Retrieves a list of entities within a specified range of a given position.
                                      This method computes the range of cells to inspect based on the query range
                                      and aggregates entities from these cells.
        clear(): Clears the spatial hash by resetting the buckets dictionary, removing all entities from the
                 spatial hash.
        (TR)
        get_key(position): Spatial hashing uygulamasında ızgarada belirli bir konuma karşılık gelen hücrenin anahtarını hesaplar ve döndürür.
        insert(entity): Konumuna göre uygun hücreye bir obje ekler. Hücre, buckets'ta zaten mevcut değilse oluşturulur.
        query(position, query_range): Belirli bir konumun belirli bir aralığındaki varlıkların listesini alır.
                                     Bu fonksiyon, sorgu aralığına göre incelenecek hücre aralığını hesaplar ve bu hücrelerdeki varlıkları toplar.
        clear(): Buckets'ı sıfırlayarak, tüm varlıkları spatial hashingten kaldırarak sıfırlar.
    """
    def __init__(self, cell_size=10):
        self.cell_size = cell_size
        self.buckets = {}

    def get_key(self, position):
        return int(position[0] // self.cell_size), int(position[1] // self.cell_size)

    def insert(self, entity):
        key = self.get_key(entity.position)
        if key not in self.buckets:
            self.buckets[key] = []
        self.buckets[key].append(entity)

    def query(self, position, query_range):
        nearby_entities = []
        start_key = self.get_key((position[0] - query_range, position[1] - query_range))
        end_key = self.get_key((position[0] + query_range, position[1] + query_range))
        for x in range(start_key[0], end_key[0] + 1):
            for y in range(start_key[1], end_key[1] + 1):
                key = (x, y)
                if key in self.buckets:
                    nearby_entities.extend(self.buckets[key])
        return nearby_entities

    def clear(self):
        self.buckets = {}
