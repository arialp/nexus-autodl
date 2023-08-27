NAME := nexus_autodl

ifeq ($(OS),Windows_NT)
    PATHSEP := ;
else
    PATHSEP := :
endif

# Update these paths with the correct paths to your Python executables in your Python installation folder
# e.g. "%localappdata%\Local\Programs\Python\Python311\python.exe" and "\Python311\Scripts\[exec].exe"
PYTHON_EXEC := PATH-to-python.exe
YAPF_PATH := PATH-to-yapf.exe
MYPY_PATH := PATH-to-mypy.exe
BUILD_PATH := PATH-to-pyinstaller.exe

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
