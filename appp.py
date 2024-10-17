import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect('agenda_db.sqlite')

# Função para criar a tabela de clientes
def create_table():
    conn = connect_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS Cliente (
        Numero INTEGER PRIMARY KEY,
        Nome TEXT NOT NULL,
        Endereco TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Função para adicionar um cliente
def add_cliente():
    try:
        numero = int(entry_numero.get())
        nome = entry_nome.get()
        endereco = entry_endereco.get()

        # Verificar se todos os campos estão preenchidos
        if not nome or not endereco:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        conn = connect_db()
        conn.execute('INSERT INTO Cliente (Numero, Nome, Endereco) VALUES (?, ?, ?)', (numero, nome, endereco))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
        clear_entries()
        load_clientes()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "O número do cliente deve ser único.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para carregar os clientes na tabela
def load_clientes():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.execute('SELECT * FROM Cliente')
    for row in cursor:
        tree.insert('', 'end', values=row)
    conn.close()

# Função para consultar um cliente pelo número
def consult_cliente():
    try:
        numero = int(entry_numero.get())
        conn = connect_db()
        cursor = conn.execute('SELECT * FROM Cliente WHERE Numero = ?', (numero,))
        client = cursor.fetchone()
        conn.close()

        if client:
            # Preenche os campos com os dados do cliente encontrado
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, client[1])  # Nome
            entry_endereco.delete(0, tk.END)
            entry_endereco.insert(0, client[2])  # Endereço
        else:
            messagebox.showwarning("Atenção", "Cliente não encontrado.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para editar um cliente selecionado
def edit_cliente():
    try:
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um cliente para editar.")
            return

        item = tree.item(selected_item)
        numero = item['values'][0]  # Pega o número do cliente selecionado
        nome = entry_nome.get()
        endereco = entry_endereco.get()

        # Verificar se todos os campos estão preenchidos
        if not nome or not endereco:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        conn = connect_db()
        conn.execute('UPDATE Cliente SET Nome = ?, Endereco = ? WHERE Numero = ?', (nome, endereco, numero))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente alterado com sucesso!")
        clear_entries()
        load_clientes()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para excluir um cliente selecionado
def delete_cliente():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
        return

    item = tree.item(selected_item)
    numero = item['values'][0]

    conn = connect_db()
    conn.execute('DELETE FROM Cliente WHERE Numero = ?', (numero,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
    load_clientes()

# Função para limpar os campos de entrada
def clear_entries():
    entry_numero.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)

# Configuração da interface do Tkinter
app = tk.Tk()
app.title("Gerenciamento de Clientes")
app.geometry("600x400")
app.configure(bg="#f0f0f0")  # Cor de fundo

# Criação da tabela de clientes no banco de dados
create_table()

# Frame para entrada de dados
frame_entry = tk.Frame(app, bg="#ffffff", bd=2, relief=tk.RAISED)
frame_entry.pack(pady=10, padx=10, fill=tk.X)

label_numero = tk.Label(frame_entry, text="Número:", bg="#ffffff")
label_numero.grid(row=0, column=0, padx=5, pady=5)
entry_numero = tk.Entry(frame_entry)
entry_numero.grid(row=0, column=1, padx=5, pady=5)

label_nome = tk.Label(frame_entry, text="Nome:", bg="#ffffff")
label_nome.grid(row=1, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_entry)
entry_nome.grid(row=1, column=1, padx=5, pady=5)

label_endereco = tk.Label(frame_entry, text="Endereço:", bg="#ffffff")
label_endereco.grid(row=2, column=0, padx=5, pady=5)
entry_endereco = tk.Entry(frame_entry)
entry_endereco.grid(row=2, column=1, padx=5, pady=5)

# Botões para ações
frame_buttons = tk.Frame(app, bg="#f0f0f0")
frame_buttons.pack(pady=10)

btn_add = tk.Button(frame_buttons, text="Adicionar", command=add_cliente, bg="#4CAF50", fg="white")
btn_add.grid(row=0, column=0, padx=5)

btn_consult = tk.Button(frame_buttons, text="Consultar", command=consult_cliente, bg="#2196F3", fg="white")
btn_consult.grid(row=0, column=1, padx=5)

btn_edit = tk.Button(frame_buttons, text="Alterar", command=edit_cliente, bg="#FFC107", fg="white")
btn_edit.grid(row=0, column=2, padx=5)

btn_delete = tk.Button(frame_buttons, text="Excluir", command=delete_cliente, bg="#F44336", fg="white")
btn_delete.grid(row=0, column=3, padx=5)

# Tabela para exibir os clientes
columns = ('Numero', 'Nome', 'Endereco')
tree = ttk.Treeview(app, columns=columns, show='headings')
tree.heading('Numero', text='Número')
tree.heading('Nome', text='Nome')
tree.heading('Endereco', text='Endereço')
tree.pack(pady=10, padx=10, fill=tk.X)

# Estilo para a tabela
style = ttk.Style()
style.configure("Treeview", background="#ffffff", foreground="#000000", rowheight=25, fieldbackground="#ffffff")
style.configure("Treeview.Heading", background="#4CAF50", foreground="white", font=('Arial', 10, 'bold'))
style.map('Treeview.Heading', background=[('active', '#5D8A3D')])

# Carregar clientes existentes
load_clientes()

# Iniciar a aplicação
app.mainloop()
