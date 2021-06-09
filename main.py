from gyazo import Api
from yaml import load
import os
import requests

def main(settings):
    if 'token' not in settings:
        print("configure client.yml with a token")
    elif not settings['token']:
        print("Need to specify token in ./client.yml")

    client = Api(access_token=settings['token'])
    for i in range(1, 10000):
        images = client.get_image_list(per_page=100, page=i)
        if len(images) == 0:
            break
        if not "images" in os.listdir("./"):
            os.mkdir("./images")

        for image in images:
            if not image.url:
                continue
            r = requests.get(image.url, stream=True)
            if r.status_code == 200:
                try:
                    with open("images/{}.png".format(image.image_id), "xb") as imgfile:
                        print("writing to file {}.png".format(image.image_id))
                        for chunk in r:
                            imgfile.write(chunk)
                except FileExistsError:
                    print("Skipping image_id {} as it already exists".format(image.image_id))
                    continue

if __name__ == '__main__':
    with open("./client.yml", "r") as f:
        settings = load(f)
    main(settings)
