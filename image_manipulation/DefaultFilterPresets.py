from .FilterPreset import FilterPreset

def getDefaultFilterPresets() -> list[FilterPreset]:
    filters : list[FilterPreset] = []

    sFilter = FilterPreset("Preset 1")
    sFilter.blur = 5
    sFilter.vFlip = True
    sFilter.hFlip = False
    sFilter.saturation = 105
    sFilter.contrast = 80
    sFilter.brightness = -20
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 2")
    sFilter.blur = 7
    sFilter.vFlip = False
    sFilter.hFlip = True
    sFilter.saturation = 95
    sFilter.contrast = 90
    sFilter.brightness = -10
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 3")
    sFilter.gaussianNoise = 15
    sFilter.vFlip = True
    sFilter.hFlip = True
    sFilter.saturation = 120
    sFilter.contrast = 110
    sFilter.brightness = -5
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 4")
    sFilter.sapNoise = 1
    sFilter.saturation = 115
    sFilter.contrast = 95
    sFilter.brightness = 2
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 5")
    sFilter.sapNoise = 1
    sFilter.vFlip = True
    sFilter.hFlip = False
    sFilter.saturation = 100
    sFilter.contrast = 105
    sFilter.brightness = 5
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 6")
    sFilter.gaussianNoise = 15
    sFilter.vFlip = False
    sFilter.hFlip = True
    sFilter.saturation = 85
    sFilter.contrast = 95
    sFilter.brightness = 15
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 7")
    sFilter.gaussianNoise = 10
    sFilter.blur = 7
    sFilter.vFlip = True
    sFilter.hFlip = True
    sFilter.saturation = 90
    sFilter.contrast = 90
    sFilter.brightness = 10
    filters.append(sFilter)

    return filters