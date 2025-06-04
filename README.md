# H-BAR

H-BAR è una semplice applicazione da riga di comando pensata per i baristi. Consente di gestire un archivio di prodotti, allegare una foto, segnare i prodotti in test e registrare velocemente il feedback dei clienti con un punteggio da 0 a 10.

## Requisiti

- Python 3
- Facoltativo per l'interfaccia web: [Flask](https://flask.palletsprojects.com/) (installabile con `pip install flask`)

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

Il nome del database è definito in `config.py` (impostato di default su `hbar.db`). Puoi modificarlo se desideri salvare l'archivio in un percorso diverso.

## Interfaccia web

Per una versione accessibile da dispositivi mobili è disponibile una piccola applicazione web.
Per avviarla:

```bash
python web_app.py
```

Poi apri il browser su `http://localhost:5000`.
L'interfaccia utilizza Bootstrap e un foglio di stile personalizzato (in `static/css/custom.css`) per essere facilmente fruibile da mobile. Permette di cercare rapidamente i prodotti, aggiungerne di nuovi con foto, segnarli come "in test" e registrare il voto del cliente con uno slider da 0 a 10.
