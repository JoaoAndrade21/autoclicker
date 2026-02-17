import pyautogui
import keyboard
import threading
import time
import tkinter as tk
from tkinter import ttk
import json
import os

CONFIG_FILE = "config.json"
running = False
click_thread = None

# ========================
# Configuração
# ========================

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "cps": 10,
        "clicks": 1,
        "button": "left",
        "hotkey": "F8",
        "fixed_position": False,
        "timer": 0
    }

def save_config():
    config = {
        "cps": float(cps_entry.get()),
        "clicks": int(clicks_entry.get()),
        "button": button_var.get(),
        "hotkey": hotkey_var.get(),
        "fixed_position": fixed_var.get(),
        "timer": int(timer_entry.get())
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = load_config()

# ========================
# Auto Click
# ========================

def click_loop():
    global running
    save_config()

    try:
        cps = float(cps_entry.get())
        clicks_per_action = int(clicks_entry.get())
        button = button_var.get()
        timer = int(timer_entry.get())
    except:
        status_label.config(text="Valores inválidos!", fg="red")
        return

    delay = 1 / cps
    start_time = time.time()

    if fixed_var.get():
        fixed_pos = pyautogui.position()

    while running:
        if timer > 0 and (time.time() - start_time) >= timer:
            break

        for _ in range(clicks_per_action):
            if not running:
                break

            if fixed_var.get():
                pyautogui.click(fixed_pos.x, fixed_pos.y, button=button)
            else:
                pyautogui.click(button=button)

            time.sleep(delay)

    running = False
    status_label.config(text="Status: PAUSADO", fg="red")

def toggle_clicking():
    global running, click_thread

    if not running:
        running = True
        status_label.config(text="Status: ATIVO", fg="#00ff88")
        click_thread = threading.Thread(target=click_loop, daemon=True)
        click_thread.start()
    else:
        running = False
        status_label.config(text="Status: PAUSADO", fg="red")

def set_hotkey():
    keyboard.unhook_all_hotkeys()
    keyboard.add_hotkey(hotkey_var.get(), toggle_clicking)

# ========================
# Interface
# ========================

root = tk.Tk()
root.title("Auto Clicker PRO")
root.geometry("400x420")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#1e1e1e", foreground="white")
style.configure("TButton", padding=6)
style.configure("TCheckbutton", background="#1e1e1e", foreground="white")

title = tk.Label(root, text="AUTO CLICKER PRO", bg="#1e1e1e", fg="#00ff88", font=("Arial", 16, "bold"))
title.pack(pady=10)

def add_label(text):
    ttk.Label(root, text=text).pack(pady=5)

add_label("Cliques por segundo (CPS):")
cps_entry = ttk.Entry(root)
cps_entry.insert(0, config["cps"])
cps_entry.pack()

add_label("Cliques por ação:")
clicks_entry = ttk.Entry(root)
clicks_entry.insert(0, config["clicks"])
clicks_entry.pack()

add_label("Botão do mouse:")
button_var = tk.StringVar(value=config["button"])
ttk.Combobox(root, textvariable=button_var, values=["left", "right"], state="readonly").pack()

add_label("Tecla de Atalho:")
hotkey_var = tk.StringVar(value=config["hotkey"])
ttk.Combobox(root, textvariable=hotkey_var, values=["F8", "F12"], state="readonly").pack()

add_label("Timer (segundos, 0 = infinito):")
timer_entry = ttk.Entry(root)
timer_entry.insert(0, config["timer"])
timer_entry.pack()

fixed_var = tk.BooleanVar(value=config["fixed_position"])
ttk.Checkbutton(root, text="Usar posição fixa (pega posição ao iniciar)", variable=fixed_var).pack(pady=10)

ttk.Button(root, text="Aplicar Tecla", command=set_hotkey).pack(pady=5)
ttk.Button(root, text="Iniciar / Pausar", command=toggle_clicking).pack(pady=10)

status_label = tk.Label(root, text="Status: PAUSADO", bg="#1e1e1e", fg="red", font=("Arial", 12, "bold"))
status_label.pack(pady=10)

set_hotkey()

root.mainloop()
