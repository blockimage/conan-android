import platform

from conans import ConanFile, CMake, tools
import os

from os import unlink

# from https://github.com/lasote/conan-android-ndk/blob/master/conanfile.py
# upgraded to r18
class AndroidndkConan(ConanFile):
    name = "android-ndk"
    version = "r17b"
    license = "GPL/APACHE2"
    url = "https://github.com/lasote/conan-android-ndk.git"
    settings = None
    options = {"host_os": ["Linux", "Windows", "Macos"], "host_arch": ["x86", "x86_64"]}

    def config_options(self):
        os_info = tools.OSInfo()
        if os_info.is_linux:
            self.options.host_os = "Linux"
        elif os_info.is_windows:
            self.options.host_os = "Windows"
        elif os_info.is_macos:
            self.options.host_os = "Macos"
        else:
            raise Exception("Unsupported platform")

        import sys
        is_64bits = sys.maxsize > 2 ** 32
        if is_64bits:
            self.options.host_arch = "x86_64"
        else:
            self.options.host_arch = "x86"

    def source(self):

        urls = {"Windows_x86_64": ["https://dl.google.com/android/repository/android-ndk-r17b-windows-x86_64.zip",
                                   "7fc0e0f94d86ea389bd18761abdc1bae2c005587"],
                "Windows_x86": ["https://dl.google.com/android/repository/android-ndk-r17b-windows-x86.zip",
                                "c3422e060b3ea955516e86737bf4237b8482d59a"],
                "Macos_x86_64": ["https://dl.google.com/android/repository/android-ndk-r17b-darwin-x86_64.zip",
                                 "2070c9a5799671e34b88d383a93af255a5ea260d"],
                "Linux_x86_64": ["https://dl.google.com/android/repository/android-ndk-r17b-linux-x86_64.zip",
                                 "2ac2e8e1ef73ed551cac3a1479bb28bd49369212"]
        }

        try:
            url, sha1 = urls.get("%s_%s" % (self.options.host_os, self.options.host_arch))
        except KeyError:
            raise Exception("Not supported OS or architecture: ")

        tools.download(url, "ndk.zip")
        #tools.check_sha1("ndk.zip", sha1)
        tools.unzip("ndk.zip", keep_permissions=True)
        unlink("ndk.zip")

    @property
    def zip_folder(self):
        return "android-ndk-%s" % self.version

    def package(self):
        self.copy("*", dst="", src=self.zip_folder, keep_path=True)

    def package_info(self):
        tools_path = os.path.join("build", "tools")
        self.cpp_info.bindirs.append(tools_path)
        self.env_info.PATH.append(os.path.join(self.package_folder, tools_path))