# (C) Copyright 2013 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

if( fckit_IS_BUILD_DIR_EXPORT )
  set( FCTEST_GENERATOR /venv/build3.12/bin/python3.12 /src/fckit/tools/fctest-generate-runner.py )
  set( FYPP /src/fckit/tools/fckit-eval.sh;/src/fckit/contrib/fypp-3.2-b8dd58b-20230822/bin/fypp )
  if( 0 )
     set( FCKIT_VENV_EXE  )
  endif()
else()
  if( 0 AND NOT ON )
     message( FATAL_ERROR "Installation of fckit python vritual environment was disabled" )
  elseif( 0 )
     set( _fckit_eval_script ${fckit_BASE_DIR}/libexec/fckit-eval.sh )
     set( FCKIT_VENV_EXE ${fckit_BASE_DIR}/ )
     set( FYPP ${_fckit_eval_script} ${FCKIT_VENV_EXE} -m fypp )
  else()
     set( FYPP ${fckit_BASE_DIR}/libexec/fckit-eval.sh 
               ${fckit_BASE_DIR}/libexec/fckit-fypp.py )
  endif()

  set( FCTEST_GENERATOR /venv/build3.12/bin/python3.12 ${fckit_BASE_DIR}/libexec/fctest-generate-runner.py )
endif()


##############################################################################################
# fckit_target_append_fypp_args( output target )
#   Purpose:
#        From a target, assemble arguments to pass to fypp. These arguments are
#        the include flags and compile definition flags.
#   Arguments:
#        output            This argument will contain the flags as a list
#        target            The name of the target to process

function( fckit_target_append_fypp_args output target )
  unset(_args)
  set( valid_target TRUE )
  if( target MATCHES "/" )
    set( valid_target FALSE )
  endif()
  if( TARGET ${target} )
    get_target_property(target_type ${target} TYPE)
    if( target_type STREQUAL "INTERFACE_LIBRARY")
      set( valid_target FALSE )
    endif()
  endif()
  if( valid_target )
    if( CMAKE_VERSION VERSION_LESS 3.12 ) # Hopefully we can remove this soon
      foreach( include_property INCLUDE_DIRECTORIES;INTERFACE_INCLUDE_DIRECTORIES )
        set( prop "$<TARGET_PROPERTY:${target},${include_property}>" )
        list( APPEND _args "$<$<BOOL:${prop}>:-I $<JOIN:${prop}, -I >>" )
      endforeach()
      foreach( definitions_property COMPILE_DEFINITIONS;INTERFACE_COMPILE_DEFINITIONS )
        set( prop "$<TARGET_PROPERTY:${target},${definitions_property}>" )
        list( APPEND _args "$<$<BOOL:${prop}>:-D $<JOIN:${prop}, -D >>" )
      endforeach()
    else()
      foreach( include_property INCLUDE_DIRECTORIES;INTERFACE_INCLUDE_DIRECTORIES )
        set( prop "$<$<TARGET_EXISTS:${target}>:$<TARGET_PROPERTY:${target},${include_property}>>" )
        list( APPEND _args "$<$<BOOL:${prop}>:-I $<JOIN:${prop}, -I >>" )
      endforeach()
      foreach( definitions_property COMPILE_DEFINITIONS;INTERFACE_COMPILE_DEFINITIONS )
        set( prop "$<$<TARGET_EXISTS:${target}>:$<TARGET_PROPERTY:${target},${definitions_property}>>" )
        list( APPEND _args "$<$<BOOL:${prop}>:-D $<JOIN:${prop}, -D >>" )
      endforeach()
    endif()
  endif()
  # Append to output and set in parent scope
  if( _args )
    set(${output} ${${output}} ${_args} PARENT_SCOPE)
  endif()
endfunction()

##############################################################################################
# fckit_preprocess_fypp_sources( output
#                                [SOURCES file1 [file2]... ]
#                                [FYPP_ARGS arg1 [arg2]... ]
#                                [FYPP_ARGS_EXCLUDE arg1 [arg2]... ]
#                                [DEPENDS dep1 [dep2]... ] )
#    Purpose:
#        Preprocess source files with fypp
#
#    Arguments:
#        output                              Append preprocessed source files to this list
#        [SOURCES file1 [file2]... ]         List of source files to append
#        [FYPP_ARGS arg1 [arg2]...]          Arguments passed to fypp
#        [FYPP_ARGS_EXCLUDE arg1 [arg2]...]  Arguments excluded from being passed to fypp; accepts bash-compatible regex
#        [DEPENDS dep1 [dep2]... ]           Dependencies before processing files
#
#    Notes:
#        The include flags and compile flags of targets with the DEPENDS argument
#        will be automatically deduced and added to the fypp command

function( fckit_preprocess_fypp_sources output )

  set( options NO_LINE_NUMBERING )
  set( single_value_args "" )
  set( multi_value_args SOURCES FYPP_ARGS FYPP_ARGS_EXCLUDE DEPENDS )
  cmake_parse_arguments( _PAR "${options}" "${single_value_args}" "${multi_value_args}"  ${_FIRST_ARG} ${ARGN} )

  unset( outfiles )

  list( APPEND _PAR_FYPP_ARGS_EXCLUDE ${FCKIT_FYPP_ARGS_EXCLUDE})
  list( APPEND _PAR_FYPP_ARGS_EXCLUDE "-D[[:space:]]?.*=([0-9])+L" )
  list( APPEND _PAR_FYPP_ARGS_EXCLUDE "-D[[:space:]]?__.*" )
  list( JOIN   _PAR_FYPP_ARGS_EXCLUDE "," _PAR_FYPP_ARGS_EXCLUDE )

  foreach( filename ${_PAR_SOURCES} )

    get_filename_component( dir ${filename} DIRECTORY )
    get_filename_component( base ${filename} NAME_WE )
    set( outfile ${CMAKE_CURRENT_BINARY_DIR} )
    if( dir )
      set( outfile "${outfile}/${dir}" )
    endif()
    set( outfile "${outfile}/${base}.F90" )

    list( APPEND outfiles ${outfile} )

    unset(args)
    list( APPEND args -l 132 ) # Line length
    list( APPEND args -p )     # Create parent folder
    set( _enable_line_numbers TRUE )
    if( _PAR_NO_LINE_NUMBERING OR FYPP_NO_LINE_NUMBERING )
      set( _enable_line_numbers FALSE )
    endif()
    if( CMAKE_Fortran_COMPILER_ID MATCHES "Cray" )
      set( _enable_line_numbers FALSE )
      # Compiler errors occur (tested with cce/8.7.5 )
    endif()
    if( _enable_line_numbers )
      list( APPEND args -n )   # Create line numbering for compile errors
      if( CMAKE_Fortran_COMPILER_ID MATCHES "Intel" )
        list( APPEND args --line-marker-format=gfortran5 )
      endif()
      if( CMAKE_Fortran_COMPILER_ID MATCHES "NAG" )
        # workaround for line markers in continuation lines ( see e.g. https://github.com/ecmwf/atlas/pull/193 )
        list( APPEND args --line-numbering-mode=nocontlines )
      endif()
      # list( APPEND args -N nocontlines )  # workaround for line numbers in continuation lines
    endif()

    if( _PAR_FYPP_ARGS )
        set( args ${args} ${_PAR_FYPP_ARGS} )
    endif()

    foreach( target ${_PAR_DEPENDS} )
      fckit_target_append_fypp_args( args ${target} )
    endforeach()

    if( dir )
      set( short_outfile "${dir}/${base}.F90" )
    else()
      set( short_outfile "${base}.F90")
    endif()

    get_source_file_property( _depends ${filename} OBJECT_DEPENDS )

    unset( ${filename}_depends )
    if( _depends )
       set( ${filename}_depends ${_depends} )
    endif()

    add_custom_command(
      OUTPUT ${outfile}
      COMMAND ${CMAKE_COMMAND} -E env FCKIT_EVAL_ARGS_EXCLUDE="${_PAR_FYPP_ARGS_EXCLUDE}" ${FYPP} ${args} ${CMAKE_CURRENT_SOURCE_DIR}/${filename} ${outfile}
      DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${filename} ${_PAR_DEPENDS} ${${filename}_depends}
      COMMENT "[fypp] Preprocessor generating ${short_outfile}" )

    set_source_files_properties(${outfile} PROPERTIES GENERATED TRUE)

    ### Extra stuff required to add correct flags
    # ecbuild 3.2 compatible properties that need to be transferred from .fypp files to .F90
    foreach( _prop COMPILE_FLAGS
                   COMPILE_FLAGS_${CMAKE_BUILD_TYPE_CAPS}
                   COMPILE_OPTIONS
                   OVERRIDE_COMPILE_FLAGS
                   OVERRIDE_COMPILE_FLAGS_${CMAKE_BUILD_TYPE_CAPS} )
      get_source_file_property( ${filename}_${_prop} ${filename} ${_prop} )
      if( ${filename}_${_prop} )
        set_source_files_properties(${outfile} PROPERTIES ${_prop} ${${filename}_${_prop}} )
      endif()
    endforeach()

  endforeach()

  # Append to output and set in parent scope
  set(${output} ${${output}} ${outfiles} PARENT_SCOPE)


endfunction()

##############################################################################################


##############################################################################################
# fckit_target_preprocess_fypp( target
#                               [FYPP_ARGS arg1 [arg2]... ]
#                               [FYPP_ARGS_EXCLUDE arg1 [arg2]... ]
#                               [DEPENDS dep1 [dep2]... ] )
#    Purpose:
#        Preprocess source files in the target with the extensions
#        {.fypp, .fypp.F90, .F90.fypp}
#
#    Arguments:
#        target                               Preprocess all files from this target
#        [FYPP_ARGS arg1 [arg2]...]           Arguments passed to fypp
#        [FYPP_ARGS_EXCLUDE arg1 [arg2]... ]  Arguments excluded from being passed to fypp; accepts bash-compatible regex
#        [DEPENDS dep1 [dep2]... ]            Dependencies before processing files
#
#    Notes:
#        The include flags and compile flags of current target and targets
#        within the DEPENDS argument will be automatically deduced
#        and added to the fypp command

function( fckit_target_preprocess_fypp _PAR_TARGET )

  set( options NO_LINE_NUMBERING )
  set( single_value_args "" )
  set( multi_value_args FYPP_ARGS FYPP_ARGS_EXCLUDE DEPENDS )
  cmake_parse_arguments( _PAR "${options}" "${single_value_args}" "${multi_value_args}"  ${_FIRST_ARG} ${ARGN} )

  if( TARGET ${_PAR_TARGET} )

      get_target_property( _target_sources ${_PAR_TARGET} SOURCES )

      unset( sources_to_be_preprocessed )
      foreach( source ${_target_sources} )
        if( source MATCHES ".fypp.F90" )
          list( APPEND sources_to_be_preprocessed ${source} )
        elseif( source MATCHES ".F90.fypp" )
          list( APPEND sources_to_be_preprocessed ${source} )
        elseif( source MATCHES ".fypp" )
          list( APPEND sources_to_be_preprocessed ${source} )
        endif()
      endforeach()
      foreach( source ${sources_to_be_preprocessed} )
        set( source_files_properties ${source} PROPERTIES HEADER_FILE_ONLY TRUE )
      endforeach()

### BUG WORKAROUND (tested upto CMake 3.13.2)
#   Even though source files to be preprocessed with final extension .F90 have just been
#   declared as HEADER_FILE_ONLY, CMake still tries to compile these files.
#   This does not happen for files ending with other extensions ( .fypp )
      set( _create_fypp_target FALSE )
      foreach( source ${sources_to_be_preprocessed} )
        if( source MATCHES ".fypp.F90" )
          set( _create_fypp_target TRUE )
          list(FILTER _target_sources EXCLUDE REGEX ${source} )
        endif()
      endforeach()
      if( NOT TARGET ${_PAR_TARGET}_fypp AND _create_fypp_target )
          set_property( TARGET ${_PAR_TARGET} PROPERTY SOURCES ${_target_sources} )
          add_custom_target( ${_PAR_TARGET}_fypp SOURCES ${sources_to_be_preprocessed} )
      endif()
### END BUG WORKAROUND



      foreach( depends_property LINK_DEPENDS;MANUALLY_ADDED_DEPENDENCIES )
        get_target_property( target_depends ${_PAR_TARGET} ${depends_property} )
        if( target_depends )
          set( preprocessed_depends ${preprocessed_depends} ${target_depends} )
        endif()
      endforeach()

      fckit_target_append_fypp_args( args ${_PAR_TARGET} )

      if( _PAR_NO_LINE_NUMBERING )
          set( _NO_LINE_NUMBERING NO_LINE_NUMBERING )
      endif()

      fckit_preprocess_fypp_sources( preprocessed_sources
          SOURCES ${sources_to_be_preprocessed}
          ${_NO_LINE_NUMBERING}
          FYPP_ARGS ${_PAR_FYPP_ARGS} ${args}
          FYPP_ARGS_EXCLUDE ${_PAR_FYPP_ARGS_EXCLUDE}
          DEPENDS ${preprocessed_depends} ${_PAR_DEPENDS}
      )

      target_sources( ${_PAR_TARGET} PRIVATE ${preprocessed_sources} )

      ### Extra stuff required to add correct flags
      if( COMMAND ecbuild_target_flags )
        list( APPEND ${_PAR_TARGET}_fortran_srcs ${preprocessed_sources} )
        list( APPEND ${_PAR_TARGET}_Fortran_srcs ${preprocessed_sources} )
        ecbuild_target_flags( ${_PAR_TARGET} "" "" "")
          # Currently it is not possible to add flags that were added within
          # ecbuild_add_library( ... FFLAGS <FFLAGS CFLAGS <CFLAGS> CXXFLAGS <CXXFLAGS> )
          # until ecbuild exports these variables
          # Therefore 3 empty strings for these.
          # Luckily this is a very tiny use case
      endif()

### BUG WORKAROUND for CMake < 3.12
#   CMake seems to not add the "-fPIC -h PIC" flags for the Cray compiler when the target
#   has the POSITION_INDEPENDENT_CODE property set, so add it manually
    if( CMAKE_VERSION VERSION_LESS 3.12 )
      get_property( _target_pic TARGET ${_PAR_TARGET} PROPERTY POSITION_INDEPENDENT_CODE )
      if( _target_pic )
        if( CMAKE_Fortran_COMPILER_ID MATCHES "Cray" )
          foreach( _src ${preprocessed_sources} )
            set_source_files_properties( ${_src} COMPILE_FLAGS "-h PIC" )
          endforeach()
        endif()
      endif()
    endif()
  endif()
### END BUG WORKAROUND

endfunction()


# (C) Copyright 2013 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

function( fctest_generate_runner )

  set( options           )
  set( single_value_args OUTPUT FILENAME )
  set( multi_value_args DEPENDS )

  cmake_parse_arguments( _PAR "${options}" "${single_value_args}" "${multi_value_args}"  ${_FIRST_ARG} ${ARGN} )

  get_filename_component(base ${_PAR_FILENAME} NAME_WE)
  set(outfile ${CMAKE_CURRENT_BINARY_DIR}/${base}_main.F90)
  set(${_PAR_OUTPUT} ${outfile} PARENT_SCOPE)

  list( APPEND _depends
    ${_PAR_FILENAME}
    ${_PAR_DEPENDS}
  )

  add_custom_command(
    OUTPUT ${outfile}
    COMMAND ${FCTEST_GENERATOR} -i ${_PAR_FILENAME} -o ${outfile}
    DEPENDS ${_depends}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "[fctest] Generating test driver ${base}_main.F90")

  set_source_files_properties(${outfile} PROPERTIES GENERATED TRUE)

endfunction()

function( add_fctest )

cmake_minimum_required( VERSION 3.12 )
cmake_policy( SET CMP0064 NEW ) # Recognize ``TEST`` as operator for the ``if()`` command. (introduced in CMake version 3.4)

  ecbuild_add_test( ${ARGV} )

  set( options           )
  set( single_value_args TARGET )
  set( multi_value_args )

  cmake_parse_arguments( _PAR "${options}" "${single_value_args}" "${multi_value_args}" ${_FIRST_ARG} ${ARGN} )

  if( TARGET ${_PAR_TARGET} )
      get_target_property( test_sources ${_PAR_TARGET} SOURCES )
      list( GET test_sources 0 TESTSUITE )

      get_filename_component( extension ${TESTSUITE} EXT )
      get_filename_component( base ${TESTSUITE} NAME_WE )

    ### Preprocess files with extension ".fypp.F90"      
      fckit_target_preprocess_fypp( ${_PAR_TARGET} )

    ### Remove TESTSUITE from target
      get_target_property( test_sources ${_PAR_TARGET} SOURCES )
      set( match_regex "${base}.F90")
      set( match_found FALSE )
      foreach( source ${test_sources} )
        if( ${source} MATCHES "${match_regex}" )
          if( match_found ) 
            message( FATAL_ERROR "Second match found for ${match_regex} in fctest ${_PAR_TARGET}" )
          endif()
          set( match_found TRUE )
          set( TESTSUITE ${source} )
          list( FILTER test_sources EXCLUDE REGEX ${source} )
        endif()
      endforeach()
      if( NOT match_found )
        message( FATAL_ERROR "No match found for ${match_regex} in fctest ${_PAR_TARGET}" )
      endif()
      set_property( TARGET ${_PAR_TARGET} PROPERTY SOURCES ${test_sources} )

    ### Add TESTRUNNER generated from TESTSUITE
      fctest_generate_runner(
          OUTPUT TESTRUNNER
          FILENAME ${TESTSUITE} )
      target_sources( ${_PAR_TARGET} PUBLIC ${TESTRUNNER} )

    ### Add dependencies
      target_link_libraries( ${_PAR_TARGET} fckit )
      if( TEST ${_PAR_TARGET} )
        set_property( TEST ${_PAR_TARGET} APPEND PROPERTY LABELS "fortran" )
      endif()

    ### Add compile flags
      list( APPEND _properties COMPILE_FLAGS COMPILE_DEFINITIONS )
      foreach( _prop ${_properties} )
          if( NOT ORIGINAL_TESTSUITE )
            set( ORIGINAL_TESTSUITE ${TESTSUITE} )
          endif()
          get_source_file_property( TESTSUITE_PROPERTY ${ORIGINAL_TESTSUITE} ${_prop} )
          if( TESTSUITE_PROPERTY )
              set_source_files_properties( ${TESTRUNNER} PROPERTIES ${_prop} ${TESTSUITE_PROPERTY} )
          endif()
      endforeach()
      if(${CMAKE_Fortran_COMPILER_ID} MATCHES GNU)
          #Disable developer-only pre-processor warnings when not compiling for Debug configurations
          target_compile_options(${_PAR_TARGET} PRIVATE $<$<NOT:$<CONFIG:Debug>>:-Wno-cpp>)
      endif()

    ### Workaround Flang issue, not able to include absolute path. Adding -I/ seems a workaround
      # but results in warning for other compilers (intel)
      if( ${CMAKE_Fortran_COMPILER_ID} MATCHES Flang )
        target_include_directories( ${_PAR_TARGET} PUBLIC ${FCKIT_INCLUDE_DIRS} "/" )
      endif()
      

      add_custom_target( ${_PAR_TARGET}_testsuite SOURCES ${TESTSUITE} )
  endif()

endfunction()


set( fckit_HAVE_ECKIT 1 )
set( fckit_ECKIT_FOUND 0 )
if( fckit_HAVE_ECKIT )
  set( fckit_ECKIT_FOUND 1 )

  # Following Required when "ECBUILD_2_COMPAT=OFF" and static linking is used
  include( CMakeFindDependencyMacro )
  find_dependency( eckit HINTS ${CMAKE_CURRENT_LIST_DIR}/../eckit /tmp/fckit/prereqs/eckitlib/lib64/cmake/eckit  )
endif()

if( fckit_FIND_REQUIRED_ECKIT AND NOT fckit_ECKIT_FOUND )
  message( FATAL_ERROR "fckit was not compiled with ECKIT enabled" )
endif()

set( FCKIT_LIBRARIES fckit )
