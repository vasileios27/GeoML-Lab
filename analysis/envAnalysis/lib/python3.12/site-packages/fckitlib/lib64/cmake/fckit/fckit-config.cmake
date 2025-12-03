# Config file for the fckit package
# Defines the following variables:
#
#  fckit_FEATURES       - list of enabled features
#  fckit_VERSION        - version of the package
#  fckit_GIT_SHA1       - Git revision of the package
#  fckit_GIT_SHA1_SHORT - short Git revision of the package
#


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was project-config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

### computed paths
set_and_check(fckit_CMAKE_DIR "${PACKAGE_PREFIX_DIR}/lib64/cmake/fckit")
set_and_check(fckit_BASE_DIR "${PACKAGE_PREFIX_DIR}/.")
if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(FCKIT_CMAKE_DIR ${fckit_CMAKE_DIR})
  set(FCKIT_BASE_DIR ${fckit_BASE_DIR})
endif()

### export version info
set(fckit_VERSION           "0.14.1")
set(fckit_GIT_SHA1          "67dd4877bae70a734f423dcb95bce1cd241fc18f")
set(fckit_GIT_SHA1_SHORT    "67dd487")

if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(FCKIT_VERSION           "0.14.1" )
  set(FCKIT_GIT_SHA1          "67dd4877bae70a734f423dcb95bce1cd241fc18f" )
  set(FCKIT_GIT_SHA1_SHORT    "67dd487" )
endif()

### has this configuration been exported from a build tree?
set(fckit_IS_BUILD_DIR_EXPORT OFF)
if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(FCKIT_IS_BUILD_DIR_EXPORT ${fckit_IS_BUILD_DIR_EXPORT})
endif()

### include the <project>-import.cmake file if there is one
if(EXISTS ${fckit_CMAKE_DIR}/fckit-import.cmake)
  set(fckit_IMPORT_FILE "${fckit_CMAKE_DIR}/fckit-import.cmake")
  include(${fckit_IMPORT_FILE})
endif()

### insert definitions for IMPORTED targets
if(NOT fckit_BINARY_DIR)
  find_file(fckit_TARGETS_FILE
    NAMES fckit-targets.cmake
    HINTS ${fckit_CMAKE_DIR}
    NO_DEFAULT_PATH)
  if(fckit_TARGETS_FILE)
    include(${fckit_TARGETS_FILE})
  endif()
endif()

### include the <project>-post-import.cmake file if there is one
if(EXISTS ${fckit_CMAKE_DIR}/fckit-post-import.cmake)
  set(fckit_POST_IMPORT_FILE "${fckit_CMAKE_DIR}/fckit-post-import.cmake")
  include(${fckit_POST_IMPORT_FILE})
endif()

### handle third-party dependencies
if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(FCKIT_LIBRARIES         "")
  set(FCKIT_TPLS              "" )

  include(${CMAKE_CURRENT_LIST_FILE}.tpls OPTIONAL)
endif()

### publish this file as imported
if( DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT )
  set(fckit_IMPORT_FILE ${CMAKE_CURRENT_LIST_FILE})
  mark_as_advanced(fckit_IMPORT_FILE)
  set(FCKIT_IMPORT_FILE ${CMAKE_CURRENT_LIST_FILE})
  mark_as_advanced(FCKIT_IMPORT_FILE)
endif()

### export features and check requirements
set(fckit_FEATURES "TESTS;PKGCONFIG;FINAL;ECKIT;ECKIT")
if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(FCKIT_FEATURES ${fckit_FEATURES})
endif()
foreach(_f ${fckit_FEATURES})
  set(fckit_${_f}_FOUND 1)
  set(fckit_HAVE_${_f} 1)
  if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
    set(FCKIT_HAVE_${_f} 1)
  endif()
endforeach()
check_required_components(fckit)
