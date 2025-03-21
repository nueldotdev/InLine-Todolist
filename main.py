import curses
from datetime import datetime
import json
import os

# File to store tasks
TASKS_FILE = "tasks.json"

# Load tasks from JSON file if it exists
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
            if not tasks:  # If the task list is empty
                return []  # Return an empty list instead of None
            return tasks
    return []  # Return an empty list for first-time use

# Save tasks to JSON file
def save_tasks():
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


tasks = load_tasks()  # Load tasks from file
selected_task = 0  # Tracks the current task 


def draw_menu(stdscr):
    global selected_task, tasks

    # Initialize colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(3, curses.COLOR_WHITE, -1)  # Light gray for unselected tasks
    curses.init_pair(2, curses.COLOR_YELLOW, -1)  # Bright color for selected task

    curses.init_color(177, 85, 87, 85)
    curses.init_pair(3, 177, -1)
    
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.refresh()

    while True:
        stdscr.clear()
        curses.init_pair(4, curses.COLOR_BLUE, -1)  # Blue color for the title
        stdscr.addstr(0, 0, "InLine Task Manager", curses.A_BOLD | curses.color_pair(4))
        stdscr.addstr(1, 0, "------------------")

        if not tasks:  # First-time use or no tasks
            stdscr.addstr(3, 0, "Welcome to InLine! 🎉", curses.color_pair(2))
            stdscr.addstr(5, 0, "It looks like you don't have any tasks yet.")
            stdscr.addstr(6, 0, "Press 'a' to add your first task!")
            stdscr.addstr(8, 0, "Commands: [h] Help, [q] Quit")
        else:
            for i, task in enumerate(tasks):
                star = "⭐" if task["starred"] else ""
                check = "✅" if task["completed"] else "⬛"
                tags = ", ".join(task["tags"]) if task["tags"] else ""
                important = "(!)" if task['important'] else ""

                # Apply styles based on selection
                # Display task text and tags
                number = f"{i + 1}. "
                task_line = f"{check} {important} {task['text']} {star}"
                if tags:
                    task_line = f"{check} {important} {task['text']} {star} ({tags})"

                if i == selected_task:
                    # Selected task: bright color + underline + bold
                    style = curses.color_pair(2) | curses.A_UNDERLINE | curses.A_BOLD
                    no_style = curses.color_pair(3)
                    pointer_style = curses.color_pair(4) | curses.A_BOLD  # Different color for pointer
                    
                    stdscr.addstr(i + 2, 0, number, no_style)
                    stdscr.addstr(i + 2, len(number), task_line, style)  # Display task text and tags
                    stdscr.addstr(i + 2, len(task_line) + 4, "<", pointer_style)  # Add a pointer to the end of the selected task
                else:
                  # Unselected tasks: light gray
                  number = f"{i + 1}."
                  style = curses.color_pair(3)
                  
                  task_line = f"{number} {check} {important} {task['text']} {star}"
                  if tags:
                      task_line = f"{number} {check} {important} {task['text']} {star} ({tags})"
                  stdscr.addstr(i + 2, 0, task_line, style)
            
            # Get some stats
            completed_tasks = [task for task in tasks if task["completed"]]
            completed_percentage = (len(completed_tasks) / len(tasks)) * 100 if tasks else 0
            stdscr.addstr(len(tasks) + 3, 0, f"{int(completed_percentage)}% of all tasks complete.", curses.color_pair(3))
            
            # Display task summary
            done_tasks = len([task for task in tasks if task["completed"]])
            pending_tasks = len(tasks) - done_tasks
            curses.init_pair(5, curses.COLOR_GREEN, -1)  # Green for done tasks
            curses.init_pair(6, curses.COLOR_WHITE, -1)  # Gray for pending tasks
            curses.init_pair(7, curses.COLOR_MAGENTA, -1)  # Gray for pending tasks
            
            completed = f"{done_tasks} "
            pending = f"{pending_tasks} "
            
            stdscr.addstr(len(tasks) + 4, 0, completed, curses.color_pair(5))
            stdscr.addstr(len(tasks) + 4, len(completed), "done ", curses.color_pair(3))
            stdscr.addstr(len(tasks) + 4, len(completed) + 5, f"• ", curses.color_pair(3))
            stdscr.addstr(len(tasks) + 4, len(completed) + 7, pending, curses.color_pair(7))
            stdscr.addstr(len(tasks) + 4, len(completed) + 7 + len(pending), f"pending", curses.color_pair(3))

            # Display commands
            stdscr.addstr(len(tasks) + 5, 0, "Commands: [h] Help, [q] Quit", curses.color_pair(3))

        stdscr.refresh()

        key = stdscr.getch()

        # Handle key presses
        if key == ord('h'):  # Show help
            stdscr.clear()
            stdscr.addstr(0, 0, "Help - Commands:")
            stdscr.addstr(2, 0, "Arrow keys: Navigate tasks")
            stdscr.addstr(3, 0, "Space: Toggle completion")
            stdscr.addstr(4, 0, "Star [*]: Toggle starring")
            stdscr.addstr(5, 0, "a: Add new task")
            stdscr.addstr(6, 0, "d: Delete task")
            stdscr.addstr(7, 0, "t: Add/Edit tags")
            stdscr.addstr(8, 0, "q: Quit")
            stdscr.addstr(10, 0, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()  # Wait for any key press
        elif key == 450:  # Up Arrow
            if tasks and selected_task > 0:
                selected_task -= 1
        elif key == 456:  # Down Arrow
            if tasks and selected_task < len(tasks) - 1:
                selected_task += 1
        elif key == ord(' '):  # Toggle completion
            if tasks:
                tasks[selected_task]["completed"] = not tasks[selected_task]["completed"]
                save_tasks()  # Save after change
        elif key == ord('*'):  # Toggle starring
            if tasks:
                tasks[selected_task]["starred"] = not tasks[selected_task]["starred"]
                save_tasks()  # Save after change
        elif key == ord('a'):  # Add new task
            stdscr.addstr(len(tasks) + 6, 0, "Enter new task: ")
            curses.echo()
            new_task_text = stdscr.getstr(len(tasks) + 6, 17).decode('utf-8')
            curses.noecho()
            if new_task_text:
                stdscr.addstr(len(tasks) + 7, 0, "Enter tags (comma-separated): ")
                curses.echo()
                new_task_tags = stdscr.getstr(len(tasks) + 7, 27).decode('utf-8')
                curses.noecho()
                
                stdscr.addstr(len(tasks) + 8, 0, "Is this important? (Y/N): ")
                curses.echo()
                importance = chr(stdscr.getch(len(tasks) + 8, 27)).lower()
                curses.noecho()
                
                important: bool = False
                
                while importance not in ["y", "n", ""]:
                  stdscr.addstr(len(tasks) + 9, 0, "Invalid input. Please enter 'Y' or 'N': ")
                  curses.echo()
                  importance = chr(stdscr.getch(len(tasks) + 9, 37)).lower()
                  curses.noecho()

                if importance == "y":
                  important = True
                elif importance == "n" or importance == "":
                  important = False
                  
                
                new_task = {
                    "id": len(tasks) + 1 if tasks else 1,
                    "text": new_task_text,
                    "tags": [tag.strip() for tag in new_task_tags.split(",")] if new_task_tags else [],
                    "starred": False,
                    "completed": False,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "important": important
                }
                if not tasks:
                    tasks = []  # Initialize tasks list if it was None
                tasks.append(new_task)
                save_tasks()  # Save after change
        elif key == ord('d'):  # Delete task
            if tasks:
                del tasks[selected_task]
                if selected_task >= len(tasks):
                    selected_task = max(0, len(tasks) - 1)
                save_tasks()  # Save after change
        elif key == ord('t'):  # Add/Edit tags
            if tasks:
                stdscr.addstr(len(tasks) + 6, 0, "Enter new tags (comma-separated): ")
                curses.echo()
                new_tags = stdscr.getstr(len(tasks) + 6, 37).decode('utf-8')
                curses.noecho()
                if new_tags:
                    tasks[selected_task]["tags"] = [tag.strip() for tag in new_tags.split(",")]
                    save_tasks()  # Save after change
        elif key == ord('q'):  # Quit
            break

def main():
    global tasks
    tasks = load_tasks()  # Load tasks from file
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()