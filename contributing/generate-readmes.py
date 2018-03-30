"""
This script updates the table of contents and all readmes in place.
"""

import os
import pathlib
import glob


def generate_main_readme(directory_of_this_script,
                         chapters,
                         chapter_titles,
                         recipes,
                         recipe_titles):

    readme = directory_of_this_script / '..' / 'README.md'
    with open(readme, 'w') as f:
        f.write("""
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/bast/cmake-recipes/master/LICENSE)

[![Travis branch](https://img.shields.io/travis/bast/cmake-recipes/master.svg?style=flat-square)](https://travis-ci.org/bast/cmake-recipes)
[![AppVeyor branch](https://img.shields.io/appveyor/ci/bast/cmake-recipes/master.svg?style=flat-square)](https://ci.appveyor.com/project/bast/cmake-recipes/branch/master)
[![Drone branch](https://www.drone-ci.science/api/badges/bast/cmake-recipes/status.svg?style=flat-square)](https://www.drone-ci.science/bast/cmake-recipes)

[![GitHub issues](https://img.shields.io/github/issues/bast/cmake-recipes.svg?style=flat-square)](https://github.com/bast/cmake-recipes/issues)
[![GitHub forks](https://img.shields.io/github/forks/bast/cmake-recipes.svg?style=flat-square)](https://github.com/bast/cmake-recipes/network)
[![GitHub stars](https://img.shields.io/github/stars/bast/cmake-recipes.svg?style=flat-square)](https://github.com/bast/cmake-recipes/stargazers)


# CMake cookbook recipes

- [Testing](testing/README.md)
- [Contributing](contributing/README.md)


## Table of contents

""")

        for chapter in chapters:
            number = int(chapter.split('-')[-1])
            f.write('- [Chapter {0}: {1}]({2}/README.md)\n'.format(number, chapter_titles[chapter], chapter))
    
        # chapter 16 is hard-coded
        f.write('- [Chapter 16: Porting a Project to CMake](https://github.com/bast/vim/compare/master...cmake-support)\n')


def locate_chapters_and_recipes(directory_of_this_script):
    """
    Returns a list of chapters and a dictionary of chapter -> list of recipes.
    """
    paths = pathlib.Path(directory_of_this_script / '..').glob('chapter-*')
    chapters = sorted((path.parts[-1] for path in paths))

    recipes = {}
    for chapter in chapters:
        paths = pathlib.Path(directory_of_this_script / '..' / chapter).glob('recipe-*')
        _recipes = sorted((path.parts[-1] for path in paths))
        recipes[chapter] = _recipes

    return chapters, recipes


def get_titles(directory_of_this_script,
               chapters,
               recipes):

    chapter_titles = {}
    for chapter in chapters:
        with open(directory_of_this_script / '..' / chapter / 'title.txt', 'r') as f:
            chapter_titles[chapter] = f.readline().strip()

    recipe_titles = {}
    for chapter in chapters:
        for recipe in recipes[chapter]:
            with open(directory_of_this_script / '..' / chapter / recipe/ 'title.txt', 'r') as f:
                recipe_titles[(chapter, recipe)] = f.readline().strip()

    return chapter_titles, recipe_titles


if __name__ == '__main__':
    directory_of_this_script = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))

    chapters, recipes = locate_chapters_and_recipes(directory_of_this_script)

    chapter_titles, recipe_titles = get_titles(directory_of_this_script,
                                               chapters,
                                               recipes)

    generate_main_readme(directory_of_this_script,
                         chapters,
                         chapter_titles,
                         recipes,
                         recipe_titles)
