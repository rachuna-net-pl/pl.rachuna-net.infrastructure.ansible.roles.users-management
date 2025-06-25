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
## ✨ Model działania

Rola działa **w dwóch krokach**, które muszą być użyte razem:

1. **Globalna definicja użytkownika**
   W zmiennych grupowych (np. `group_vars/all.yml`) definiujesz dane kont:

   * `input_role_user_accounts` – zwykli użytkownicy,
   * `input_role_technical_accounts` – konta techniczne.

2. **Lokalna aktywacja użytkownika na hoście**
   W `group_vars/<grupa>.yml` lub `host_vars/<host>.yml` poprzez dodanie zmiennej `input_role_accounts_on_host`, która:

   * Wskazuje, którzy użytkownicy mają być założeni na danym hoście,
   * Opcjonalnie przypisuje ich do grup systemowych (`system_groups`).

> [!warning]
> ⚠️ Jeśli użytkownik nie został aktywowany przez >`input_role_accounts_on_host`, **nie zostanie założony**, nawet jeśli został zdefiniowany globalnie.


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
public_ssh_key: "klucz-publiczny"  # opcjonalne
private_ssh_key: "klucz-prywatny"  # opcjonalne
authorized_keys:  # opcjonalne
  - authorized_key: "klucz-publiczny"
    state: present

# Dla kont technicznych - ta sama struktura
```

---
## Użycie

### `group_vars/all.yml`

```yaml
user_accounts:
  - username: user1
    comment: "Pierwszy użytkownik"
    shell: /bin/bash

  - username: user2
    comment: "Drugi użytkownik"
    shell: /bin/bash

technical_accounts:
  - username: jenkins
    comment: "Konto CI"
    public_ssh_key: "ssh-rsa AAAAB3..."
```

---
### `group_vars/web-servers.yml` (lub `host_vars/web1.yml`)

```yaml
accounts_on_host:
  - username: user1
    system_groups:
      - sudo

  - username: jenkins
    system_groups:
      - docker
```

---
## 🔧 Playbook

```yaml
- hosts: all
  become: true
  roles:
    - role: users_management
      vars:
        input_role_user_accounts: "{{ user_accounts }}"
        input_role_technical_accounts: "{{ technical_accounts }}"
        input_role_accounts_on_host: "{{ accounts_on_host }}"
```

---
## 🧠 Dobre praktyki

* Umieszczaj `input_role_user_accounts` i `input_role_technical_accounts` w `group_vars/all.yml`, aby centralnie definiować konta.
* W `group_vars/<group>.yml` lub `host_vars/<host>.yml` dodawaj tylko `input_role_accounts_on_host`, aby sterować obecnością użytkowników i ich przynależnością do grup systemowych.
* Dzięki temu Twoja infrastruktura będzie **czysta**, **czytelna** i **łatwa do utrzymania**.

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
