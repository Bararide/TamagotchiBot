import psycopg2 as ps

from pet_container import Pet

class database_handler:

    def __init__(self) -> None:
        self.connection = ps.connect(
            user = 'Bararide',
            password = 'Nikita0642',
            database = 'tamagotchi',
            host = '127.0.0.1'
        )

        self.connection.autocommit = True 

    def include_coordinate(self, pet: Pet) -> None:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"UPDATE tamagotchi.public.pets SET latitude = '{pet.latitude}', longitude = '{pet.longitude}' where pet_owner = '{pet.owner}';"
                )
            except Exception as e:
                print(e)

    def create(self, pet: Pet) -> None:
        with self.connection.cursor() as cursor:
            try:
                pet.latitude = None
                pet.longitude = None
                cursor.execute(
                    f"insert into tamagotchi.public.users(user_name) values('{pet.owner}')"
                )

                cursor.execute(
                    f"insert into tamagotchi.public.pets(pet_owner, pet_animal, pet_name, pet_health) values('{pet.owner}', '{pet.animal}', '{pet.pet_name}', '{pet.health}')"
                )

                cursor.execute(
                    "select * from tamagotchi.public.users"
                )
                users = cursor.fetchall()
                for user in users:
                    print(user)

            except Exception as e:
                print(f"Error {e}")

    def create_pet(self, pet: Pet, userid: str) -> Pet:
        with self.connection.cursor() as cursor:           
            try:
                cursor.execute(
                    f"select * from tamagotchi.public.pets where pet_owner = '{userid}'"
                )
                result = cursor.fetchone()
                pet.owner = result[0]
                pet.animal = result[1]
                pet.pet_name = result[2]
                pet.health = result[3]
                pet.latitude = result[4]
                pet.longitude= result[5]
            except Exception as e:
                print(f"Error {e}")

    def check(self, text: str) -> bool:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"select user_name from tamagotchi.public.users where user_name = '{text}';"
                )
                if(str(cursor.fetchone())) == "None":
                    print(cursor.fetchone())
                    return True
                else: 
                    print(cursor.fetchone())
                    return False
            except Exception as e:
                print(f"Error {e}")