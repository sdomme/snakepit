
#!/usr/bin/env cram
# vim: set syntax=cram :

  $ export PROJECT_ROOT=$TESTDIR/../../
  $ cp $PROJECT_ROOT/snakepit.yaml .
  $ ls
  snakepit.yaml

  $ snakepit snakepit.yaml
  $ cat moto.spec
  # do not create debug-packages
  %define debug_package %{nil}
  
  # deactivcate python bytecompiling
  %global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
  
  Name:          moto
  Version:       0.3.1
  Release:       0_miniconda_3.9.1
  Summary:       A library that allows your python tests to easily mock out the boto library (EXPERIMENTAL SNAKEPIT STANDALONE)
  Group:         Development/Tools
  License:       Apache
  BuildRoot:     %{_tmppath}/%{name}-%{version}-root
  BuildRequires: /bin/bash wget make-opt-writable
  AutoReqProv:   no
  
  %description
  moto via miniconda generated by snakepit (EXPERIMENTAL)
  
  %build
  echo MY_USER=$USER
  # clean, just in case
  rm -rf /opt/moto
  # install miniconda into /opt
  wget -nv http://repo.continuum.io/miniconda/Miniconda-3.9.1-Linux-%{_build_arch}.sh
  bash Miniconda-3.9.1-Linux-x86_64.sh -b -p /opt/moto
  # bootstrap pip
  /opt/moto/bin/conda install --yes pip
  # use pip to install moto
  /opt/moto/bin/pip install  moto==0.3.1
  # cleanup the conda install a little
  /opt/moto/bin/conda clean --tarballs --packages --yes
  # cleanup the conda install a little more
  rm -rvf /opt/moto/pkgs/*
  
  %install
  # create /opt/moto in buildroot
  mkdir -p %{buildroot}/opt/moto
  # copy the built miniconda env into the buildroot
  cp -r /opt/moto %{buildroot}/opt
  ls %{buildroot}/opt/moto
  # create a /usr/bin
  install -m 755 -d %{buildroot}/usr/bin
  # do all the symlinks
  
  ln -s /opt/moto/bin/moto_server %{buildroot}/usr/bin
  
  
  %clean
  # remove the result of the build step
  rm -rf /opt/moto
  
  %files
  %defattr(-,root,root,-)
  /opt/moto
  
  /usr/bin/moto_server
  
  
  %post (no-eol)
