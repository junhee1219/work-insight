import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from openpyxl import load_workbook
import os

def get_filename_from_path(filepath):
    basename = os.path.basename(filepath)  
    return os.path.splitext(basename)[0]

def get_sequences(list_of_ints):
    sequence_count = 1
    sequences = []
    for row in list_of_ints:
        next_item = None
        if list_of_ints.index(row) < (len(list_of_ints) - 1):
            next_item = list_of_ints[list_of_ints.index(row) + 1]
        if (row + 1) == next_item:
            sequence_count += 1
        else:
            first_in_sequence = list_of_ints[list_of_ints.index(row) - sequence_count + 1]
            sequences.append([first_in_sequence, sequence_count])
            sequence_count = 1
    return sequences

def get_delete_row(sheet, target_column, filtered_data, max_row, start_row):
# 삭제할 행 번호를 저장할 리스트
    rows_to_delete = []
    # 2행부터 마지막 행까지 반복하면서 B열의 값을 확인
    for row in range(start_row, max_row + 1):
        if sheet[f'{target_column}{row}'].value != filtered_data:
            rows_to_delete.append(row)
    return get_sequences(rows_to_delete)

def split_main(filename, target_column_list, start_row_list):
    workbook = load_workbook(filename, data_only=True)
    sheetlist = workbook.sheetnames
    split_data = set()
    for i in sheetlist:
        sheet = workbook[i]
        max_row = sheet.max_row
        target_column = target_column_list.get(i, "None")
        if target_column == "None":
            continue
        for row in range(start_row_list[i], max_row + 1):
            split_data.add(sheet[f'{target_column}{row}'].value)  
        
    # split_data로부터 각 파일 생성 , 분리
    for i in split_data:
        filepath = os.path.dirname(filename) + f"/{get_filename_from_path(filename)}_{i}.xlsx"
        workbook.save(filepath)
        this_workbook = load_workbook(filepath, data_only=True)

        for j in sheetlist:
            this_sheet = this_workbook[j]
            target_column = target_column_list.get(j, "None")
            max_row = this_sheet.max_row
            start_row = start_row_list[j]
            if target_column == "None":
                continue
            for sequence in reversed(get_delete_row(this_sheet, target_column, i, max_row, start_row)):
                this_sheet.delete_rows(sequence[0],sequence[1])
        this_workbook.save(filepath)

# 엑셀 파일 로드

sheet_column_list = {}
combos = {}
def print_selection():
    global combos, sheet_column_list, file_path, entries
    target_column_list = {}
    start_row_list = {}
    for sheet_name, combo in combos.items():
        index = combo.current()  # 현재 선택된 인덱스
        if index >= 0:  # 선택된 항목이 있는 경우
            column_key = list(sheet_column_list[sheet_name].keys())[index]
            target_column_list[sheet_name] = column_key
    for sheet_name, entry in entries.items():
        startnum = entry.get()
        if startnum == '' or startnum is None:
            startnum = 0
        start_row_list[sheet_name] = int(startnum)
    split_main (file_path, target_column_list, start_row_list)
        
def only_numbers(char):
    return char.isdigit()
    
def open_file():
    global  combos, sheet_column_list,file_path, entries
    for widget in content_frame.winfo_children():  # content_frame 내의 모든 위젯을 순회
        widget.destroy()  # 각 위젯을 제거

    file_label.config(text="파일을 불러오는 중입니다...")
    sheet_column_list = {}
    file_path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("xlsx files", "*.xlsx")])
    if file_path:
        file_label.config(text=file_path)
        wb = load_workbook(file_path, data_only=True)
        for i in wb.sheetnames:
            sheet = wb[i]
            column_values = {"None" : "해당시트분리안함"}
            for column in sheet.iter_cols(min_row=1, max_row=1):
                column_letter = column[0].column_letter
                column_values[column_letter] = column_letter
            sheet_column_list[i] = column_values
        combos = {}  
        entries = {}
        tk.Label(content_frame, text= "시트명").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(content_frame, text= "기준컬럼").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(content_frame, text= "시작행").grid(row=0, column=2, padx=10, pady=5)
        
        for i, (sheet_name, headers) in enumerate(sheet_column_list.items()):
            tk.Label(content_frame, text= sheet_name).grid(row=i+1, column=0, padx=10, pady=5)
            combo = ttk.Combobox(content_frame, values=list(headers.values()), state='readonly')
            combo.grid(row=i+1, column=1, padx=10, pady=5)
            combos[sheet_name] = combo
            vcmd = (root.register(only_numbers), '%S')
            entry = ttk.Entry(content_frame, validate='key', validatecommand=vcmd)
            entry.grid(row=i+1, column=2, padx=10, pady=5)
            entries[sheet_name] = entry

        print_btn = tk.Button(content_frame, text="엑셀파일 쪼개기 실행", command=print_selection)
        print_btn.grid(row=len(wb.sheetnames)+1, column=0, columnspan=2, pady=10)
    else:
        file_label.config(text="선택된 파일이 없습니다.")
            
root = tk.Tk()
root.title("엑셀파일분리")
file_label = tk.Label(root, text="선택된 파일이 없습니다.")  # 파일 경로를 표시할 라벨
file_label.pack(padx=10, pady=5)

open_file_button = tk.Button(root, text="Open File", command=open_file)
open_file_button.pack(pady=10)

remark = tk.Label(root, text="개선/문의 : leejunhee1219@kakao.com")  # 파일 경로를 표시할 라벨
remark.pack(padx=10, pady=5)

content_frame = tk.Frame(root)  # 동적 요소들을 위한 프레임
content_frame.pack(fill='both', expand=True)
root.mainloop()

