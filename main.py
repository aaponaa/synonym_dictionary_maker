import dearpygui.dearpygui as dpg
import pandas as pd

from functions import dico_sdist, unique_list, to_my_csv

all_data = pd.read_csv("total_data.csv", encoding="UTF-8")

fen_hi = 630
fen_wi = 800 


# My Variables 
class Dv:
    ch_col = all_data.columns.values.tolist()
    lexicon = []
    list_col = unique_list("objet", all_data)  # dpg.get_value(select_col)
    my_dico = {}
    tag_dico = []
    cor_tag_dico = []
    wndo = False
    iwd = False
    input_tol = 5
    word_sel = ""
    select_remove = ""
    lexicon_removal = []


def remove_data():
    print("yoyoyoy")


def to_csv():
    to_my_csv(Dv.my_dico)


def affect_data():
    Dv.input_tol = dpg.get_value("slider_tol")
    Dv.word_sel = dpg.get_value("select_word")

def submit_data():
    print(Dv.list_col)
    print(Dv.input_tol)
    print(dico_sdist(Dv.list_col, Dv.input_tol, Dv.word_sel))
    return dico_sdist(Dv.list_col, Dv.input_tol, Dv.word_sel)


# Selector windows
def make_but():
    result_button = submit_data()
    for x in result_button:
        dpg.add_checkbox(label=x, callback=stack_dic)

def fen_but():
    if Dv.wndo:
        dpg.delete_item("windhos")
    Dv.wndo = True
    Dv.lexicon = []
    with dpg.window(label="Select_Yours_Synonyms:",
                    tag="windhos",
                    width=fen_wi/2,
                    height=fen_hi/2,
                    pos=[0, 100],
                    no_resize=True,
                    no_move=True,
                    no_collapse=True,
                    no_background=True,
                    no_close=True
                    ):
        make_but()

def stack_dic(sender):
    if dpg.get_value(sender):
        Dv.lexicon.append(dpg.get_item_label(sender))
        print(Dv.lexicon)
    elif not dpg.get_value(sender):
        Dv.lexicon.remove(dpg.get_item_label(sender))
        print(Dv.lexicon)


#Dico windows 
def fen_dico():
    if Dv.iwd:
        dpg.delete_item("fen_dico")
    Dv.iwd = True
    with dpg.window(label="Here is your Dico:",
                    tag="fen_dico",
                    width=fen_wi/2,
                    height=fen_hi/2,
                    pos=[400, 100],
                    no_resize=True,
                    no_move=True,
                    no_collapse=True,
                    no_close=True,
                    no_background=True,
                    ):
        Dv.tag_dico = list(Dv.my_dico.keys())
        dpg.add_listbox(tag="list_dico", items=Dv.tag_dico, width=370, callback=make_dico_but)
        make_dico_but()

def make_dico_but():
    Dv.select_remove = dpg.get_value("list_dico")
    result_button = Dv.my_dico[Dv.select_remove]
    with dpg.window(tag="res_dico"):
        for x in result_button:
            dpg.add_checkbox(label=x, callback=stack_remove)

def to_my_dico():
    if Dv.my_dico == {}:
        Dv.my_dico = {dpg.get_value(select_word): Dv.lexicon}
    else:
        Dv.my_dico[dpg.get_value(select_word)] = Dv.lexicon

    for i in Dv.lexicon:
        Dv.list_col.remove(i)
    Dv.lexicon = []
    dpg.delete_item("Word_Selection")
    fen_word()
    fen_dico()
    affect_data()
    fen_but()

def stack_remove(sender):
    if dpg.get_value(sender):
        Dv.lexicon_removal.append(dpg.get_item_label(sender))
        print(Dv.lexicon_removal)
    elif not dpg.get_value(sender):
        Dv.lexicon_removal.remove(dpg.get_item_label(sender))
        print(Dv.lexicon_removal)

def fen_word():
    with dpg.window(pos=[34, 455],
                    width=360,
                    height=90,
                    min_size=[30, 20],
                    tag="Word_Selection",
                    no_close=True,
                    no_resize=True,
                    no_move=True,
                    no_collapse=True,
                    no_background=True,
                    ):
        dpg.add_combo(
            items=Dv.list_col,
            label="Word",
            tag="select_word",
            default_value=Dv.list_col[7],
            callback=affect_data,
            width=300
        )
        dpg.add_button(
            label="Search",
            callback=fen_but
        )

# Create the Gui interface
dpg.create_context()
dpg.set_global_font_scale(1.25)

with dpg.window(label="MainWindows",
                width=fen_wi,
                height=fen_hi,
                tag="MainWindows",
                no_close=True,
                no_resize=True,
                no_move=True,
                no_collapse=True,
                no_bring_to_front_on_focus=True
                ):
    select_col = dpg.add_combo(
        user_data=True,
        width=150,
        label="Column",
        default_value=Dv.ch_col[4],
        items=Dv.ch_col,
        callback=submit_data
    )
    Dv.list_col = unique_list(dpg.get_value(select_col), all_data)
    text1 = dpg.add_text("Syn Nonym's Project:", pos=[400, 60])

    with dpg.group(label="menu", pos=[400, 483]):
        dpg.add_slider_int(
            user_data=True,
            tag="slider_tol",
            label="Tolerance",
            width=300,
            default_value=5,
            max_value=10,
            callback=affect_data
        )
        but_submit = dpg.add_button(
            label="To the dictionary",
            callback=to_my_dico,
        )
        but_csv = dpg.add_button(
            label="Go to csv",
            callback=to_csv
        )
        with dpg.window(pos=[34, 455],
                        width=360,
                        height=90,
                        min_size=[30, 20],
                        tag="Word_Selection",
                        no_close=True,
                        no_resize=True,
                        no_move=True,
                        no_collapse=True,
                        no_background=True,
                        ):
            select_word = dpg.add_combo(
                items=Dv.list_col,
                label="Word",
                tag="select_word",
                default_value=Dv.list_col[7],
                callback=affect_data,
                width=300
            )
            but_search = dpg.add_button(
                label="Search",
                callback=fen_but
            )
affect_data()

# Where the program turn
dpg.create_viewport(title='Custom Title', width=fen_wi, height=fen_hi, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.start_dearpygui()

dpg.destroy_context()
