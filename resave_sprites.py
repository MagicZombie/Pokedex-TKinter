from PIL import Image

# Resave png images as gifs for TKINTER
for pokemon in range(152):
    sprite = Image.open('sprites/' + str(pokemon) + '.png')
    sprite = sprite.resize((250, 230))
    # Create a new background layer that is pure white
    bg = Image.new("RGB", (250,230), color=(255, 255, 255))
    # Past the first sprite on top of the new bg to replace transparency
    bg.paste(sprite, sprite)
    # Resave new image as gif
    bg.save('sprites/gifs/' + str(pokemon) + '.gif')