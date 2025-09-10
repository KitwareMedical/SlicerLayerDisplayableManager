cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(LayerDisplayableManager)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/KitwareMedical/SlicerLayerDisplayableManager")
set(EXTENSION_CONTRIBUTORS "Thibault Pelletier (Kitware SAS)")
set(EXTENSION_DESCRIPTION "A 3D Slicer module introducing a new displayable manager architecture for layered rendering and interaction handling.")
set(EXTENSION_ICONURL "https://github.com/KitwareMedical/SlicerLayerDisplayableManager/raw/main/Doc/LayerDisplayableManager.png")
set(EXTENSION_SCREENSHOTURLS "https://github.com/KitwareMedical/SlicerLayerDisplayableManager/raw/main/Doc/LayeredDisplayableManager_UML.jpg")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(LayerDM)

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
