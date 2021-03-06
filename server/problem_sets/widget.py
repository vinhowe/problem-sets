#  Copyright (c) 2019 Thomas Howe

from abc import ABC, abstractmethod

from problem_sets.serialization import Serializable


class WidgetOptions(Serializable, ABC):
    """
    Abstract widget options, to be extended by the options for each specific widget
    """

    def __init__(self, w_type: str):
        self.w_type = w_type
        super().__init__()

    @abstractmethod
    def serialize(self):
        return {"type": self.w_type}

    @classmethod
    def deserialize(cls, serialized: dict):
        pass


class Widget(Serializable):
    def __init__(self, options: WidgetOptions):
        self.options = options

    def serialize(self) -> object:
        return {"options": self.options.serialize()}

    @classmethod
    def deserialize(cls, serialized: dict):
        pass


class TextWidgetOptions(WidgetOptions):
    def __init__(self, text: str):
        super().__init__("text")

        self.text = text

    def serialize(self):
        return {**(super().serialize()), "text": self.text}

    @classmethod
    def deserialize(cls, serialized: dict):
        pass


class ImageWidgetOptions(WidgetOptions):
    def __init__(self, id: str):
        super().__init__("image")

        self.id = id

    def serialize(self):
        return {**(super().serialize()), "id": self.id}

    @classmethod
    def deserialize(cls, serialized: dict):
        pass


"""
DEPRECATED. For reference only.
"""


def build_text_widget_options(text: str) -> TextWidgetOptions:
    """ DEPRECATED"""
    return TextWidgetOptions(text)


def build_graph_widget_demo(options: dict):
    return {
        "type": "graph",
        "options": {
            "functions": [
                {"expression": "2x", "min": -2, "max": 2, "step": 0.05},
                {"expression": "5x", "min": -2, "max": 2, "step": 0.5},
            ],
            "tables": [
                {"xValues": [0, 1, 2, 3, 4, 5], "yValues": [0, 1, 2.5, 4, 7, 18]}
            ],
        },
    }


def build_table_widget_demo():
    return {
        "type": "table",
        "options": {
            "xValues": [0, 1, 2, 3, 4, 5],
            "yValues": [0, 1, 2.5, 4, 7, 18],
            "xLabel": "x",
            "yLabel": "y",
            "labelsLabel": "candidate",
            "labels": ["A", "B", "C", "D", "E", "F"],
        },
    }
