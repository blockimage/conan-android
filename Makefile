ndk-build:
	conan create android-ndk block/testing

toolchain-build:
	conan create android-toolchain block/testing -pr ./armeabi-clang
	conan create android-toolchain block/testing -pr ./arm64a-clang
	conan create android-toolchain block/testing -pr ./armeabi-gcc
	conan create android-toolchain block/testing -pr ./arm64a-gcc

gtest:
	conan create libgtest block/testing -pr ./armeabi-clang
	conan create libgtest block/testing -pr ./arm64a-clang
	conan create libgtest block/testing -pr ./armeabi-gcc
	conan create libgtest block/testing -pr ./arm64a-clang

