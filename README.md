**Service auto**
**Aplicatie tip consola**  
    1. CRUD mașină: id, model, an achiziție, nr. km, în garanție. Km și anul achiziției să fie strict pozitivi.  
    2. CRUD card client: id, nume, prenume, CNP, data nașterii (`dd.mm.yyyy`), data înregistrării (`dd.mm.yyyy`). CNP-ul trebuie să fie unic.  
    3. CRUD tranzacție:  id, id_mașină, id_card_client (poate fi nul), sumă piese, sumă manoperă, data și ora. Dacă există un card client, atunci aplicați o reducere de `10%` pentru manoperă. Dacă mașina este în garanție, atunci piesele sunt gratis. Se tipărește prețul plătit și reducerile acordate.  
    4. Căutare mașini și clienți. Căutare full text.  
    5. Afișarea tuturor tranzacțiilor cu suma cuprinsă într-un interval dat.  
    6. Afișarea mașinilor  ordonate descrescător după suma obținută pe manoperă.  
    7. Afișarea cardurilor client ordonate descrescător după valoarea reducerilor obținute.  
    8. Ștergerea tuturor tranzacțiilor dintr-un anumit interval de zile.  
    9. Actualizarea garanției la fiecare mașină: o mașină este în garanție dacă și numai dacă are maxim `3` ani de la achiziție și maxim `60 000` de km.  

0. Teste și specificații la toate iterațiile.

1. **Iterația 1** 
   - Toate CRUD-urile, minim încă o funcționalitate diferită de CRUD. Cu validări, arhitectură stratificată cu toate elementele descrise la curs. Salvarea datelor în fișiere.  

2. **Iterația 2**
   - Toate funcționalitățile în afară de Undo+Redo. 
   - Repository generic, clase proprii de excepții. 
   - Folosirea type hinting, ABC, protocol.

3. **Iterația 3**
   - Implementat Undo+Redo eficient.
   - Refactorizat toate funcționalitățile posibile folosind `map`, `filter`, `list comprehensions`, `reduce`, `filter`.
   - Refactorizat minim o metodă folosind recursivitate.
   - Refactorizat minim două metode folosind lambda.
   - Implementat și folosit o funcție proprie de sortare care să aibă aceeași interfață cu funcția `sorted` din Python. 
  
**căutare full text** înseamnă că stringul introdus de utilizator se caută în toate câmpurile tuturor entităților menționate. Se returnează toate entitățile în ale căror câmpuri se găsește stringul. Se pot returna entități de tipuri diferite.
