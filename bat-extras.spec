%global debug_package %{nil}

Name:           bat-extras
Version:        2022.07.27
Release:        2%{?dist}
Summary:        Bash scripts that integrate bat with various command line tools

License:        MIT
URL:            https://github.com/eth-p/bat-extras
Source0:        %{url}/archive/v%{version}.tar.gz

Requires:       bat git man-db ripgrep
BuildRequires:  bat git

BuildArch:      noarch

%description
Bash scripts that integrate bat with various command line tools.

- batgrep
  - Quickly search through and highlight files using ripgrep.
  - Requirements: ripgrep
- batman
  - Read system manual pages (man) using bat as the manual page formatter.
- batpipe
  - A less (and soon bat) preprocessor for viewing more types of files in the terminal.
- batwatch
  - Watch for changes in one or more files, and print them with bat.
  - Requirements: entr (optional)
- batdiff
  - Diff a file against the current git index, or display the diff between two files.
  - Requirements: bat, delta (optional)
- prettybat
  - Pretty-print source code and highlight it with bat.
  - Requirements: (see doc/prettybat.md)

%prep
%autosetup

# get static binaries of shfmt
%global _shfmt_ver 3.5.1
case "$(uname -m)" in
    x86_64)
        _ARCH=amd64
        ;;
    aarch64)
        _ARCH=arm64
        ;;
    *)
        echo "Unsupported architecture!"
        exit 1
        ;;
esac
_SHFMT_DL_URL="https://github.com/mvdan/sh/releases/download/v%{_shfmt_ver}/shfmt_v%{_shfmt_ver}_linux_${_ARCH}"

mkdir shfmt-bin
curl -Lfo "shfmt-bin/shfmt" "${_SHFMT_DL_URL}"
chmod +x "shfmt-bin/shfmt"
# bin in shfmt-bin

%build
_SHFMT_BIN_DIR=$(realpath "shfmt-bin")
export PATH="${_SHFMT_BIN_DIR}:${PATH}"

./build.sh

%install
# bin
mkdir -p %{buildroot}%{_bindir}
install -Dpm 755 -t %{buildroot}%{_bindir} bin/bat{grep,man,pipe,watch,diff} bin/prettybat

# manpage
mkdir -p %{buildroot}%{_mandir}/man1
install -Dpm 644 -t %{buildroot}%{_mandir}/man1 man/*

# doc
mkdir -p %{buildroot}%{_docdir}/%{name}
install -Dpm 644 -t %{buildroot}%{_docdir}/%{name} doc/*

%files
%license LICENSE.md
%doc README.md
%{_bindir}/batgrep
%{_bindir}/batman
%{_bindir}/batpipe
%{_bindir}/batwatch
%{_bindir}/batdiff
%{_bindir}/prettybat
%{_mandir}/man1/batgrep.1*
%{_mandir}/man1/batman.1*
%{_mandir}/man1/batpipe.1*
%{_mandir}/man1/batwatch.1*
%{_mandir}/man1/batdiff.1*
%{_mandir}/man1/prettybat.1*
%{_docdir}/%{name}/*

%changelog
* Tue Aug 09 2022 cyqsimon - 2022.07.27-2
- Build for `noarch`

* Wed Aug 03 2022 cyqsimon - 2022.07.27-1
- Release 2022.07.27
