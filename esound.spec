%define major	0
%define libname	%mklibname esound %{major}
%define develname %mklibname esound -d

Summary:	The Enlightened Sound Daemon
Name:		esound
Version:	0.2.41
Release:	9
License:	LGPLv2+
Group:		System/Servers
URL:		ftp://ftp.gnome.org/pub/GNOME/sources/esound/

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/esound/esound-%{version}.tar.bz2
# (fc) 0.2.28 default options : increase spawn process waiting time, release device after 2s of inactivity
Patch0:		esound-0.2.37-defaultoptions.patch

BuildRequires:	pkgconfig(audiofile)
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd412-xml

%description
EsounD (the Enlightened Sound Daemon) is a server process that allows multiple
applications to share a single sound card. For example, when you're listening
to music from your CD and you receive a sound-related event from ICQ, your
applications won't have to jockey for the attention of your sound card.

EsounD mixes several audio streams for playback by a single audio device.

%package utils
Summary:	Utilities for EsounD
Group:		Sound
Requires:	%{libname} = %{version}-%{release}

%description utils
Utility applications for EsounD

%package -n %{libname}
Summary:	Libraries for EsounD
Group:		System/Libraries
Provides:	libesound

%description -n %{libname}
These are the libraries for EsounD.

%package -n %{develname}
Summary:	Includes and more to develop EsounD applications
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	esound-devel

%description -n %{develname}
Libraries, include files and other resources you can use to develop EsounD
applications.

%prep
%setup -q
%patch0 -p1 -b .defaultoptions

%build

%configure2_5x \
	--disable-static \
	--with-libwrap \
	--disable-alsa

%make LIBS='-lm'

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std
mv %{buildroot}%_datadir/doc/esound installed-docs

# (cg) We no longer ship the actual deamon - PulseAudio does this these days
rm -f %{buildroot}%{_sysconfdir}/esd.conf %{buildroot}%{_bindir}/esd %{buildroot}%{_mandir}/man1/esd.1*

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
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%{_bindir}/esd-config
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man1/esd-config.1*



%changelog
* Wed Nov 16 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.2.41-6
+ Revision: 731110
- added build fix for missing DSO symbol to libm
- rebuild
  cleaned up spec
  removed defattr
  removed clean section
  disabled static build
  removed old ldconfig scriptlets
  removed req for esound by lib pkg
  removed unnecessary provides & reqs in devel pkg
  converted BR to pkgconfig provide
  removed BuildRoot
  removed mkrel

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.41-5
+ Revision: 664149
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.41-4mdv2011.0
+ Revision: 605105
- rebuild

* Sun Feb 21 2010 Colin Guthrie <cguthrie@mandriva.org> 0.2.41-3mdv2010.1
+ Revision: 509045
- Do not package the daemon as this is now provided by PulseAudio

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.2.41-2mdv2010.0
+ Revision: 424388
- rebuild

* Wed Nov 19 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.41-1mdv2009.1
+ Revision: 304366
- new version
- drop patch 3

* Wed Sep 03 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.40-1mdv2009.0
+ Revision: 279958
- new version
- drop patch 1

  + Emmanuel Andry <eandry@mandriva.org>
    - apply devel policy
    - check major

* Wed Jul 16 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.39-1mdv2009.0
+ Revision: 236263
- fix buildrequires
- new version
- update license
- drop patches 2,4
- patch to make it build

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.2.38-7mdv2009.0
+ Revision: 220727
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Feb 07 2008 Frederic Crozat <fcrozat@mandriva.com> 0.2.38-6mdv2008.1
+ Revision: 163719
- update patch4 to fix memory leak (Ubuntu)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 12 2007 Frederic Crozat <fcrozat@mandriva.com> 0.2.38-5mdv2008.1
+ Revision: 117849
- Add missing dependencies

* Sat Dec 08 2007 Colin Guthrie <cguthrie@mandriva.org> 0.2.38-4mdv2008.1
+ Revision: 116534
- Split package into daemon and utils subpackages
- Add multi-user patch (changes default socket path

* Fri Nov 16 2007 Frederic Crozat <fcrozat@mandriva.com> 0.2.38-3mdv2008.1
+ Revision: 109069
- Update patch2 with Fedora version and add bug number for it

* Fri Sep 21 2007 Frederic Crozat <fcrozat@mandriva.com> 0.2.38-2mdv2008.0
+ Revision: 91771
- Update patch0 : lower sound card release to 1s inactivity
- Patch3 (Ubuntu): protect dsp_init with a mutex to prevent race conditions from multiple calls

* Fri May 04 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.38-1mdv2008.0
+ Revision: 22230
- new version
- drop patch 3


* Sat Mar 31 2007 Frederic Crozat <fcrozat@mandriva.com> 0.2.37-3mdv2007.1
+ Revision: 150022
- Update patch0: release audio device after 2s inactivity when esd is started
  manually too (Mdv bug #30006)

* Mon Mar 19 2007 Frederic Crozat <fcrozat@mandriva.com> 0.2.37-2mdv2007.1
+ Revision: 146409
- Patch3 (SVN): fix 99%% cpu and fd leaks (Mdv bug #29640)

  + Thierry Vignaud <tvignaud@mandriva.com>
    - no need to package big ChangeLog when NEWS is already there

* Tue Feb 27 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.2.37-1mdv2007.1
+ Revision: 126475
- fix buildrequires
- Import esound

* Mon Feb 26 2007 Götz Waschk <waschk@mandriva.org> 0.2.37-1mdv2007.1
- add docs
- unpack patches
- drop patch 3
- New version 0.2.37

* Wed Aug 23 2006 Frederic Crozat <fcrozat@mandriva.com> 0.2.36-5mdv2007.0
- Update patch3, fix bug #24365

* Fri Aug 11 2006 Frederic Crozat <fcrozat@mandriva.com> 0.2.36-4mdv2007.0
- Patch4 (CVS): various bug fixes
- Use mkrel

* Mon May 15 2006 Stefan van der Eijk <stefan@eijk.nu> 0.2.36-3mdk
- rebuild for sparc

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.2.36-2mdk
- Rebuild

* Wed Jun 08 2005 Götz Waschk <waschk@mandriva.org> 0.2.36-1mdk
- license is LGPL
- New release 0.2.36

* Thu Feb 24 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.2.35-2mdk
- cleanup patch2 (libdir) to make esd-config arch-independent

* Fri Aug 13 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.2.35-1mdk
- Release 0.2.35
- Regenerate patch0
- Enable libtoolize

* Sat Apr 03 2004 Götz Waschk <waschk@linux-mandrake.com> 0.2.34-2mdk
- disable alsa again (fcrozat)

* Sat Apr 03 2004 Götz Waschk <waschk@linux-mandrake.com> 0.2.34-1mdk
- reenable alsa
- new version

