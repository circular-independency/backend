from db.sql_utils import initialize_db, read_and_init_table
from db.models import *
import os


if __name__ == "__main__":
    sql_file = "./db//sql/20250412_dhdb_create_sqlite.sql"  # your SQL file
    db_file = "./db//dhdb.sqlite"  # your output database file

    if os.path.exists(db_file):
        os.remove(db_file)

    initialize_db(sql_file, db_file)

    category_file = "./db/data/food_category.csv"
    shop_file = "./db/data/shop.csv"
    user_file = "./db/data/user.csv"


    read_and_init_table(db_file, category_file, FoodCategory, "food_category")
    read_and_init_table(db_file, shop_file, Shop, "shop")
    read_and_init_table(db_file, user_file, User, "user")


