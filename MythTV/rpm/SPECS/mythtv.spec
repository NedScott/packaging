#
# This spec file was split from the original
# larger mythtv spec file.  This work builds
# on previous works from (at least):
#
#    Chris Petersen <cpetersen@mythtv.org>
#    Jarod Wilson <jarod@wilsonet.com>
#    Richard Shaw <hobbes1069@gmail.com>
#    Axel Thimm <Axel.Thimm@ATrpms.net>
#    David Bussenschutt <buzz@oska.com>
#    Nicolas Chauvet <kwizart@gmail.com>
#    Sérgio Basto <sergio@serjux.com>
#    Adrian Reber <adrian@lisas.de>
#    Xavier Bachelot <xavier@bachelot.org>
#    Paul Howarth <paul@city-fan.org>
#

%global _hardened_build 1

# Basic descriptive tags for this package:
Name:           mythtv
Summary:        A digital video recorder (DVR) application
URL:            http://www.mythtv.org/

#
# Specify the commit hash for the source for this rpm
#
%global commit  %{?MYTHTV_COMMIT}%{!?MYTHTV_COMMIT:0}

# Version/Release info
Version:        %{?MYTHTV_VERSION}%{!?MYTHTV_VERSION:0.0}
Release:        100%{?dist}

# The primary license is GPLv2+, but bits are borrowed from a number of
# projects... For a breakdown of the licensing, see PACKAGE-LICENSING.
License:        GPLv2+ and LGPLv2+ and LGPLv2 and (GPLv2 or QPL) and (GPLv2+ or LGPLv2+)

################################################################################

# The following options are disabled by default.  Use --with to enable them
%define with_llvm           %{?_with_llvm:           1} %{?!_with_llvm:           0}

################################################################################

# Source based on commit hash
Source0:        https://github.com/MythTV/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

Source200:      mythtv-mythbackend.service
Source201:      mythtv-99-mythbackend.rules
Source202:      mythtv-logrotate.conf
Source203:      mythtv-mythjobqueue.service
Source204:      mythtv-mythmediaserver.service
Source210:      mythtv-mythbackend-tmpfiles.conf
Source220:      mythtv-LICENSING
Source300:      mythtv-mythfrontend.png
Source301:      mythtv-mythfrontend.desktop
Source302:      mythtv-mythtv-setup.png
Source303:      mythtv-mythtv-setup.desktop

# For el7, include software collections to get gcc 8
%if (0%{?rhel} == 7)
%if %{with_llvm}
BuildRequires:  llvm-toolset-7
%else
BuildRequires:  devtoolset-8
%endif
%endif

# Python prefix adjustments (python for rhel < 8 of fedora < 31, python3 for everything else)
%if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
%if (0%{?rhel})
%global py_prefix python
%else
%global py_prefix python2
%endif
%else
%global py_prefix python3
%endif

# Global MythTV and Shared Build Requirements

BuildRequires:  git
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
%if %{with_llvm}
BuildRequires:  llvm
BuildRequires:  clang
%else
BuildRequires:  gcc-c++
BuildRequires:  gcc
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel        >= 5.3
BuildRequires:  qt5-qtscript-devel      >= 5.3
BuildRequires:  qt5-qtwebkit-devel      >= 5.3
BuildRequires:  freetype-devel
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  mariadb-connector-c-devel
%else
BuildRequires:  mariadb-devel
%endif
%if ((0%{?fedora}) || ((0%{?rhel}) && (0%{?rhel} < 8)))
BuildRequires:  libcec-devel
%endif
BuildRequires:  libvpx-devel
BuildRequires:  lm_sensors-devel
BuildRequires:  lirc-devel
BuildRequires:  nasm

# X, and Xv video support
BuildRequires:  libXv-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  mesa-libGLU-devel
%ifarch %arm
BuildRequires:  mesa-libGLES-devel
%endif
BuildRequires:  xorg-x11-proto-devel

# OpenGL video output and vsync support
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel

# Misc A/V format support
BuildRequires:  fftw-devel
BuildRequires:  flac-devel
BuildRequires:  lame-devel
BuildRequires:  libcdio-devel
BuildRequires:  libcdio-paranoia-devel
BuildRequires:  libogg-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
BuildRequires:  taglib-devel
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  xvidcore-devel
BuildRequires:  exiv2-devel
BuildRequires:  nv-codec-headers
BuildRequires:  libaom-devel
%if ((0%{?fedora}) || (0%{?rhel} > 7))
BuildRequires:  libdav1d-devel
%endif
# (non-free) BuildRequires:  fdk-aac-devel

# External library support
BuildRequires:  hdhomerun-devel
%if ((0%{?fedora}) || ((0%{?rhel}) && (0%{?rhel} < 8)))
BuildRequires:  libbluray-devel
%endif
BuildRequires:  libsamplerate-devel
BuildRequires:  libXNVCtrl-devel
BuildRequires:  lzo-devel
BuildRequires:  minizip-devel

# Audio framework support
BuildRequires:  alsa-lib-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  avahi-compat-libdns_sd-devel

# Bluray support
BuildRequires:  libxml2-devel
#BuildRequires:  libudf-devel

# Subtitle support
BuildRequires:  libass-devel

# Need dvb headers to build in dvb support
BuildRequires:  kernel-headers

# FireWire cable box support
%if ((0%{?fedora}) || ((0%{?rhel}) && (0%{?rhel} < 8)))
BuildRequires:  libavc1394-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel
%endif

# HW video support
BuildRequires:  libvdpau-devel
BuildRequires:  libva-devel
BuildRequires:  libcrystalhd-devel
%if (0%{?fedora})
BuildRequires:  libomxil-bellagio-devel
%endif

# systemd ready and journald logging support
BuildRequires:  systemd-devel
BuildRequires:  systemd

# API Build Requirements
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(DBI)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(Net::UPnP::QueryResponse)
BuildRequires:  perl(Net::UPnP::ControlPoint)
BuildRequires:  perl(DBD::mysql)
BuildRequires:  perl(IO::Socket::INET6)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(XML::Simple)

BuildRequires:  %{py_prefix}
BuildRequires:  %{py_prefix}-pycurl
BuildRequires:  %{py_prefix}-lxml
BuildRequires:  %{py_prefix}-rpm-macros
BuildRequires:  %{py_prefix}-urlgrabber
BuildRequires:  %{py_prefix}-requests
BuildRequires:  %{py_prefix}-simplejson
BuildRequires:  %{py_prefix}-future

%if ((0%{?rhel}) && (0%{?rhel} < 8))
BuildRequires:  MySQL-python
%else
%if ((0%{?fedora}) || ((0%{?rhel}) && (0%{?rhel} < 8)))
BuildRequires:  %{py_prefix}-mysql
%endif
%endif
BuildRequires:  %{py_prefix}-devel


# python fixups
BuildRequires:  /usr/bin/pathfix.py



################################################################################
# Requirements for the mythtv meta package

Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-backend          = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-docs             = %{version}-%{release}
Requires:       mythtv-frontend         = %{version}-%{release}
Requires:       mythtv-setup            = %{version}-%{release}
Requires:       mythtv-mythwelcome      = %{version}-%{release}
Requires:       mythtv-mythshutdown     = %{version}-%{release}
Requires:       perl-MythTV             = %{version}-%{release}
Requires:       php-MythTV              = %{version}-%{release}
%if ((0%{?fedora}) || ((0%{?rhel}) && (0%{?rhel} < 8)))
Requires:       %{py_prefix}-MythTV     = %{version}-%{release}
%endif
Requires:       mythtv-mythffmpeg       = %{version}-%{release}
Requires:       mariadb
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Recommends:     xmltv
%endif

################################################################################

%description
MythTV provides a unified graphical interface for recording and viewing
television programs. Refer to the mythtv package for more information.

There are also several add-ons and themes available. In order to facilitate
installations with smart/apt-get/yum and other related package
resolvers this meta-package can be used to install all in one sweep.

MythTV implements the following DVR features, and more, with a
unified graphical interface:

- Basic 'live-tv' functionality. Pause/Fast Forward/Rewind "live" TV.
- Video compression using RTjpeg or MPEG-4, and support for DVB and
  hardware encoder cards/devices.
- Program listing retrieval using XMLTV
- Themable, semi-transparent on-screen display
- Electronic program guide
- Scheduled recording of TV programs
- Resolution of conflicts between scheduled recordings
- Basic video editing

################################################################################

%package docs
Summary:        MythTV documentation
BuildArch:      noarch

Requires:       mythtv-filesystem       = %{version}-%{release}

%description docs
MythTV documentation

################################################################################

%package devel
Summary:        Development files for mythtv

Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}
Requires:       mythtv-mythffmpeg-libs  = %{version}-%{release}

%description devel
MythTV development headers and libraries

################################################################################

%package filesystem
Summary:        Filesystem definitions for mythtv
BuildArch:      noarch

%description filesystem
MythTV filesystem directory definitions

################################################################################

%package libs
Summary:        Libraries providing mythtv support

Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-mythffmpeg-libs  = %{version}-%{release}
Requires:       qt5-qtbase-mysql

%description libs
MythTV run-time libraries

################################################################################

%package base-themes
Summary:        Core user interface themes for mythtv

Requires:       mythtv-filesystem       = %{version}-%{release}

%description base-themes
MythTV base themes for graphical applications

################################################################################

%package frontend
Summary:        Client component of mythtv (a DVR)

Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}
%if ((0%{?fedora}) || ((0%{?rhel}) && (0%{?rhel} < 8)))
Requires:       %{py_prefix}-MythTV     = %{version}-%{release}
%endif
Requires:       perl-MythTV             = %{version}-%{release}

%description frontend
MythTV frontend, a graphical interface for recording and
viewing television, video, and music content.

################################################################################

%package backend
Summary:        Server component of mythtv (a DVR)

Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}
Requires:       mythtv-mythffmpeg       = %{version}-%{release}
%if ((0%{?fedora}) || ((0%{?rhel}) && (0%{?rhel} < 8)))
Requires:       %{py_prefix}-MythTV     = %{version}-%{release}
%endif
Requires:       perl-MythTV             = %{version}-%{release}
Requires:       systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Recommends:     xmltv-grabbers
%endif

%description backend
MythTV backend, the server for video capture and content services.

################################################################################

%package setup
Summary:        Program to setup the MythTV backend

Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}
%if ((0%{?fedora}) || (0%{?rhel} > 7))
Recommends:     xmltv-grabbers
%endif

%description setup
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the setup software for configuring the
mythtv backend.

################################################################################

%package mythwelcome
Summary:        Program to shutdown and wakeup the MythTV backend

Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}

%description mythwelcome
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the mythwelcome software for
system shutdown and wakeup

################################################################################

%package mythshutdown
Summary:        Program to shutdown and wakeup the MythTV system

Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       mythtv-base             = %{version}-%{release}
Requires:       mythtv-base-themes      = %{version}-%{release}
Requires:       mythtv-libs             = %{version}-%{release}

%description mythshutdown
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the mythshutdown software for
system shutdown and wakeup

################################################################################

%package base
Summary:        Common components needed by multiple other MythTV components

Requires(pre):  shadow-utils
Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       logrotate
Requires:       google-droid-sans-mono-fonts
Requires:       google-droid-sans-fonts
Requires:       google-droid-serif-fonts
Requires:       perl(Date::Manip)
Requires:       perl(DateTime::Format::ISO8601)
Requires:       perl(Image::Size)
Requires:       perl(JSON)
Requires:       perl(LWP::Simple)
Requires:       perl(SOAP::Lite)
Requires:       perl(XML::Simple)
Requires:       perl(XML::XPath)

%description base
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains components needed by multiple other MythTV components.

################################################################################

%package mythffmpeg
Summary:        MythTV build of FFMpeg

Requires:       mythtv-mythffmpeg-libs  = %{version}-%{release}

%description mythffmpeg
MythTV FFMpeg utilities.

################################################################################

%package mythffmpeg-libs
Summary:        Libraries for MythTV build of FFMpeg

%description mythffmpeg-libs
MythTV FFMpeg libraries

################################################################################

%package -n perl-MythTV
Summary:        Perl bindings for MythTV
BuildArch:      noarch

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(IO::Socket::INET6)
Requires:       perl(Config)
Requires:       perl(DBD::mysql)
Requires:       perl(Net::UPnP)
Requires:       perl(Net::UPnP::ControlPoint)
Requires:       perl(File::Copy)
Requires:       perl(Sys::Hostname)
Requires:       perl(DBI)
Requires:       perl(HTTP::Request)
Requires:       perl(POSIX)
Requires:       perl(LWP::UserAgent)
Requires:       perl(Fcntl)
Requires:       perl(Exporter)

%description -n perl-MythTV
MythTV perl bindings

################################################################################

%package -n php-MythTV
Summary:        PHP bindings for MythTV
BuildArch:      noarch

Requires:       mythtv-filesystem       = %{version}-%{release}
Requires:       php-common

%description -n php-MythTV
MythTV PHP bindings

################################################################################

%if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
%package -n python2-MythTV
%else
%package -n python3-MythTV
%endif
Summary:        Python bindings for MythTV
BuildArch:      noarch

Requires:       %{py_prefix}-libs
Requires:       %{py_prefix}-lxml
Requires:       %{py_prefix}-future
Requires:       %{py_prefix}-urlgrabber
Requires:       %{py_prefix}-requests
Requires:       %{py_prefix}-simplejson
%if ((0%{?rhel}) && (0%{?rhel} < 8))
Requires:       MySQL-python
%else
%if ((0%{?fedora}) || ((0%{?rhel}) && (0%{?rhel} < 8)))
Requires:       %{py_prefix}-mysql
%endif
Requires:       %{py_prefix}-requests-cache
%endif

%if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
#
%else
Obsoletes:      python2-MythTV          <= %{version}-%{release}
%endif

%if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
%{?python_provide:%python_provide python2-MythTV}
%else
%{?python_provide:%python_provide python3-MythTV}
%endif

%if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
%description -n python2-MythTV
%else
%description -n python3-MythTV
%endif
MythTV python bindings

################################################################################

%prep

%autosetup -p1 -n %{name}-%{commit}

%if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
pathfix.py -pni "%{__python2} %{py2_shbang_opts}" .
%else
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .
%endif

################################################################################

%build

%if (0%{?rhel} == 7)
%if %{with_llvm}
source scl_source enable llvm-toolset-7 >/dev/null 2>/dev/null && true || true
%else
source scl_source enable devtoolset-8 >/dev/null 2>/dev/null && true || true
%endif
%endif

pushd mythtv

    # Similar to 'percent' configure, but without {_target_platform} and
    # {_exec_prefix} etc... MythTV no longer accepts the parameters that the
    # configure macro passes, so we do this manually.

    CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
    CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \

%if %{with_llvm}
    CFLAGS="${CFLAGS//-fstack-clash-protection}" ; export CFLAGS ;
    CXXFLAGS="${CXXFLAGS//-fstack-clash-protection}" ; export CXXFLAGS ;
%endif

    ./configure                                     \
%if %{with_llvm}
        --cc="clang"                                \
        --cxx="clang"                               \
%else
        --cc="gcc"                                  \
        --cxx="g++"                                 \
%endif
        --extra-cflags="${CFLAGS}"                  \
        --extra-cxxflags="${CXXFLAGS}"              \
        --prefix=%{_prefix}                         \
        --bindir=%{_bindir}                         \
        --libdir-name=%{_lib}                       \
        --compile-type=profile                      \
%if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
        --python=%{__python2}                       \
%else
        --python=%{__python3}                       \
%endif
        --perl-config-opts="INSTALLDIRS=vendor OPTIMIZE=\"$RPM_OPT_FLAGS\"" \
        --enable-libmp3lame                         \
        --enable-libx264                            \
        --enable-libx265                            \
        --enable-libxvid                            \
        --enable-libvpx

    make %{?_smp_mflags}

popd

################################################################################

%install

%if (0%{?rhel} == 7)
%if %{with_llvm}
source scl_source enable llvm-toolset-7 >/dev/null 2>/dev/null && true || true
%else
source scl_source enable devtoolset-8 >/dev/null 2>/dev/null && true || true
%endif
%endif

pushd mythtv

    make install                          INSTALL_ROOT=%{buildroot} -j 1

    # log and rotate configuration
    mkdir -p                              %{buildroot}%{_localstatedir}/log/mythtv
    mkdir -p                              %{buildroot}%{_sysconfdir}/logrotate.d
    install -m 0644 %{SOURCE202}          %{buildroot}%{_sysconfdir}/logrotate.d/mythtv

    # Remove mythffserver (removed with v30 commit d24aa851 for FFmpeg 4.0 merge,
    # and deprecated in earlier FFmpeg variants, so do not package it in any case)
    rm -f                                 %{buildroot}%{_bindir}/mythffserver

    # Remove mythhdhomerun_config (removed with v30 commit 4b577277 and the upstream
    # hdhomerun_config binary is available as part of all current distros packages)
    rm -f                                 %{buildroot}%{_bindir}/mythhdhomerun_config

    # Add in a dummy mythexternrecorder if not built for an older mythtv
    # (mythexternrecorder added in v30 commit 826d57e3, and backported to
    # later fixes/29)
    if [ ! -e "%{buildroot}%{_bindir}/mythexternrecorder" ] ; then
    touch                                 %{buildroot}%{_bindir}/mythexternrecorder
    fi

    # Insure various files/directories exist for optional feature builds
    if [ ! -e "%{buildroot}%{_bindir}/mythwikiscripts" ] ; then
    touch                                 %{buildroot}%{_bindir}/mythwikiscripts
    fi
    if [ ! -e "%{buildroot}%{_bindir}/mythpython" ] ; then
    touch                                 %{buildroot}%{_bindir}/mythpython
    fi
    %if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
    mkdir -p                              %{buildroot}%{python2_sitelib}/MythTV
    %else
    mkdir -p                              %{buildroot}%{python3_sitelib}/MythTV
    %endif
    mkdir -p                              %{buildroot}%{perl_vendorlib}/MythTV
    if [ ! -e "%{buildroot}%{perl_vendorlib}/MythTV.pm" ] ; then
    touch                                 %{buildroot}%{perl_vendorlib}/MythTV.pm
    fi
    mkdir -p                              %{buildroot}%{perl_vendorlib}/IO/Socket/INET
    if [ ! -e "%{buildroot}%{perl_vendorlib}/IO/Socket/INET/MythTV.pm" ] ; then
    touch                                 %{buildroot}%{perl_vendorlib}/IO/Socket/INET/MythTV.pm
    fi
    mkdir -p                              %{buildroot}%{_datadir}/mythtv/bindings/php
    mkdir -p                              %{buildroot}%{_datadir}/mythtv/hardwareprofile
    mkdir -p                              %{buildroot}%{_datadir}/mythtv/metadata
    mkdir -p                              %{buildroot}%{_datadir}/mythtv/internetcontent

    # Add in dummy filters directory if not installed as future merge
    # (from render branch) will be deleting filters directory
    mkdir -p                              %{buildroot}%{_libdir}/mythtv/filters

    # Add in dummy externrecorder if not installed
    mkdir -p                              %{buildroot}%{_datadir}/%{name}/externrecorder

    # dir for backend, and starter config.xml
    mkdir -p %{buildroot}%{_localstatedir}/lib/mythtv/.mythtv
    install -m 0644 contrib/config_files/config.xml \
                                          %{buildroot}%{_localstatedir}/lib/mythtv/.mythtv/config.xml

    # docs
    mkdir -p                              %{buildroot}%{_datadir}/doc/%{name}
    install -m 0644 README*               %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 UPGRADING             %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 AUTHORS               %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 COPYING               %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 FAQ                   %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 keys.txt              %{buildroot}%{_datadir}/doc/%{name}/
    install -m 0644 %{SOURCE220}          %{buildroot}%{_datadir}/doc/%{name}/LICENSING
    cp -r           data                  %{buildroot}%{_datadir}/doc/%{name}/
    cp -r           database              %{buildroot}%{_datadir}/doc/%{name}/
    cp -r           contrib               %{buildroot}%{_datadir}/doc/%{name}/
    # turn off execute bits for any docs (to keep build happy)
    find                                  %{buildroot}%{_datadir}/doc/%{name}/ \
                                          -type f -executable -exec chmod -x {} \;
    # tmpfiledir
    mkdir -p                              %{buildroot}%{_tmpfilesdir}
    install -m 0644 %{SOURCE210}          %{buildroot}%{_tmpfilesdir}/mythbackend.conf

    # systemd config
    mkdir -p -m 0755                      %{buildroot}%{_unitdir}
    install -m 0644 %{SOURCE200}          %{buildroot}%{_unitdir}/mythbackend.service
    install -m 0644 %{SOURCE203}          %{buildroot}%{_unitdir}/mythjobqueue.service
    install -m 0644 %{SOURCE204}          %{buildroot}%{_unitdir}/mythmediaserver.service

    # Install udev rules for devices that may initialize late in the boot
    # process so they are available for mythbackend.
    mkdir -p                              %{buildroot}%{_udevrulesdir}
    install -m 0644 %{SOURCE201}          %{buildroot}%{_udevrulesdir}/99-mythbackend.rules

    # devel
    mkdir -p                              %{buildroot}%{_datadir}/%{name}/build/
    install -m 0644 settings.pro          %{buildroot}%{_datadir}/%{name}/build/

    # Desktop entries
    mkdir -p                              %{buildroot}%{_datadir}/pixmaps
    mkdir -p                              %{buildroot}%{_datadir}/applications
    install -m 0644 %{SOURCE300}          %{buildroot}%{_datadir}/pixmaps/mythfrontend.png
    install -m 0644 %{SOURCE301}          %{buildroot}%{_datadir}/applications/mythfrontend.desktop
    desktop-file-validate                 %{buildroot}%{_datadir}/applications/mythfrontend.desktop
    install -m 0644 %{SOURCE302}          %{buildroot}%{_datadir}/pixmaps/mythtv-setup.png
    install -m 0644 %{SOURCE303}          %{buildroot}%{_datadir}/applications/mythtv-setup.desktop
    desktop-file-validate                 %{buildroot}%{_datadir}/applications/mythtv-setup.desktop

    # remove unnecessary packaging/SCM files
    find %{buildroot} -name .gitignore -delete >/dev/null
    find %{buildroot} -name .packlist -delete >/dev/null

    %{_fixperms} %{buildroot}

popd

################################################################################

%pre base
# Add the "mythtv" user, with membership in the audio and video group
getent group mythtv >/dev/null || groupadd -r mythtv
getent passwd mythtv >/dev/null || \
    useradd -r -g mythtv \
    -d "/var/lib/mythtv" -s /bin/sh \
    -c "mythbackend user" mythtv
for group in 'video' 'audio' 'cdrom' 'dialout'
{
    ent=`getent group $group 2>/dev/null`
    # only proceed if the group exists
    if [ $? -eq 0 ]; then
        cnt=`echo "$ent" | cut -d: -f4 | tr ',' '\n' | grep -c '^mythtv$'`
        cnt=$(($cnt + 0))
        if [ $cnt -lt 1 ]; then
            usermod -a -G $group mythtv
        fi
    fi
}
exit 0

%if (0%{?rhel} == 7)
%post libs -p /sbin/ldconfig
%endif

%if (0%{?rhel} == 7)
%post mythffmpeg-libs -p /sbin/ldconfig
%endif

%post backend
    %systemd_post mythbackend.service
    %systemd_post mythjobqueue.service
    %systemd_post mythmediaserver.service

%preun backend
    %systemd_preun mythbackend.service
    %systemd_preun mythjobqueue.service
    %systemd_preun mythmediaserver.service

%if (0%{?rhel} == 7)
%postun libs -p /sbin/ldconfig
%endif

%if (0%{?rhel} == 7)
%postun mythffmpeg-libs -p /sbin/ldconfig
%endif

%postun backend
    %systemd_postun_with_restart mythbackend.service
    %systemd_postun_with_restart mythjobqueue.service
    %systemd_postun_with_restart mythmediaserver.service

################################################################################


%files
%defattr(0644, root, root, 0755)


%files docs
%defattr(0644, root, root, 0755)
%{_datadir}/doc/%{name}


%files devel
%defattr(0644, root, root, 0755)
%{_libdir}/libmyth*.so
%{_includedir}/%{name}
%{_datadir}/mythtv/build


%files base
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/locales
%{_datadir}/mythtv/hardwareprofile
%{_datadir}/mythtv/i18n
%{_datadir}/mythtv/fonts
%defattr(-, root, root, 0755)
%{_datadir}/mythtv/metadata
%defattr(0644, root, root, 0755)
%config(noreplace) %{_sysconfdir}/logrotate.d/mythtv
%attr(0755, mythtv, mythtv) %dir %{_localstatedir}/log/mythtv
%defattr(0755, root, root, 0755)
%{_bindir}/mythccextractor
%{_bindir}/mythcommflag
%{_bindir}/mythpreviewgen
%{_bindir}/mythtranscode
%{_bindir}/mythmetadatalookup
%{_bindir}/mythutil
%{_datadir}/mythtv/mythconverg*.pl
%attr(0755, mythtv, mythtv) %dir %{_localstatedir}/lib/mythtv
%attr(0755, mythtv, mythtv) %dir %{_localstatedir}/lib/mythtv/.mythtv
%attr(0644, mythtv, mythtv) %config(noreplace) %{_localstatedir}/lib/mythtv/.mythtv/config.xml


%files filesystem
%defattr(0644, root, root, 0755)
%dir %{_datadir}/mythtv
%dir %{_datadir}/mythtv/bindings


%files libs
%defattr(0755, root, root, 0755)
%{_libdir}/libmyth*.so.*
%exclude %{_libdir}/libmythavdevice.*
%exclude %{_libdir}/libmythavfilter.*
%exclude %{_libdir}/libmythavformat.*
%exclude %{_libdir}/libmythavcodec.*
%exclude %{_libdir}/libmythpostproc.*
%exclude %{_libdir}/libmythswresample.*
%exclude %{_libdir}/libmythswscale.*
%exclude %{_libdir}/libmythavutil.*
%{_libdir}/mythtv/filters
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/MXML_scpd.xml
%{_datadir}/mythtv/CDS_scpd.xml
%{_datadir}/mythtv/CMGR_scpd.xml
%{_datadir}/mythtv/MSRR_scpd.xml


%files backend
%defattr(0755, root, root, 0755)
%{_bindir}/mythbackend
%{_bindir}/mythexternrecorder
%{_bindir}/mythfilldatabase
%{_bindir}/mythfilerecorder
%{_bindir}/mythjobqueue
%{_bindir}/mythmediaserver
%{_bindir}/mythreplex
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/backend-config/
%{_unitdir}/mythbackend.service
%{_unitdir}/mythjobqueue.service
%{_unitdir}/mythmediaserver.service
%{_udevrulesdir}/99-mythbackend.rules
%{_datadir}/mythtv/internetcontent
%{_datadir}/mythtv/html
%{_datadir}/mythtv/externrecorder
%{_tmpfilesdir}/*
%{_datadir}/mythtv/devicemaster.xml
%{_datadir}/mythtv/deviceslave.xml


%files setup
%defattr(0755, root, root, 0755)
%{_bindir}/mythtv-setup
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/setup.xml
%{_datadir}/pixmaps/mythtv-setup.png
%{_datadir}/applications/mythtv-setup.desktop


%files frontend
%defattr(0755, root, root, 0755)
%{_bindir}/mythavtest
%{_bindir}/mythfrontend
%{_bindir}/mythlcdserver
%{_bindir}/mythscreenwizard
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/MFEXML_scpd.xml
%{_datadir}/pixmaps/mythfrontend.png
%{_datadir}/applications/mythfrontend.desktop


%files mythshutdown
%defattr(0755, root, root, 0755)
%{_bindir}/mythshutdown


%files mythwelcome
%defattr(0755, root, root, 0755)
%{_bindir}/mythwelcome


%files base-themes
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/themes


%files mythffmpeg
%defattr(0755, root, root, 0755)
%attr(0755, root, root) %{_bindir}/mythffmpeg
%attr(0755, root, root) %{_bindir}/mythffprobe


%files mythffmpeg-libs
%defattr(0755, root, root, 0755)
%{_libdir}/libmythavdevice.so.*
%{_libdir}/libmythavfilter.so.*
%{_libdir}/libmythavformat.so.*
%{_libdir}/libmythavcodec.so.*
%{_libdir}/libmythpostproc.so.*
%{_libdir}/libmythswresample.so.*
%{_libdir}/libmythswscale.so.*
%{_libdir}/libmythavutil.so.*


%files -n perl-MythTV
%defattr(0644, root, root, 0755)
%{perl_vendorlib}/MythTV
%{perl_vendorlib}/MythTV.pm
%{perl_vendorlib}/IO/Socket/INET/MythTV.pm


%files -n php-MythTV
%defattr(0644, root, root, 0755)
%{_datadir}/mythtv/bindings/php


%if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
%files -n python2-MythTV
%else
%files -n python3-MythTV
%endif
%defattr(0644, root, root, 0755)
%attr(0755, root, root) %{_bindir}/mythpython
%attr(0755, root, root) %{_bindir}/mythwikiscripts
%if (((0%{?fedora}) && (0%{?fedora} < 31)) || ((0%{?rhel}) && (0%{?rhel} < 8)))
%{python2_sitelib}/*
%else
%{python3_sitelib}/*
%endif


################################################################################


%changelog

* Wed May 09 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com>
- Rework for managed rebuilds

