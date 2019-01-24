from re import findall
import urllib.request
import os
from sqlite3 import *
from string import *

###########################################################
# Scrape information for database

# Open downloaded page for names and IDs in read mode
pokemon_page = 'PokePage.html'
scrape_file = open(pokemon_page, 'U').read()

# Find all pokemon names and delete excessive entries
pokemon_names = findall('<a class="ent-name".*>(.*)</a><br>', scrape_file)
del pokemon_names[151:]

# Find all pokemon ID numbers and delete excessive entries
pokemon_id = findall('<small>(#[0-9]*)</small><br><a class="ent-name', scrape_file)
del pokemon_id[151:]

# Open downloaded page 1 for images in read mode
images_page = 'Images.html'
images_scrape = open(images_page, 'U').read()

# Find all pokemon images on Page 1
pokemon_images = findall('imgboxart">\s*<img src="(.*\.[a-z]*)" />', images_scrape)

# Update images page, Open downloaded page 2 for images in read mode
images_page = 'Images_2.html'
images_scrape = open(images_page, 'U').read()

# Find and append pokemon images on Page 2
pokemon_images2 = findall('imgboxart">\s*<img src="(.*\.[a-z]*)" />', images_scrape)
for poke_sprite in pokemon_images2:
    pokemon_images.append(poke_sprite)

###########################################################
# Connect to Database and clear previous entries

# Make connection and Get cursor
connection = connect(database = 'pokemon_db.db')
poke_db = connection.cursor()

# Delete all entries when scraper is run
delete_query = "DELETE from pokemon"
poke_db.execute(delete_query)
connection.commit()

# Create function to insert into table
def insert_func(poke_num, poke_name):
    # Remove hash from pokemon ID numbers
    poke_num = poke_num[1:]
    # Remove weird punctuation from Pokemon names
    # Replace Nidoran female icon with (F)
    if poke_num == '029':
        poke_name = poke_name[:6] + ' (F)'
    # Replace Nidoran female icon with (M)
    if poke_num == '032':
        poke_name = poke_name[:6] + ' (M)'
    # Replace Farfetch'd quote mark with a space
    if poke_num == '083':
        poke_name = poke_name.replace("'", ' ')
    # Create and execute insert query with pokemon name and number
    insert_query = "INSERT INTO pokemon (Name, id_number, Sprite) " \
    + "values ('" + poke_name + "', " + poke_num + ")"
    poke_db.execute(insert_query)
    connection.commit()

# Call insert function for each Pokemon in list
for pokemon in range(151):
    insert_func(pokemon_id[pokemon], pokemon_names[pokemon])

# Close the database connection and cursor
poke_db.close()
connection.close()

# Section to download images to local source, only needs to run once
# os.chdir('/Users/coope/Documents/Python/Pokedex/sprites')
# for url_name in range(len(pokemon_images)):
#     urllib.request.urlretrieve(pokemon_images[url_name], str(url_name + 1) + '.png')