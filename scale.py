class Scale():
    def __init__(self, **kwargs):
        self.UUID = kwargs.get("UUID", "")
        self.manufacturerData = kwargs.get("manufacturerData", bytes())

        self.address = kwargs.get("address", "")
        self.rawData = kwargs.get("rawData", bytes())
        self.unit = kwargs.get("unit", "")
        self.weight = kwargs.get("weight", "")
        self.sequence = kwargs.get("sequence", "")

        self.isStabilized = kwargs.get("isStabilized", False)
        self.loadRemoved = kwargs.get("loadRemoved", False)
    
    def __str__(self):
        """Override the default print behavior"""
        import json
        vars = dict(self.__dict__)
        # Convert bytes to a hex string for a better lisibility
        vars["manufacturerData"] = self.manufacturerData.hex()
        vars["rawData"] = self.rawData.hex()
        return json.dumps(vars, indent=4, sort_keys=True)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return \
            self.UUID == other.UUID and \
            self.manufacturerData == other.manufacturerData and \
            self.address == other.address and \
            self.rawData == other.rawData and \
            self.unit == other.unit and \
            self.weight == other.weight and \
            self.sequence == other.sequence and \
            self.isStabilized == other.isStabilized and \
            self.loadRemoved == other.loadRemoved
