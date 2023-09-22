import psycopg2 as ps

class database_handler:

    def __init__(self) -> None:
        self.connection = ps.connect(
            user = 'Bararide',
            password = 'Nikita0642',
            database = 'tamagotchi',
            host = '127.0.0.1'
        )

        self.connection.autocommit = True 

    def set_owner(self, user_id: str) -> None:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO tamagotchi.public.pets (pet_owner) values ('{user_id}');"
                )

            except Exception as e:
                print(f"Error {e}")

    def set_animal(self, animal: str, user_id: str) -> None:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"UPDATE tamagotchi.public.pets SET pet_animal = '{str(animal)}' WHERE pet_owner = '{user_id}';"
                )

            except Exception as e:
                print(f"Error {e}")

    def set_name(self, name: str, user_id: str) -> None:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"UPDATE tamagotchi.public.pets SET pet_name = '{str(name)}' where pet_owner = '{user_id}';"
                )

            except Exception as e:
                print(f"Error {e}")

    def set_health(self, health: str, user_id: str) -> None:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"UPDATE tamagotchi.public.pets SET pet_health = '{str(health)}' where pet_owner = '{user_id}';"
                )

            except Exception as e:
                print(f"Error {e}")

    def set_photo(self, photo_id: str, user_id: str):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"UPDATE tamagotchi.public.pets SET pet_photo = '{photo_id}' where pet_owner = '{user_id}';"
                )
            except Exception as e:
                print(e)

    def set_lotitude(self, lotitude: str, user_id: str):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"UPDATE tamagotchi.public.pets SET latitude = '{lotitude}' where pet_owner = '{user_id}';"
                )
            except Exception as e:
                print(e)

    def set_longitude(self, longitude: str, user_id: str):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"UPDATE tamagotchi.public.pets SET longitude = '{longitude}' where pet_owner = '{user_id}';"
                )
            except Exception as e:
                print(e)

    def get_animal(self, user_id: str) -> str:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"select pet_animal from tamagotchi.public.pets where pet_owner = '{user_id}';"
                )

                return str(cursor.fetchone()[0])

            except Exception as e:
                print(f"Error {e}")
                return None

    def get_name(self, user_id: str) -> str:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"select pet_name from tamagotchi.public.pets where pet_owner = '{user_id}';"
                )

                return str(cursor.fetchone()[0])

            except Exception as e:
                print(f"Error {e}")
                return None

    def get_health(self, user_id: str) -> str:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"select pet_health from tamagotchi.public.pets where pet_owner = '{user_id}';"
                )
                return str(cursor.fetchone()[0])

            except Exception as e:
                print(f"Error {e}")
                return None
            
    def get_photo(self, user_id: str) -> str:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"select pet_photo from tamagotchi.public.pets where pet_owner = '{user_id}';"
                )
                return str(cursor.fetchone()[0])

            except Exception as e:
                print(f"Error {e}")
                return None


    def check_id(self, text: str) -> bool:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"select pet_owner from tamagotchi.public.pets where pet_owner = '{text}';"
                )
                if(str(cursor.fetchone())) == "None":
                    return False
                else: 
                    return True
            except Exception as e:
                print(f"Error {e}")

    def check_photo(self, text: str) -> bool:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"select pet_photo from tamagotchi.public.pets where pet_owner = '{text}';"
                )
                if(str(cursor.fetchone()[0])) == "None":
                    return False
                else:
                    return True
            except Exception as e:
                print(f"Error {e}")

    def check_latitude(self, text: str) -> bool:
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"select latitude from tamagotchi.public.pets where pet_owner = '{text}';"
                )
                if(str(cursor.fetchone()[0])) == "None":
                    return False
                else:
                    return True
            except Exception as e:
                print(f"Error {e}")