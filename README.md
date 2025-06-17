# wifipixiedust

WiFi Pixie Dust — це інструмент для сканування Wi-Fi мереж та виконання Pixie Dust атак на WPS-захищені мережі. Цей проєкт використовує Python і бібліотеку Scapy для сканування мереж, а також Reaver для виконання атак.

## Особливості

- Сканування доступних Wi-Fi мереж у режимі моніторингу.
- Виведення SSID, BSSID та каналу кожної знайденої мережі.
- Виконання Pixie Dust атак на WPS-захищені мережі.
- Підтримка ручного вибору мережі для атаки.

## Вимоги

- Python 3.8 або новіший.
- Права адміністратора для запуску скрипта.
- Мережева карта з підтримкою режиму моніторингу.
- Встановлені утиліти:
  - [Scapy](https://scapy.net/)
  - [Reaver](https://github.com/t6x/reaver-wps-fork-t6x)

## Установка

1. Клонувати репозиторій:
   ```bash
   git clone https://github.com/yourusername/wifipixiedust.git
   cd wifipixiedust
2. Встановлення залежності:
  ```apt install reaver

```markdown
   ```

3. Встановити Python-залежності:
   ```bash
   pip install -r requirements.txt
   ```

## Використання

1. Перевести мережеву карту в режим моніторингу:
   ```bash
   sudo ifconfig wlan0 down
   sudo iwconfig wlan0 mode monitor
   sudo ifconfig wlan0 up
   ```

2. Запустити скрипт:
   ```bash
   python main.py
   ```

3. Вибрати мережу для атаки та слідувати інструкціям.

## Приклад виводу

```
Scanning for networks...
SSID: Network1, BSSID: 00:11:22:33:44:55, Channel: 6
SSID: Network2, BSSID: 66:77:88:99:AA:BB, Channel: 11

Discovered networks:
1. SSID: Network1, BSSID: 00:11:22:33:44:55, Channel: 6
2. SSID: Network2, BSSID: 66:77:88:99:AA:BB, Channel: 11

Select a network to attack: 1
Running Pixie Dust attack...
```

## Попередження

Цей інструмент призначений виключно для освітніх цілей та тестування безпеки власних мереж. Використання його для несанкціонованого доступу до чужих мереж є незаконним.

## Ліцензія

Цей проєкт ліцензований під [MIT License](LICENSE).
```
