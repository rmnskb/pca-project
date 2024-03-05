# TODO: create a script which will update the DB once per business day after market closure
import pca_dax.db as db
#
# with db.create_connection() as conn:
#     new_column = 'stock_index'
#     predefined_value = 'DAX'
#     cursor = conn.cursor()
#
#     alter_query = f"""ALTER TABLE companies ADD COLUMN {new_column} VARCHAR"""
#     cursor.execute(alter_query)
#
#     update_query = f"""UPDATE companies SET {new_column} = '{predefined_value}'"""
#     cursor.execute(update_query)
#
#     conn.commit()

# db.populate_info(index='STOXX')
