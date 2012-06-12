Summary: LightDM GTK+ Greeter
Name:	 lightdm-gtk
Version: 1.1.6
Release: 2%{?dist}

License: GPLv3+
URL:	 https://launchpad.net/lightdm-gtk-greeter
Source0: https://launchpad.net/lightdm-gtk-greeter/trunk/%{version}/+download/lightdm-gtk-greeter-%{version}.tar.gz

# tweak default config
Patch1: lightdm-gtk-greeter-1.1.5-fedora.patch

BuildRequires: gettext
BuildRequires: intltool
BuildRequires: pkgconfig(liblightdm-gobject-1)
BuildRequires: pkgconfig(gtk+-3.0)

Obsoletes: lightdm-gtk-greeter < 1.1.5-4
Provides:  lightdm-gtk-greeter = %{version}-%{release}

Provides: lightdm-greeter = 1.2

# for /usr/share/backgrounds/default.png
Requires: desktop-backgrounds-compat
Requires: lightdm

%description
A LightDM greeter that uses the GTK+ toolkit.


%prep
%setup -q -n lightdm-gtk-greeter-%{version}

%patch1 -p1 -b .fedora


%build
%configure \
  --disable-static

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

%find_lang lightdm-gtk-greeter 


%files -f lightdm-gtk-greeter.lang
%doc ChangeLog COPYING NEWS README
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-gtk-greeter.conf
%{_sbindir}/lightdm-gtk-greeter
%{_datadir}/lightdm-gtk-greeter
%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop


%changelog
* Tue Jun 12 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.6-2
- Provides: lightdm-greeter = 1.2

* Mon Jun 11 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.6-1
- lightdm-gtk-greeter-1.1.6
- fix Source Url
- add %%doc's
- License: GPLv3+

* Thu Apr 26 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.5-4
- lightdm-gtk-greeter => lightdm-gtk rename

* Wed Apr 25 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.5-3
- Requires: lightdm
- use /usr/share/backgrounds/default.png by default

* Tue Apr 24 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.5-2
- adapt for fedora

* Sat Apr 07 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.5-1
+ Revision: 789754
- update to new version 1.1.5

* Mon Mar 26 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.4-3
+ Revision: 787060
- drop requires on gnome-themes-standard (quite bloated)

* Sun Mar 25 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.4-2
+ Revision: 786642
- spec file clean
- rebuild for new lightdm

* Fri Mar 02 2012 Matthew Dawkins <mattydaw@mandriva.org> 1.1.4-1
+ Revision: 781826
- imported package lightdm-gtk-greeter

