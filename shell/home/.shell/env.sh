# Homebrew
export PATH=/usr/local/bin:${PATH}:/usr/local/sbin

# Android
export ANDROID_HOME=${HOME}/Library/Android/sdk
export PATH=${PATH}:${ANDROID_HOME}/tools
export PATH=${PATH}:${ANDROID_HOME}/platform-tools
export PATH=${PATH}:/usr/local/opt/llvm/bin

# macOS has weird TMPDIR settings by default
export TMPDIR=/tmp

# Default compilers to use
export CXX=mpicxx
export CC=mpicc
# TODO: Only Mac
# export OMPI_CXX=g++-7

