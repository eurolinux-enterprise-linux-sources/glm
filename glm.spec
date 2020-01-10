# The library consists of headers only
%global debug_package %{nil}

Name:           glm
Version:        0.9.6.3
Release:        1%{?dist}
Summary:        C++ mathematics library for graphics programming

License:        MIT
URL:            http://glm.g-truc.net/
Source0:        http://downloads.sourceforge.net/ogl-math/%{name}-%{version}/%{name}-%{version}.zip
Patch0:         glm-0.9.5.2-smallercount.patch
Patch1:         glm-0.9.6.1-ulp.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1185298
Patch2:         glm-0.9.6.1-bigendian.patch
Patch3:         glm-0.9.6.3-nom64.patch

BuildRequires:  cmake

%description
GLM is a C++ library for doing mathematics operations
required in many OpenGL based applications. Its interface
has been designed to resemble the built-in matrix and vector
types of the OpenGL shading language.

%package        devel
Group:          Development/Libraries
Summary:        C++ mathematics library for graphics programming
BuildArch:      noarch

# As required in
# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Static_Libraries_2
Provides:       %{name}-static = %{version}-%{release}

%description    devel
GLM is a C++ library for doing mathematics operations
required in many OpenGL based applications. Its interface
has been designed to resemble the built-in matrix and vector
types of the OpenGL shading language.

%{name}-devel is only required for building software that uses
the GLM library. Because GLM currently is a header-only library,
there is no matching run time package.

%package        doc
Summary:        Documentation for %{name}-devel
Group:          Documentation
BuildArch:      noarch

%description    doc
The %{name}-doc package contains reference documentation and
a programming manual for the %{name}-devel package.

%prep
# Some glm releases, like version 0.9.3.1, place contents of
# the source archive directly into the archive root. Others,
# like glm 0.9.3.2, place them into a single subdirectory.
# The former case is inconvenient, but it can be be
# compensated for with the -c option of the setup macro.
#
# When updating this package, take care to check if -c is
# needed for the particular version.
#
# Also it looks like some versions get shipped with a common
# directory in archive root, but with an unusual name for the
# directory. In this case, use the -n option of the setup macro.
%setup -q -n glm

# A couple of files had CRLF line-ends in them.
# Check with rpmlint after updating the package that we are not
# forgetting to convert line endings in some files.
#
# This release of glm seems to have shipped with no CRLF file
# endings at all, so these are commented out.
sed -i 's/\r//' copying.txt
sed -i 's/\r//' readme.txt
sed -i 's/\r//' doc/api/doxygen.css
sed -i 's/\r//' doc/api/dynsections.js
sed -i 's/\r//' doc/api/jquery.js
sed -i 's/\r//' doc/api/tabs.css


%patch0 -p1 -b .smallercount
%patch1 -p1 -b .ulp
%patch2 -p1 -b .bigendian
%patch3 -p1 -b .nom64

%build
mkdir build
cd build
%{cmake} -DGLM_TEST_ENABLE=ON ..
make %{?_smp_mflags}

%check
cd build

# Some tests are disabled due to known upstream bugs:
# https://github.com/g-truc/glm/issues/212
# https://github.com/g-truc/glm/issues/296
ctest --output-on-failure -E '(test-gtc_packing|test-gtc_integer)'

%install
cd build

make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name CMakeLists.txt -exec rm -f {} ';'

# This is not packaged until there is consensus that
# packages should install FindSomething.cmake files.
# https://bugzilla.redhat.com/show_bug.cgi?id=1022088
rm $RPM_BUILD_ROOT%{_libdir}/cmake/FindGLM.cmake

%files devel
%doc copying.txt readme.txt
%{_includedir}/%{name}

%files doc
%doc copying.txt
%doc doc/%{name}.pdf
%doc doc/api/

%changelog
* Sun Apr 26 2015 Joonas Sarajärvi <muep@iki.fi> - 0.9.6.3-1
- Update to upstream GLM version 0.9.6.3

* Mon Apr 20 2015 David Tardon <dtardon@redhat.com> - 0.9.6.1-3
- make -devel noarch
- install license file in -doc, as required by packaging guidelines

* Wed Jan 28 2015 Dan Horák <dan[at]danny.cz> - 0.9.6.1-2
- fix build on big endian arches, patch by Jakub Cajka from #1185298

* Tue Jan 06 2015 Joonas Sarajärvi <muep@iki.fi> - 0.9.6.1-1
- Update to upstream GLM version 0.9.6.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Joonas Sarajärvi <muep@iki.fi> - 0.9.5.2-3
- Reduce test array size to avoid memory allocation failure in tests
- Resolve a number of aliasing warnings
- Disable the packing test

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 29 2014 Joonas Sarajärvi <muep@iki.fi> - 0.9.5.2-1
- Update to upstream GLM version 0.9.5.2

* Tue Sep 24 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.6-2
- Fix building on ARM

* Tue Sep 24 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.6-1
- Update to upstream GLM version 0.9.4.6
- Bug fixes

* Tue Aug 20 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.5-1
- Update to upstream GLM version 0.9.4.5
- Bug fixes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.4-1
- Update to upstream GLM version 0.9.4.4
- Bug fixes

* Mon Apr 15 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.3-1
- Update to upstream GLM version 0.9.4.3
- This version introduces just minor bug fixes

* Fri Mar 08 2013 Joonas Sarajärvi <muep@iki.fi> - 0.9.4.2-1
- Update to upstream GLM version 0.9.4.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 04 2012 Dan Horák <dan[at]danny.cz> - 0.9.3.4-2
- fix build on non-x86 arches

* Sun Sep 02 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.4-1
- Update to a new upstream version
- Work around problems in glm::log2 for integers

* Sat Sep 01 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.2-3
- Skip gtx_integer test that is known as broken

* Sat Sep 01 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.2-2
- Remove prebuilt binaries shipped in upstream source archive

* Fri May 04 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.2-1
- Update to upstream version 0.9.3.2

* Mon Feb 13 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-5
- Use global instead of define
- Clarify the comment about GLM zip archives
- Remove the unnecessary rm command from install section
- Remove misleading reference to non-existing glm package

* Mon Feb 06 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-4
- Add virtual Provides: that is required for static-only libraries
- Make descriptions in devel and doc packages more accurate

* Mon Feb 06 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-3
- Fix items pointed out in Comment 2 of #787510

* Mon Feb 06 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-2
- Build and run the self-test suite shipped with glm
- Add subpackage for manual and reference docs

* Sun Feb 05 2012 Joonas Sarajärvi <muep@iki.fi> - 0.9.3.1-1
- Initial RPM packaging
