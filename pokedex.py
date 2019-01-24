from tkinter import *
from sqlite3 import *
from tkinter import ttk

# Create window
pokedex_window = Tk()

# Name Window
pokedex_window.title('Kanto Pokedex')

# Size window
pokedex_window.geometry('640x400')

# Change background color
pokedex_window.config(bg='red', borderwidth=5,
                    relief='raised')

###########################################################
# Connect to Database

try:
    connection = connect(database = 'pokemon_db.db')
    pokemon_data = connection.cursor()
except OperationalError:
    print('Error: DataBase not found.')

###########################################################
# Functions

# Define Dropdown Search function
def search_dropdown():
    option_selected = poke_dropdown_variable.get()
    if option_selected != 'Select':
        name_query = "SELECT id_number, Name FROM pokemon " \
        + "WHERE name='" + option_selected + "'"
        pokemon_data.execute(name_query)
        data_returned = pokemon_data.fetchall()
        for item in data_returned:
            display_num = str(item[0])
            display_name = str(item[1])
            poke_name['text'] = '#' + display_num + ': ' \
            + display_name
            current_sprite['file'] = sprites[item[0]]
    else:
        poke_name['text'] = '\u2596\u258AMISSING\u258FNO\u259E'
        current_sprite['file'] = sprites[0]

#Create function to select from table
def search(poke_name='null', id=0):
    if poke_name != 'null':
        poke_name = poke_name.capitalize()
        poke_select = "SELECT id_number, name FROM pokemon WHERE" \
        + " name='" + poke_name + "'"
        pokemon_data.execute(poke_select)
        data_returned = pokemon_data.fetchall()
        for item in data_returned:
            print(item[0])
            display_num = str(item[0])
            display_name = str(item[1])
            poke_name['text'] = '#' + display_num + ': ' \
            + display_name
            current_sprite['file'] = sprites[item[0]]
    elif id != 0:
        poke_select = "SELECT id_number, name FROM pokemon WHERE" \
        + " id_number=" + str(id) 
        pokemon_data.execute(poke_select)
        data_returned = pokemon_data.fetchall()
        for item in data_returned:
            print(item[1])
            display_num = str(item[0])
            display_name = str(item[1])
            poke_name['text'] = '#' + display_num + ': ' \
            + display_name
            current_sprite['file'] = sprites[item[0]]

# Define name search function
def search_name():
    option_selected = text_search_var.get()
    search(poke_name=option_selected)

# Define number search function
def search_num():
    option_selected = num_var.get()
    search(id=int(option_selected))

###########################################################
# LEFT SIDE GUI

# Create and place label group
left_gui = LabelFrame(pokedex_window, relief='flat', bg='red')
left_gui.grid(column=0, row=0)

# Create grey border for image display
display_border = LabelFrame(left_gui, relief='groove', bg='grey')
display_border.grid(column=0, row=0, rowspan=3, padx=5, pady=5)

# Create list of sprites to display
sprites = []
for sprite in range(152):
    sprites.append('sprites/gifs/' + str(sprite) + '.gif')
sprites.append('sprites/gifs/Select.gif')

# Create and place image display
current_sprite = PhotoImage(file=sprites[152])
sprite_display = Label(display_border, image = current_sprite,
                            borderwidth=3, relief='groove')
sprite_display.grid(column=0, row=0, padx=7 ,pady=7,
                    rowspan=2)

###########################################################
# MIDDLE DIVIDER GUI

# Create and place 'hinge' square
hinge = Label(pokedex_window, text='', bg='red',
                width=10, height=25, relief='raised',
                borderwidth=4)
hinge.grid(column=1, row=0, rowspan=3)

###########################################################
# RIGHT SIDE GUI

# Create and place label group
right_gui = LabelFrame(pokedex_window, relief='flat', bg='red')
right_gui.grid(column=2, row=0)

# Create and place text display window for pokemon names
poke_name = Label(right_gui, text='', bg='light green', 
                    fg='dark green', width=20, height=3,
                    font='system 15 bold', borderwidth=3,
                    relief='groove')
poke_name.grid(column=2, row=0, padx=10, pady=10, 
                    columnspan=2)

# Create and place label group for fake buttons
fake_buttons_group = LabelFrame(right_gui, relief='flat', bg='red')
fake_buttons_group.grid(column=2, row=1, columnspan=2)

# Create and place fake buttons
for square in range(5):
    fake_button = Label(fake_buttons_group, relief='raised',
                        bg='slate blue', width=5, height=2)
    fake_button.grid(column=square, row=0)

# Create and place dropdown for pokemon names
# Get list of pokemon names from database
poke_list = ['Select']
select_query = "SELECT Name FROM pokemon"
pokemon_data.execute(select_query)
database_call = pokemon_data.fetchall()
for item in database_call:
    poke_list.append(item)

# Create dropdown/combo box widget
poke_dropdown_variable = StringVar(right_gui)
poke_dropdown_variable.set(poke_list[0])
poke_dropdown = ttk.Combobox(right_gui, textvariable=poke_dropdown_variable,
                values=poke_list, state='readonly')
# poke_dropdown.config(width=17, wraplength=150, anchor='w')
poke_dropdown.grid(column=2, row=2, padx=5, pady=5)

# Create and place dropdown search button
dropdown_search = Button(right_gui, text='Search',
                            command=search_dropdown)
dropdown_search.grid(column=3, row=2, padx=5, pady=5)

# Create and place text entry name box 
text_search_var = StringVar()
text_search = Entry(right_gui, textvariable=text_search_var,
                    width=24)
text_search.grid(column=2, row=3, padx=2, pady=2)
text_search_var.set('')

# Create and place name search button
name_search = Button(right_gui, text='Search',
                            command=search_name)
name_search.grid(column=3, row=3, padx=2, pady=2)

# Create and place text entry number box
num_var = StringVar()
num = Entry(right_gui, textvariable=num_var,
                    width=24)
num.grid(column=2, row=4, padx=5, pady=5)
num_var.set('')

# Create and place number search button
number_search = Button(right_gui, text='Search',
                            command=search_num)
number_search.grid(column=3, row=4, padx=2, pady=2)

#Start event loop
pokedex_window.mainloop()

# Close database connection and cursor
pokemon_data.close()
connection.close()