from libpyvinyl.BaseData import BaseData
from libpyvinyl.BaseFormat import BaseFormat
import inspect
import numpy

import h5py
import numpy as np


from libpyvinyl.BaseData import DataCollection
import Shadow

class Shadow3Data(BaseData):
    def __init__(self,
                 key,
                 data_dict=None,
                 filename=None,
                 file_format_class=None,
                 file_format_kwargs=None):

        #  There are only two sections need to consider by the simulation package developers:

        # A dictionary whose keys are the expected keys of the dictionary returned by get_data(), we just simply would like to get a “number” from a NumberData
        expected_data = {}
        ### DataClass developer's job start
        # expected_data["number"] = None
        expected_data["DUMMY"] = None

        ### DataClass developer's job end

        super().__init__(key,
                         expected_data,
                         data_dict,
                         filename,
                         file_format_class,
                         file_format_kwargs)

    @classmethod
    def supported_formats(self):
        format_dict = {}
        ### DataClass developer's job start
        self._add_ioformat(format_dict, Shadow3GfileFormat)
        ### DataClass developer's job end
        return format_dict


class Shadow3GfileFormat(BaseFormat):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def format_register(self):
        key = "Gfile"
        desciption = "Gfile format for Shadow3Data"
        file_extension = ".dat"
        read_kwargs = [""]
        write_kwargs = [""]
        return self._create_format_register(
            key, desciption, file_extension, read_kwargs, write_kwargs
        )

    @classmethod
    def read(cls, filename: str) -> dict:
        """Read the data from the file with the `filename` to a dictionary. The dictionary will
        be used by its corresponding data class."""
        flag = cls.shadow3_file_type(filename)
        if flag == 0:
            oe0 = Shadow.Source()
            oe0.load(filename)
            return oe0.to_dictionary()
        elif flag == 1:
            oe1 = Shadow.OE()
            oe1.load(filename)
            return oe1.to_dictionary()
        else:
            raise Exception("Error loading file %s (flag=%d)" % (filename, flag) )

    @classmethod
    def write(cls, object: Shadow3Data, filename: str, key: str = None):


        dict1 = object.get_data()
        keys = dict1.keys()
        if 'F_WIGGLER' in keys:
            shadow_object = Shadow.Source()
            print(">>>>>>>>>>>> source")
        elif 'F_GRATING' in keys:
            shadow_object = Shadow.OE()
            print(">>>>>>>>>>>> oe")
        else:
            raise Exception("Mismatch data")

        i_list = cls.__get_valiable_list(shadow_object)

        for name in i_list:
            try:
                value = dict1[name]
                if isinstance(value, str):
                    value = bytes(value, 'UTF-8')
                elif isinstance(value, numpy.ndarray):
                    for list_item in value:
                        if isinstance(list_item, str):
                            list_item = bytes(list_item, 'UTF-8')
                setattr(shadow_object, name, value)
            except:
                raise Exception("Error setting parameters name %s" % name)

        shadow_object.write(filename)

        if key is None:
            original_key = object.key
            key = original_key + "_to_Shadow3GfileFormat"
            return object.from_file(filename, cls, key)
        else:
            return object.from_file(filename, cls, key)

        # """Save the data with the `filename`."""
        # data_dict = object.get_data()
        # number = data_dict["number"]
        # with h5py.File(filename, "w") as h5:
        #     h5["number"] = number
        # if key is None:
        #     original_key = object.key
        #     key = original_key + "_to_H5Format"
        #     return object.from_file(filename, cls, key)
        # else:
        #     return object.from_file(filename, cls, key)

    @staticmethod
    def direct_convert_formats():
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return []

    @staticmethod
    def shadow3_file_type(filename):
        with open(filename) as f:
            if 'F_WIGGLER' in f.read():
                return 0
        with open(filename) as f:
            if 'F_GRATING' in f.read():
                return 1
        return -1

    @staticmethod
    def __get_valiable_list(object1):
        """
        returns a list of the Shadow.Source or Shadow.OE variables
        """
        mem = inspect.getmembers(object1)
        mylist = []
        for i,var in enumerate(mem):
            if var[0].isupper():
                mylist.append(var[0])
        return(mylist)


# class TXTFormat(BaseFormat):
#     def __init__(self) -> None:
#         super().__init__()
#
#     @classmethod
#     def format_register(self):
#         key = "TXT"
#         desciption = "TXT format for NumberData"
#         file_extension = ".txt"
#         read_kwargs = [""]
#         write_kwargs = [""]
#         return self._create_format_register(
#             key, desciption, file_extension, read_kwargs, write_kwargs
#         )
#
#     @classmethod
#     def read(cls, filename: str) -> dict:
#         """Read the data from the file with the `filename` to a dictionary. The dictionary will
#         be used by its corresponding data class."""
#         number = float(np.loadtxt(filename))
#         data_dict = {"number": number}
#         return data_dict
#
#     @classmethod
#     def write(cls, object: Shadow3Data, filename: str, key: str = None):
#         """Save the data with the `filename`."""
#         data_dict = object.get_data()
#         arr = np.array([data_dict["number"]])
#         np.savetxt(filename, arr, fmt="%.3f")
#         if key is None:
#             original_key = object.key
#             key = original_key + "_to_TXTFormat"
#             return object.from_file(filename, cls, key)
#         else:
#             return object.from_file(filename, cls, key)
#
#     @staticmethod
#     def direct_convert_formats():
#         # Assume the format can be converted directly to the formats supported by these classes:
#         # AFormat, BFormat
#         # Redefine this `direct_convert_formats` for a concrete format class
#         return [H5Format]
#
#     @classmethod
#     def convert(
#         cls, obj: Shadow3Data, output: str, output_format_class: str, key=None, **kwargs
#     ):
#         """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
#         if output_format_class is H5Format:
#             cls.convert_to_H5Format(obj.filename, output)
#         else:
#             raise TypeError(
#                 "Direct converting to format {} is not supported".format(
#                     output_format_class
#                 )
#             )
#         # Set the key of the returned object
#         if key is None:
#             original_key = obj.key
#             key = original_key + "_from_TXTFormat"
#             return obj.from_file(output, output_format_class, key)
#         else:
#             return obj.from_file(output, output_format_class, key)
#
#     @classmethod
#     def convert_to_H5Format(cls, input: str, output: str):
#         """The engine of convert method."""
#         print("Directly converting TXTFormat to H5Format")
#         number = float(np.loadtxt(input))
#         with h5py.File(output, "w") as h5:
#             h5["number"] = number
#
#
# class H5Format(BaseFormat):
#     def __init__(self) -> None:
#         super().__init__()
#
#     @classmethod
#     def format_register(self):
#         key = "H5"
#         desciption = "H5 format for NumberData"
#         file_extension = ".h5"
#         read_kwargs = [""]
#         write_kwargs = [""]
#         return self._create_format_register(
#             key, desciption, file_extension, read_kwargs, write_kwargs
#         )
#
#     @classmethod
#     def read(cls, filename: str) -> dict:
#         """Read the data from the file with the `filename` to a dictionary. The dictionary will
#         be used by its corresponding data class."""
#         with h5py.File(filename, "r") as h5:
#             number = h5["number"][()]
#         data_dict = {"number": number}
#         return data_dict
#
#     @classmethod
#     def write(cls, object: Shadow3Data, filename: str, key: str = None):
#         """Save the data with the `filename`."""
#         data_dict = object.get_data()
#         number = data_dict["number"]
#         with h5py.File(filename, "w") as h5:
#             h5["number"] = number
#         if key is None:
#             original_key = object.key
#             key = original_key + "_to_H5Format"
#             return object.from_file(filename, cls, key)
#         else:
#             return object.from_file(filename, cls, key)
#
#     @staticmethod
#     def direct_convert_formats():
#         # Assume the format can be converted directly to the formats supported by these classes:
#         # AFormat, BFormat
#         # Redefine this `direct_convert_formats` for a concrete format class
#         return []

if __name__ == "__main__":


    # Test if the definition works
    data = Shadow3Data(key="test")
    print(data.key)
    print(data.expected_data)

    #
    # # see: libpyvinyl/tests/unit/test_BaseData.py
    #
    # test_data = Shadow3Data(key="test_data")
    # my_dict = {"number": 4}
    # test_data.set_dict(my_dict)
    # print(test_data.get_data())
    # assert test_data.get_data()["number"] == 4
    #
    #
    # # """Test creating a DataCollection instance with two datasets"""

    #
    # test_data1 = Shadow3Data(key="test_data1")
    # test_data2 = Shadow3Data(key="test_data2")
    #
    # test_data1.set_dict({"number": 5})
    # test_data2.set_dict({"number": 10})
    #
    # collection = DataCollection(test_data1, test_data2)
    # assert collection["test_data1"].get_data()["number"] == 5
    # assert collection["test_data2"].get_data()["number"] == 10
    #
    # value_collection = collection.get_data()
    # assert value_collection["test_data1"]["number"] == 5
    # assert value_collection["test_data2"]["number"] == 10

    # Shadow data


    oe0 = Shadow.Source()
    oe0_dict = oe0.to_dictionary()

    shadow_data0 = Shadow3Data(key="oe0")
    shadow_data0.set_dict(oe0_dict)
    # print(shadow_data0.get_data())

    oe1 = Shadow.OE()
    oe1_dict = oe1.to_dictionary()
    # print(oe0_dict)

    shadow_data1 = Shadow3Data(key="oe1")
    shadow_data1.set_dict(oe1_dict)
    # print(shadow_data.get_data())

    print(shadow_data0.get_data())
    print(shadow_data1.get_data())

    shadow_beamline = DataCollection(shadow_data0, shadow_data1)
    print(shadow_beamline["oe0"].get_data())
    print(shadow_beamline["oe1"].get_data())

    print(len(shadow_beamline))
    print(shadow_beamline.to_list())

    # file i/o
    Shadow3Data.list_formats()
    oe0 = Shadow.Source()
    oe0.write("tmp0.dat")
    test_data = Shadow3Data(key="test_data")
    test_data.set_file("tmp0.dat", Shadow3GfileFormat)
    # print(test_data.get_data())

    oe1 = Shadow.OE()
    oe1.write("tmp1.dat")
    test_data = Shadow3Data(key="test_data")
    test_data.set_file("tmp1.dat", Shadow3GfileFormat)
    test_data.write('tmp11.dat', Shadow3GfileFormat)
    tmp = Shadow.OE()
    tmp.load('tmp11.dat')
    # print(test_data.get_data())

