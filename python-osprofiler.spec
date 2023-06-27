%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order jaeger-client opentelemetry-exporter-otlp opentelemetry-sdk
# Created by pyp2rpm-1.1.0b
%global pypi_name osprofiler
%global with_doc 1

%global common_desc OSProfiler is an OpenStack cross-project profiling library.


Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Profiler Library

License:        Apache-2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:    OpenStack Profiler Library
Obsoletes: python2-%{pypi_name} < %{version}-%{release}

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for the OpenStack Profiler Library
Group:      Documentation

%description doc
Documentation for the OpenStack Profiler Library
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/sphinx-build/ s/-W//' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done
# Uncap elasticsearch
sed -i 's/\(.*elasticsearch>=.*\),\(.*\)/\1/' test-requirements.txt

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s osprofiler %{buildroot}%{_bindir}/osprofiler-3

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/osprofiler
%{_bindir}/osprofiler-3
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.dist-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
