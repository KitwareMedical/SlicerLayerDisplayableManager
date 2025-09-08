#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/KitwareMedical/SlicerLayerDisplayableManager")
set(EXTENSION_CONTRIBUTORS "Thibault Pelletier (Kitware SAS)")
set(EXTENSION_DESCRIPTION "A 3D Slicer module introducing a new displayable manager architecture for layered rendering and interaction handling.")
set(EXTENSION_ICONURL "https://github.com/KitwareMedical/SlicerLayerDisplayableManager/raw/main/Docs/LayerDisplayableManager.png")
set(EXTENSION_SCREENSHOTURLS "https://github.com/KitwareMedical/SlicerLayerDisplayableManager/raw/main/Docs/LayeredDisplayableManager_UML.jpg")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension version
find_program(GIT_EXECUTABLE NAMES git REQUIRED)
execute_process(
  COMMAND "${GIT_EXECUTABLE}" "describe" "--tags" "--abbrev=0" "--match" "v[0-9]*"
  RESULT_VARIABLE git_code
  OUTPUT_VARIABLE git_stdout
  ERROR_VARIABLE git_stderr
)

if(NOT git_code EQUAL 0)
  message(FATAL_ERROR "Failed to determined project version using Git.\n"
    "GIT_EXECUTABLE: ${GIT_EXECUTABLE}\n"
    "Return Code: ${git_code}\n"
    "Standard error:\n${git_stdout}\n"
    "Standard error:\n${git_stderr}\n"
  )
endif()

string(STRIP "${git_stdout}" git_stdout) # git output will end with a newline
string(SUBSTRING "${git_stdout}" 1 -1 LayerDM_VERSION) # remove first character
string(REPLACE "." ";" version_components "${LayerDM_VERSION}") # this creates a list
list(GET version_components 0 LayerDM_VERSION_MAJOR)
list(GET version_components 1 LayerDM_VERSION_MINOR)
list(GET version_components 2 LayerDM_VERSION_PATCH)

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(LayerDM)

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
