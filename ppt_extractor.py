from pptx import Presentation
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

대소문자구분 = True

def ppt추출함수(input_filename, search_text, keep_slides):
    prs = Presentation(input_filename)
    save_slide_ids = set()
    del_slides = set()
    for slide_number in keep_slides:
        try:
            save_slide_ids.add(prs.slides[slide_number - 1].slide_id)
        except IndexError:
            messagebox.showinfo("오류", f"{slide_number}번 슬라이드는 존재하지 않습니다.")
            return
    if 대소문자구분 :
        for slide in prs.slides:
            breaker = False
            for shape in slide.shapes:
                if shape.has_text_frame:

                    if shape.text and search_text in shape.text:
                        save_slide_ids.add(slide.slide_id)
                        breaker = True
                        break

                if shape.has_table:
                    for row in shape.table.rows:
                        if breaker:
                            break
                        for cell in row.cells:

                            if search_text in cell.text:

                                save_slide_ids.add(slide.slide_id)
                                breaker = True
                                break
    else:
        for slide in prs.slides:
            breaker = False
            for shape in slide.shapes:
                if shape.has_text_frame:
                    if shape.text and search_text.upper() in shape.text.upper():
                        save_slide_ids.add(slide.slide_id)
                        breaker = True
                        break
                if shape.has_table:
                    for row in shape.table.rows:
                        if breaker:
                            break
                        for cell in row.cells:
                            if search_text.upper() in cell.text.upper():
                                save_slide_ids.add(slide.slide_id)
                                breaker = True
                                break
    for slide in prs.slides._sldIdLst:
        if not (int(slide.get("id")) in save_slide_ids):
            del_slides.add(slide)
    for i in del_slides:
        prs.slides._sldIdLst.remove(i)
    prs.save(f"{search_text}.pptx")


def toggle(current_state):
    global 대소문자구분
    if current_state:
        대소문자구분 = False
    else:
        대소문자구분 = True

