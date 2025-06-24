import pytest
import re

def test_user_molecule_test_exists(host):
    user = host.user("molecule-test")
    assert user.exists, "Użytkownik 'molecule-test' nie istnieje!"

def test_user_molecule_test_has_gecos(host):
    user = host.user("molecule-test")
    assert user.exists, "Użytkownik 'molecule-test' nie istnieje!"
    assert user.gecos == "Molecule Test User", f"Opis użytkownika (GECOS) to '{user.gecos}', a nie 'AAAA'"

def test_user_molecule_test_has_bash_shell(host):
    user = host.user("molecule-test")
    assert user.exists, "Użytkownik 'molecule-test' nie istnieje!"
    assert user.shell == "/bin/bash", f"Użytkownik 'molecule-test' ma powłokę '{user.shell}', a nie '/bin/bash'"

def test_user_molecule_test_home_directory(host):
    user = host.user("molecule-test")
    assert user.exists, "Użytkownik 'molecule-test' nie istnieje!"
    assert user.home == "/home/molecule-test", f"Katalog domowy to '{user.home}', a nie '/home/molecule-test'"
