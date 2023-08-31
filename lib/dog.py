import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    pass
    
      all = []  # A list to hold all instances of Dog.

    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        # SQL query to create a table for dogs if it doesn't exist.
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        # SQL query to drop the dogs table if it exists.
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)

    def save(self):
        if self.id is None:
            # SQL query to insert a new dog into the database.
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            # Get the ID of the last inserted row and assign it to the instance.
            self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        return self

    @classmethod
    def create(cls, name, breed):
        # Create a new dog instance, save it to the database, and return it.
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        if row is None:
            return None
        # Create a new dog instance from a database row and return it.
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        # SQL query to retrieve all dogs from the database.
        sql = """
            SELECT *
            FROM dogs
        """
        all_dogs = CURSOR.execute(sql).fetchall()

        # Create Dog instances from each database row and store in the 'all' list.
        cls.all = [cls.new_from_db(row) for row in all_dogs]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        # SQL query to find a dog by its name.
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()

        # Create a Dog instance from the found row and return it.
        return cls.new_from_db(dog)

    @classmethod
    def find_by_id(cls, id):
        # SQL query to find a dog by its ID.
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)

    @classmethod
    def find_or_create_by(cls, name, breed):
        # SQL query to find a dog by its name and breed.
        sql = """
            SELECT * FROM dogs
            WHERE name = ? AND breed = ?
        """
        result = CURSOR.execute(sql, (name, breed)).fetchone()
        if result:  # A dog with that name and breed is already in the database.
            return cls.new_from_db(result)
        else:  # This dog is not yet in the database, so create and return it.
            new_dog = cls.create(name, breed)
            return new_dog

    def update(self):
        if self.id is not None:
            # SQL query to update a dog's name and breed using its ID.
            sql = """
                UPDATE dogs
                SET name = ?, breed = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            # Commit the changes to the database.
            CONN.commit()