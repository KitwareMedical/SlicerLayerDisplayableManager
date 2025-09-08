
#-----------------------------------------------------------------------------
set(MODULE_NAME LayerDM)
set(MODULE_TITLE ${MODULE_NAME})

set(${MODULE_NAME}_VERSION_MAJOR 1)
set(${MODULE_NAME}_VERSION_MINOR 0)
set(${MODULE_NAME}_VERSION_PATCH 0)

set(${MODULE_NAME}_VERSION "${${MODULE_NAME}_VERSION_MAJOR}.${${MODULE_NAME}_VERSION_MINOR}.${${MODULE_NAME}_VERSION_PATCH}")

string(TOUPPER ${MODULE_NAME} MODULE_NAME_UPPER)

#-----------------------------------------------------------------------------
add_subdirectory(MRMLDM)

#-----------------------------------------------------------------------------
set(MODULE_EXPORT_DIRECTIVE "Q_SLICER_QTMODULES_${MODULE_NAME_UPPER}_EXPORT")

set(MODULE_INCLUDE_DIRECTORIES 
)

set(MODULE_SRCS
  qSlicer${MODULE_NAME}Module.cxx
  qSlicer${MODULE_NAME}Module.h
)

set(MODULE_MOC_SRCS
  qSlicer${MODULE_NAME}Module.h
)

set(MODULE_UI_SRCS
)

set(MODULE_TARGET_LIBRARIES
)

set(MODULE_RESOURCES
)

#-----------------------------------------------------------------------------
slicerMacroBuildLoadableModule(
  NAME ${MODULE_NAME}
  TITLE ${MODULE_TITLE}
  EXPORT_DIRECTIVE ${MODULE_EXPORT_DIRECTIVE}
  INCLUDE_DIRECTORIES ${MODULE_INCLUDE_DIRECTORIES}
  SRCS ${MODULE_SRCS}
  MOC_SRCS ${MODULE_MOC_SRCS}
  UI_SRCS ${MODULE_UI_SRCS}
  TARGET_LIBRARIES ${MODULE_TARGET_LIBRARIES}
  RESOURCES ${MODULE_RESOURCES}
  WITH_GENERIC_TESTS
)

#-----------------------------------------------------------------------------
if (BUILD_TESTING)
  add_subdirectory(Testing)
endif ()
