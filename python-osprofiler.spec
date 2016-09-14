%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# Created by pyp2rpm-1.1.0b
%global pypi_name osprofiler

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Profiler Library

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

Requires: python-six
Requires: python-webob

%description
OSProfiler is an OpenStack cross-project profiling library.


%package doc
Summary:    Documentation for the OpenStack Profiler Library
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  git

%description doc
Documentation for the OpenStack Profiler Library


%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
rm -f requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%doc README.rst
%license LICENSE
%{_bindir}/osprofiler
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%files doc
%doc html
%license LICENSE

%changelog
