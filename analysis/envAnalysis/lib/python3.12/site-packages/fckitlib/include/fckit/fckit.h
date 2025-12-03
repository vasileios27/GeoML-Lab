#if 0
(C) Copyright 2013 ECMWF.

This software is licensed under the terms of the Apache Licence Version 2.0
which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
In applying this licence, ECMWF does not waive the privileges and immunities
granted to it by virtue of its status as an intergovernmental organisation nor
does it submit to any jurisdiction.
#endif

#if 0
// clang-format off
#endif

#ifndef FCKIT_H
#define FCKIT_H

#define FCKIT_GIT_SHA1      "67dd4877bae70a734f423dcb95bce1cd241fc18f"
#define FCKIT_VERSION       "0.14.1"

#define FCKIT_HAVE_ECKIT                           1
#define FCKIT_HAVE_ECKIT_MPI_PARALLEL              0
#define FCKIT_HAVE_FINAL                           1
#define FCKIT_FINAL_FUNCTION_RESULT                1
#define FCKIT_FINAL_UNINITIALIZED_LOCAL            0
#define FCKIT_FINAL_UNINITIALIZED_INTENT_OUT       1
#define FCKIT_FINAL_UNINITIALIZED_INTENT_INOUT     0
#define FCKIT_FINAL_NOT_PROPAGATING                0
#define FCKIT_FINAL_NOT_INHERITING                 0
#define FCKIT_FINAL_BROKEN_FOR_ALLOCATABLE_ARRAY   0
#define FCKIT_FINAL_BROKEN_FOR_AUTOMATIC_ARRAY     0
#define FCKIT_HAVE_ECKIT_TENSOR                    1
#define FCKIT_FINAL impure elemental
#define FCKIT_FINAL_DEBUGGING 0

#define FCKIT_SUPPRESS_UNUSED( X ) \
associate( unused_ => X ); \
end associate

#define PGIBUG_ATLAS_197 0
#if 0
Following is to workaround PGI bug which prevents the use of function c_ptr()
PGI bug present from version 17.10, fixed since version 19.4
#endif
#if PGIBUG_ATLAS_197
#define CPTR_PGIBUG_A cpp_object_ptr
#define CPTR_PGIBUG_B shared_object_%cpp_object_ptr
#else
#define CPTR_PGIBUG_A c_ptr()
#define CPTR_PGIBUG_B c_ptr()
#endif

#define PGIBUG_ATLAS_197_DEBUG 0
#if 0
When above PGIBUG_ATLAS_197_DEBUG==1 then the c_ptr() member functions are disabled from compilation,
to detect possible dangerous use cases when the PGI bug ATLAS-197 is present.
#endif

#define XLBUG_FCKIT_14 1
#if 0
Following is to workaround XL bug where allocate( character(len=xxx,kind=c_char ) :: string )
does not compile
#endif
#if XLBUG_FCKIT_14
#define FCKIT_ALLOCATE_CHARACTER( VARIABLE, SIZE ) allocate( character(len=(SIZE)) :: VARIABLE )
#else
#define FCKIT_ALLOCATE_CHARACTER( VARIABLE, SIZE ) allocate( character(len=(SIZE),kind=c_char) :: VARIABLE )
#endif

#if 0
// clang-format on
#endif

#endif
