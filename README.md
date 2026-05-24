# event-planner

link here:
https://event-planner-b5mk.onrender.com/

descpr.:
projekt na programko; new lebo stary som omylom wipol cize to je iba rerun

zadanie:
Zadanie 8: Webová aplikácia „Plánovanie udalostí a registrácia účastníkov“

Cieľ projektu

Vytvorte webovú aplikáciu na plánovanie udalostí, správu miest konania a registráciu účastníkov.

Backend musí byť vytvorený v Django.
Frontend je ľubovoľný.

Aplikácia musí byť na konci projektu nasadená online na free platforme.

Opis aplikácie

Organizátor potrebuje systém, v ktorom bude možné:

- vytvárať udalosti
- určovať miesto konania
- priraďovať kategórie alebo tagy
- registrovať účastníkov
- sledovať kapacitu udalosti

Povinné modely

1. Event
- názov
- popis
- dátum
- čas
- kapacita
- miesto konania

2. Location
- názov miesta
- adresa
- mesto
- kapacita

3. Tag
- názov tagu
- popis

4. User
- používateľ systému

Povinný M:N vzťah

Povinné riešenie:
Event ↔ User

Odporúčané riešenie cez model Registration
- používateľ
- udalosť
- dátum registrácie
- stav registrácie

Voliteľne môžete pridať:
Event ↔ Tag

Povinné funkcionality

CRUD operácie

Minimálne pre:
- Event
- Location
- Tag

Registrácia účastníkov
- registrovať používateľa na udalosť
- odhlásiť používateľa z udalosti
- zobraziť zoznam účastníkov
- kontrolovať kapacitu udalosti

Vyhľadávanie a filtrovanie
- podľa dátumu
- podľa mesta
- podľa tagu
- podľa organizátora

Prihlásenie používateľa

Minimálne 2 roly:
- organizátor / admin
- účastník

API alebo frontend
- Django templates + jednoduché API
alebo
- oddelený frontend + REST API

Povinné nasadenie

Projekt musí byť nasadený online na free platforme.

Povinné odovzdanie
- Git repozitár
- odkaz na aplikáciu
- README
- stručná dokumentácia
- prezentácia

Spoločné požiadavky pre všetky zadania

Každý projekt musí obsahovať:
- backend v Django
- databázové modely a migrácie
- aspoň jeden vzťah M:N
- CRUD operácie nad hlavnými entitami
- autentifikáciu používateľa
- minimálne 2 používateľské roly
- filtrovanie alebo vyhľadávanie
- Git repozitár
- README
- nasadenie na free platforme
