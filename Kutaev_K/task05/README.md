## Техническая спецификация на классы 

**Класс Match**

Описывает матч, данные которого содержаться в файле

* `id` - идентификатор матча
* `map` - карта, на которой проводился матч
* `teams_list[]` - список команд в данном матче
* `halves_list[]` - список полуматчей данного матча

**Класс Team**

Описывает команду, принимающую участие в игре

* `name` - имя команды
* `players_list[]` - список игроков команды

**Класс Player**

Описывает игрока матча

* `steam_id` - Steam ID игрока
* `name` - имя игрока
* `team_name` - название команды

**Класс Half**

Описывает полуматч

* `number` - номер полуматча
* `ct_team` - команда за CT
* `t_team` - команда за T
* `rounds_list[]` - список раундов данного полуматча

**Класс Round**

Описывает раунд матча

* `number` - номер раунда по счету
* `winner` - команда победитель раунда 
* `kills_list[]` - список убийств в раунде
* `grenades_list[]` - список кинутых гранат
* `damage_list[]` - список урона в течении раунда
* `weapon_fires_list[]` - список выстрелов за раунд

**Класс Kills**

Описывает убийство

* `attacker_steam_id` - Steam ID атакующего игрока
* `victim_steam_id` - Steam ID жертвы
* `assistant_steam_id` - Steam ID ассист игрока
* `is_suicide` - является ли убийство [Роскомнадзор] (True/False)
* `is_firstkill` - является ли убийство first blood
* `is_headshot` - является ли убийство headshot-ом
* `is_trade` - игрок разменял или был разменян 
* `traded_steam_id` - Steam ID разменянного игрока

**Класс Grenade**

Описывает кинутую гранату

* `thrower_steam_id` - Steam ID бросающего
* `grenade_type` - тип гранаты

**Класс Damage**

Описывает урон в течении раунда

* `attacker_steam_id` - Steam ID атакующего игрока
* `victim_steam_id` - Steam ID жертвы
* `hp_damage` - нанесенный урон здоровью
* `armor_damage` - нанесенный урон броне
* `weapon` - орудие, из которого нанесен урон

**Класс Weapon fire**

Описывает выстрел в течении раунда

* `attacker_steam_id` - Steam ID атакующего игрока
* `weapon` - орудие

## Классы для подсчета статистики

**Класс Statistics**

Описывает полученную статистику 

* teams_list - список команд

**Класс TeamStats**  (наследуемся от Team)

Описывает статистику по команде

- `name` - имя команды
- `players_list[]` - список игроков команды

Новые

* first_half_score
* second_half_score
* final_score

**Класс PlayerStats** (наследуемся от Player)

Описывает статистику игрока

- `steam_id` - Steam ID игрока
- `name` - имя игрока
- `team_name` - название команды

Новые

* kills_count
* death_count
* assist_count
* accuracy
* hs_percent
* average_round_damage
* utility_damage
* kast
* rating_2_0


