# H-BAR

H-BAR è una semplice applicazione da riga di comando pensata per i baristi. Consente di gestire un archivio di prodotti, allegare una foto, segnare i prodotti in test e registrare velocemente il feedback dei clienti con un punteggio da 0 a 10.

## Requisiti

- Python 3

## Utilizzo

1. **Aggiungere un prodotto**
   ```bash
   python hbar.py add "Nome prodotto" --photo /percorso/foto.jpg --in-test
   ```

2. **Elencare i prodotti** (i prodotti in test compaiono in alto)
   ```bash
   python hbar.py list
   ```

3. **Cercare un prodotto**
   ```bash
   python hbar.py search "termini"
   ```

4. **Marcare o smarcare un prodotto come "in test"**
   ```bash
   python hbar.py mark <id_prodotto>
   python hbar.py mark <id_prodotto> --off  # per rimuovere la modalità test
   ```

5. **Registrare rapidamente il feedback di un cliente**
   ```bash
   python hbar.py rate <id_prodotto> <punteggio_da_0_a_10>
   ```

Il database SQLite `hbar.db` viene creato nella stessa cartella e mantiene le informazioni tra un utilizzo e l'altro.
