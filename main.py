#!/usr/bin/env python3

####################
##  Focus Finder  ##
##  for Empire TV ##
##  2025 by SFoX  ##
####################

import os
import platform
import locale
from collections import defaultdict

try:
    from termcolor import colored
    use_colors = True
except ImportError:
    def colored(text, color, attrs=None):
        return text
    use_colors = False

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def get_language():
    current_locale = locale.getlocale()
    if not current_locale[0]:
        current_locale = locale.getdefaultlocale()

    language = current_locale[0] if current_locale and current_locale[0] else "en"

    if language.startswith("de"):
        return "de"
    return "en"

def get_prompt_message(language, key):
    messages = {
        "de": {
            "prompt": "Bitte geben Sie bis zu 3 Zielgruppen ein (oder 'exit' zum Beenden):",
            "exit": "Programm beendet.",
            "none_entered": "Keine Zielgruppen eingegeben.",
            "group": "Zielgruppe"
        },
        "en": {
            "prompt": "Please enter up to 3 target groups (or 'exit' to quit):",
            "exit": "Program exited.",
            "none_entered": "No target groups entered.",
            "group": "Target group"
        }
    }
    return messages[language].get(key, "")

def get_genres(language):
    genre_data = {
        "de": {
            "Männer": ["Action", "Sport", "Western", "SciFi", "Horror"],
            "Frauen": ["Comedy", "Spielshow: Drama", "Liebe", "Horror"],
            "Kinder": ["Fantasy", "Comedy", "SciFi", "Western", "Musik"],
            "Rentner": ["Doku", "Western", "Spielshow: Drama"],
            "Paare": ["Liebe", "Drama", "Musik", "Spielshow: Horror"],
            "Musiker": ["Musik", "Horror", "Fantasy", "Action", "Western"],
            "Sportler": ["Sport", "Liebe", "Doku", "Action", "Drama", "Comedy"],
            "Streber": ["SciFi", "Fantasy", "Doku", "Western", "Horror"]
        },
        "en": {
            "Men": ["Action", "Sport", "Western", "SciFi", "Horror"],
            "Women": ["Comedy", "Game Show: Drama", "Love", "Horror"],
            "Children": ["Fantasy", "Comedy", "SciFi", "Western", "Music"],
            "Elders": ["Documentary", "Western", "Game Show: Drama"],
            "Lovers": ["Love", "Drama", "Music", "Game Show: Horror"],
            "Rockers": ["Music", "Horror", "Fantasy", "Action", "Western"],
            "Athletes": ["Sport", "Love", "Documentary", "Action", "Drama", "Comedy"],
            "Nerds": ["SciFi", "Fantasy", "Documentary", "Western", "Horror"]
        }
    }
    return genre_data.get(language, genre_data["en"])

def get_selected_target_groups(language):
    prompt = get_prompt_message(language, "prompt")
    exit_message = get_prompt_message(language, "exit")
    group_label = get_prompt_message(language, "group")

    print("\n" + prompt)
    selected_target_groups = []
    for i in range(1, 4):
        target_group = input(f"{i}. {group_label}? ").strip().lower()
        if target_group == "exit":
            print(exit_message)
            return None
        if target_group:
            selected_target_groups.append(target_group)
        else:
            break
    return selected_target_groups

def calculate_common_genres(selected_target_groups, genres):
    if not selected_target_groups:
        return []

    common_genres = set(genres[selected_target_groups[0].capitalize()])
    for group in selected_target_groups[1:]:
        common_genres &= set(genres.get(group.capitalize(), []))

    genre_scores = defaultdict(int)
    for group in selected_target_groups:
        group_genres = genres.get(group.capitalize(), [])
        for rank, genre in enumerate(group_genres, start=1):
            if genre in common_genres:
                genre_scores[genre] += len(group_genres) - rank + 1

    return sorted(genre_scores, key=genre_scores.get, reverse=True)

def print_colored_genres(genres, language):
    colors = ["green", "yellow", "yellow", "red", "red"]
    if language == "de":
        genre_message = "Gemeinsame Genres, gewichtet nach Wichtigkeit:"
    else:
        genre_message = "Common genres, weighted by importance:"
    print(genre_message)

    for rank, genre in enumerate(genres, start=1):
        if use_colors:
            color = colors[min(rank - 1, len(colors) - 1)]
            print(colored(f"{rank}. {genre}", color))
        else:
            print(f"{rank}. {genre}")

def display_available_groups(language, genres):
    if language == "de":
        genre_message = "Verfügbare Gruppen: "
    else:
        genre_message = "Available Groups: "
    print(genre_message)
    if use_colors:
        print(", ".join([colored(group, "white", attrs=["bold"]) for group in genres.keys()]))
    else:
        print(", ".join(genres.keys()))

def main():
    language = get_language()
    genres = get_genres(language)

    while True:
        display_available_groups(language, genres)
        selected_target_groups = get_selected_target_groups(language)
        if selected_target_groups is None:
            break

        if selected_target_groups:
            common_genres = calculate_common_genres(selected_target_groups, genres)
            print_colored_genres(common_genres, language)
        else:
            print(get_prompt_message(language, "none_entered"))
        print("\n")

if __name__ == "__main__":
    clear_terminal()
    main()
