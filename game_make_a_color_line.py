"""
Game creation. The goal is to put the moveable blocks in the appropriate columns.
The object is selected first, then its direction.
If the move is not possible or no object is selected to move, errors pop up.
The rules of the game appear at startup.
After completing the game, a pop-up window displays the time and the number of moves spent.
"""


from datetime import datetime
from tkinter import *


def start():
    def start_game():
        global start_time
        a.destroy()
        start_time = datetime.now()

    a = Toplevel(root)
    a.geometry('+300+400')
    Label(a, text="You need to put the colors in one row. The color for the row is shown at the top.",
          font='bolt').pack(expand=1)
    Label(a, text="First click on the object you want to move.", font='bolt').pack(expand=1)
    Label(a, text="Then choose the direction where you want to move the selected object.",
          font='bolt').pack(expand=1)
    Button(a, text="Start", command=start_game).pack(expand=1)
    a.transient(root)
    a.grab_set()


def reset_selected_object():
    global choose_direction_flag, choose_object_flag
    label_object.configure(fg='black')
    label_direction.configure(fg='white')
    content.grid_slaves(selected_object_row, selected_object_column)[0].config(relief=RAISED)
    choose_object_flag = True
    choose_direction_flag = False


def congratulations():
    def destroy_top_widow():
        a.destroy()
        root.destroy()

    global start_time
    a = Toplevel()
    a.geometry('400x150+400+400')
    Label(a, text="Congratulations! You completed the game!", font='bolt').pack(expand=1)
    Label(a, text=f"Steps taken: {score}", font='bolt').pack(expand=1)
    Label(a, text=f"Elapsed time: {datetime.now()-start_time}", font='bolt').pack(expand=1)
    Button(a, text="OK", command=destroy_top_widow).pack(expand=1)


def check_end_of_game():
    global score
    label_object.configure(fg='black')
    label_direction.configure(fg='white')
    score += 1
    if (red_button_1.grid_info()['column'] == red_button_2.grid_info()['column'] ==
        red_button_3.grid_info()['column'] == red_button_4.grid_info()['column'] ==
        red_button_5.grid_info()['column'] == red_label_0.grid_info()['column']) and (
            yellow_button_1.grid_info()['column'] == yellow_button_2.grid_info()['column'] ==
            yellow_button_3.grid_info()['column'] == yellow_button_4.grid_info()['column'] ==
            yellow_button_5.grid_info()['column'] == yellow_label_0.grid_info()['column']) and (
            green_button_1.grid_info()['column'] == green_button_2.grid_info()['column'] ==
            green_button_3.grid_info()['column'] == green_button_4.grid_info()['column'] ==
            green_button_5.grid_info()['column'] == green_label_0.grid_info()['column']):
        congratulations()


def no_object_selected():
    def destroy_top_widow():
        a.destroy()

    a = Toplevel()
    a.geometry('400x150+400+400')
    Label(a, text="Firstly select the object to move", font='bolt').pack(expand=1)
    Button(a, text="OK", command=destroy_top_widow).pack(expand=1)


def wrong_direction_chosen():
    def destroy_top_widow():
        a.destroy()

    label_object.configure(fg='black')
    label_direction.configure(fg='white')
    content.grid_slaves(selected_object_row, selected_object_column)[0].config(relief=RAISED)
    a = Toplevel()
    a.geometry('400x150+400+400')
    Label(a, text="Invalid direction selected", font='bolt').pack(expand=1)
    Button(a, text="OK", command=destroy_top_widow).pack(expand=1)


def try_left():
    global choose_direction_flag, selected_object_row, selected_object_column, choose_object_flag
    if choose_direction_flag:
        choose_direction_flag = False
        if selected_object_column - 1 >= 0 and \
                step_accessibility_array[selected_object_row][selected_object_column - 1]:
            step_accessibility_array[selected_object_row][selected_object_column - 1] = False
            step_accessibility_array[selected_object_row][selected_object_column] = True
            content.grid_slaves(selected_object_row, selected_object_column)[0]. \
                grid_configure(row=selected_object_row, column=selected_object_column - 1)
            choose_object_flag = True
            content.grid_slaves(selected_object_row, selected_object_column - 1)[0].config(relief=RAISED)
            check_end_of_game()

        else:
            wrong_direction_chosen()
            choose_object_flag = True

    else:
        no_object_selected()


def try_up():
    global choose_direction_flag, selected_object_row, selected_object_column, choose_object_flag
    if choose_direction_flag:
        choose_direction_flag = False
        if selected_object_row - 1 >= 0 and \
                step_accessibility_array[selected_object_row - 1][selected_object_column]:
            step_accessibility_array[selected_object_row - 1][selected_object_column] = False
            step_accessibility_array[selected_object_row][selected_object_column] = True
            content.grid_slaves(selected_object_row, selected_object_column)[0]. \
                grid_configure(row=selected_object_row - 1, column=selected_object_column)
            choose_object_flag = True
            content.grid_slaves(selected_object_row - 1, selected_object_column)[0].config(relief=RAISED)
            check_end_of_game()

        else:
            wrong_direction_chosen()
            choose_object_flag = True

    else:
        no_object_selected()


def try_down():
    global choose_direction_flag, selected_object_row, selected_object_column, choose_object_flag
    if choose_direction_flag:
        choose_direction_flag = False
        if selected_object_row + 1 <= 6 and \
                step_accessibility_array[selected_object_row + 1][selected_object_column]:
            step_accessibility_array[selected_object_row + 1][selected_object_column] = False
            step_accessibility_array[selected_object_row][selected_object_column] = True
            content.grid_slaves(selected_object_row, selected_object_column)[0]. \
                grid_configure(row=selected_object_row + 1, column=selected_object_column)
            choose_object_flag = True
            content.grid_slaves(selected_object_row + 1, selected_object_column)[0].config(relief=RAISED)
            check_end_of_game()

        else:
            wrong_direction_chosen()
            choose_object_flag = True

    else:
        no_object_selected()


def try_right():
    global choose_direction_flag, selected_object_row, selected_object_column, choose_object_flag
    if choose_direction_flag:
        choose_direction_flag = False
        if selected_object_column + 1 <= 4 and \
                step_accessibility_array[selected_object_row][selected_object_column + 1]:
            step_accessibility_array[selected_object_row][selected_object_column + 1] = False
            step_accessibility_array[selected_object_row][selected_object_column] = True
            content.grid_slaves(selected_object_row, selected_object_column)[0]. \
                grid_configure(row=selected_object_row, column=selected_object_column + 1)
            choose_object_flag = True
            content.grid_slaves(selected_object_row, selected_object_column + 1)[0].config(relief=RAISED)
            check_end_of_game()

        else:
            wrong_direction_chosen()
            choose_object_flag = True

    else:
        no_object_selected()


def object_selected(code_of_object):
    global choose_object_flag, selected_object_row, selected_object_column, choose_direction_flag
    if choose_object_flag:
        label_object.configure(fg='white')
        label_direction.configure(fg='black')
        selected_object = dict_code_buttons[code_of_object]
        selected_object_row = selected_object.grid_info()['row']
        selected_object_column = selected_object.grid_info()['column']
        content.grid_slaves(selected_object_row, selected_object_column)[0].config(relief=SUNKEN)
        choose_object_flag = False
        choose_direction_flag = True


selected_object_row = None
selected_object_column = None
choose_object_flag = True
choose_direction_flag = False
step_accessibility_array = [[False for j in range(5)] for i in range(7)]
step_accessibility_array[3][1] = True
step_accessibility_array[3][3] = True
step_accessibility_array[5][1] = True
step_accessibility_array[5][3] = True
score = 0
start_time = 0

root = Tk()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.title('Line up the colors')
root.geometry(f"+{int(w / 4)}+{int(h / 4)}")
root.resizable(False, False)
content = Frame(root, width=630, height=490, bg='white')
frame = Frame(content, borderwidth=5, relief="ridge", width=350, height=490, bg='white')

label_direction = Label(content, text="Choose direction", fg='white', bg='white', font='bolt')
label_object = Label(content, text="Choose object", fg='black', bg='white', font='bolt')
label_1 = Label(content, text="Choose direction", fg='red')
left_button = Button(content, text="🢀", command=try_left)
right_button = Button(content, text="🢂", command=try_right)
up_button = Button(content, text="🢁", command=try_up)
down_button = Button(content, text="🢃", command=try_down)
reset_object_button = Button(content, text="Reset object", command=reset_selected_object)

block_label_1 = Label(content, bg='black', fg='white', relief=RAISED, width=3)
block_label_2 = Label(content, bg='black', fg='white', relief=RAISED, width=3)
block_label_3 = Label(content, bg='black', fg='white', relief=RAISED, width=3)
block_label_4 = Label(content, bg='black', fg='white', relief=RAISED, width=3)
block_label_5 = Label(content, bg='black', fg='white', relief=RAISED, width=3)
block_label_6 = Label(content, bg='black', fg='white', relief=RAISED, width=3)
red_label_0 = Label(content, bg='red', fg='white', width=2)
red_button_1 = Button(content, bg='red', fg='white', width=2, command=lambda: object_selected('r1'))
red_button_2 = Button(content, bg='red', fg='white', width=2, command=lambda: object_selected('r2'))
red_button_3 = Button(content, bg='red', fg='white', width=2, command=lambda: object_selected('r3'))
red_button_4 = Button(content, bg='red', fg='white', width=2, command=lambda: object_selected('r4'))
red_button_5 = Button(content, bg='red', fg='white', width=2, command=lambda: object_selected('r5'))
yellow_label_0 = Label(content, bg='yellow', fg='white', width=2)
yellow_button_1 = Button(content, bg='yellow', fg='white', width=2, command=lambda: object_selected('y1'))
yellow_button_2 = Button(content, bg='yellow', fg='white', width=2, command=lambda: object_selected('y2'))
yellow_button_3 = Button(content, bg='yellow', fg='white', width=2, command=lambda: object_selected('y3'))
yellow_button_4 = Button(content, bg='yellow', fg='white', width=2, command=lambda: object_selected('y4'))
yellow_button_5 = Button(content, bg='yellow', fg='white', width=2, command=lambda: object_selected('y5'))
green_label_0 = Label(content, bg='mediumturquoise', fg='white', width=2)
green_button_1 = Button(content, bg='mediumturquoise', fg='white', width=2, command=lambda: object_selected('g1'))
green_button_2 = Button(content, bg='mediumturquoise', fg='white', width=2, command=lambda: object_selected('g2'))
green_button_3 = Button(content, bg='mediumturquoise', fg='white', width=2, command=lambda: object_selected('g3'))
green_button_4 = Button(content, bg='mediumturquoise', fg='white', width=2, command=lambda: object_selected('g4'))
green_button_5 = Button(content, bg='mediumturquoise', fg='white', width=2, command=lambda: object_selected('g5'))

dict_code_buttons = {
    'r1': red_button_1, 'r2': red_button_2, 'r3': red_button_3, 'r4': red_button_4, 'r5': red_button_5,
    'y1': yellow_button_1, 'y2': yellow_button_2, 'y3': yellow_button_3, 'y4': yellow_button_4, 'y5': yellow_button_5,
    'g1': green_button_1, 'g2': green_button_2, 'g3': green_button_3, 'g4': green_button_4, 'g5': green_button_5
}

content.grid(column=0, row=0)
frame.grid(column=0, row=2, columnspan=5, rowspan=5)
label_direction.grid(column=6, row=0, columnspan=3, rowspan=2)
label_object.grid(column=0, row=1, columnspan=5)
left_button.grid(column=6, row=3)
right_button.grid(column=8, row=3)
up_button.grid(column=7, row=2)
down_button.grid(column=7, row=4)
reset_object_button.grid(column=7, row=5)
block_label_1.grid(column=1, row=2)
block_label_2.grid(column=1, row=4)
block_label_3.grid(column=1, row=6)
block_label_4.grid(column=3, row=2)
block_label_5.grid(column=3, row=4)
block_label_6.grid(column=3, row=6)
red_label_0.grid(column=4, row=0)
red_button_1.grid(column=0, row=3)
red_button_2.grid(column=2, row=4)
red_button_3.grid(column=4, row=4)
red_button_4.grid(column=0, row=6)
red_button_5.grid(column=2, row=6)
yellow_label_0.grid(column=0, row=0)
yellow_button_1.grid(column=2, row=2)
yellow_button_2.grid(column=2, row=3)
yellow_button_3.grid(column=0, row=4)
yellow_button_4.grid(column=4, row=5)
yellow_button_5.grid(column=4, row=6)
green_label_0.grid(column=2, row=0)
green_button_1.grid(column=0, row=2)
green_button_2.grid(column=4, row=2)
green_button_3.grid(column=4, row=3)
green_button_4.grid(column=0, row=5)
green_button_5.grid(column=2, row=5)
start()
root.mainloop()
