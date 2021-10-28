import os
import geopandas as gpd
import matplotlib.pyplot as plt
import imageio

covid_data_path = './covid_data_brazil'

# Read images and generate final .gif
def to_gif():
    images = []
    image_path = './images'
    file_names = [f'{c}.png' for c in range(1, len(os.listdir(image_path))+1)]

    for i in file_names:
        images.append(imageio.imread(os.path.join(image_path, i)))
        
    imageio.mimsave('./map.gif', images, duration=0.1)

# Iterate over data and read it
def read_data():
    list = os.listdir(covid_data_path)

    list_shp = []
    for i in list:
        if '.shp' in i:
            if '.xml' in i:
                pass
            else:
                list_shp.append(i)
    return list_shp

def generate_images():
    list_shp = read_data()

    brasil = gpd.read_file('./brazil/UFEBRASIL.shp')
    brasil.head()

    # Base Image
    brasil.plot(figsize=(15,10), edgecolor='white', linewidth=0.5, color='#CCCCCC')
    base = brasil.plot(figsize=(15,10), edgecolor='white', linewidth=0.5, color='#CCCCCC')

    # Create a new image from each day of the processed list
    for key, values in enumerate(list_shp):
        covid = gpd.read_file(os.path.join(covid_data_path, values))
        covid.crs = brasil.crs
        
        base = brasil.plot(color='#CCCCCC', edgecolor='white', linewidth=0.5, figsize=(15,10))
        ax = covid.plot(ax=base, color='red', markersize=13)
        ax.axis('off')

        ax.set_title(f'Brazil Covid-19 Propagation COVID-19 (2020)\n Day {values[6:8]}-{values[9:-4]}', \
                    fontdict={'fontsize':'30', 'fontweight':'40'})
        base.set_axis_off()
        plt.savefig(f'./images/{key+1}.png')
        plt.close()
    to_gif() 

generate_images()


