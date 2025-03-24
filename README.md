# RAG_Praktik
Din kode implementerer en RAG (Retrieval-Augmented Generation)-model, der kombinerer søgning i ChromaDB med svargenerering fra OpenAI.

 - database.py: Læser PDF'er, opdeler teksten og gemmer den i ChromaDB.
 - chatbot.py: Søger i ChromaDB efter relevante tekststykker og bruger OpenAI til at formulere svar baseret på fundet information.

Systemet sikrer, at svarene kun er baseret på de gemte data og ikke på AI'ens generelle viden
