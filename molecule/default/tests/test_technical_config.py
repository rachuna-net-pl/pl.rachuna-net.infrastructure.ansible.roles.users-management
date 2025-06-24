import pytest
import re

def test_user_molecule_test_exists(host):
    user = host.user("molecule-technical-test")
    assert user.exists, "Użytkownik 'molecule-technical-test' nie istnieje!"

def test_user_molecule_test_has_gecos(host):
    user = host.user("molecule-technical-test")
    assert user.exists, "Użytkownik 'molecule-technical-test' nie istnieje!"
    assert user.gecos == "Molecule Technical Test User", f"Opis użytkownika (GECOS) to '{user.gecos}', a nie 'AAAA'"

def test_user_molecule_test_has_bash_shell(host):
    user = host.user("molecule-technical-test")
    assert user.exists, "Użytkownik 'molecule-technical-test' nie istnieje!"
    assert user.shell == "/bin/bash", f"Użytkownik 'molecule-technical-test' ma powłokę '{user.shell}', a nie '/bin/bash'"

def test_user_molecule_test_home_directory(host):
    user = host.user("molecule-technical-test")
    assert user.exists, "Użytkownik 'molecule-technical-test' nie istnieje!"
    assert user.home == "/home/molecule-technical-test", f"Katalog domowy to '{user.home}', a nie '/home/molecule-technical-test'"
