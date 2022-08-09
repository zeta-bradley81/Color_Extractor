from flask import Flask, render_template, request, flash
import extcolors
import requests

app = Flask(__name__)
app.secret_key = "asdfjkl;"
LIMIT = 9
image_path = 'last_image'

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        try:
            with open('last_image', 'wb') as temp_file:
                img_file = request.files['uploaded_image']
                img_file.save(dst=temp_file)
                pn, ph = process()
                with open('last_palette.txt', 'w') as f:
                    f.write(str(ph))
                return render_template('index.html', colors=pn, length=len(pn), hex_values=ph)
        except:
            pn = 0
            ph = 0
            flash("There was an issue processing your file. Please try again with a different image.")
            return render_template('index.html', colors=0, length=0, hex_values=0)

    else:
        return render_template('index.html', colors=0)
    # return render_template('shop_index.html')


def process():
    rgb_colors, pixels = extcolors.extract_from_path(path=image_path, tolerance=20, limit=LIMIT)
    palette = []
    palette_names = []
    # Convert from RGB to Hex and adds color to the palette
    for x in range(len(rgb_colors)):
        this_color = ""
        for y in rgb_colors[x][0]:
            z = format(y, '02x')
            this_color += z
        palette.append(f'#{this_color}')
        color_name = requests.get(url=f'https://www.thecolorapi.com/id?hex={this_color}')
        color_name.raise_for_status()
        json_response = color_name.json()
        palette_names.append(json_response['name']['value'])
    return palette_names, palette

# if running from your own IDE, uncomment the flask development server
#
# if __name__ == '__main__':
#     app.run(debug=True)


# TODO think about resizing the images
# TODO think about exporting hex palette as a csv or txt