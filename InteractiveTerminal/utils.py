from dataclasses import dataclass, field
import typing as T

def use_passed_or_default(passed, **defaults):
    new_kwargs = {}
    new_kwargs.update(defaults)
    new_kwargs.update(passed)
    return new_kwargs



ItemType = T.TypeVar("ItemType")

@dataclass(frozen=True)
class CircularList(T.Generic[ItemType]):
    """
    Easy circular list implementation that lets you create
    an object for next / previous.

    Underlying list is shared between all instances.
    """
    items: T.List[ItemType] = field(default_factory=list)
    index: int = 0

    def next(self) -> "CircularList[ItemType]":
        return self.seek(1)
    
    def prev(self) -> "CircularList[ItemType]":
        return self.seek(-1)
    
    def get(self) -> T.Optional[ItemType]:
        return self[0]

    def seek(self, rel_idx: int) -> "CircularList[ItemType]":
        if len(self.items) == 0:
            return CircularList(items=self.items, index=0)
        else:
            return CircularList(items=self.items, index=(self.index + rel_idx) % len(self.items))

    def __getitem__(self, index: int) -> T.Optional[ItemType]:
        if len(self.items) == 0:
            return None
        else:
            return self.items[(self.index + index) % len(self.items)]
    
    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> T.Generator[ItemType, None, None]:
        for i in range(len(self)):
            yield self[i]

    def find(self, condition: T.Callable[[ItemType], bool]) -> T.Optional[ItemType]:
        for i in self:
            if condition(i):
                return i
    
        return None

    
    def find_index(self, condition: T.Callable[[ItemType], bool]) -> T.Optional[int]:
        for i in range(len(self)):
            if condition(self[i]):
                return i
    
        return None

    def append(self, item: ItemType) -> int:
        """
        Append to the underlying store. Return the relative index
        """
        self.items.append(item)
        return (len(self.items) - 1) - self.index
    
    def pop(self) -> "CircularList[ItemType]":
        """
        Pop at my current location. Return a new circular
        list pointing to the previous element
        """
        if len(self.items) == 0:
            return self
        else:
            self.items.pop(self.index)
            return self.prev()


