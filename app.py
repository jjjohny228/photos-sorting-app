from flask import Flask, render_template, jsonify, request, send_file
import shutil
from pathlib import Path

app = Flask(__name__)

# Пути (замените на свои)
DATA_DIR = Path("./")
FULL_DIR = DATA_DIR / "full_dataset"
CATEGORIES = {
    'like': Path("like"), 'dislike': Path("dislike"),
    'only_sex': Path("only_sex"), 'delete': Path("delete")
}
photo_index = 0

images = sorted(list(FULL_DIR.glob("*.jpg")) + list(FULL_DIR.glob("*.png")))

# Создать папки
for cat_dir in CATEGORIES.values():
    cat_dir.mkdir(exist_ok=True)


def get_next_image():
    """Получить случайное неотсортированное фото"""
    return images[photo_index] if images else None


@app.route('/')
def index():
    global photo_index
    img_path = get_next_image()
    photo_index += 1
    img_url = f"/image/{img_path.name}" if img_path else None
    return render_template('index.html', img_url=img_url)


@app.route('/image/<path:filename>')
def serve_image(filename):
    img_path = FULL_DIR / filename
    if img_path.exists():
        return send_file(str(img_path), mimetype='image/png')  # или 'image/jpeg'
    return "❌ File not found: " + filename, 404

@app.route('/debug')
def debug():
    return jsonify({
        'full_dir_count': len(list(FULL_DIR.glob('*'))),
        'sample_files': [f.name for f in list(FULL_DIR.glob('*'))[:3]],
        'dirs': {k: str(v.exists()) for k,v in CATEGORIES.items()}
    })


@app.route('/sort', methods=['POST'])
def sort_image():
    data = request.json
    filename = data['filename']
    category = data['category']

    src = FULL_DIR / filename
    dst = CATEGORIES[category] / filename

    if src.exists():
        shutil.move(str(src), str(dst))
        return jsonify({'status': 'ok', 'message': f'Moved to {category}'})

    return jsonify({'status': 'error', 'message': 'File not found'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5020)
