%define major	0
%define libname	%mklibname esound %{major}

Summary:	The Enlightened Sound Daemon
Name:		esound
Version: 0.2.38
Release: %mkrel 6
License:	LGPL
Group:		System/Servers

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/esound/esound-%{version}.tar.bz2
# (fc) 0.2.28 default options : increase spawn process waiting time, release device after 2s of inactivity
Patch0:		esound-0.2.37-defaultoptions.patch
# (fc) 0.2.28-3mdk don't add -L/usr/lib to ldflags (GNOME bug #435652)
Patch2:		esound-multilib.patch
# (fc) 0.2.38-2mdv protect dsp_init with a mutex to prevent race conditions from multiple calls (Ubuntu)
Patch3:		esound-0.2.38-preventlock.patch
# (cg) 0.2.38-4mdk multi-user patch for esd to assume the socket path is /tmp/.esd-$USER/socket
Patch4: 	esound-0.2.38-multi-user.patch
URL:		ftp://ftp.gnome.org/pub/GNOME/sources/esound/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: audiofile-devel
BuildRequires: docbook-utils docbook-dtd31-sgml

%description
EsounD (the Enlightened Sound Daemon) is a server process that allows multiple
applications to share a single sound card. For example, when you're listening
to music from your CD and you receive a sound-related event from ICQ, your
applications won't have to jockey for the attention of your sound card.

EsounD mixes several audio streams for playback by a single audio device.

%package daemon
Summary: Original EsounD daemon (now superceeded by PulseAudio)
Group: Sound
Provides: esound = %{version}-%{release}

%description daemon
The original EsounD daemon (now superceeded by PulseAudio)

%package utils
Summary: Utilities for EsounD
Group: Sound

%description utils
Utility applications for EsounD

%package -n %{libname}
Summary: Libraries for EsounD
Group: System/Libraries
Provides: libesound
Requires: esound

%description -n %{libname}
These are the libraries for EsounD.

%package -n %{libname}-devel
Summary:	Includes and more to develop EsounD applications
Group:		Development/C
Requires:	audiofile-devel 
Requires:	%{libname} = %{version}
Provides: 	libesound-devel
Provides:	esound-devel
Obsoletes:  esound-devel

%description -n %{libname}-devel
Libraries, include files and other resources you can use to develop EsounD
applications.

%prep
%setup -q
%patch0 -p1 -b .defaultoptions
%patch2 -p1 -b .multilib
%patch3 -p1 -b .preventlock
%patch4 -p1 -b .multiuser

%build

%configure2_5x --with-libwrap --disable-alsa
%make

%install
rm -rf %buildroot installed-docs
%makeinstall_std
mv %buildroot%_datadir/doc/esound installed-docs

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files daemon
%config(noreplace) %{_sysconfdir}/esd.conf
%{_bindir}/esd
%{_mandir}/man1/esd.1*

%files utils
%defattr(-, root, root)
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
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%{_bindir}/esd-config
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/*a
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man1/esd-config.1*


