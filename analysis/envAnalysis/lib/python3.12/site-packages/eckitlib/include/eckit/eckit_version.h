#ifndef eckit_version_h
#define eckit_version_h

#define eckit_VERSION_STR "1.32.3"
#define eckit_VERSION     "1.32.3"

#define eckit_VERSION_MAJOR 1
#define eckit_VERSION_MINOR 32
#define eckit_VERSION_PATCH 3


#ifdef __cplusplus
extern "C" {
#endif

const char * eckit_version();

unsigned int eckit_version_int();

const char * eckit_version_str();

const char * eckit_git_sha1();

#ifdef __cplusplus
}
#endif

#endif // eckit_version_h
