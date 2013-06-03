
%global _hardened_build 1

Summary:        LightDM GTK+ Greeter
Name:           lightdm-gtk
Version:        1.6.0
Release:        1%{?dist}

License:        GPLv3+
URL:            https://launchpad.net/lightdm-gtk-greeter
Source0:        https://launchpad.net/lightdm-gtk-greeter/1.6/%{version}/+download/lightdm-gtk-greeter-%{version}.tar.gz

# tweak default config
Patch1:         lightdm-gtk-greeter-1.5.2-fedora.patch

## upstreamable patches
# avoid setting background when given bogus screen geometry
# http://bugzilla.redhat.com/915986
Patch50:        lightdm-gtk-greeter-1.5.2-bg_crash.patch

BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  pkgconfig(liblightdm-gobject-1)
BuildRequires:  pkgconfig(gtk+-3.0)

Obsoletes:      lightdm-gtk-greeter < 1.1.5-4
Provides:       lightdm-gtk-greeter = %{version}-%{release}

Provides:       lightdm-greeter = 1.2

Requires:       lightdm%{?_isa}
# for /usr/share/backgrounds/default.png
Requires:       desktop-backgrounds-compat
# owner of HighContrast gtk/icon themes
Requires:       gnome-themes-standard
# for /usr/share/pixmaps/fedora-logo-small.png
Requires:       system-logos

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description
A LightDM greeter that uses the GTK+ toolkit.


%prep
%setup -q -n lightdm-gtk-greeter-%{version}

%patch1 -p1 -b .fedora
%patch50 -p1 -b .bg_crash


%build
%configure \
  --disable-static

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

%find_lang lightdm-gtk-greeter 

# own alternatives target
touch %{buildroot}%{_datadir}/xgreeters/lightdm-greeter.desktop


%post
%{_sbindir}/update-alternatives \
  --install %{_datadir}/xgreeters/lightdm-greeter.desktop \
  lightdm-greeter \
  %{_datadir}/xgreeters/lightdm-gtk-greeter.desktop \
  20 

%postun
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives \
  --remove lightdm-greeter \
  %{_datadir}/xgreeters/lightdm-gtk-greeter.desktop
fi

%files -f lightdm-gtk-greeter.lang
%doc ChangeLog COPYING NEWS README
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-gtk-greeter.conf
%{_sbindir}/lightdm-gtk-greeter
%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop
# own alternatives target
%ghost %{_datadir}/xgreeters/lightdm-greeter.desktop


%changelog
* Mon Jun 03 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0 (#962765)

* Tue May 14 2013 Rex Dieter <rdieter@fedoraproject.org> 1.5.2-1
- lightdm-gtk-1.5.2 is available (#962765)

* Mon May 06 2013 Rex Dieter <rdieter@fedoraproject.org> 1.5.1-3
- avoid crash in gdk_cairo_set_source_pixbuf with bogus geometry values (#915986)

* Thu Apr 25 2013 Rex Dieter <rdieter@fedoraproject.org> 1.5.1-2
- lightdm package should be built with PIE flags (#955147)

* Mon Feb 11 2013 Rex Dieter <rdieter@fedoraproject.org> 1.5.1-1
- 1.5.1

* Mon Jan 28 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.5.0-1
- 1.5.0

* Fri Dec 07 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.1-3
- missing icons in high-contrast mode (#881352)

* Wed Nov 28 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.1-2
- Requires: system-logos

* Wed Oct 03 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1
- Make lightdm requirement arch specific

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.6-3
- try using alternatives

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

