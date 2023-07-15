from os import remove

"""
REMOVE SKIN RENDERS
"""
for i in range(10):
    for j in range(0, 360, 180):
        try:
            remove(f"{i} {j}.png")
        except:
            pass
