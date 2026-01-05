class FilterPreset:
    def __init__(self, name: str | None = None) -> None:
        self.blur = 0
        self.name = name if (name is not None) else "Default"

        self.saturation = 100
        self.contrast = 100
        self.brightness = 0

        self.hFlip = False
        self.vFlip = False

        self.sapNoise = 0
        self.gaussianNoise = 0

    def toString(self) -> str:
        string = f"name: {self.name}, blur: {self.blur}, sat : {self.saturation}, \
        brightness : {self.brightness}, contrast : {self.contrast}, \
        hFlip : {self.hFlip}, vFlip : {self.vFlip}, sap : {self.sapNoise}, \
        gaussian : {self.gaussianNoise}"
        return string
