import mysql.connector
import csv

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sklep"
    )

def list_clients():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM klienci")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()

def search_client():
    nazwisko = input("Podaj nazwisko klienta: ")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM klienci WHERE nazwisko LIKE %s", (f"%{nazwisko}%",))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print("Brak klienta o takim nazwisku.")
    cursor.close()
    conn.close()

def client_orders():
    try:
        client_id = int(input("Podaj ID klienta: "))
    except ValueError:
        print("ID musi być liczbą!")
        return
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM zamowienia WHERE klient_id = %s", (client_id,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("Brak zamówień dla tego klienta.")
    cursor.close()
    conn.close()

def order_value():
    try:
        zamowienie_id = int(input("Podaj ID zamówienia: "))
    except ValueError:
        print("ID musi być liczbą!")
        return
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(p.cena * z.ilosc)
        FROM pozycje_zamowienia z
        JOIN produkty p ON z.produkt_id = p.id
        WHERE z.zamowienie_id = %s
    """, (zamowienie_id,))
    result = cursor.fetchone()
    if result and result[0]:
        print(f"Wartość zamówienia: {result[0]:.2f} PLN")
    else:
        print("Zamówienie nie istnieje lub brak pozycji.")
    cursor.close()
    conn.close()

def export_to_csv():
    table = input("Podaj nazwę tabeli do eksportu: ")
    if table not in ["klienci", "produkty", "zamowienia", "pozycje_zamowienia"]:
        print("Nieprawidłowa tabela.")
        return
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    with open(f"{table}.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Zapisano {table}.csv")
    cursor.close()
    conn.close()

def menu():
    while True:
        print("\nMENU:")
        print("1. Wyświetl listę klientów")
        print("2. Wyszukaj klienta po nazwisku")
        print("3. Wyświetl zamówienia klienta")
        print("4. Oblicz wartość zamówienia")
        print("5. Eksport tabeli do CSV")
        print("0. Wyjście")
        wybor = input("Wybierz opcję: ")
        if wybor == "1":
            list_clients()
        elif wybor == "2":
            search_client()
        elif wybor == "3":
            client_orders()
        elif wybor == "4":
            order_value()
        elif wybor == "5":
            export_to_csv()
        elif wybor == "0":
            break
        else:
            print("Nieznana opcja.")

if __name__ == "__main__":
    menu()
