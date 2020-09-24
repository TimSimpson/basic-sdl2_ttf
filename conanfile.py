
import os.path
import shutil

import conans
from conans import tools


class GzipDownloader:

    def __init__(self, base_name, url, md5_sum):
        self._base_name = base_name
        self._url = url
        self._md5_sum = md5_sum
        self._gzip_name = "{}.tar.gz".format(self._base_name)

    def _get_gzip_path(self, folder):
        return os.path.join(folder, self._gzip_name)

    def get_extracted_directory(self, folder):
        return os.path.join(folder, self._base_name)

    def _confirm_valid_gzip_file_or_download(self, folder):
        gzip_path = self._get_gzip_path(folder)
        if os.path.exists(gzip_path):
            try:
                tools.check_md5(gzip_path, self._md5_sum)
                return gzip_path
            except BaseException:
                os.remove(gzip_path)

        tools.download(self._url, gzip_path)
        tools.check_md5(gzip_path, self._md5_sum)
        return gzip_path

    def _clean_extracted_directory(self, folder):
        extracted_directory = self.get_extracted_directory(folder)
        if os.path.exists(extracted_directory):
            shutil.rmtree(extracted_directory)

    def download(self, folder):
        gzip_path = self._confirm_valid_gzip_file_or_download(folder)
        self._clean_extracted_directory(folder)
        tools.unzip(gzip_path)


class BasicSdl(conans.ConanFile):
    name = "sdl2_ttf"
    version = "b_2.0.15"
    license = ""
    author = ""
    description = "A basic version of the SDL2 TTF library"

    settings = "os", "compiler", "build_type", "arch"

    requires = (
        "sdl2/b_2.0.9@TimSimpson/testing",
    )

    options = {
        "fPIC": [True, False],
        "shared": [True, False],
    }
    default_options = {
        "fPIC": True,
        "shared": False
    }

    _gzip_downloader = GzipDownloader(
        base_name='SDL2_ttf-2.0.15',
        url="https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.15.tar.gz",
        md5_sum="04fe06ff7623d7bdcb704e82f5f88391"
    )

    def source(self):
        self._gzip_downloader.download(self.source_folder)

    def build(self):
        src = self._gzip_downloader.get_extracted_directory(self.source_folder)
        with tools.chdir(self.build_folder):
            atools = conans.AutoToolsBuildEnvironment(self)
            atools.configure(configure_dir=src)
            atools.make()
            atools.install()

    def package(self):
        built_packages = os.path.join(self.build_folder, "package")
        self.copy("*", src=built_packages)

    def package_info(self):
        self.cpp_info.name = "sdl2_ttf"
        self.cpp_info.libs = ["SDL2_ttf"]
        self.cpp_info.includedirs.append(os.path.join("include", "SDL2"))
