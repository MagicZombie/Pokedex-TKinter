from selenium import webdriver
from re import findall
from urllib.request import urlopen, urlretrieve, Request
import time

# Currently struggling with 403 forbidden errors!!!
# Also add a 'sleep' or 'wait' command at end of loop
# to prevent the program moving faster than the network
# connection

# Use Selenium to connect to Bulbapedia through Chrome
browser = webdriver.Chrome()
browser.get('https://www.pokemon.com/us/pokedex/bulbasaur')

# 
header = {'User-Agent': 'Mozilla/5.0'}

# Empty lists to hold data
pokemon_entry = []

# Iterate over pokemon in range
for pokemon in range(150):
    # Find current url for pokemon
    current_url = browser.current_url
    # Use header in request
    req = Request(current_url, headers=header)
    # Open page for reading in python
    pokemon_open = urlopen(req)
    decoded_pokemon = pokemon_open.read().decode('UTF-8')
    # Set wait time to ensure page has loaded in
    time.sleep(7)
    # Find pokemons name with regex
    current_pokemon = findall('og:description" content="([a-zA-Z\s\S.]*\.)" />', decoded_pokemon)
    # Add pokemon name to list
    pokemon_entry.append(current_pokemon[0])
    # Close link to web page
    pokemon_open.close()
    # Find button to move to next page and click it
    button = browser.find_element_by_class_name('next')
    button.click()
    print(pokemon_entry)

# Close connection to chrome browser
browser.quit()

