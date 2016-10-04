%global pre_release rc2
%global rel 1

Name:           sway
Version:        0.10
%if %{pre_release}
Release:        0.%{rel}.%{pre_release}%{?dist}
%else
Release:        %{rel}%{?dist}
%endif
Summary:        i3-compatible window manager for Wayland
Group:          User Interface/X
License:        MIT
URL:            https://github.com/SirCmpwn/sway
%if %{pre_release}
Source0:        https://github.com/SirCmpwn/%{name}/archive/%{version}-%{pre_release}.tar.gz
%else
Source0:        https://github.com/SirCmpwn/%{name}/archive/%{version}.tar.gz
%endif
BuildRequires:  cmake
BuildRequires:  pkgconfig(wlc)
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  asciidoc
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pam-devel
Requires:       dmenu
Recommends:     rxvt-unicode-256color-ml
Recommends:     ImageMagick
Suggests:       xorg-x11-server-Xwayland

%description
Sway is a tiling window manager supporting Wayland compositor protocol and 
i3-compatible configuration.

%prep
%if %{pre_release}
%setup -qn %{name}-%{version}-%{pre_release}
%else
%setup -q
%endif
mkdir %{_target_platform}

%build
pushd %{_target_platform}
%cmake \
       -DBUILD_SHARED_LIBS:BOOL=OFF \
       -Dzsh-completions=YES \
       -Ddefault-wallpaper=NO \
       -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
       ..
popd
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}
# Set default terminal to urxvt256c-ml
sed -i 's/^set $term urxvt$/set \$term urxvt256c-ml/' %{buildroot}%{_sysconfdir}/sway/config
# Set Fedora background as default background
sed -i "s|^output \* bg .*|output * bg /usr/share/backgrounds/f%{fedora}/default/normalish/f%{fedora}.png fill|" %{buildroot}%{_sysconfdir}/sway/config

%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/sway
%config(noreplace) %{_sysconfdir}/sway/config
%config %{_sysconfdir}/pam.d/swaylock
%{_mandir}/man1/sway*.1*
%{_mandir}/man5/sway*.5*
%{_bindir}/sway
%{_bindir}/swaybar
%{_bindir}/swaybg
%{_bindir}/swaygrab
%{_bindir}/swaylock
%{_bindir}/swaymsg
%{_datadir}/wayland-sessions/sway.desktop
%{_datadir}/zsh/site-functions/_sway*

%changelog
* Tue Oct 04 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.10-0.1.rc2
- Update to 0.10-rc2

* Wed Sep 28 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.10-0.1.rc1
- Update to 0.10-rc1

* Tue Sep 06 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.9-4
- Do not Require the urxvt shell
- Rebuild due to a wlc rebuild
- Add Recommends ImageMagick

* Wed Aug 10 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.9-3
- Remove some compilation flags that were not needed

* Sun Aug 07 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.9-2
- Add dmenu dependency
- Add rxvt-unicode-256color-ml dependency
- Use urxvt256c-ml instead of urxvt by default
- Improve default wallpaper
- Add suggests xorg-x11-server-Xwayland

* Wed Aug 03 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.9-1
- Upgrade to 0.9

* Thu Jul 07 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.8-2
- Move ffmpeg and ImageMagick from Required to Suggested

* Thu Jul 07 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.8-1
- Update to version 0.8
- Re-enable ZSH bindings
- Remove sway wallpapers

* Sun May 29 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.7-1
- Update to version 0.7
- Drop ZSH bindings that are no longer shipped with Sway

* Thu May 05 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.6-1
- Update to current upstream version

* Wed Apr 06 2016 Fabio Alessandro Locati <fale@redhat.com> - 0.3-1
- Update to current upstream version

* Sun Feb 14 2016 Fabio Alessandro Locati <fale@redhat.com> - 0-1.20160214git016a774
- Initial packaging
