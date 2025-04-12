from sql_utils import initialize_db, insert_dataframe_to_table, read_and_init_table
from models import *



if __name__ == "__main__":
    sql_file = "./sql/20250412_dhdb_create_sqlite.sql"  # your SQL file
    db_file = "./dhdb.sqlite"  # your output database file

    initialize_db(sql_file, db_file)

    category_file = "./data/food_category.csv"
    shop_file = "./data/shop.csv"
    user_file = "./data/user.csv"


    read_and_init_table(db_file, category_file, FoodCategory, "food_category")
    read_and_init_table(db_file, shop_file, Shop, "shop")
    read_and_init_table(db_file, user_file, User, "user")


