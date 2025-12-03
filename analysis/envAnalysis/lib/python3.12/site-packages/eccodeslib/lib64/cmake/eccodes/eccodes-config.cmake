# Config file for the eccodes package
# Defines the following variables:
#
#  eccodes_FEATURES       - list of enabled features
#  eccodes_VERSION        - version of the package
#  eccodes_GIT_SHA1       - Git revision of the package
#  eccodes_GIT_SHA1_SHORT - short Git revision of the package
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
set_and_check(eccodes_CMAKE_DIR "${PACKAGE_PREFIX_DIR}/lib64/cmake/eccodes")
set_and_check(eccodes_BASE_DIR "${PACKAGE_PREFIX_DIR}/.")
if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(ECCODES_CMAKE_DIR ${eccodes_CMAKE_DIR})
  set(ECCODES_BASE_DIR ${eccodes_BASE_DIR})
endif()

### export version info
set(eccodes_VERSION           "2.44.0")
set(eccodes_GIT_SHA1          "aa85928d05036a1bce3cab330bc75681dc26c234")
set(eccodes_GIT_SHA1_SHORT    "aa85928")

if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(ECCODES_VERSION           "2.44.0" )
  set(ECCODES_GIT_SHA1          "aa85928d05036a1bce3cab330bc75681dc26c234" )
  set(ECCODES_GIT_SHA1_SHORT    "aa85928" )
endif()

### has this configuration been exported from a build tree?
set(eccodes_IS_BUILD_DIR_EXPORT OFF)
if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(ECCODES_IS_BUILD_DIR_EXPORT ${eccodes_IS_BUILD_DIR_EXPORT})
endif()

### include the <project>-import.cmake file if there is one
if(EXISTS ${eccodes_CMAKE_DIR}/eccodes-import.cmake)
  set(eccodes_IMPORT_FILE "${eccodes_CMAKE_DIR}/eccodes-import.cmake")
  include(${eccodes_IMPORT_FILE})
endif()

### insert definitions for IMPORTED targets
if(NOT eccodes_BINARY_DIR)
  find_file(eccodes_TARGETS_FILE
    NAMES eccodes-targets.cmake
    HINTS ${eccodes_CMAKE_DIR}
    NO_DEFAULT_PATH)
  if(eccodes_TARGETS_FILE)
    include(${eccodes_TARGETS_FILE})
  endif()
endif()

### include the <project>-post-import.cmake file if there is one
if(EXISTS ${eccodes_CMAKE_DIR}/eccodes-post-import.cmake)
  set(eccodes_POST_IMPORT_FILE "${eccodes_CMAKE_DIR}/eccodes-post-import.cmake")
  include(${eccodes_POST_IMPORT_FILE})
endif()

### handle third-party dependencies
if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(ECCODES_LIBRARIES         "")
  set(ECCODES_TPLS              "" )

  include(${CMAKE_CURRENT_LIST_FILE}.tpls OPTIONAL)
endif()

### publish this file as imported
if( DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT )
  set(eccodes_IMPORT_FILE ${CMAKE_CURRENT_LIST_FILE})
  mark_as_advanced(eccodes_IMPORT_FILE)
  set(ECCODES_IMPORT_FILE ${CMAKE_CURRENT_LIST_FILE})
  mark_as_advanced(ECCODES_IMPORT_FILE)
endif()

### export features and check requirements
set(eccodes_FEATURES "TESTS;PKGCONFIG;PRODUCT_GRIB;PRODUCT_BUFR;BUILD_TOOLS;GEOGRAPHY;JPG;JPG_LIBOPENJPEG;PNG;AEC;FORTRAN;MEMFS;ECCODES_THREADS;ECCODES_THREADS")
if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
  set(ECCODES_FEATURES ${eccodes_FEATURES})
endif()
foreach(_f ${eccodes_FEATURES})
  set(eccodes_${_f}_FOUND 1)
  set(eccodes_HAVE_${_f} 1)
  if(DEFINED ECBUILD_2_COMPAT AND ECBUILD_2_COMPAT)
    set(ECCODES_HAVE_${_f} 1)
  endif()
endforeach()
check_required_components(eccodes)
