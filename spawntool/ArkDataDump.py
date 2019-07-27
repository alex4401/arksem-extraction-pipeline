class AssetData:
    def __init__(self, data_object):
        self.__data__ = data_object
    
    def find_export_by_id(self, searched_id):
        for export in self.__data__:
            if export["export_id"] == searched_id:
                return export
        return None
    
    def find_export_by_type(self, searched_type):
        for export in self.__data__:
            if export["export_type"] == searched_type:
                return export
        return None
    
    def find_exports_by_type(self, searched_type):
        output = []
        for export in self.__data__:
            if export["export_type"] == searched_type:
                output.append(export)
        return output