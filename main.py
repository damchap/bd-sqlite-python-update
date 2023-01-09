import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def open_file():
    global filename
    filename = filedialog.askopenfilename(title="Ouvrir un fichier", filetypes=[('Fichier texte', '*.txt')])

    # afficher le chemin du fichier txt
    lbl_file = tk.Label(root, text=filename)
    lbl_file.grid(row=0, column=1, sticky='e')
    return filename


def open_db():
    global db
    db = filedialog.askopenfilename(title="Ouvrir un fichier", filetypes=[('Fichier sqlite', '*.db')])

    # afficher le chemin du fichier sqlite positionné a droite du bouton btn_db
    lbl_db = tk.Label(root, text=db)

    lbl_db.grid(row=1, column=1, sticky='e')

    return db


def update_db():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    with open(filename, 'r') as f:
        for line in f:
            # récupérer la date et le nom apres un nombre de caractere fixe (14 pour la date et 1 pour l'espace)
            date = line[:15]
            print(date)
            name = line[16:]
            print(name)
            # convertir la date en format date sqlite
            print(date)
            date = date[:4] + '-' + date[4:6] + '-' + date[6:8] + ' ' + date[9:11] + ':' + date[11:13] + ':' + date[
                                                                                                               13:15]
            print(date)
            # vérifier si la date existe dans la base de données
            c.execute('SELECT * FROM table_nom WHERE date = ?', (date,))
            if c.fetchone() is None:
                c.execute('INSERT INTO table_nom  VALUES (?, ?)', (name, date))
            else:
                c.execute('UPDATE table_nom SET nom = ? WHERE date = ?', (name, date))
    conn.commit()
    conn.close()
    messagebox.showinfo('Info', 'La base de données a été mise à jour.')


root = tk.Tk()

# Création de la fenêtre principale
root.title('Mise à jour de la base de données')
root.geometry('800x200', )

# Bouton choix du fichier txt
btn_file = tk.Button(root, text='Choisir le fichier txt', command=open_file, justify='right')
btn_file.grid(row=0, column=0, sticky='w')

# Bouton choix du fichier sqlite
btn_db = tk.Button(root, text='Choisir le fichier sqlite', command=open_db)
btn_db.grid(row=1, column=0, sticky='w')

# Bouton mise à jour de la base de données
btn_update = tk.Button(root, text='Mettre à jour la base de données', command=update_db)
btn_update.grid(row=2, column=0 , sticky='w')

# Bouton de sortie
btn_quit = tk.Button(root, text='Quitter', command=root.destroy)
btn_quit.grid(row=2, column=2, sticky='e')

# Lancement de la boucle principale
root.mainloop()
