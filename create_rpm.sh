#!/bin/bash

# Stop on first error
set -e

PACKAGEVERSION=${PACKAGEVERSION:-$TRAVIS_BUILD_NUMBER}
export PACKAGEVERSION

if [ -z "$VERSION" ]; then
    echo "VERSION is missing"
    exit 1
fi

if [ -z "$PACKAGEVERSION" ]; then
    echo "PACKAGEVERSION is missing"
    exit 1
fi

# Prepare for rpm-build
mkdir -p rpm-build
pushd rpm-build
mkdir -p _build

# Create directories
mkdir -p opt/insight-reporting-framework
mkdir -p var/log/insight-reporting-framework
mkdir -p etc/palette-insight-server

# Copy the package contents
cp -v ../*.py opt/insight-reporting-framework
cp -v ../requirements.txt opt/insight-reporting-framework
cp -v ../*.sh opt/insight-reporting-framework
cp -v ../reporting-framework-config.yml etc/palette-insight-server
cp -v ../reporting-framework-delta-config.yml etc/palette-insight-server
cp -v ../scripts/* opt/insight-reporting-framework

echo "BUILDING VERSION:v$VERSION"

# build the rpm
rpmbuild -bb --buildroot $(pwd) --define "version $VERSION" --define "buildrelease $PACKAGEVERSION" --define "_rpmdir $(pwd)/_build" ../insight-reporting-framework.spec
popd
