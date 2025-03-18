creazione di un programma che dagli ascx del questionario, tenta, tramite l'uso dell'intelligenza artificiale di compilare il tracciato spss usato per le elaborazioni successive.
al momento i dati di cui dispone sono limitati (20 record), ma si spera che in futuro con l'apprendimento possa spiccare il volo.
presenta 3 tab:
train/Allena => dove mostrargli l'ascx e come deve venire interpretato;
generate/genera => dove da una cartella di file ascx tenta di creare il tracciato spss sulla base delle informazioni ottenute dal modello allenato;
update/Aggiorna => dove prende i file generato e ti permette di sistemare le voci, per poi caricarle dentro al modello
in più presenta una tab chiamata settings/impostazioni dove si può cambiare la lingua e esportare/importare i file del modello (utile per la condivisione)

il programma usa scikit-learn
per compilare il programma, bisogna avere installato pyinstaller e lanciare questo comando:
pyinstaller --onefile --windowed --add-data "data;data" main.py

i file csv, json e il modello sono anche salvati in questa cartella temporanea all'esecuzione del programma:
C:\Users\<username>\AppData\Local\Temp\_MEIXXXXXX\data
