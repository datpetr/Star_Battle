import pygame
import os
import sys
import pkgutil
import start screen

search_path = ['.'] # Используем None, чтобы увидеть все модули, импортируемые из sys.path
all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
print(all_modules)
