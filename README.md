# RAG_Praktik
Din kode implementerer en RAG (Retrieval-Augmented Generation)-model, der kombinerer søgning i ChromaDB med svargenerering fra OpenAI.

database.py: 
- Formål: Læse PDF-filer, dele dem op i mindre bidder og gemme dem i ChromaDB.
  1. PDF'er indlæses fra mappen "data".
  2. Teksten splittes i små bidder (300 tegn med 100 overlap).
  3. Data gemmes i ChromaDB (en lokal database til søgning).

 🔹 Efter kørsel af database.py har du nu en database med tekststykker fra PDF'erne.

chatbot.py: 
- Formål: Søge i ChromaDB og få svar fra OpenAI.
  1. Bruger indtaster et spørgsmål.
  2. ChromaDB søger efter det mest relevante tekststykke.
  3. OpenAI bruger tekststykket til at formulere et svar.
  4. Svaret vises på skærmen.
  5. Programmet fortsætter, indtil brugeren skriver "exit", "quit" eller "stop".

 🔹 Systemet sikrer, at svarene kun er baseret på de gemte data og ikke på AI'ens generelle viden
