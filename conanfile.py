import os

from conan import ConanFile
from conan.tools.files import copy, collect_libs
from conan.tools.gnu import Autotools, AutotoolsToolchain


class OpenCVRecipe(ConanFile):
    name = "opencv"
    version = "1.1.0"
    package_type = "library"
    user = "soleil"

    license = "Intel Open Source Computer Vision Library License"
    author = "Intel Corporation"
    url = "https://github.com/opencv/opencv"
    description = "OpenCV 1.1.0 computer vision library"
    topics = ("computer-vision", "image-processing", "autotools")

    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": False,
    }

    exports_sources = "*"

    def generate(self):
        toolchain = AutotoolsToolchain(self)
        toolchain.generate()

    def build(self):
        configure_args = [
            "--enable-shared={}".format("yes" if self.options.shared else "no"),
            "--enable-sse2=yes",
            "--enable-openmp=no",
            "--enable-apps=no",
            "--with-swig=no",
            "--with-python=no",
            "--with-octave=no",
            "--with-gtk=no",
            "--with-gthread=no",
            "--with-v4l=no",
            "--with-gstreamer=no",
            "--with-ffmpeg=no",
            "--with-xine=no",
            "--with-1394libs=no",
            "--with-unicap=no",
            "--with-imageio=no",
            "--with-quicktime=no",
            "--with-carbon=no",
        ]
        autotools = Autotools(self)
        autotools.configure(args=configure_args)
        autotools.make()

    def package(self):
           copy(self, "*.so*", src=self.build_folder,
               dst=os.path.join(self.package_folder, "lib"), keep_path=False)
           copy(self, "*.a", src=self.build_folder,
               dst=os.path.join(self.package_folder, "lib"), keep_path=False)

           for include_dir in ("cxcore/include", "cv/include", "cvaux/include",
                           "ml/include", "otherlibs/highgui"):
              copy(self, "*.h", src=os.path.join(self.source_folder, include_dir),
                  dst=os.path.join(self.package_folder, "include"),
                  keep_path=False)
              copy(self, "*.hpp", src=os.path.join(self.source_folder, include_dir),
                  dst=os.path.join(self.package_folder, "include"),
                  keep_path=False)

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
