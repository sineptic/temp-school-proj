from flask import Flask, request

app = Flask(__name__)


class Box:
    name: str
    color: str

    def __init__(self, name, color) -> None:
        self.name = name
        self.color = color


boxes = [Box(name="3", color="blue"), Box(name="asdf", color="red")]


@app.route("/")
def index():
    global boxes
    return f"""
        <html>
            <body>
                <div>
                    {len(boxes)} boxes are created
                </div>
                <a href="/boxes"> Click me </a>
            </body>
        </html>
    """


def render_boxes(boxes):
    output = ""
    for box in boxes:
        output += f"""
        <div style="color: {box.color};">
        {box.name}
        </div>
        """
    return output


def generate_page(message: str, boxes: list[Box]):
    return f"""
    <html>
    <body>
        <div>
            {message}

            <div>
                Boxes:
                {render_boxes(boxes)}
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/boxes", methods=["post"])
def boxes_page():
    name = request.args.get("name")
    color = request.args.get("color")

    global boxes
    if not isinstance(name, str):
        return generate_page("you must provide name", boxes)
    if (
        color != "red"
        and color != "green"
        and color != "blue"
        and color != "yellow"
        and color != "magenta"
    ):
        return generate_page(
            f"color must be red, green, blue, yellow or magenta, but you provide '{color}'",
            boxes,
        )

    for box in boxes:
        if box.name == name or box.color == color:
            return generate_page(
                "name and color must be unique",
                boxes,
            )

    boxes.append(Box(name, color))
    return generate_page(
        "box created",
        boxes,
    )


@app.route("/boxes", methods=["get"])
def boxes_display_page():
    return ""


app.run(debug=True)
