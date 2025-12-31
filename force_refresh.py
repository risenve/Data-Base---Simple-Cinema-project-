
import sys
sys.path.insert(0, '.')

print("=== Force refreshing SQLAlchemy metadata ===")

from app.database import Base, engine

# 1. Очистить ВСЁ
Base.metadata.clear()

# 2. Пересоздать метаданные из БД
Base.metadata.reflect(bind=engine)

# 3. Проверить
print("Tables after refresh:", list(Base.metadata.tables.keys()))

if 'events' in Base.metadata.tables:
    table = Base.metadata.tables['events']
    print("\nColumns in 'events':")
    for col in table.columns:
        print(f"  - {col.name}: {col.type}")
    
    # Проверить, есть ли extra_metadata
    has_extra = 'extra_metadata' in table.columns
    print(f"\nHas extra_metadata column: {has_extra}")

# 4. Переимпортировать модели
import importlib
import app.models
importlib.reload(app.models)

print("\n✅ Metadata refreshed")
