NAME := nexus_autodl

ifeq ($(OS),Windows_NT)
    PATHSEP := ;
else
    PATHSEP := :
endif

# Update these paths with the correct paths to your Python executables
PYTHON_EXEC := PATH-to-python.exe		"%localappdata%\Local\Programs\Python\Python311\python.exe"
YAPF_PATH := PATH-to-yapf.exe			"%localappdata%\Local\Programs\Python\Python311\yapf.exe"
MYPY_PATH := PATH-to-mypy.exe			"%localappdata%\Local\Programs\Python\Python311\mypy.exe"
BUILD_PATH := PATH-to-pyinstaller.exe	"%localappdata%\Local\Programs\Python\Python311\pyinstaller.exe"

all: yapf mypy build

build: $(NAME).py
	$(BUILD_PATH) --clean -F --add-data templates$(PATHSEP)templates --icon icon.ico $<

clean:
	$(RM) -r build dist *.spec

mypy: $(NAME).py
	$(MYPY_PATH) $<

yapf: $(NAME).py
	$(PYTHON_EXEC) $(YAPF_PATH) -i --style style.yapf $<

.PHONY: build clean mypy yapf
