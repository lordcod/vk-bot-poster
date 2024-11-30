with open('images/1.png', 'rb') as f:
    data = f.read()


for i in range(1, 151):
    with open(f'images/{i}.png', 'wb+') as f:
        f.write(data)
