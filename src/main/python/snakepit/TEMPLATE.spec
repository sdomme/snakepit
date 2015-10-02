# do not create debug-packages
%define debug_package %{nil}

# deactivcate python bytecompiling
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:          {{ pypi_package_name }}
Version:       {{ pypi_package_version }}
Release:       {{ build }}
Summary:       {{ pypi_package_name }} via {{ conda_dist_flavour }}{{ conda_dist_flavour_version }} generated by snakepit (EXPERIMENTAL)
Group:         Development/Tools
License:       UNKNOWN
Source0:       %{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
BuildRequires: /bin/bash wget make-opt-writable
AutoReqProv:   no

%description
{{ pypi_package_name }} via {{ conda_dist_flavour }}{{ conda_dist_flavour_version }} generated by snakepit (EXPERIMENTAL)

%build
echo MY_USER=$USER
# clean, just in case
rm -rf /opt/{{ pypi_package_name }}
# install {{ conda_dist_flavour }} into /opt
wget -nv http://repo.continuum.io/{{ conda_dist_flavour }}/{{ conda_dist_flavour_urlprefix }}{{ conda_dist_flavour_version }}-{{ conda_dist_version }}-Linux-%{_build_arch}.sh
bash {{ conda_dist_flavour_urlprefix }}{{ conda_dist_flavour_version }}-{{ conda_dist_version }}-Linux-x86_64.sh -b -p /opt/{{ pypi_package_name }}
# bootstrap pip
/opt/{{ pypi_package_name }}/bin/conda install --yes pip
# use pip to install {{ pypi_package_name }}
/opt/{{ pypi_package_name }}/bin/pip install {{ extra_pip_args }} {{ pypi_package_name }}=={{ pypi_package_version }}
# cleanup the conda install a little
/opt/{{ pypi_package_name }}/bin/conda clean --tarballs --packages --yes
# cleanup the conda install a little more
rm -rvf /opt/{{ pypi_package_name }}/pkgs/*

%install
# create /opt/{{ pypi_package_name }} in buildroot
mkdir -p %{buildroot}/opt/{{ pypi_package_name }}
# copy the built {{ conda_dist_flavour }} env into the buildroot
cp -r /opt/{{ pypi_package_name }} %{buildroot}/opt
ls %{buildroot}/opt/{{ pypi_package_name }}
# create a /usr/bin
install -m 755 -d %{buildroot}/usr/bin
# do all the symlinks
{% for item in symlinks %}
ln -s /opt/{{ pypi_package_name }}/bin/{{ item }} %{buildroot}/usr/bin
{% endfor %}

%clean
# remove the result of the build step
rm -rf /opt/{{ pypi_package_name }}

%files
%defattr(-,root,root,-)
/opt/{{ pypi_package_name }}
{% for item in symlinks %}
/usr/bin/{{ item }}
{% endfor %}

%post
