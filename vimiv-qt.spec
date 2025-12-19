# Disabled by default, rely on upstream's test
# Requires pytest-bdd that is not in Mandriva
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
Version:        0.9.0
Release:        2
Summary:        An image viewer with vim-like keybindings
 
License:        GPLv3+
URL:            https://karlch.github.io/vimiv-qt/
Source0:        https://github.com/karlch/vimiv-qt/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(python)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pyqt5)
 
%if %{with tests}
BuildRequires:  python3dist(pytest)
# Not available in Mandriva anyway
#BuildRequires:  python3dist(flaky)
%endif

# Not listed in setup.py
# Missing in Mandriva
#Requires: python-piexif
# python3-qt5-base is pulled in but SVG requires python3-qt5
Requires: PyQt5
# For icons
Requires: hicolor-icon-theme
 
%{?python_enable_dependency_generator}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
%description
Vimiv is an image viewer with vim-like keybindings. It is written in python3
using the Qt5 toolkit and is free software, licensed under the GPL.
 
The initial GTK3 version of vimiv will no longer be maintained.

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
%py_build

%install
%py_install
%make_install
 
%files
%license LICENSE
%doc README.md
%{python_sitearch}/%{binname}-%{version}-py%{python_version}.egg-info
%{python_sitearch}/%{binname}
%{_bindir}/%{binname}
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{binname}.*
%{_metainfodir}/%{appdataid}.metainfo.xml
%{_mandir}/man1/%{binname}.*
