import os
import cv2
import requests
import numpy as np
from tkinter import Tk, Label, Button, messagebox, Canvas, Scrollbar, Frame
from tkinter.ttk import Treeview, Progressbar, Style
from PIL import Image, ImageTk
from ultralytics import YOLO
import shutil
from datetime import datetime
import base64

# URL do servidor da câmera
camera_url = "http://192.168.240.108:5000/capture"

# Função para limpar previsões antigas
def clear_old_predictions():
    save_dir = os.path.join(base_path, "runs", "detect")  
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)  
        print("Previsões antigas apagadas.")


def fetch_frame_from_server():
    try:
        
        response = requests.get(camera_url, stream=True, timeout=5)
        if response.status_code == 200:
            
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            return frame
        else:
            print(f"Falha ao obter frame. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao conectar ao servidor da camera: {e}")
        return None

def capture_and_predict():
    
    frame = fetch_frame_from_server()
    if frame is None:
        messagebox.showerror("Erro", "Falha ao capturar imagem da camera do Raspberry Pi.")
        return

    # Feedback visual
    capture_button.config(bg="#d32f2f")  # Temporariamente muda cor do botão
    root.update_idletasks()

    # Limpar previsões antigas antes de começar
    clear_old_predictions()

    # Salvar a imagem capturada temporariamente
    captured_image_path = os.path.join(base_path, "captured_image.jpg")
    cv2.imwrite(captured_image_path, frame)

    # Atualizar barra de progresso
    progress_bar["value"] = 50
    status_label.config(text="Processando imagem...")
    root.update_idletasks()

    try:
        # Carregar o modelo
        model = YOLO(model_path)

        # Fazer a previsão
        results = model.predict(source=captured_image_path, conf=0.25, save=True)

        # Obter o diretório onde os resultados foram guardadps
        save_dir = results[0].save_dir if hasattr(results[0], 'save_dir') else model.predictor.save_dir
        result_image_path = os.path.join(save_dir, os.path.basename(captured_image_path))

        
        detected_classes = [model.names[int(cls)] for cls in results[0].boxes.cls] if results and len(results[0].boxes) > 0 else []

        if "normal_box" in detected_classes and "destroyed_box" not in detected_classes:
            result_text = "Caixa em boas condições"
        elif "destroyed_box" in detected_classes:
            result_text = "Caixa danificada"
        else:
            result_text = "Nenhuma caixa identificada ou resultado incerto"

        
        result_label.config(text=f"Resultado: {result_text}")

        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_table.insert("", "end", values=(timestamp, result_text))

        
        display_image(result_image_path)

        
        progress_bar["value"] = 100
        status_label.config(text="Processamento concluído.")
    except Exception as e:
        
        messagebox.showerror("Erro", f"Erro ao processar a imagem: {e}")
        status_label.config(text="Erro no processamento.")
    finally:
        
        capture_button.config(bg="#004d40")
        progress_bar["value"] = 0

# URL da API OutSystems
    url = "https://personal-xbd4mls0.outsystemscloud.com/segrupo22_service/rest/api/post"

    try:
        # Abrir a imagem resultante e convertê-la em Base64
        with open(result_image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Dados para enviar na requisição
        payload = {
            "Estado": result_text,
            "Image": base64_image,
            "DataValidacao":timestamp
        }

        # Cabeçalhos (autenticação e tipo de conteúdo)
        headers = {
            "Content-Type": "application/json"
        }

        # Fazer requisição POST
        response = requests.post(url, json=payload, headers=headers)

        # Verificar resposta
        if response.status_code == 200:
            print("Sucesso:", response.json())
        else:
            print(f"Erro ({response.status_code}):", response.text)

    except Exception as e:
        print("Erro na requisição:", str(e))
# Função para exibir a imagem processada
def display_image(image_path):
    img = Image.open(image_path)
    img = img.resize((600, 400))  
    img_tk = ImageTk.PhotoImage(img)

    image_label.config(image=img_tk)
    image_label.image = img_tk

# Função para atualizar o feed ao vivo da camera
def update_live_feed():
    frame = fetch_frame_from_server()
    if frame is not None:
        # Converter o frame do OpenCV para o formato do PIL
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((600, 400))
        img_tk = ImageTk.PhotoImage(img)

        live_feed_label.config(image=img_tk)
        live_feed_label.image = img_tk

    
    root.after(100, update_live_feed)

# rodapw
def update_footer():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    footer_label.config(text=f"Hora Atual: {current_time} | Status da Câmera: {'Ativa' if fetch_frame_from_server() is not None else 'Inativa'}")
    root.after(1000, update_footer)

# Caminho do modelo
base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, "best.pt")

# Criar a interface
root = Tk()
root.title("Análise de Caixas - YOLO")
root.geometry("1024x768")
root.configure(bg="#e0f7fa")

# Estilo do tema
style = Style()
style.configure("TFrame", background="#e0f7fa")
style.configure("TLabel", background="#e0f7fa", font=("Helvetica", 12), foreground="#004d40")
style.configure("TButton", font=("Helvetica", 10, "bold"), foreground="#ffffff", background="#004d40")
style.map("TButton", background=[("active", "#00695c")])

# scrolldown
canvas = Canvas(root, bg="#e0f7fa")
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


title_label = Label(scrollable_frame, text="Sistema de Análise de Caixas", font=("Helvetica", 20, "bold"), bg="#e0f7fa", fg="#004d40")
title_label.pack(pady=10)

live_feed_label = Label(scrollable_frame, text="Feed da camera ao vivo", bg="#e0f7fa", relief="solid", borderwidth=1)
live_feed_label.pack(pady=10)

capture_button = Button(scrollable_frame, text="Capturar e Processar Imagem", command=capture_and_predict, bg="#004d40", fg="#ffffff", relief="raised")
capture_button.pack(pady=20)

progress_bar = Progressbar(scrollable_frame, mode="determinate", length=500)
progress_bar.pack(pady=10)

status_label = Label(scrollable_frame, text="Aguardando interação...", font=("Helvetica", 12, "italic"), bg="#e0f7fa", fg="#004d40")
status_label.pack(pady=10)

result_label = Label(scrollable_frame, text="Resultado:", font=("Helvetica", 14, "bold"), bg="#e0f7fa", fg="#004d40")
result_label.pack(pady=20)

image_label = Label(scrollable_frame, text="Imagem Processada", bg="#e0f7fa", relief="solid", borderwidth=1)
image_label.pack(pady=10)

history_label = Label(scrollable_frame, text="Histórico de Processamento", font=("Helvetica", 14, "bold"), bg="#e0f7fa", fg="#004d40")
history_label.pack(pady=10)

history_table = Treeview(scrollable_frame, columns=("Hora", "Status"), show="headings", height=8)
history_table.heading("Hora", text="Data/Hora")
history_table.heading("Status", text="Status")
history_table.pack(pady=10)

footer_label = Label(scrollable_frame, text="", font=("Helvetica", 10), bg="#004d40", fg="#ffffff", anchor="w")
footer_label.pack(fill="x", pady=10)


update_footer()


update_live_feed()


root.mainloop()
