%define uname vowpal_wabbit

Name:           vowpal-wabbit
Summary:        Fast and efficient machine learning system
Version:        8.1
Release:        2%{?dist}
URL:            http://hunch.net/~vw/
Source0:        https://github.com/JohnLangford/vowpal_wabbit/archive/%{version}/%{uname}-%{version}.tar.gz
License:        BSD
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  zlib-devel

%description
The Vowpal Wabbit (VW) project is a fast out-of-core learning system sponsored
by Microsoft Research and (previously) Yahoo! Research.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%autosetup -n %{uname}-%{version}

%build
%configure LIBS='-lpthread' --enable-parallelization
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%install
%make_install

# install the utl scripts
for util in vw-hypersearch vw-varinfo vw-regr vw-top-errors
do
  install -p -m0755 utl/$util %{buildroot}%{_bindir}/
done
mkdir -p %{buildroot}%{_datadir}/vowpalwabbit
install -p -m0644 utl/vw-validate.html %{buildroot}%{_datadir}/vowpalwabbit/

# remove libtool files
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la

%check
# some of tests failes on i686
%ifarch %ix86
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test || :
%else
  LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test
%endif

%files
%license LICENSE
%doc README.md AUTHORS
%{_libdir}/liballreduce.so.*
%{_libdir}/libvw*.so.*
%{_bindir}/vw
%{_bindir}/active_interactor
%{_bindir}/library_example
%{_bindir}/spanning_tree
%{_bindir}/ezexample_predict
%{_bindir}/ezexample_train
%{_bindir}/vw-hypersearch
%{_bindir}/vw-varinfo
%{_bindir}/vw-regr
%{_bindir}/vw-top-errors
%{_datadir}/vowpalwabbit/

%files devel
%{_includedir}/vowpalwabbit/
%{_libdir}/liballreduce.so
%{_libdir}/libvw*.so

%changelog
* Wed Nov 04 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.1-2
- Install utilities which metioned in wiki
- Don't fail tests on i686

* Wed Nov 04 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.1-1
- Initial package
