%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-ros-core
Version:        0.10.0
Release:        3%{?dist}%{?release_suffix}
Summary:        ROS ros_core package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-rolling-ament-cmake
Requires:       ros-rolling-ament-cmake-auto
Requires:       ros-rolling-ament-cmake-gmock
Requires:       ros-rolling-ament-cmake-gtest
Requires:       ros-rolling-ament-cmake-pytest
Requires:       ros-rolling-ament-cmake-ros
Requires:       ros-rolling-ament-index-cpp
Requires:       ros-rolling-ament-index-python
Requires:       ros-rolling-ament-lint-auto
Requires:       ros-rolling-ament-lint-common
Requires:       ros-rolling-class-loader
Requires:       ros-rolling-common-interfaces
Requires:       ros-rolling-launch
Requires:       ros-rolling-launch-ros
Requires:       ros-rolling-launch-testing
Requires:       ros-rolling-launch-testing-ament-cmake
Requires:       ros-rolling-launch-testing-ros
Requires:       ros-rolling-launch-xml
Requires:       ros-rolling-launch-yaml
Requires:       ros-rolling-pluginlib
Requires:       ros-rolling-rcl-lifecycle
Requires:       ros-rolling-rclcpp
Requires:       ros-rolling-rclcpp-action
Requires:       ros-rolling-rclcpp-lifecycle
Requires:       ros-rolling-rclpy
Requires:       ros-rolling-ros-environment
Requires:       ros-rolling-ros2cli-common-extensions
Requires:       ros-rolling-ros2launch
Requires:       ros-rolling-rosidl-default-generators
Requires:       ros-rolling-rosidl-default-runtime
Requires:       ros-rolling-sros2
Requires:       ros-rolling-sros2-cmake
Requires:       ros-rolling-ros-workspace
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
A package to aggregate the packages required to use publish / subscribe,
services, generate messages and other core ROS concepts.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Tue Feb 20 2024 Steven! Ragnarök <steven@openrobotics.org> - 0.10.0-3
- Autogenerated by Bloom

