"""build SVG files


"""
import xmltodict

#: an empty svg file as a basis
SVG_FILE = """
<svg
   xmlns:ns="http://PURL.org/dc/elements/1.1/"
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" >
    <title>knittingpattern</title>
    <defs></defs>
</svg>
"""


class SVGBuilder(object):
    """This class builds an SVG to a file.

    The class itself does not know what the objects look like.
    It offers a more convinient interface to build SVG files.
    """

    def __init__(self):
        """Initialize this object without arguments."""
        self._structure = xmltodict.parse(SVG_FILE)
        self._layer_id_to_layer = {}
        self._svg = self._structure["svg"]

    @property
    def bounding_box(self):
        """the bounding box of this SVG
        ``(min_x, min_y, max_x, max_y)``

        .. code:: python

            svg_builder10x10.bounding_box = (0, 0, 10, 10)
            assert svg_builder10x10.bounding_box == (0, 0, 10, 10)

        ``viewBox``, ``width`` and ``height`` are computed from this.
        """
        return (self._min_x, self._min_y, self._max_x, self._max_y)

    @bounding_box.setter
    def bounding_box(self, bbox):
        min_x, min_y, max_x, max_y = bbox
        self._min_x = min_x
        self._min_y = min_y
        self._max_x = max_x
        self._max_y = max_y
        self._svg["@height"] = str(max_y - min_y)
        self._svg["@width"] = str(max_x - min_x)
        self._svg["@viewBox"] = "{} {} {} {}".format(min_x, min_y,
                                                     max_x, max_y)

    def place(self, x, y, svg, layer_id):
        """Place the :paramref:`svg` content at ``(x, y)`` position
        in the SVG, in a layer with the id :paramref:`layer_id`.

        :param float x: the x position of the svg
        :param float y: the y position of the svg
        :param str svg: the SVG to place at ``(x, y)``
        :param str layer_id: the id of the layer that this
          :paramref:`svg` should be placed inside

        """
        content = xmltodict.parse(svg)
        self.place_svg_dict(x, y, content, layer_id)

    def place_svg_dict(self, x, y, svg_dict, layer_id, group={}):
        """Same as :meth:`place` but with a dictionary as :paramref:`svg_dict`

        :param dict svg_dict: a dictionary returned by `xmltodict.parse()
          <https://github.com/martinblech/xmltodict>`__
        """
        group_ = {
                "@transform": "translate({},{})".format(x, y),
                "g": list(svg_dict.values())
            }
        group_.update(group)
        layer = self._get_layer(layer_id)
        layer["g"].append(group_)

    def _get_layer(self, layer_id):
        """
        :return: the layer with the :paramref:`layer_id`. If the layer
          does not exist, it is created.
        :param str layer_id: the id of the layer
        """
        if layer_id not in self._layer_id_to_layer:
            self._svg.setdefault("g", [])
            layer = {
                    "g": [],
                    "@inkscape:label": layer_id,
                    "@id": layer_id,
                    "@inkscape:groupmode": "layer",
                    "@class": "row"
                }
            self._layer_id_to_layer[layer_id] = layer
            self._svg["g"].append(layer)
        return self._layer_id_to_layer[layer_id]

    def write_to_file(self, file):
        """Writes the current SVG to the :paramref:`file`

        :param file: a file-like object
        """
        xmltodict.unparse(self._structure, file, pretty=True)


__all__ = ["SVGBuilder", "SVG_FILE"]
