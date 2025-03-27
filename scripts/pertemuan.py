import feedparser
from html import unescape
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# URL RSS feed Medium
FEED_URL = "https://medium.com/feed/@dikaelsaputra"
output_folder = "assets"
os.makedirs(output_folder, exist_ok=True)

def fetch_medium_post_summary(feed_url, post_link):
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries:
        if entry.link == post_link:
            return entry.summary  # Mengembalikan summary jika ditemukan

    return None  # Mengembalikan None jika summary tidak ditemukan

def update_readme(summary, readme_path, post_link):
    if summary is None:
        print(f"Skipping update for {readme_path} as summary is not found.")
        return  # Tidak mengubah README jika summary tidak ditemukan

    # Unescape HTML entities in the summary
    summary = unescape(summary)

    # Baca isi README yang ada
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.readlines()

    # Menandai bagian yang perlu diperbarui
    start_marker = "<!--START_SECTION:medium-->"
    end_marker = "<!--END_SECTION:medium-->"
    start_idx = None
    end_idx = None

    for idx, line in enumerate(readme_content):
        if start_marker in line:
            start_idx = idx
        if end_marker in line:
            end_idx = idx

    # Menyiapkan konten baru
    new_content = f'[Baca di Medium]({post_link})\n\n{summary}\n'

    # Hanya memperbarui jika marker ditemukan
    if start_idx is not None and end_idx is not None:
        updated_content = readme_content[:start_idx + 1] + [new_content] + readme_content[end_idx:]

        # Simpan kembali isi README yang telah diperbarui
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_content)

def fetch_post_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    thumbnail_url = soup.find('meta', {'property': 'og:image'})
    thumbnail_url = thumbnail_url['content'] if thumbnail_url else None

    publish_date = soup.find('span', {'data-testid': 'storyPublishDate'})
    publish = publish_date.text.strip() if publish_date else '0'

    readers_count = soup.find('span', {'data-testid': 'storyReadTime'})
    readers = readers_count.text.strip() if readers_count else '0'

    return thumbnail_url, publish, readers

def create_post_image(post_data, index):
    width, height = 400, 550
    image = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font_size = 62
    font = ImageFont.truetype('assets/Helvetica-Bold.ttf', font_size)
    
    if post_data[0]:
        try:
            response = requests.get(post_data[0])
            img = Image.open(BytesIO(response.content))
            img.thumbnail((400, 400))  
            image.paste(img, (0, 0))
        except Exception as e:
            print(f"Error loading image: {e}")
     
    text_claps = [f"{post_data[2]}", f"{post_data[1]}"]
    line_height = 10  
    text_x = 0       
    text_y = 415      
    
    for line in text_claps:
        draw.text((text_x, text_y), line, font=font, fill='black')
        text_y += font_size + line_height  
    
    output_path = os.path.join(output_folder, f'post_{index + 1}.png')
    image.save(output_path, "PNG")

if __name__ == "__main__":
    posts = [
        ("https://medium.com/@dikaelsaputra/instalasi-flutter-di-windows-758eb1830828?source=rss-272e0aace4a6------2", 'pertemuan-lainnya/README.md'),
        ("https://medium.com/@dikaelsaputra/instalasi-android-studio-di-windows-89c66a7fb97e?source=rss-272e0aace4a6------2", 'pertemuan-01/README.md'),
        ("https://medium.com/@dikaelsaputra/arsitektur-android-eb07231e3546?source=rss-272e0aace4a6------2", 'pertemuan-02/README.md'),
        ("https://medium.com/@dikaelsaputra/instalasi-figma-alat-desain-ui-ux-d2d3e5bade78?source=rss-272e0aace4a6------2", 'pertemuan-03/README.md'),
        ("https://medium.com/@dikaelsaputra/desain-ui-aplikasi-android-di-android-studio-9d8edc4abec5?source=rss-272e0aace4a6------2", 'pertemuan-04/README.md'),
        ("https://medium.com/@dikaelsaputra/desain-aplikasi-di-figma-langkah-tips-layout-046f84ba7ce5?source=rss-272e0aace4a6------2", 'pertemuan-05/README.md'),
        ("https://medium.com/@dikaelsaputra/mengenal-linearlayout-dan-relativelayout-di-android-studio-700bbf5a0b62?source=rss-272e0aace4a6------2", 'pertemuan-06/README.md'),
        ("https://medium.com/@dikaelsaputra/membuat-kalkulator-sederhana-di-android-studio-dengan-java-992adefbcbe8?source=rss-272e0aace4a6------2", 'pertemuan-07/README.md')
        ]
    
    for post_link, readme_path in posts:
        summary = fetch_medium_post_summary(FEED_URL, post_link)
        update_readme(summary, readme_path, post_link)

    for index, (post_url, _) in enumerate(posts):
        post_data = fetch_post_data(post_url)
        create_post_image(post_data, index)