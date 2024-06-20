import psycopg2

class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host="localhost", port="5432",
                                               database='clothingStoreDatabase', user='postgres', password='********')
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Помилка при з'єднанні з PostgreSQL", error)

    def get_col_names(self):
        return [d[0] for d in self.cursor.description]

    def create_db(self):
        f = open("create_db.txt", "r")

        self.cursor.execute(f.read())
        self.connection.commit()

    def get(self, tname, condition):
        try:
            query = f'SELECT * FROM {tname}'

            if condition:
                query += ' WHERE ' + condition

            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def insert(self, tname, columns, values):
        try:
            query = f'INSERT INTO {tname} ({columns}) VALUES ({values});'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def delete(self, tname, condition):
        try:
            query = f'DELETE FROM {tname} WHERE {condition};'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def update(self, tname, condition, statement):
        try:
            query = f'UPDATE {tname} SET {statement} WHERE {condition}'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def searchByersByCriteria(self, city, name, amount):
        query = f'''
                SELECT buyer_id, name, city, date AS order_date, order_id, product_id, amount 
                FROM order_item AS o_item
                JOIN  "order" AS o
                ON o.id = o_item.order_id
                JOIN buyer AS b
                ON b.id = o.buyer_id
                WHERE  amount > {amount} AND b.city LIKE '{city}%' AND b.name LIKE '{name}%';
                '''
        try:
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def searchOrdersByCriteria(self, city, name, postal_code):
        query = f'''
                SELECT name, email, city, postal_code, orders.id as order_id, date as order_date
                FROM buyer AS b
                JOIN "order" AS o
                ON b.id = o.buyer_id
                WHERE b.city LIKE '{city}%' AND b.name LIKE '{name}%' AND b.postal_code = '{postal_code}';
                '''
        try:
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def searchProductsByCriteria(self, price, amount, total_quantity):
        query = f'''
                SELECT DISTINCT product_id, name, price, amount, total_quantity 
                FROM order_item AS o_item
                JOIN product AS p
                ON o_item.product_id = p.id
                WHERE price > {price} AND amount > {amount} AND total_quantity > {total_quantity};
                '''
        try:
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def fillProductByRandomData(self):
        sql = """
        CREATE OR REPLACE FUNCTION randomProducts()
            RETURNS void AS $$
        DECLARE
            step integer  := 0;
        BEGIN
            LOOP EXIT WHEN step > 10;
                INSERT INTO product (name, description, price)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    substring(md5(random()::text), 1, 15),
                    (random() * (5000 - 1) + 1)::integer,
                    (random() * (7000 - 1) + 1)::integer
                );
                step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomProducts();
        """
        try:
            self.cursor.execute(sql)
        finally:
            self.connection.commit()
