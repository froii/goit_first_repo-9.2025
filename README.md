python ! 
go be ready for creating calculator ! 



# Створення venv
python -m venv venv

# Активація
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
source venv/Scripts/activate  # Git Bash

# Збереження пакетів
pip freeze > requirements.txt
Відновлення з файлу:
pip install -r requirements.txt
