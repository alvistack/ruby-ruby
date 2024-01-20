# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global __strip /bin/true

%global __brp_mangle_shebangs /bin/true

Name: ruby3.3
Epoch: 100
Version: 3.3.3
Release: 1%{?dist}
Summary: Interpreter of object-oriented scripting language Ruby
License: BSD-2-Clause
URL: https://github.com/ruby/ruby/tags
Source0: %{name}_%{version}.orig.tar.gz
Source99: %{name}.rpmlintrc
BuildRequires: autoconf
BuildRequires: bison
BuildRequires: cargo >= 1.56.0
BuildRequires: chrpath
BuildRequires: fdupes
BuildRequires: gcc
BuildRequires: gmp-devel
BuildRequires: libffi-devel
BuildRequires: libtool
BuildRequires: libyaml-devel
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: ruby >= 2.5
BuildRequires: rust >= 1.56.0
BuildRequires: zlib-devel
Provides: ruby(abi) = 3.3.0
Provides: ruby(runtime_executable) = 3.3
Provides: ruby-default = %{epoch}:%{version}-%{release}
Provides: ruby3.3-stdlib = %{epoch}:%{version}-%{release}
Provides: ruby33 = %{epoch}:%{version}-%{release}
Conflicts: ruby-default < %{epoch}:%{version}-%{release}
Conflicts: ruby3.3-stdlib < %{epoch}:%{version}-%{release}
Conflicts: ruby33 < %{epoch}:%{version}-%{release}
Obsoletes: ruby-default < %{epoch}:%{version}-%{release}
Obsoletes: ruby3.3-stdlib < %{epoch}:%{version}-%{release}
Obsoletes: ruby33 < %{epoch}:%{version}-%{release}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming. It has many features to process text files
and to do system management tasks (as in perl). It is simple,
straight-forward, and extensible.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
./autogen.sh
%configure \
    --with-destdir=%{buildroot} \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --datadir=%{_datadir} \
    --docdir=%{_docdir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --sysconfdir=%{_sysconfdir} \
    --disable-rpath \
    --disable-static \
    --enable-mkmf-verbose \
    --enable-pie \
    --enable-shared \
    --enable-yjit \
    --with-compress-debug-sections=no
%make_build

%install
%make_install
fdupes -qnrps %{buildroot}
find %{buildroot} -type f -name '*.so' -exec chrpath -d {} \;
find %{buildroot} -type f -exec sed -i 's?%{buildroot}??g' {} \;
find %{buildroot} -type f -exec sed -i 's?^#!.*ruby.*?#!/usr/bin/ruby?g' {} \;

%check

%package -n ruby3.3-libs
Summary: Libraries necessary to run Ruby
Requires: ruby3.3 = %{epoch}:%{version}-%{release}
Provides: ruby(release) = 3.3

%description -n ruby3.3-libs
This package is a dependency package, which depends on default Ruby
version (currently v3.3).

%package -n ruby3.3-doc
Summary: Documentation for Ruby 3.3

%description -n ruby3.3-doc
This package contains the autogenerated documentation for Ruby 3.3.

%package -n ruby3.3-devel
Summary: Header files for compiling extension modules for Ruby (default version)
Requires: ruby3.3 = %{epoch}:%{version}-%{release}
Requires: ruby3.3-libs = %{epoch}:%{version}-%{release}

%description -n ruby3.3-devel
This package is a dependency package, which depends on default Ruby
version (currently v3.3).

%package -n rubygems
Summary: Package management framework for Ruby
Requires: ruby3.3 = %{epoch}:%{version}-%{release}
Provides: gem = %{epoch}:%{version}-%{release}
Provides: ruby(rubygems) = %{epoch}:%{version}-%{release}

%description -n rubygems
A package (also known as a library) contains a set of functionality that
can be invoked by a Ruby program, such as reading and parsing an XML
file. These packages are called 'gems' and RubyGems is a tool to
install, create, manage and load these packages in your Ruby
environment. RubyGems is also a client for RubyGems.org, a public
repository of Gems that allows you to publish a Gem that can be shared
and used by other developers.

%package -n rubygem-racc
Summary: Ruby LALR parser generator
Requires: ruby3.3 = %{epoch}:%{version}-%{release}
Provides: rubygem(racc) = %{epoch}:%{version}-%{release}

%description -n rubygem-racc
Racc is LALR(Look-Ahead LR) parser generator for Ruby, written in Ruby.
It allows programmers to easily write syntactic parsers from simple
rules, like yacc and bison.

%package -n rubygem-rake
Summary: Ruby make-like utility
Requires: ruby3.3 = %{epoch}:%{version}-%{release}
Provides: rubygem(rake) = %{epoch}:%{version}-%{release}

%description -n rubygem-rake
Rake is a simple ruby build program with capabilities similar to make.

%package -n rubygem-bundler
Summary: Manage Ruby application dependencies (runtime)
Requires: ruby3.3 = %{epoch}:%{version}-%{release}
Provides: rubygem(bundler) = %{epoch}:%{version}-%{release}

%description -n rubygem-bundler
Bundler manages a Ruby application's dependencies through its entire
life, across many machines, systematically and repeatably.

%package -n rubygem-syntax_suggest
Summary: Help you find the syntax when you get an "unexpected end"
Requires: ruby3.3 = %{epoch}:%{version}-%{release}
Provides: rubygem(syntax_suggest) = %{epoch}:%{version}-%{release}

%description -n rubygem-syntax_suggest
An error in your code forces you to stop. SyntaxSuggest helps you find
those errors to get you back on your way faster.

%package -n ruby3.3-rubygem-bundler
Summary: Manage Ruby application dependencies (runtime)
Requires: rubygem-bundler = %{epoch}:%{version}-%{release}

%description -n ruby3.3-rubygem-bundler
Bundler manages a Ruby application's dependencies through its entire
life, across many machines, systematically and repeatably.

%package -n rubypick
Summary: Stub to allow choosing Ruby runtime
Requires: ruby3.3 = %{epoch}:%{version}-%{release}

%description -n rubypick
Fedora /usr/bin/ruby stub to allow choosing Ruby runtime. Similarly to
rbenv or RVM, it allows non-privileged user to choose which is preferred
Ruby runtime for current task.

%package -n ruby
Summary: Interpreter of object-oriented scripting language Ruby (default version)
Requires: ruby3.3 = %{epoch}:%{version}-%{release}

%description -n ruby
This package is a dependency package, which depends on default Ruby
version (currently v3.3).

%package -n ruby-devel
Summary: Header files for compiling extension modules for Ruby (default version)
Requires: ruby3.3-devel

%description -n ruby-devel
This package is a dependency package, which depends on default Ruby
version (currently v3.3).

%if 0%{?sle_version} > 150000
%package -n ruby2.5
Summary: Interpreter of object-oriented scripting language Ruby (default version)
Requires: ruby3.3 = %{epoch}:%{version}-%{release}

%description -n ruby2.5
This package is a dependency package, which depends on default Ruby
version (currently v3.3).

%package -n ruby2.5-rubygem-bundler
Summary: Manage Ruby application dependencies (runtime)
Requires: rubygem-bundler = %{epoch}:%{version}-%{release}
Provides: rubygem(bundler) = %{epoch}:%{version}-%{release}

%description -n ruby2.5-rubygem-bundler
Bundler manages a Ruby application's dependencies through its entire
life, across many machines, systematically and repeatably.
%endif

%post -n ruby3.3-libs -p /sbin/ldconfig
%postun -n ruby3.3-libs -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/erb
%{_bindir}/irb
%{_bindir}/rbs
%{_bindir}/rdbg
%{_bindir}/rdoc
%{_bindir}/ri
%{_bindir}/ruby
%{_bindir}/typeprof
%{_mandir}/*/*

%files -n ruby3.3-libs
%dir %{_libdir}/ruby
%{_libdir}/*.so.*
%{_libdir}/ruby/*

%files -n ruby3.3-doc
%dir %{_datadir}/ri
%{_datadir}/ri/*

%files -n ruby3.3-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n rubygems
%{_bindir}/gem

%files -n rubygem-racc
%{_bindir}/racc

%files -n rubygem-rake
%{_bindir}/rake

%files -n rubygem-bundler
%{_bindir}/bundle
%{_bindir}/bundler

%files -n rubygem-syntax_suggest
%{_bindir}/syntax_suggest

%files -n ruby3.3-rubygem-bundler
%license COPYING

%files -n rubypick
%license COPYING

%files -n ruby
%license COPYING

%files -n ruby-devel
%license COPYING

%if 0%{?sle_version} > 150000
%files -n ruby2.5
%license COPYING

%files -n ruby2.5-rubygem-bundler
%license COPYING
%endif

%changelog
