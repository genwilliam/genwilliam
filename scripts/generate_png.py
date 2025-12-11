import requests
from PIL import Image, ImageDraw, ImageFont
import json
import os

ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# 读取 GitHub 用户信息
username = "genwilliam"
user_api = f"https://api.github.com/users/{username}"
repos_api = f"https://api.github.com/users/{username}/repos?per_page=200"

user = requests.get(user_api).json()
repos = requests.get(repos_api).json()

# --- GitHub Stats PNG ---
stats_img = Image.new("RGB", (600, 200), (40, 40, 40))
draw = ImageDraw.Draw(stats_img)

font = ImageFont.load_default()

draw.text((20, 20), f"GitHub Stats - {username}", fill=(255, 255, 255), font=font)
draw.text((20, 60), f"Followers: {user.get('followers', '?')}", fill=(200, 200, 200), font=font)
draw.text((20, 90), f"Public Repos: {user.get('public_repos', '?')}", fill=(200, 200, 200), font=font)
draw.text((20, 120), f"Total Stars: {sum(r.get('stargazers_count', 0) for r in repos)}", fill=(200, 200, 200), font=font)

stats_img.save(f"{ASSETS_DIR}/github-stats.png")

# --- Top Languages PNG ---
lang_count = {}

for repo in repos:
    lang = repo.get("language")
    if lang:
        lang_count[lang] = lang_count.get(lang, 0) + 1

langs_img = Image.new("RGB", (600, 200), (30, 30, 30))
draw = ImageDraw.Draw(langs_img)

draw.text((20, 20), "Top Languages", fill=(255, 255, 255), font=font)

y = 60
for lang, count in lang_count.items():
    draw.text((20, y), f"{lang}: {count} repos", fill=(200, 200, 200), font=font)
    y += 25

langs_img.save(f"{ASSETS_DIR}/top-langs.png")

# --- Trophy PNG ---
trophy_img = Image.new("RGB", (600, 200), (50, 50, 50))
draw = ImageDraw.Draw(trophy_img)

draw.text((20, 20), "Trophies", fill=(255, 215, 0), font=font)
draw.text((20, 70), "🏆 Most Active Developer", fill=(255, 215, 0), font=font)
draw.text((20, 110), "🔥 Always Coding", fill=(255, 215, 0), font=font)

trophy_img.save(f"{ASSETS_DIR}/trophy.png")