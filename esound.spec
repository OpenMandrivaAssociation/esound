%define major	0
%define libname	%mklibname esound %{major}
%define devname %mklibname esound -d

Summary:	The Enlightened Sound Daemon
Name:		esound
Version:	0.2.41
Release:	9
License:	LGPLv2+
Group:		System/Servers
Url:		ftp://ftp.gnome.org/pub/GNOME/sources/esound/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/esound/esound-%{version}.tar.bz2
# (fc) 0.2.28 default options : increase spawn process waiting time, release device after 2s of inactivity
Patch0:		esound-0.2.37-defaultoptions.patch

BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-utils
BuildRequires:	pkgconfig(audiofile)

%description
EsounD (the Enlightened Sound Daemon) is a server process that allows multiple
applications to share a single sound card. For example, when you're listening
to music from your CD and you receive a sound-related event from ICQ, your
applications won't have to jockey for the attention of your sound card.

EsounD mixes several audio streams for playback by a single audio device.

%package utils
Summary:	Utilities for EsounD
Group:		Sound

%description utils
Utility applications for EsounD

%package -n %{libname}
Summary:	Libraries for EsounD
Group:		System/Libraries
Provides:	libesound

%description -n %{libname}
These are the libraries for EsounD.

%package -n %{devname}
Summary:	Includes and more to develop EsounD applications
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel

%description -n %{devname}
Libraries, include files and other resources you can use to develop EsounD
applications.

%prep
%setup -q
%autopatch -p1

%build
%configure2_5x \
	--disable-static \
	--with-libwrap \
	--disable-alsa

%make LIBS='-lm'

%install
%makeinstall_std
mv %{buildroot}%_datadir/doc/esound installed-docs

# (cg) We no longer ship the actual deamon - PulseAudio does this these days
rm -f %{buildroot}%{_sysconfdir}/esd.conf \
	%{buildroot}%{_bindir}/esd \
	%{buildroot}%{_mandir}/man1/esd.1*

%files utils
%doc installed-docs/*
%doc AUTHORS INSTALL NEWS README TIPS TODO
%{_bindir}/esdcat
%{_bindir}/esdctl
%{_bindir}/esddsp
%{_bindir}/esdfilt
%{_bindir}/esdloop
%{_bindir}/esdmon
%{_bindir}/esdplay
%{_bindir}/esdrec
%{_bindir}/esdsample
%{_mandir}/man1/esd[a-z]*

%files -n %{libname}
%{_libdir}/libesd.so.%{major}
%{_libdir}/libesd.so.%{major}.2.39
%{_libdir}/libesddsp.so.%{major}
%{_libdir}/libesddsp.so.%{major}.2.39


%files -n %{devname}
%{_bindir}/esd-config
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man1/esd-config.1*

