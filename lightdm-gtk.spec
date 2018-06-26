
Summary:        LightDM GTK Greeter
Name:           lightdm-gtk
Version:        2.0.5
Release:        2%{?dist}

License:        GPLv3+
URL:            https://launchpad.net/lightdm-gtk-greeter
Source0:        %url/2.0/%{version}/+download/lightdm-gtk-greeter-%{version}.tar.gz

Source10:       60-lightdm-gtk-greeter.conf
Patch1:         lightdm-gtk-greeter-readd-language.patch

## upstreamable patches
# https://bugzilla.redhat.com/show_bug.cgi?id=1178498
# (lookaside cache)
Patch102:       lightdm-gtk-greeter-1.8.5-add-cinnamon-badges.patch

BuildRequires:  gettext
BuildRequires:  intltool
# exo-csource
BuildRequires:  exo-devel
BuildRequires:  pkgconfig(liblightdm-gobject-1)
BuildRequires:  pkgconfig(gtk+-3.0)
# for autogen.sh
BuildRequires:  gnome-common
BuildRequires:  gobject-introspection-devel

Obsoletes:      lightdm-gtk2 < 1.8.5-15

Obsoletes:      lightdm-gtk-common < 2.0
Obsoletes:      lightdm-gtk-greeter < 1.1.5-4
Provides:       lightdm-gtk-greeter = %{version}-%{release}
Provides:       lightdm-greeter = 1.2

Requires:       lightdm%{?_isa}

# for default background/wallpaper
%if 0%{?fedora}
%global background #333333
Requires:       desktop-backgrounds-compat
%endif
%if 0%{?rhel}
%global background %{_datadir}/backgrounds/day.jpg
Requires:       system-logos
%endif
# owner of HighContrast gtk/icon themes
Requires:       gnome-themes-standard

# Fix issue with lightdm-autologin-greeter pulled in basic-desktop netinstall.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1481192
Supplements: (lightdm%{?_isa} and lightdm-autologin-greeter)

%description
A LightDM greeter that uses the GTK3 toolkit.


%prep
%autosetup -n lightdm-gtk-greeter-%{version} -p1

NOCONFIGURE=1 ./autogen.sh

%if 0%{?background:1}
sed -i.background -e "s|#background=.*|background=%{background}|" \
  data/lightdm-gtk-greeter.conf
%endif

echo "default-user-image=#fedberry-logo-icon" >>data/lightdm-gtk-greeter.conf


%build
%configure \
  --disable-silent-rules \
  --disable-static \
  --disable-libindicator \
  --enable-at-spi-command="%{_libexecdir}/at-spi-bus-launcher --launch-immediately" \
  --enable-kill-on-sigterm

%make_build


%install
%make_install

install -m644 -p -D %{SOURCE10} \
  %{buildroot}%{_datadir}/lightdm/lightdm.conf.d/60-lightdm-gtk-greeter.conf

%find_lang lightdm-gtk-greeter 

# create/own GREETER_DATA_DIR
mkdir -p %{buildroot}%{_datadir}/lightdm-gtk-greeter/

## unpackaged files
rm -fv %{buildroot}%{_docdir}/lightdm-gtk-greeter/sample-lightdm-gtk-greeter.css


%pre
%{_sbindir}/update-alternatives \
  --remove lightdm-greeter \
  %{_datadir}/xgreeters/lightdm-gtk-greeter.desktop 2> /dev/null ||:


%files -f lightdm-gtk-greeter.lang
%license COPYING
%doc ChangeLog NEWS README
%doc data/sample-lightdm-gtk-greeter.css
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-gtk-greeter.conf
%{_sbindir}/lightdm-gtk-greeter
%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop
%dir %{_datadir}/lightdm-gtk-greeter/
%{_datadir}/icons/hicolor/scalable/places/*badge-symbolic.svg
%{_datadir}/lightdm/lightdm.conf.d/60-lightdm-gtk-greeter.conf


%changelog
* Thu Apr 12 2018 Vaughan Agrez <devel@agrez.net> 2.0.5-2
- Update %%configure switches

* Sat Mar 24 2018 Vaughan Agrez <devel@agrez.net> 2.0.5-1
- New release - 2.0.5
- Drop Patch0 & Patch103
- Update patch1 (add back language button)
- Drop obsolete %%post icon scriptlets
- Add configure option --enable-kill-on-sigterm

* Thu Nov 23 2017 Vaughan Agrez <devel@agrez.net> 2.0.3-5
- New release - 2.0.3
- Sync with upstream Fedora:
  * remove atspi spawn code, rhbz (#1477879)
  * Add Supplements: (lightdm%{?_isa} and lightdm-autologin-greeter),
  fixing rhbz#1481192
  * Fix compile on arm arch
- Bump release

* Mon Apr 10 2017 Vaughan Agrez <devel@agrez.net> 2.0.2-5
- Use background colour instead of default wallpaper
- Use fedberry-logo-icon as default user image

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-3
- restore add-cinnamon-badgets.patch

* Wed Nov 16 2016 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-2
- %%build: fix typo in --enable-at-spi-command target

* Thu Oct 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.0.2-1
- lightdm-gtk-2.0.2 (#1382947)

* Sat Apr 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.0.1-1
- lightdm-gtk-2.0.1 (#1132844)
- use conf.d snippets (#1096216)
- drop -common subpkg

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 13 2015 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-19
- use patch instead of sed (for previous commit)

* Fri Jul 10 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.5-18
- fix wrong path to at-spi-bus-launcher

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-16
- unset_AT_SPI_BUS.patch (#1175026)

* Tue Mar 24 2015 Rex Dieter <rdieter@fedoraproject.org> 1.8.5-15
- drop (temporary) -gtk2 subpkg support

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

