 
set(SOURCE_FILES
     base64.c
     connection.c
     daemon.c
     digestauth.c
     internal.c
     md5.c
     memorypool.c
     mhd_mono_clock.c
     mhd_str.c
     postprocessor.c
     reason_phrase.c
     response.c
     sysfdsetsize.c
     tsearch.c
    )

set (HEADER_FILES
 microhttpd.h
 #plibc.h
 platform.h
 MHD_config.h
)

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/src/mhttpd)

ADD_LIBRARY(mhttpd SHARED ${SOURCE_FILES})



SET_TARGET_PROPERTIES(mhttpd PROPERTIES CLEAN_DIRECT_OUTPUT 1)
SET_TARGET_PROPERTIES(mhttpd PROPERTIES VERSION 1.0 SOVERSION 1)

INSTALL(TARGETS mhttpd DESTINATION lib)
INSTALL(FILES ${HEADER_FILES} DESTINATION include/mhttpd)
