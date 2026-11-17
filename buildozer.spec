[app]
title = Secure Deletion
package.name = securedeletion
package.domain = org.secure
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.min_api = 21

# (str) Android SDK version (Optional)
android.sdk=33
# (str) Source file include (let empty to include all files)
source.dir = .
