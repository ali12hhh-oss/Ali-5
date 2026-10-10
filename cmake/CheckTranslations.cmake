# Verifies that a fresh lupdate does not add or remove source-message keys.
# Translation text, locations, XML formatting and plural-form normalization may legitimately
# differ after lupdate; comparing whole files incorrectly fails for those translation-only edits.
# Invoked as a CTest; required -D: SOURCE_DIR, BINARY_DIR. Optional: CONFIG.

if(NOT SOURCE_DIR OR NOT BINARY_DIR)
    message(FATAL_ERROR "CheckTranslations.cmake needs SOURCE_DIR, BINARY_DIR")
endif()

set(_catalog "${SOURCE_DIR}/i18n/drift.ts")
if(NOT EXISTS "${_catalog}")
    message(FATAL_ERROR
        "Missing ${_catalog}. Run:\n"
        "  cmake --build build --target update_translations")
endif()

set(_snapshot "${BINARY_DIR}/i18n-check/i18n")
file(REMOVE_RECURSE "${BINARY_DIR}/i18n-check")
file(COPY "${SOURCE_DIR}/i18n" DESTINATION "${BINARY_DIR}/i18n-check")

set(_build_cmd "${CMAKE_COMMAND}" --build "${BINARY_DIR}" --target update_translations)
if(CONFIG)
    list(APPEND _build_cmd --config "${CONFIG}")
endif()
execute_process(COMMAND ${_build_cmd} RESULT_VARIABLE _rv)
if(_rv)
    message(FATAL_ERROR "update_translations failed (exit ${_rv})")
endif()

find_program(_python_executable NAMES python3 python)
if(NOT _python_executable)
    message(FATAL_ERROR "Python 3 is required to validate translation source keys")
endif()

execute_process(
    COMMAND "${_python_executable}"
        "${SOURCE_DIR}/scripts/check_translation_sources.py"
        "${_snapshot}" "${SOURCE_DIR}/i18n"
    RESULT_VARIABLE _check_rv
)
if(_check_rv)
    message(FATAL_ERROR "Translation source check failed (exit ${_check_rv})")
endif()
