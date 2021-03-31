# Disabled by default, rely on upstream's test
# Requires pytest-bdd that is not in Fedora
%bcond_with tests
 
%global pypi_name vimiv-qt
%global binname vimiv
%global appdataid org.karlch.vimiv.qt
 
%global _description %{expand:
Vimiv is an image viewer with vim-like keybindings. It is written in python3
using the Qt5 toolkit and is free software, licensed under the GPL.
 
The initial GTK3 version of vimiv will no longer be maintained.
 
- Simple library browser
- Thumbnail mode
- Basic image editing
- Command line with tab completion
- Complete customization with style sheets
 
Full documentation is available at https://karlch.github.io/vimiv-qt.}
 
 
Name:           %{pypi_name}
Version:        0.8.0
Release:        1%{?dist}
Summary:        An image viewer with vim-like keybindings
 
License:        GPLv3+
URL:            https://karlch.github.io/vimiv-qt/
Source0:        https://github.com/karlch/vimiv-qt/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires: make
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-qt5-devel
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/desktop-file-validate
 
%if %{with tests}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist flaky}
%endif
# Not listed in setup.py
Requires: python3-piexif
# python3-qt5-base is pulled in but SVG requires python3-qt5
Requires: python3-qt5
# For icons
Requires: hicolor-icon-theme
 
 
# Replaces the vimiv package now
# Last version of vimiv in Fedora is 0.9.1-13
Provides:   vimiv = 0.9.2
Obsoletes:  vimiv < 0.9.1-14
 
%{?python_enable_dependency_generator}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
%description %_description
%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info
# Don't do the python bit there
mv -v misc/Makefile .
sed -i '/python3 setup.py install/ d' Makefile
sed -i '/LICENSE/ d' Makefile
# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'
 
%build
%py3_build
%install
%py3_install
%make_install
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appdataid}.metainfo.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{binname}.desktop
 
%check
%if %{with tests}
pytest-%{python3_version}
%endif
 
%files
%license LICENSE
%doc README.md
%{python3_sitearch}/%{binname}-%{version}-py%{python3_version}.egg-info
%{python3_sitearch}/%{binname}
%{_bindir}/%{binname}
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{binname}.*
%{_metainfodir}/%{appdataid}.metainfo.xml
%{_mandir}/man1/%{binname}.*
