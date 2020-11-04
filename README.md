# YourBankAccount
The application allows to manage a bank account. You can also create a new one or log in to yours. 

If user chooses to create a new account then a new account number is generated basic on the Luhn algorythm and for the card is provided also a PIN code. Also a default balanse -0 is assigned to every new account. All the information are added to the SQL data base.

If user chooses to log into the account then must provide an account number and the PIN. The information are veryfied with the data base. If the card or PIN is wrong then user will not be able to log in. 

After logging into account user has six options:
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit

The 1st option gives the information about current balance. At the beginning it's always 0.
The 2nd option allows to add money to the account.
The 3rd option allows to transfer money to another account which exist in the data base. User cannot transfer more money than the current balance and also cannot transfer money to own account.Programm also checks if the provided account number pass the Luhn algorythm.
The 4th option closing the account and delete it from the data base.
"Log out" option logs out from the account ans shows the main menu and "Exit" closes the application.
