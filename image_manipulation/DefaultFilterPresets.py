from .FilterPreset import FilterPreset

def getDefaultFilterPresets() -> list[FilterPreset]:
    filters : list[FilterPreset] = []

    sFilter = FilterPreset("Preset 1")
    sFilter.blur = 9
    sFilter.vFlip = True
    sFilter.hFlip = False
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 2")
    sFilter.blur = 30
    sFilter.vFlip = False
    sFilter.hFlip = True
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 3")
    sFilter.gaussianNoise = 25
    sFilter.vFlip = True
    sFilter.hFlip = True
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 4")
    sFilter.sapNoise = 4
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 5")
    sFilter.sapNoise = 4
    sFilter.vFlip = True
    sFilter.hFlip = False
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 6")
    sFilter.gaussianNoise = 45
    sFilter.vFlip = False
    sFilter.hFlip = True
    filters.append(sFilter)

    sFilter = FilterPreset("Preset 7")
    sFilter.gaussianNoise = 15
    sFilter.blur = 15
    sFilter.vFlip = True
    sFilter.hFlip = True
    filters.append(sFilter)

    return filters