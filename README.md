# V Cleb

**V Cleb** is a video editor for Android and desktop, built around a multi-track timeline, video and audio tools, effects, transitions, titles, captions, and export.

The official user-facing app name is **V Cleb**. Android package identity and launcher labels, the Windows installer and shortcuts, the Windows portable package name, and the desktop window title use this branding. The internal CMake target remains `drift` to avoid a risky source-wide rename; the packaged Windows application is named `v-cleb.exe`. This is a branding-only packaging change and does not remove or disable app features or addons.

The current V Cleb launcher artwork is used for the app icon. Icon artwork changes are separate from the application-name configuration.

## Build and test

This repository uses GitHub Actions for builds.

- Open the [Actions page](https://github.com/ali12hhh-oss/Ali-5/actions) to view Android and desktop build results.
- Download the APK from the successful workflow's Artifacts section when an APK artifact is provided.
- Test installation, media import, project save/reopen, editing, and export before preparing a release.

## Source and license

This project contains third-party components and retains their applicable license and attribution files. Review the repository's [LICENSE](LICENSE) and component notices before distributing modified builds.

## Project documentation

Build instructions, implementation notes, and other project documentation are available in the `docs/` directory.
