from ultralytics import YOLO
import streamlit as st
import cv2
import yt_dlp
import pandas as pd
import PIL
import settings
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from pathlib import Path
import tempfile
import random
import string
import os
import numpy as np

# Garante que o diretório de SAÍDA exista ao iniciar
settings.OUTPUT_DIR.mkdir(exist_ok=True)

# Mapeamento de classes
CLASSES = {
    0: "Vidro", 1: "Lata", 2: "Papel",
    3: "Plástico"
}

# Mapeamento de Pontos por Classe
PONTOS_POR_CLASSE = {
    "Vidro": 10,
    "Lata": 15,
    "Papel": 0,
    "Plástico": 5
}

def load_model(model_path):
    """Carrega o modelo YOLO a partir do caminho especificado."""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Erro ao carregar o modelo: {e}")
        return None

def save_uploaded_file(uploaded_file):
    """Salva um arquivo carregado em um local temporário e retorna o caminho."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Erro ao salvar arquivo temporário: {e}")
        return None

def process_uploaded_images(source_imgs, model, confidence):
    """
    Processa uma lista de imagens carregadas (ou caminhos de imagem), realiza a detecção
    e retorna os dados e as imagens para exibição.
    """
    
    # Ordena as imagens pelo nome do arquivo (se for objeto) ou pelo caminho (se for str)
    source_imgs.sort(key=lambda x: x.name if hasattr(x, 'name') else x)
    
    detections_data = []
    processed_images_display = []
    for i, source_image in enumerate(source_imgs):
        # Se for um caminho de arquivo (string), abre a imagem. Se for um objeto UploadedFile, também funciona.
        img_pil = PIL.Image.open(source_image).convert('RGB')
        res = model.predict(img_pil, conf=confidence)
        boxes = res[0].boxes
        res_plotted = res[0].plot()[:, :, ::-1]
        processed_images_display.append({'original': img_pil, 'detected': res_plotted})
        
        classes = [int(box.cls[0]) for box in boxes]
        detected_class_names = [CLASSES.get(cls, "") for cls in classes]
        status = "Reciclável" if detected_class_names else "Nenhum item"
        
        # Calcula a pontuação
        score = sum(PONTOS_POR_CLASSE.get(name, 0) for name in detected_class_names)

        # Define o nome da fonte
        source_name = os.path.basename(source_image) if isinstance(source_image, str) else source_image.name

        detections_data.append({
            'Fonte': f"Imagem {i+1:02d} ({source_name})",
            'Itens': len(classes),
            'Classes': detected_class_names,
            'Pontos': score,
            'Status': status
        })
    return detections_data, processed_images_display

def process_video_stream(vid_cap, model, confidence, source_name='Vídeo Analisado', tracker=None, roi_coords=None, counting_direction=None, line_position_percent=None, trail_length=30):
    """
    Processa um stream de vídeo (com exibição), exibe os resultados lado a lado
    e coleta dados de detecção para o relatório.
    """
    col1, col2 = st.columns(2)
    st_frame1 = col1.empty()
    st_frame2 = col2.empty()

    counted_ids = set()
    track_history = {}
    all_detected_classes = []

    while vid_cap.isOpened():
        success, image = vid_cap.read()
        if not success:
            break

        image_resized = cv2.resize(image, (720, int(720 * (9/16))))

        if roi_coords and counting_direction and line_position_percent is not None:
            res_plotted, detected_classes, new_counted_ids, new_track_history = process_video_frame(
                image_resized, model, confidence, counted_ids, roi_coords, track_history, counting_direction, line_position_percent, display=True, trail_length=trail_length
            )
            counted_ids = new_counted_ids
            track_history = new_track_history
            all_detected_classes.extend(detected_classes)
        else:
            res = model.predict(image_resized, conf=confidence)
            res_plotted = res[0].plot()
            boxes = res[0].boxes
            frame_classes = [int(box.cls[0]) for box in boxes]
            all_detected_classes.extend(frame_classes)
        
        st_frame1.image(image_resized, caption='Original', channels="BGR", width='stretch')
        st_frame2.image(res_plotted, caption='Detectado', channels="BGR", width='stretch')

    vid_cap.release()
    
    all_detected_class_names_for_scoring = [CLASSES.get(cls, "") for cls in all_detected_classes]
    score = sum(PONTOS_POR_CLASSE.get(name, 0) for name in all_detected_class_names_for_scoring)

    unique_classes_ids = sorted(list(set(all_detected_classes)))
    detected_class_names_display = [CLASSES.get(cls, "") for cls in unique_classes_ids]
    status = "Reciclável" if detected_class_names_display else "Nenhum item"
    
    detections_data = [{
        'Fonte': source_name,
        'Itens': len(counted_ids) if roi_coords else len(all_detected_classes),
        'Classes': detected_class_names_display,
        'Pontos': score,
        'Status': status
    }]
    return detections_data

def process_video_stream_for_batch(vid_cap, model, confidence, roi_coords=None, counting_direction=None, line_position_percent=None, trail_length=30):
    """
    Versão modificada que não exibe frames, apenas processa e retorna os dados.
    Ideal para análise em lote, para não poluir a tela.
    """
    counted_ids = set()
    track_history = {}
    all_detected_classes = []

    while vid_cap.isOpened():
        success, image = vid_cap.read()
        if not success:
            break

        if roi_coords and counting_direction and line_position_percent is not None:
            _, detected_classes, new_counted_ids, new_track_history = process_video_frame(
                image, model, confidence, counted_ids, roi_coords, track_history, counting_direction, line_position_percent, display=False, trail_length=trail_length
            )
            counted_ids = new_counted_ids
            track_history = new_track_history
            all_detected_classes.extend(detected_classes)
        else:
            res = model.predict(image, conf=confidence, verbose=False)
            boxes = res[0].boxes
            frame_classes = [int(box.cls[0]) for box in boxes]
            all_detected_classes.extend(frame_classes)

    vid_cap.release()
    
    all_detected_class_names_for_scoring = [CLASSES.get(cls, "") for cls in all_detected_classes]
    score = sum(PONTOS_POR_CLASSE.get(name, 0) for name in all_detected_class_names_for_scoring)

    unique_classes_ids = sorted(list(set(all_detected_classes)))
    detected_class_names_display = [CLASSES.get(cls, "") for cls in unique_classes_ids]
    status = "Reciclável" if detected_class_names_display else "Nenhum item"
    
    detections_data = [{
        'Fonte': 'Vídeo em Lote',
        'Itens': len(counted_ids) if roi_coords else len(all_detected_classes),
        'Classes': detected_class_names_display,
        'Pontos': score,
        'Status': status
    }]
    return detections_data

def process_batch_videos(uploaded_videos, model, confidence, progress_bar, status_text, roi_coords=None, counting_direction=None, line_position_percent=None, trail_length=30):
    """
    Processa uma lista de vídeos carregados em lote.
    """
    batch_detections_data = []
    total_videos = len(uploaded_videos)
    for i, video_file in enumerate(uploaded_videos):
        progress_bar.progress((i) / total_videos)
        status_text.text(f"Analisando vídeo {i+1}/{total_videos}: {video_file.name}")
        temp_video_path = save_uploaded_file(video_file)
        if temp_video_path:
            try:
                vid_cap = cv2.VideoCapture(temp_video_path)
                video_detections = process_video_stream_for_batch(vid_cap, model, confidence, roi_coords, counting_direction, line_position_percent, trail_length=trail_length)
                if video_detections:
                    video_detections[0]['Fonte'] = video_file.name
                    batch_detections_data.extend(video_detections)
            except Exception as e:
                st.error(f"Não foi possível processar o vídeo {video_file.name}. Erro: {e}")
            finally:
                Path(temp_video_path).unlink()
    progress_bar.progress(1.0)
    status_text.text(f"Análise de {total_videos} vídeo(s) concluída!")
    return batch_detections_data

def process_stored_video(conf, model, source_vid_key, roi_coords=None, counting_direction=None, line_position_percent=None, trail_length=30):
    """Lida com a lógica de vídeo da lista pré-definida."""
    try:
        source_vid_path = str(settings.VIDEOS_DICT.get(source_vid_key))
        vid_cap = cv2.VideoCapture(source_vid_path)
        return process_video_stream(vid_cap, model, conf, source_name=source_vid_key, roi_coords=roi_coords, counting_direction=counting_direction, line_position_percent=line_position_percent, trail_length=trail_length)
    except Exception as e:
        st.error(f"Erro ao carregar vídeo: {e}")
        return []

def get_youtube_stream_url(youtube_url):
    """Extrai a URL de stream de um vídeo do YouTube."""
    try:
        ydl_opts = {'format': 'best[ext=mp4]', 'no_warnings': True, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info['url']
    except Exception as e:
        st.error(f"Não foi possível obter o vídeo do YouTube. A URL é válida? Erro: {e}")
        return None

def process_video_frame(image, model, confidence, counted_ids, roi_coords, track_history, counting_direction, line_position_percent, display=True, trail_length=30):
    """
    Processa um único frame de vídeo, realiza o rastreamento de objetos,
    conta itens que cruzam uma linha em uma região de interesse (ROI) e retorna o frame com as anotações.
    """
    height, width, _ = image.shape
    roi_x1 = int(width * roi_coords[0] / 100)
    roi_y1 = int(height * roi_coords[1] / 100)
    roi_x2 = int(width * roi_coords[2] / 100)
    roi_y2 = int(height * roi_coords[3] / 100)

    res = model.track(image, conf=confidence, persist=True, tracker="bytetrack.yaml", verbose=False)
    
    if display:
        res_plotted = res[0].plot()
    else:
        res_plotted = image.copy()

    if display:
        # Desenha a ROI
        cv2.rectangle(res_plotted, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)
        cv2.putText(res_plotted, "Area de Contagem", (roi_x1, roi_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Lógica da Linha de Contagem
        is_horizontal = "cima" in counting_direction
        if is_horizontal:
            line_y = roi_y1 + int((roi_y2 - roi_y1) * line_position_percent / 100)
            cv2.line(res_plotted, (roi_x1, line_y), (roi_x2, line_y), (255, 0, 0), 2)
        else: # Vertical
            line_x = roi_x1 + int((roi_x2 - roi_x1) * line_position_percent / 100)
            cv2.line(res_plotted, (line_x, roi_y1), (line_x, roi_y2), (255, 0, 0), 2)

    detected_classes = []
    if res[0].boxes.id is not None:
        boxes = res[0].boxes.xyxy.cpu().numpy().astype(int)
        ids = res[0].boxes.id.cpu().numpy().astype(int)
        clss = res[0].boxes.cls.cpu().numpy().astype(int)

        for box, track_id, cls in zip(boxes, ids, clss):
            center_x, center_y = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2

            if track_id not in track_history:
                track_history[track_id] = []
            
            # Limita o histórico de rastro
            track_history[track_id].append((center_x, center_y))
            if len(track_history[track_id]) > trail_length:
                track_history[track_id].pop(0) # Remove o ponto mais antigo

            # Desenha o ponto central
            if display:
                cv2.circle(res_plotted, (center_x, center_y), 5, (0, 255, 0), -1)

            # Desenha o rastro
            if display and len(track_history[track_id]) > 1:
                cv2.polylines(res_plotted, [np.array(track_history[track_id], np.int32)], False, (0, 255, 255), 2)


            if len(track_history[track_id]) > 1:
                prev_x, prev_y = track_history[track_id][-2]
                
                if roi_x1 < center_x < roi_x2 and roi_y1 < center_y < roi_y2:
                    is_horizontal = "cima" in counting_direction
                    if is_horizontal:
                        line_y = roi_y1 + int((roi_y2 - roi_y1) * line_position_percent / 100)
                    else: # Vertical
                        line_x = roi_x1 + int((roi_x2 - roi_x1) * line_position_percent / 100)
                    
                    crossed = False
                    if counting_direction == "De baixo para cima" and prev_y > line_y and center_y <= line_y:
                        crossed = True
                    elif counting_direction == "De cima para baixo" and prev_y < line_y and center_y >= line_y:
                        crossed = True
                    elif counting_direction == "Da esquerda para a direita" and prev_x < line_x and center_x >= line_x:
                        crossed = True
                    elif counting_direction == "Da direita para a esquerda" and prev_x > line_x and center_x <= line_x:
                        crossed = True

                    if crossed and track_id not in counted_ids:
                        counted_ids.add(track_id)
                        detected_classes.append(cls)
                        if display:
                            cv2.circle(res_plotted, (center_x, center_y), 5, (0, 0, 255), -1)

    if display:
        count_text = f"Itens Contados: {len(counted_ids)}"
        cv2.putText(res_plotted, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return res_plotted, detected_classes, counted_ids, track_history

def create_graphs_in_memory(detections_data):
    """Cria gráficos para o relatório e retorna como um dicionário de caminhos de arquivo."""
    graph_images = {}
    if not detections_data: return graph_images
    df = pd.DataFrame(detections_data)
    all_classes = [item for sublist in df['Classes'] for item in sublist]
    if all_classes:
        class_counts = pd.Series(all_classes).value_counts()
        plt.figure(figsize=(10, 6)); class_counts.plot(kind='bar', color='skyblue')
        plt.title("Frequência de Classes Detectadas", fontsize=16); plt.ylabel("Contagem", fontsize=14)
        plt.xticks(rotation=45, ha='right'); plt.tight_layout()
        hist_path = settings.OUTPUT_DIR / "histograma_classes.png"
        plt.savefig(hist_path); plt.close()
        graph_images['histogram'] = str(hist_path)
        
        plt.figure(figsize=(10, 6)); plt.pie(class_counts, labels=class_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title("Proporção de Classes Detectadas", fontsize=16)
        pie_path = settings.OUTPUT_DIR / "proporcao_classes.png"
        plt.savefig(pie_path); plt.close()
        graph_images['pie_chart'] = str(pie_path)

    status_counts = df['Status'].value_counts()
    plt.figure(figsize=(8, 5)); sns.barplot(x=status_counts.index, y=status_counts.values, hue=status_counts.index, palette="rocket", legend=False)
    plt.title("Análise de Status (Reciclável vs. Nenhum item)", fontsize=16); plt.ylabel("Contagem", fontsize=14)
    status_path = settings.OUTPUT_DIR / "analise_status.png"
    plt.savefig(status_path); plt.close()
    graph_images['status_bar'] = str(status_path)
    return graph_images

def generate_pdf_report(detections_data, graph_images):
    """Gera um relatório PDF unificado com pontuação e cupom de desconto."""
    pdf = FPDF(); pdf.set_auto_page_break(auto=True, margin=15); pdf.add_page()
    pdf.set_font("Arial", 'B', 16); pdf.cell(0, 10, 'Relatório de Análise de Recicláveis', 0, 1, 'C')
    pdf.set_font("Arial", 'I', 12); pdf.cell(0, 10, f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'C'); pdf.ln(10)
    
    # Tabela de Detalhes
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(45, 10, 'Fonte', 1); pdf.cell(20, 10, 'Nº Itens', 1)
    pdf.cell(20, 10, 'Pontos', 1); pdf.cell(80, 10, 'Classes Detectadas', 1)
    pdf.cell(25, 10, 'Status Final', 1); pdf.ln()
    pdf.set_font("Arial", '', 9)
    total_pontos = sum(item.get('Pontos', 0) for item in detections_data)
    for item in detections_data:
        class_str = ', '.join(item['Classes']) if item['Classes'] else "Nenhuma"
        pdf.cell(45, 10, str(item['Fonte']), 1)
        pdf.cell(20, 10, str(item['Itens']), 1)
        pdf.cell(20, 10, str(item.get('Pontos', 0)), 1)
        x_before, y_before = pdf.get_x(), pdf.get_y()
        pdf.multi_cell(80, 10, class_str, 1, 'L'); pdf.set_xy(x_before + 80, y_before)
        pdf.cell(25, 10, item['Status'], 1); pdf.ln()
    
    # Seção do Cupom
    if total_pontos > 0:
        credito_valor = total_pontos * 0.01 # 1 ponto = R$ 0,01
        coupon_code = generate_coupon_code()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16); pdf.cell(0, 10, 'Seu Cupom de Desconto', 0, 1, 'C'); pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Pontuação Total: {total_pontos} pontos", 0, 1, 'C')
        pdf.cell(0, 10, f"Valor do Crédito: R$ {credito_valor:.2f}", 0, 1, 'C')
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 14); pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 15, f"CÓDIGO: {coupon_code}", 1, 1, 'C', fill=True)

    if graph_images:
        pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, 'Análise Gráfica', 0, 1, 'C'); pdf.ln(5)
        for graph_path in graph_images.values():
            if Path(graph_path).exists():
                pdf.image(graph_path, w=180); pdf.ln(5)
    pdf_file_path = settings.OUTPUT_DIR / "relatorio_analise.pdf"
    pdf.output(pdf_file_path)
    return pdf_file_path

def generate_coupon_code(length=12):
    """Gera um código de cupom aleatório no formato XXXX-XXXX-XXXX."""
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(length))
    return f"{code[:4]}-{code[4:8]}-{code[8:]}"