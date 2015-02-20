
%global _hardened_build 1

Summary:        LightDM GTK3 Greeter
Name:           lightdm-gtk
Version:        1.8.5
Release:        14%{?dist}

License:        GPLv3+
URL:            https://launchpad.net/lightdm-gtk-greeter
Source0:        https://launchpad.net/lightdm-gtk-greeter/1.8/%{version}/+download/lightdm-gtk-greeter-%{version}.tar.gz

# tweak default config
Patch1:         lightdm-gtk-greeter-1.8.1-fedora.patch
Patch2:         lightdm-gtk-greeter-1.8.1-rhel7.patch

## upstreamable patches
# avoid setting background when given bogus screen geometry
# http://bugzilla.redhat.com/915986
Patch50:        lightdm-gtk-greeter-1.8.5-bg_crash.patch
# fix out-of-tree builds
Patch51:        lightdm-gtk-greeter-1.8.5-vpath.patch

## upstream patches
# backport fix for mouse cursor
# http://bazaar.launchpad.net/~lightdm-gtk-greeter-team/lightdm-gtk-greeter/trunk/revision/298
Patch100:       lightdm-gtk-greeter-1.8.5-lp#1024482.patch
# add badges for Mate and Window Maker
# http://bazaar.launchpad.net/~lightdm-gtk-greeter-team/lightdm-gtk-greeter/trunk/revision/311
Patch101:       lightdm-gtk-greeter-1.9.1-badges.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1178498
Patch102:       lightdm-gtk-greeter-1.8.5-add-cinnamon-badges.patch

BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  pkgconfig(liblightdm-gobject-1)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk+-2.0)

Obsoletes:      lightdm-gtk-greeter < 1.1.5-4
Provides:       lightdm-gtk-greeter = %{version}-%{release}
Provides:       lightdm-greeter = 1.2
Requires:       %{name}-common = %{version}-%{release}
Requires:       lightdm%{?_isa}

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description
A LightDM greeter that uses the GTK3 toolkit.

%package common
Summary: Common files for %{name}
# when -common was split out
Conflicts: lightdm-gtk < 1.8.5-5
# for default background/wallpaper
%if 0%{?fedora}
Requires:       desktop-backgrounds-compat
%endif
%if 0%{?rhel}
Requires:       system-logos
%endif
# owner of HighContrast gtk/icon themes
Requires:       gnome-themes-standard
BuildArch:      noarch
%description common
%{summary}.

%package -n lightdm-gtk2
Summary:        LightDM GTK2 Greeter
Provides:       lightdm-greeter = 1.2
Requires:       %{name}-common = %{version}-%{release}
Requires:       lightdm%{?_isa}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%description -n lightdm-gtk2
A LightDM greeter that uses the GTK2 toolkit.


%prep
%setup -q -n lightdm-gtk-greeter-%{version}

%patch100 -p1 -b .lp#1024482
%patch101 -p0 -b .badges
%patch102 -p1 -b .cinnamon-badges

%patch50 -p1 -b .bg_crash
%patch51 -p1 -b .vpath

%if 0%{?rhel} > 6
%patch2 -p1 -b .rhel7
%else
%patch1 -p1 -b .fedora
%endif


%build
%global _configure ../configure
mkdir %{_target_platform}
pushd %{_target_platform}
%configure \
  --disable-silent-rules \
  --disable-static

make %{?_smp_mflags}
popd

# gtk2 build
mkdir %{_target_platform}-gtk2
pushd %{_target_platform}-gtk2
%configure \
  --disable-silent-rules \
  --disable-static \
  --with-gtk2

make %{?_smp_mflags}
popd


%install
# GTK2
make install DESTDIR=%{buildroot} -C %{_target_platform}-gtk2
mv %{buildroot}%{_sbindir}/lightdm-gtk-greeter \
   %{buildroot}%{_sbindir}/lightdm-gtk2-greeter
mv %{buildroot}%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop \
   %{buildroot}%{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop
sed -i \
  -e 's|^Exec=lightdm-gtk-greeter|Exec=lightdm-gtk2-greeter|' \
  -e 's|GTK+|GTK2|g' \
   %{buildroot}%{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop

# GTK3
make install DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang lightdm-gtk-greeter 

# create/own GREETER_DATA_DIR
mkdir -p %{buildroot}%{_datadir}/lightdm-gtk-greeter/

# own alternatives target
touch %{buildroot}%{_datadir}/xgreeters/lightdm-greeter.desktop

## unpackaged files
rm -fv %{buildroot}%{_docdir}/lightdm-gtk-greeter/sample-lightdm-gtk-greeter.css


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

%files
%doc ChangeLog COPYING NEWS README
%doc data/sample-lightdm-gtk-greeter.css
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-gtk-greeter.conf
%{_sbindir}/lightdm-gtk-greeter
%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop
%dir %{_datadir}/lightdm-gtk-greeter/
# own alternatives target
%ghost %{_datadir}/xgreeters/lightdm-greeter.desktop

%post common
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:

%postun common
if [ $1 -eq 0 ]; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans common
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files common -f lightdm-gtk-greeter.lang
%{_datadir}/icons/hicolor/scalable/places/*badge-symbolic.svg

%post -n lightdm-gtk2
%{_sbindir}/update-alternatives \
  --install %{_datadir}/xgreeters/lightdm-greeter.desktop \
  lightdm-greeter \
  %{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop \
  15

%postun -n lightdm-gtk2
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives \
  --remove lightdm-greeter \
  %{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop
fi

%files -n lightdm-gtk2
%doc ChangeLog COPYING NEWS README
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-gtk-greeter.conf
%{_sbindir}/lightdm-gtk2-greeter
%dir %{_datadir}/lightdm-gtk-greeter/
%{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop
# own alternatives target
%ghost %{_datadir}/xgreeters/lightdm-greeter.desktop


%changelog
* Fri Feb 20 2015 Rex Dieter <rdieter@fedoraproject.org> - 1.8.5-14
- merge epel branch mods
- (fedora) drop Requires: system-logos (not used anymore)

* Thu Feb 19 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.5-13
- fix build of cinnamon badge

* Tue Feb 17 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.5-12
- add cinnamon badge

* Sat Jan 31 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.5-11
- add badges for Mate and Window Maker (#1178498)

* Fri Nov 07 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-10
- revert +Requires: gnome-icon-theme, adwaita reportedly good enough now (#1128697)

* Mon Oct 06 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-9
- cursor theme doesn't change (#989152)

* Sun Oct 05 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.8.5-8
- create/own %%{_datadir}/lightdm-gtk-greeter/
- -gtk2: own lightdm-greeter.desktop alternatives target

* Sun Oct 05 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-7
- -gtk2: fix alternatives, omit dup'd translations
- -common: fix %%posttrans icon scriptlet

* Sat Oct 04 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-6
- lightdm-gtk2: support alternatives (for default lightdm greeter)

* Sat Oct 04 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-5
- lightdm-gtk2, -common subpkgs

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-3
- missing icons, +Requires: gnome-icon-theme (#1128697)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-1
- 1.8.5 (#1094437)

* Mon Mar 31 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.4-1
- 1.8.4 (#1076529)

* Tue Mar 04 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.2-1
- 1.8.2 (#1047209)

* Thu Feb 20 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.1-1
- 1.8.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-3
- CVE-2014-0979 (#149420,1049422)

* Tue Oct 08 2013 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-2
- lightdm-gtk-greeter segfaults if session last used is uninstalled (#1002782)

* Thu Sep 19 2013 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-1
- lightdm-gtk-1.6.1 (#1009531)

* Sun Aug 18 2013 Rex Dieter <rdieter@fedoraproject.org> 1.6.0-3
- rebuild (lightdm)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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

