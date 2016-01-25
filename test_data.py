from item_catalog import db
from item_catalog.models import Item, Category

# Test Categories
category_tools = Category("Tools")
category_toys = Category("Toys")
category_electronics = Category("Electronics")

# Add Categories to session
db.session.add(category_tools)
db.session.add(category_toys)
db.session.add(category_electronics)

# Test Items
items = []
items.append(Item('Screwdriver', 'A screwdriver screws things', category_tools))
items.append(Item('Wrench', 'A wrench wrenches things', category_tools))
items.append(Item('Saw', 'A saw saws things', category_tools))
items.append(Item('Legos', 'Best toy ever', category_toys))
items.append(Item('Micro Machines', 'Small toys that are good for accidently stepping on.', category_toys))
items.append(Item('Hotwheels', 'Vroom Vroom', category_toys))
items.append(Item('Television',
                  'A television, commonly referred to as TV, telly or the tube, also called idiot box, is a telecommunication medium used for transmitting sound with moving images in monochrome (black-and-white), or in colour, and in two or three dimensions. It can refer to a television set, a television program, or the medium of television transmission. Television is a mass medium, for entertainment, education, news and advertising.',
                  category_electronics))
items.append(Item('VCR', 'I remember when these were cool', category_electronics))

# Add items to session
for item in items:
    db.session.add(item)

# Commit test data
db.session.commit()
