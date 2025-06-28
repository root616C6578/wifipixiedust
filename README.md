# wifipixiedust

WiFi Pixie Dust — це інструмент для сканування Wi-Fi мереж та виконання Pixie Dust або mkd4 атак на WPS-захищені мережі. Проєкт використовує Python і бібліотеку Scapy для сканування мереж, а також Reaver і mkd4 для виконання атак.

## Особливості

- Сканування доступних Wi-Fi мереж у режимі моніторингу.
- Виведення SSID, BSSID та каналу кожної знайденої мережі.
- Виконання Pixie Dust або mkd4 атак на WPS-захищені мережі.
- Підтримка ручного вибору мережі та методу атаки.
- Перевірка прав root та існування інтерфейсу перед запуском.
- Обмеження часу виконання Pixie Dust атаки (120 секунд).

## Вимоги

- Python 3.8 або новіший.
- Права адміністратора для запуску скрипта.
- Мережева карта з підтримкою режиму моніторингу.
- Встановлені утиліти:
  - [Scapy](https://scapy.net/)
  - [Reaver](https://github.com/t6x/reaver-wps-fork-t6x)
  - mkd4 (опційно, для mkd4 атаки)

## Установка

1. Клонувати репозиторій:
   ```bash
   git clone https://github.com/root616C6578/wifipixiedust.git
   cd wifipixiedust
   ```
2. Встановити залежності:
   ```bash
   sudo apt install reaver
   pip install scapy
   # Для mkd4 атаки встановіть mkd4 окремо
   ```
3. Запустити скрипт:
   ```bash
   sudo python attack.py
   ```

## Використання

1. Перевести мережеву карту в режим моніторингу (скрипт зробить це автоматично, але інтерфейс має існувати):
   ```bash
   sudo ifconfig wlan0 down
   sudo iwconfig wlan0 mode monitor
   sudo ifconfig wlan0 up
   ```
2. Запустити скрипт:
   ```bash
   sudo python attack.py
   ```
3. Вибрати інтерфейс, мережу та тип атаки (Pixie Dust або mkd4), слідувати інструкціям у консолі.

## Приклад виводу

```
Enter the interface name: wlan0
Scanning for networks (press Ctrl+C to stop)...
SSID: Network1, BSSID: 00:11:22:33:44:55, Channel: 6
SSID: Network2, BSSID: 66:77:88:99:AA:BB, Channel: 11

Available networks:
0: Network1 (00:11:22:33:44:55) on Channel 6
1: Network2 (66:77:88:99:AA:BB) on Channel 11

Enter the number of the network to attack: 0

Choose an attack method:
1. Pixie Dust
2. mdk4
3. Exit
Choose attack method: 1

Running Pixie Dust attack...
```

## Попередження

Цей інструмент призначений виключно для освітніх цілей та тестування безпеки власних мереж. Використання його для несанкціонованого доступу до чужих мереж є незаконним.

## Ліцензія

Цей проєкт ліцензований під [MIT License](LICENSE)
