import flet as ft
try:
    print("AudioEncoder options:")
    for e in ft.AudioEncoder:
        print(f"  {e.name}: {e.value}")
except Exception as e:
    print(e)
