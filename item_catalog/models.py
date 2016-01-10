from item_catalog import db


# ---- Class Definitions ----#
# Shelter class
class Item(db.Model):
    # Table Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
