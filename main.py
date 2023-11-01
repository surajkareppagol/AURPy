from util import AUR_PKG

pkg_name = input("📦️ Package: ")

aur_pkg = AUR_PKG(pkg_name)

aur_pkg.check_and_install_pkg()
