#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "fckit" for configuration "RelWithDebInfo"
set_property(TARGET fckit APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(fckit PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "eckit;eckit_mpi"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib64/libfckit.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libfckit.so"
  )

list(APPEND _cmake_import_check_targets fckit )
list(APPEND _cmake_import_check_files_for_fckit "${_IMPORT_PREFIX}/lib64/libfckit.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
