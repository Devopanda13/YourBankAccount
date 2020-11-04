
# from string import digits
from secrets import choice
from random import randint
import sqlite3

conn = sqlite3.connect('card2.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card (
  id INTEGER, 
  number TEXT, 
  pin TEXT, 
  balance INTEGER DEFAULT 0)""")
conn.commit()


class BankCard:

  def __init__(self, card_number, pin_number):
    global cur
    self.card_number = card_number
    self.pin_number = pin_number
    cur.execute('SELECT * FROM card')
    results = cur.fetchall()
    rows_number = len(results)

    cur.execute("INSERT INTO card VALUES (:id, :number, :pin, :balance)",
      {"id":rows_number+1, "number": self.card_number, "pin":self.pin_number,"balance": 0})
    conn.commit()


  def loggingin(self, card_number_tocheck, pin_number_tocheck):
    global cur
    self.card_number_tocheck = card_number_tocheck
    self.pin_number_tocheck = pin_number_tocheck

    cur.execute("SELECT pin FROM card WHERE number = :number",{"number": self.card_number_tocheck})
    correct_pin = (cur.fetchall())
    if correct_pin != []:
      correct_pin = str(correct_pin[0][0])
      if correct_pin == self.pin_number_tocheck:
        print("\nYou have successfully logged in!\n")
        BankCard.loggedin(self)
      else:
        print("Wrong card number or PIN!\n")
    else:
      print("Wrong card number or PIN!\n")


  def loggedin(self):
    while True:
      loggedin_action = input('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n')
      if loggedin_action == "1":
        cur.execute("SELECT balance FROM card WHERE number = :number",{"number": self.card_number_tocheck})
        print("\nBalance:",cur.fetchall()[0][0],"\n")
      elif loggedin_action == "2":
        new_card = BankCard.add_income(self)
      elif loggedin_action == "3":
        BankCard.do_transfer(self)
      elif loggedin_action == "4":
        BankCard.close_account(self)
      elif loggedin_action == "5":
        print("\nYou have successfully logged out!\n")
        break
      elif loggedin_action == "0":
        exit()

  def luhn_algorithm(x):
    y = x[:-1]
    index = 0
    new_code = []
    while index < 15:
      for i in y[index]:
        i = int(i)
        if index%2 == 0 or index == 0:
          i = i*2
        if i > 9:
          i -= 9
        index += 1
        new_code.append(i)

    items_sum = sum(new_code)
    if items_sum%10 == 0:
      contr_no = '0'
    else:
      contr_no = (items_sum - (items_sum%10) + 10) - items_sum

    new_card_number = x[:-1] + str(contr_no)
    return new_card_number
  
  def add_income(self):
    income = input("\nEnter income:\n")
    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?",(income, self.card_number_tocheck))
    conn.commit()
    print("Income was added!\n")

  def do_transfer(self):
    print("\nTransfer")
    number_for_transfer = input("Enter card number:\n")
    luhn_card_no = BankCard.luhn_algorithm(number_for_transfer)
    if number_for_transfer != luhn_card_no:
      print("Probably you made a mistake in the card number. Please try again!\n")
    else:
      cur.execute("SELECT number FROM card WHERE number = :number",{"number": number_for_transfer})
      number_for_transfer = cur.fetchall()
      if number_for_transfer == []:
        print("Such a card does not exist.\n")
      else:
        number_for_transfer = str(number_for_transfer[0][0])
        if number_for_transfer == self.card_number_tocheck:
          print("You can't transfer money to the same account!\n")
        else:
          money_to_transfer = int(input("Enter how much money you want to transfer:\n"))
          cur.execute("SELECT balance FROM card WHERE number = :number",{"number": self.card_number_tocheck})
          current_balance = (cur.fetchall()[0][0])
          if current_balance >= money_to_transfer:
            cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?",(money_to_transfer, number_for_transfer))
            conn.commit()
            cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?",(money_to_transfer, self.card_number_tocheck))
            conn.commit()
            print("Success!\n")
          else:
            print("Not enough money!\n")

  def close_account(self):
    cur.execute("DELETE FROM card WHERE  number = :number",{"number": self.card_number_tocheck})
    conn.commit()
    print("\nThe account has been closed!\n")
    main()


def main():
  while True:
    action = input("1. Create an account \n2. Log into account \n0. Exit\n")

    if action == '1':
      print("\nYour card has been created\nYour card number:")
      card_number = '400000' + (''.join(choice('0123456789') for i in range(10)))
      new_card_number = BankCard.luhn_algorithm(card_number)
      print(new_card_number)
      pin_number = ''.join(choice('123456789') for i in range(4))
      print("Your card PIN: \n" + pin_number + "\n")
      newcard = BankCard(new_card_number,pin_number)

    elif action == '2':
      card_number_tocheck = input("\nEnter your card number:\n")
      pin_number_tocheck = input("Enter your PIN:\n")
      newcard = BankCard(None, None)
      newcard.loggingin(card_number_tocheck,pin_number_tocheck)

    elif action == '0':
      print("Bye!")
      conn.close()
      break
    else:
      print("Please enter the right number")

main()
