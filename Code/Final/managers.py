"""All MySQL requests needed by catalog"""
from database import cnx


class ProductManager:

    def __init__(self):
        self.list_categories = list()
        self.list_products_category = list()
        self.list_products = list()
        self.list_categories_product = list()
        self.set_classified_categories = set()
        self.list_enumerated_categories = list()
        self.list_description = list()

    def get_product_description(self, bar_code):
        """Find all information the customer needs about his new product"""
        cursor = cnx.cursor()
        query01 = """
            SELECT
                DISTINCT
                    product.name,
                    nutriscore.name,
                    product.description,
                    product.url
            FROM
                product
            INNER JOIN
                nutriscore
            ON
                product.nutriscore_id = nutriscore.id
            INNER JOIN
                product_category
            ON
                product.bar_code = product_category.product_bar_code
            INNER JOIN
                category
            ON
                product_category.category_id = category.id
            WHERE
                product.bar_code = %s
            """
        p = bar_code
        cursor.execute(query01, (p,))
        results = cursor.fetchall()
        cursor.close()
        self.list_description = []
        self.list_description = results
        return self.list_description

    def get_product_stores(self, bar_code):
        """Find the store where the product is referenced. We need the
        store id for saving the product."""
        cursor = cnx.cursor()
        query01 = """
            SELECT
                store.name, store.id
            From
                store
            INNER JOIN
                product_store
            ON
                store.id = product_store.store_id
            WHERE
                product_store.product_bar_code = %s
        """
        p = bar_code
        cursor.execute(query01, (p,))
        results = cursor.fetchall()
        cursor.close()
        # List with store name and store id
        self.list_stores_tuples = []
        # List with just store name
        self.list_stores = []
        self.list_stores_tuples = results
        # Put store name in self.list_store from self.list_stores_tuples
        for i, store in enumerate(self.list_stores_tuples):
            self.list_stores.append(self.list_stores_tuples[i][0])
        return self.list_stores
        pass

    def classify_categories(self):
        """Get all items from 'category' tables, add the tuple to the
        collection if its second element hasn't the first fourth caracters
        in common with tuple(s) allready in the collection. Finally put all
        those items in a list ordered and numbered."""
        cursor = cnx.cursor()
        cursor.execute(
            """
            SELECT
                *
            FROM
                category
            """
        )
        results = cursor.fetchall()
        cursor.close()
        self.list_categories = []
        self.list_enumerated_categories = []
        # Put the the query results in a list.
        for result in results:
            # category with the same fourth first caracters are not added
            item_in = [item
                       for item in self.list_categories
                       if result[1][:4] in item[1][:4]
                       ]
            if item_in != []:
                continue
            else:
                self.list_categories.append(result)
        # Extract the first word of the second element of the list of tuple
        # and put it in a set to avoid duplicates
        for i, element in enumerate(self.list_categories):
            self.set_classified_categories.add(
                (self.list_categories[i][1].split(" "))[0]
            )
        # Browse the collection in ordered way and put its items in a numerate
        # list
        for i, category in enumerate(
                sorted(self.set_classified_categories), start=1
        ):
            self.list_enumerated_categories.append((i, category))
        return self.list_enumerated_categories

    def get_subcategories_from_categories(self, category):
        """Get categories which names start like the sub-category name"""
        cursor = cnx.cursor()
        query01 = """
            SELECT
                *
            FROM
                category
            WHERE
                name LIKE CONCAT (%s, '%')
            """
        p = category
        cursor.execute(query01, (p,))
        results = cursor.fetchall()
        cursor.close()
        self.list_subcategories = []
        for i, result in enumerate(results, start=1):
            self.list_subcategories.append((i, result[1]))
        return self.list_subcategories

    def get_all_products(self):
        """Get all product by name"""
        cursor = cnx.cursor()
        cursor.execute(
            """
            SELECT
                name
            FROM
                product
            """
        )
        results = cursor.fetchall()
        cursor.close()
        self.list_products = []
        for i, result in enumerate(results, start=1):
            self.list_products.append((i, result))
        return self.list_products

    def get_products_category_like_by_bar_code(self, bar_code):
        """Find the products that have the most category in common
        with the initial product."""
        cursor = cnx.cursor()
        query03 = """
            SELECT
                product_bar_code,
                product.name,
                nutriscore.name,
                COUNT(category_id) AS nombre_categorie
            FROM
                product_category
            INNER JOIN
                product
            ON
                product_category.product_bar_code = product.bar_code
            INNER JOIN
                nutriscore
            ON
                product.nutriscore_id = nutriscore.id
            WHERE
                product_bar_code != %s
            AND
                category_id
            IN
                (
                SELECT
                    category_id
                FROM
                    product_category
                WHERE
                    product_bar_code = %s
                )
            AND
                nutriscore.name < (
                SELECT
                    nutriscore.name
                FROM
                    nutriscore
                INNER JOIN
                    product ON product.nutriscore_id = nutriscore.id
                WHERE product.bar_code = %s
                )
            GROUP BY
                product_bar_code
            ORDER BY
                nombre_categorie
            DESC LIMIT 6;
            """
        p = bar_code
        cursor.execute(query03, (p, p, p))
        results = cursor.fetchall()
        cursor.close()
        # cleaning the list
        self.list_prod_cat_bar = []
        # Filling the list with number, bar code, name, score and number
        # of category in common.
        for i, result in enumerate(results, start=1):
            self.list_prod_cat_bar.append(
                (i,
                 result[0],
                 result[1],
                 result[2],
                 result[3]
                 )
            )
        return self.list_prod_cat_bar

    def get_products_by_category(self, category):
        """Find all products in relation with a category"""
        cursor = cnx.cursor()
        query01 = """
            SELECT
                DISTINCT product.name,product.bar_code,nutriscore.name
            AS
                nutriscore
            FROM
                product
            INNER JOIN
                product_category
            ON
                product.bar_code = product_category.product_bar_code
            INNER JOIN
                category
            ON
                product_category.category_id = category.id
            INNER JOIN
                nutriscore
            ON
                product.nutriscore_id = nutriscore.id
            WHERE
                category.name LIKE CONCAT ('%', %s, '%')
            ORDER BY
                nutriscore.name;
            """
        p = category
        cursor.execute(query01, (p,))
        results = cursor.fetchall()
        cursor.close()
        # Cleaning the list
        self.list_products_category = []
        # Filling the list
        for i, result in enumerate(results, start=1):
            self.list_products_category.append(
                (i, (result[0], result[1], result[2]))
            )
        return self.list_products_category

    def record_product(self, old_product, new_product):
        """Recording the original product and his substitution"""
        cursor = cnx.cursor()
        cursor.execute(
            """
            INSERT INTO
                stored_product (original_bar_code, substitution_bar_code)
            VALUES (
                %(old_product)s,
                %(new_product)s
                )
            """,
            {
                "old_product": old_product,
                "new_product": new_product
            }
        )
        cnx.commit()
        print("Produit enregistré !")
        cursor.close()
        return

    def list_stored_product(self):
        """Create a list of tuples. Each tuple contain the original product
        and a list of one or more substitues."""
        # Step 1 : create a set of originals bar_code
        cursor = cnx.cursor()
        query01 = """
            SELECT original_bar_code
            FROM stored_product
        """
        cursor.execute(query01)
        results01 = cursor.fetchall()
        cursor.close()
        list_original_product = set()
        # The list we need.
        self.list_saved_product = []
        for result01 in results01:
            list_original_product.add(result01[0])
        # Step 2 : for each originals bar_code, find the substitutes
        for original_product in list_original_product:
            list_substitute_product = []
            self.get_product_description(original_product)
            info_product = self.list_description
            original_product_name = info_product[0][0]
            # Check if product description exsists
            if info_product[0][2] == '':
                original_product_description = "(sans description)"
            else:
                original_product_description = info_product[0][2]
            original_product_score = info_product[0][1]
            original_product_url = info_product[0][3]
            cursor = cnx.cursor()
            query03 = """
                SELECT substitution_bar_code
                FROM stored_product
                WHERE original_bar_code = %s
            """
            p = original_product
            cursor.execute(query03, (p,))
            results03 = cursor.fetchall()
            cursor.close()
            # find the substitutes for the current product
            for result03 in results03:
                self.get_product_description(result03[0])
                info_substitute = self.list_description
                substitute_product_name = info_substitute[0][0]
                if info_substitute[0][2] == '':
                    substitute_product_description = "(sans description)"
                else:
                    substitute_product_description = info_substitute[0][2]
                substitute_product_score = info_substitute[0][1]
                substitute_product_url = info_substitute[0][3]
                list_substitute_product.append(
                    (
                        substitute_product_name,
                        substitute_product_description,
                        substitute_product_score,
                        substitute_product_url
                    )
                )
            self.list_saved_product.append((
                (
                    original_product_name,
                    original_product_description,
                    original_product_score,
                    original_product_url
                ),
                list_substitute_product
            ))

        return self.list_saved_product


def main():
    """Instantiation and starting the program."""
    test_category = ProductManager()
    answer = input("Une catégorie ?")
    test_category.get_all_by_category(answer)


if __name__ == "__main__":
    main()
