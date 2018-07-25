%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# Created by pyp2rpm-1.1.0b
%global pypi_name osprofiler
%global with_doc 1

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global common_desc OSProfiler is an OpenStack cross-project profiling library.


Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Profiler Library

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr

%description
%{common_desc}

%package -n python2-%{pypi_name}
Summary:    OpenStack Profiler Library
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires: python2-oslo-concurrency >= 3.26.0
Requires: python2-oslo-serialization >= 2.18.0
Requires: python2-prettytable >= 0.7.2
Requires: python2-oslo-messaging >= 5.2.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-requests
Requires: python2-six
%if 0%{?fedora} > 0
Requires: python2-netaddr
Requires: python2-webob
%else
Requires: python-netaddr
Requires: python-webob
%endif

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for the OpenStack Profiler Library
Group:      Documentation

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description doc
Documentation for the OpenStack Profiler Library
%endif


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:    OpenStack Profiler Library
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr

Requires:       python3-netaddr
Requires:       python3-oslo-concurrency >= 3.26.0
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-prettytable >= 0.7.2
Requires:       python3-oslo-messaging >= 5.2.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-requests
Requires:       python3-six
Requires:       python3-webob

%description -n python3-%{pypi_name}
%{common_desc}
%endif


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -f requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
python setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/osprofiler %{buildroot}%{_bindir}/osprofiler-%{python3_version}
ln -s ./osprofiler-%{python3_version} %{buildroot}%{_bindir}/osprofiler-3
%endif

%py2_install

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/osprofiler
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/osprofiler-3
%{_bindir}/osprofiler-%{python3_version}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%changelog
