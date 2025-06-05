import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from collections import deque
import pandas as pd

# Pages
page_references = [8, 1, 2, 3, 1, 4, 1, 5, 3, 4, 1, 4, 3, 2, 3, 1, 2, 8, 1, 2]
frame_size = 4

# Simulation structures
memory = deque()
memory_states = []
actions = []
page_faults = 0

for page in page_references:
    removed = None
    inserted = None
    page_fault = False

    if page not in memory:
        page_faults += 1
        page_fault = True
        if len(memory) >= frame_size:
            removed = memory.popleft()
        memory.append(page)
        inserted = page
    else:
        memory.remove(page)
        memory.append(page)

    memory_states.append(list(memory))
    actions.append({'inserted': inserted, 'removed': removed, 'page_fault': page_fault})

#Matplotlib Part
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 5)
ax.set_ylim(-0.5, frame_size - 0.5)
ax.set_yticks(range(frame_size))
ax.set_yticklabels([f"Frame {i+1}" for i in range(frame_size)])
ax.set_xlabel("Memory Frame Content")

rects = []
texts = []
for i in range(frame_size):
    rect = Rectangle((0, i - 0.4), 1, 0.8, facecolor='lightgray', edgecolor='black')
    ax.add_patch(rect)
    rects.append(rect)
    text = ax.text(0.5, i, "", ha='center', va='center', fontsize=12, color='black')
    texts.append(text)

def update(frame):
    mem = memory_states[frame]
    act = actions[frame]
    ax.set_title(f"Step {frame+1}/{len(page_references)} - Incoming Page: {page_references[frame]} | "
                 f"Total Page Faults: {sum(a['page_fault'] for a in actions[:frame+1])}")

    for i in range(frame_size):
        if i < len(mem):
            page = mem[i]
            texts[i].set_text(str(page))
            if act['inserted'] == page and act['page_fault']:
                rects[i].set_facecolor('green')  
            elif act['removed'] == page:
                rects[i].set_facecolor('red')    
            else:
                rects[i].set_facecolor('blue')   
        else:
            texts[i].set_text("")
            rects[i].set_facecolor('lightgray')

ani = FuncAnimation(fig, update, frames=len(page_references), interval=1000, repeat=False)
plt.subplots_adjust(top=0.8)
plt.show()

#EXCEL OUTPUT PART
excel_rows = []
for i, (mem, act) in enumerate(zip(memory_states, actions)):
    row = {
        "Step": i + 1,
        "Incoming Page": page_references[i],
        "Page Fault": "Yes" if act["page_fault"] else "No",
        "Inserted Page": act["inserted"] if act["page_fault"] else "",
        "Removed Page": act["removed"] if act["removed"] else ""
    }

    for j in range(frame_size):
        key = f"Memory Frame {j+1}"
        row[key] = mem[j] if j < len(mem) else ""

    excel_rows.append(row)

df = pd.DataFrame(excel_rows)
df.to_excel("lru_simulation_output.xlsx", index=False)
print("✅ Excel file created: lru_simulation_output.xlsx")
