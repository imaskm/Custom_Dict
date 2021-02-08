from dataclasses import dataclass
from typing import Any
import copy


@dataclass
class MyStructHash:
    key: Any
    value: Any


class CustomDict:

    def __init__(self):
        self.__initialize()

    def __initialize(self):
        self.size = 1000
        self.current_keys = 0
        self.empty_indices = self.size
        self.list = [None] * self.size

    def get_hash_code(self, key):
        code = hash(key) % self.size
        # print(key, code, self.size, hash(key))
        return code

    def __contains__(self, key):
        hash_index = self.get_hash_code(key)
        if self.list[hash_index] is not None:
            for struct_object in self.list[hash_index]:
                if struct_object.key == key:
                    return True

        return False

    def __insert(self, key, value):

        hash_index = self.get_hash_code(key)
        new_struct_obj = MyStructHash(key=key, value=value)
        if self.list[hash_index] is None:
            self.list[hash_index] = [new_struct_obj]
            # self.size += 1
            # self.list.append(None)
            self.current_keys += 1
            self.empty_indices -= 1
            if self.empty_indices == 0:
                pass
        else:
            for struct_object in self.list[hash_index]:
                if struct_object.key == new_struct_obj.key:
                    struct_object.value = new_struct_obj.value
                    return
            self.list[hash_index].append(new_struct_obj)
            self.current_keys += 1

    def __iter__(self):
        for hashing_objects in self.list:
            if hashing_objects is not None:
                for struct_objects in hashing_objects:
                    yield struct_objects.key

    def __len__(self):
        return self.current_keys

    def __getitem__(self, key):
        hash_index = self.get_hash_code(key)
        if self.list[hash_index] is not None:
            for struct_object in self.list[hash_index]:
                if struct_object.key == key:
                    return struct_object.value

        raise KeyError(key)

    def get(self, key, default=None):
        hash_index = self.get_hash_code(key)
        if self.list[hash_index] is not None:
            for struct_object in self.list[hash_index]:
                if struct_object.key == key:
                    return struct_object.value

        return default

    def __setitem__(self, key, value):
        self.__insert(key, value)

    def __eq__(self, other):

        if len(self) != len(other):
            return False
        for k, v in self.items():
            if k not in other or v != other[k]:
                return False

        return True

    def items(self):
        for hashing_objects in self.list:
            if hashing_objects is not None:
                for struct_objects in hashing_objects:
                    yield struct_objects.key, struct_objects.value

    def keys(self):
        for hashing_objects in self.list:
            if hashing_objects is not None:
                for struct_objects in hashing_objects:
                    yield struct_objects.key

    def values(self):
        for hashing_objects in self.list:
            if hashing_objects is not None:
                for struct_objects in hashing_objects:
                    yield struct_objects.value

    def __delitem__(self, key):

        hash_index = self.get_hash_code(key)
        if self.list[hash_index] is not None:
            for struct_object in self.list[hash_index]:
                if struct_object.key == key:
                    self.list[hash_index].remove(struct_object)
                    self.current_keys -= 1
                    self.empty_indices += 1
                    return

        raise KeyError(key)

    def pop(self, key, default=None):

        hash_index = self.get_hash_code(key)
        if self.list[hash_index] is not None:
            for struct_object in self.list[hash_index]:
                if struct_object.key == key:
                    self.list[hash_index].remove(struct_object)
                    self.current_keys -= 1
                    return struct_object.value
        if default:
            return default

        raise KeyError(key)

    def copy(self):
        return copy.copy(self)

    # def popitem(self, key):
    #
    #     hash_index = self.get_hash_code(key)
    #     if self.list[hash_index] is not None:
    #         for struct_object in self.list[hash_index]:
    #             if struct_object.key == key:
    #
    #                 self.list[hash_index].remove(struct_object)
    #                 self.current_keys -= 1
    #                 return struct_object.key,struct_object.value
    #
    #     raise KeyError(key)

    def clear(self):
        self.__initialize()

    def setdefault(self, key, default=None):

        hash_index = self.get_hash_code(key)
        if self.list[hash_index] is not None:
            for struct_object in self.list[hash_index]:
                if struct_object.key == key:
                    return struct_object.value
        self.__insert(key, default)
        return default

    def update(self, new_data):

        try:
            for key, value in new_data.items():
                self[k] = value
        except AttributeError:
            index = 0
            try:
                for key, value in new_data:
                    index += 1
                    self[key] = value
            except TypeError:
                raise TypeError(f"cannot convert dictionary update sequence element #{index} to a sequence")

    def __str__(self):
        result = "{"
        for k, v in self.items():
            result += str(k) + ": " + str(v) + ", "

        if result != "{":
            result = result[:-2]
        result += "}"
        return result




# Testing the custome dict
c = CustomDict()
c["key1"] = "value1"
c["key2"] = "value2"
c["key3"] = "value3"
c["key4"] = "value4"
c["key5"] = "value5"
c["key6"] = "value6"
# import pdb
# pdb.set_trace()
c["key2"] = "value12"

print(c.pop("key1"))

c.update(((1, 2), (5, 6)))

print(c.setdefault(21, "default value"))

print("dictionary")
for k, v in c.items():
    print(k, v)

print("----------------")
d = c.copy()
# d1 = CustomDict()
# d1[1] = 2

print(d==c)
