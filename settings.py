from pathlib import Path
import sys

# Get the absolute path of the current file
FILE = Path(__file__).resolve()
# Get the parent directory of the current file
ROOT = FILE.parent
# Add the root path to the sys.path list if it is not already there
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
# Get the relative path of the root directory with respect to the current working directory
ROOT = ROOT.relative_to(Path.cwd())

# --- Fontes ---
IMAGE = 'Imagem'
VIDEO = 'Vídeo'
WEBCAM = 'Webcam'
YOUTUBE = 'YouTube'
SOURCES_LIST = [IMAGE, VIDEO, WEBCAM, YOUTUBE]

# --- Diretórios de Ativos (Assets) ---
ASSETS_DIR = ROOT / 'assets'
IMG_DIR = ASSETS_DIR / 'img'
IMAGE_DIR = ASSETS_DIR / 'images'
VIDEO_DIR = ASSETS_DIR / 'videos'
TRAINING_RESULTS_DIR = ASSETS_DIR / 'training_results'

# --- Dicionário de Imagens ---
IMAGES_DICT = {
    'imagem_1': IMAGE_DIR / 'imagem_1.jpg',
    'imagem_2': IMAGE_DIR / 'imagem_2.jpg',
    'imagem_3': IMAGE_DIR / 'imagem_3.jpg',
    'imagem_4': IMAGE_DIR / 'imagem_4.jpg',
    'imagem_5': IMAGE_DIR / 'imagem_5.jpg',
    'imagem_6': IMAGE_DIR / 'imagem_6.jpg',
    'imagem_7': IMAGE_DIR / 'imagem_7.jpg',
}

# --- Diretório de Saída (Output) ---
OUTPUT_DIR = ROOT / 'output'

# --- Diretório do Modelo ---
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best.pt'

# --- Dicionário de Vídeos ---
VIDEOS_DICT = {
    'video_1': VIDEO_DIR / 'video_1.mp4',
    'video_2': VIDEO_DIR / 'video_2.mp4',
    'video_3': VIDEO_DIR / 'video_3.mp4',
    'video_4': VIDEO_DIR / 'video_4.mp4',

}

# --- Webcam ---
WEBCAM_PATH = 0
