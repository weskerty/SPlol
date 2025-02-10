import os
import json
from pathlib import Path

def get_files(directory, extensions):
    """Get all files in a directory with specific extensions."""
    try:
        return sorted([
            f for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in extensions
        ])
    except Exception as e:
        print(f"Error reading directory {directory}: {e}")
        return []

def process_gallery(image_dir, html_dir):
    """Process a single gallery directory."""
    if not os.path.exists(image_dir) or not os.path.exists(html_dir):
        print(f"Directory not found: {image_dir} or {html_dir}")
        return []
    
    image_files = get_files(image_dir, {'.jpg', '.jpeg', '.png', '.gif', '.webp'})
    html_files = get_files(html_dir, {'.html'})
    gallery_items = []
    
    # Create a mapping of HTML files for quick lookup
    html_file_map = {os.path.splitext(f)[0]: f for f in html_files}
    
    for image_file in image_files:
        name = os.path.splitext(image_file)[0]
        html_file = html_file_map.get(name)
        
        if html_file:
            gallery_items.append({
                "image": f"web/otros/Imagenes/{os.path.basename(image_dir)}/{image_file}",
                "link": f"web/otros/Imagenes/{os.path.basename(image_dir)}/{html_file}",
                "name": name
            })
    
    return gallery_items

def create_gallery_json():
    """Create the main gallery JSON file."""
    base_path = Path("web", "otros", "Imagenes")
    galleries = {}
    
    for category in ["Politicos", "Empresas"]:
        category_path = base_path / category
        print(f"Processing {category} path: {category_path}")
        
        if category_path.exists():
            galleries[category.lower()] = {
                "images": process_gallery(category_path, category_path)
            }
        else:
            print(f"Category directory not found: {category_path}")

    
    # Save the JSON
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({"galleries": galleries}, f, indent=2, ensure_ascii=False)
        print("JSON file created successfully")
    except Exception as e:
        print(f"Error creating JSON file: {e}")

if __name__ == "__main__":
    create_gallery_json()