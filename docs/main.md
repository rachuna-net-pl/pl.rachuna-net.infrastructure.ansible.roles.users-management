## Wymagania

- Ansible w wersji co najmniej 2.9
- System operacyjny: 
  - Debian (wszystkie wersje)
  - Ubuntu (wszystkie wersje)
  - Alpine Linux (wszystkie wersje)
  - RedHat Enterprise Linux (7, 8, 9)
- Uprawnienia administratora (root) na docelowych serwerach

---
## Funkcjonalność

Rola wykonuje następujące operacje:

1. **Zarządzanie kontami użytkowników** - tworzenie i konfiguracja kont:
    - Tworzenie kont zwykłych użytkowników
    - Tworzenie kont technicznych
    - Ustawianie powłoki, katalogu domowego i komentarza
    - Zarządzanie UID i GID

2. **Konfiguracja grup** - zarządzanie grupami użytkowników:
    - Tworzenie grup dla użytkowników
    - Przypisywanie użytkowników do grup systemowych
    - Zarządzanie GID dla grup

3. **Zarządzanie kluczami SSH** - konfiguracja dostępu SSH:
    - Instalacja kluczy publicznych i prywatnych
    - Konfiguracja authorized_keys
    - Ustawianie odpowiednich uprawnień dla plików

---
## Zmienne

### Zmienne konfiguracyjne (defaults/main.yml)

| Zmienna | Domyślna wartość | Opis |
|---------|------------------|------|
| `input_role_technical_accounts` | `[]` | Lista kont technicznych do utworzenia |
| `input_role_user_accounts` | `[]` | Lista kont użytkowników do utworzenia |
| `input_role_users_on_host` | `[]` | Lista użytkowników do skonfigurowania na hoście |

### Struktura definicji użytkownika

```yaml
# Dla zwykłych użytkowników
username: nazwa_użytkownika
comment: "Komentarz dla użytkownika"
shell: /bin/bash  # opcjonalne, domyślnie /bin/bash
uid: 1000  # opcjonalne
gid: 1000  # opcjonalne
home_path: /home/użytkownik  # opcjonalne
system_groups: ['sudo', 'docker']  # opcjonalne
public_ssh_key: "klucz-publiczny"  # opcjonalne
private_ssh_key: "klucz-prywatny"  # opcjonalne
authorized_keys:  # opcjonalne
  - authorized_key: "klucz-publiczny"
    state: present

# Dla kont technicznych - ta sama struktura
```

---
## Użycie

### Podstawowa konfiguracja użytkownika

```yaml
- hosts: all
  roles:
    - role: users_management
      vars:
        input_role_user_accounts:
          - username: jan_kowalski
            comment: "Jan Kowalski"
            system_groups: ['sudo']
```

### Konfiguracja konta technicznego z kluczami SSH

```yaml
- hosts: all
  roles:
    - role: users_management
      vars:
        input_role_technical_accounts:
          - username: jenkins
            comment: "Jenkins CI Account"
            shell: /bin/bash
            public_ssh_key: "ssh-rsa AAAAB3..."
            authorized_keys:
              - authorized_key: "ssh-rsa AAAAB3..."
                state: present
```

### Konfiguracja wielu użytkowników

```yaml
- hosts: all
  roles:
    - role: users_management
      vars:
        input_role_user_accounts:
          - username: user1
            comment: "Pierwszy użytkownik"
          - username: user2
            comment: "Drugi użytkownik"
        input_role_technical_accounts:
          - username: backup
            comment: "Konto do backupu"
```

---
## Bezpieczeństwo

Rola implementuje następujące praktyki bezpieczeństwa:

- Bezpieczne uprawnienia dla plików SSH (0600)
- Bezpieczne uprawnienia dla katalogów SSH (0700)
- Możliwość definiowania określonych grup systemowych
- Ukrywanie wrażliwych danych w logach (no_log)

---
## Testowanie


> Rola zawiera testy Molecule, które można uruchomić następującymi komendami:

```bash
# Przygotowanie środowiska
python3 -m venv ~/.venvs/molecule
source ~/.venvs/molecule/bin/activate
pip install --upgrade pip
pip3 install ansible-core molecule pytest-testinfra ansible-lint

# Uruchomienie testów
molecule test

# Pojedyncze komendy
molecule create    # Utworzenie środowiska testowego
molecule converge  # Uruchomienie roli
molecule verify    # Weryfikacja rezultatów
molecule destroy   # Usunięcie środowiska testowego
```
> [!tip]
> Testy znajdują się w katalogu `molecule/default/tests/` i obejmują:
>
>   - Weryfikację tworzenia użytkowników
>   - Sprawdzenie konfiguracji katalogów domowych
>   - Testy konfiguracji powłoki
>   - Weryfikację kont technicznych

---
## Uwagi

> [!important]
> ⚠️ **Ważne**: 
> - Upewnij się, że podane grupy systemowe istnieją przed dodaniem do nich użytkowników
> - Klucze SSH powinny być odpowiednio zabezpieczone przed dodaniem do roli
> - Zaleca się używanie unikalnych UID/GID dla uniknięcia konfliktów
> - Wrażliwe dane (np. klucze SSH) powinny być przechowywane w bezpieczny sposób (np. ansible-vault)
