%define major	0
%define libname	%mklibname esound %{major}

Summary:	The Enlightened Sound Daemon
Name:		esound
Version: 0.2.38
Release: %mkrel 1
License:	LGPL
Group:		System/Servers

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/esound/esound-%{version}.tar.bz2
# (fc) 0.2.28 default options : increase spawn process waiting time, release device after 2s of inactivity
Patch0:		esound-0.2.37-defaultoptions.patch
# (fc) 0.2.28-3mdk don't add -L/usr/lib to ldflags
Patch2:		esound-0.2.35-libdir.patch
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

%package -n %{libname}
Summary: Libraries for EsounD
Group: System/Libraries
Provides: libesound
Requires: esound >= %{version}-%{release}

%description -n %{libname}
These are the libraries for EsounD.

%package -n %{libname}-devel
Summary:	Includes and more to develop EsounD applications
Group:		Development/C
Requires:	%{name} = %{version}
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
%patch2 -p1 -b .libdir

%build

%configure2_5x --with-libwrap --disable-alsa
%make

%install
rm -rf %buildroot installed-docs
%makeinstall_std
mv %buildroot%_datadir/doc/esound installed-docs

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc installed-docs/*
%doc AUTHORS INSTALL NEWS README TIPS TODO
%config(noreplace) %{_sysconfdir}/esd.conf
%{_bindir}/esd
%{_bindir}/esdcat
%{_bindir}/esdctl
%{_bindir}/esddsp
%{_bindir}/esdfilt
%{_bindir}/esdloop
%{_bindir}/esdmon
%{_bindir}/esdplay
%{_bindir}/esdrec
%{_bindir}/esdsample
%{_mandir}/man1/esd.1*
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


