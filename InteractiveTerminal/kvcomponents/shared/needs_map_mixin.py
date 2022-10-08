from ...models.map.maps import Map
from kivy.properties import ObjectProperty


class NeedsMap:
    the_map: Map = ObjectProperty(None, allownone=True)

    def adapt_to_map(self, *args):
        to_update = []
        if hasattr(self, "children"):
            for each_child in self.children:
                if isinstance(each_child, NeedsMap):
                    to_update.append(each_child)
        for each_attr in dir(self):
            possible_child = getattr(self, each_attr)
            if (
                isinstance(possible_child, NeedsMap)
                and possible_child not in to_update
            ):
                to_update.append(possible_child)

        for each_update in to_update:
            each_update.the_map = self.the_map

    def map_init(self):
        self.bind(the_map=self.adapt_to_map)
