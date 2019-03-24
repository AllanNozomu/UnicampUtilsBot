from tempfile import NamedTemporaryFile
from src.discipline import Discipline

import json
import os
import subprocess
import io
import re

LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', os.path.dirname(os.path.abspath(__file__)))
BIN_DIR = os.path.join(LAMBDA_TASK_ROOT, 'bin')
LIB_DIR = os.path.join(LAMBDA_TASK_ROOT, 'libparser')

def convert_number(hour):
    return int(hour[:hour.find(':')])

def merge_lines(lines):
    new_lines = []
    for i in range(len(lines)):
        if (i % 3 == 0):
            str_list = []
            for j in range(max(len(lines[i]), len(lines[i+1]))):
                if j >= len(lines[i]):
                    str_list.append(lines[i + 1][j])
                elif j >= len(lines[i+1]):
                    str_list.append(lines[i][j])
                else:
                    str_list.append(lines[i][j] if lines[i][j] != ' ' else lines[i+1][j])
            new_lines.append(''.join(str_list))
        elif (i % 3 == 2):
            new_lines.append(lines[i])
    return [l.strip() for l in new_lines]

def pdf_handler():
    with NamedTemporaryFile(suffix='.txt', delete=False) as f:
        text_path = f.name
    
    try:
        if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE']:
            output = subprocess.check_output([os.path.join(BIN_DIR, 'pdftotext'), '-layout', '/tmp/test.pdf', text_path], shell=False, env=dict(LD_LIBRARY_PATH=os.path.join(LIB_DIR, 'pdftotext')))
        else:
            output = subprocess.check_output(['pdftotext', '-layout', '/tmp/test.pdf', text_path], shell=False, env=dict(LD_LIBRARY_PATH=os.path.join(LIB_DIR, 'pdftotext')))
    except:
        os.remove(text_path)
        raise Exception("Arquivo passado nao eh um pdf")

    with io.open(text_path, mode='r', encoding='utf-8', errors='ignore') as f:
        text = f.read().strip()
    
    try:
        lines = [l for l in text.split('\n') if l.strip() != '']
        
        ini = 0
        remove_lines = list(range(len(lines)))[::-1]
        program = re.compile("\d+:\d+H")
        
        for i in range(len(lines)):
            if program.match(lines[i].strip().split(' ')[0]):
                remove_lines.remove(i)
                remove_lines.remove(i+1)
                remove_lines.remove(i+2)
        
        for i in remove_lines:
            del lines[i]
        lines = merge_lines(lines)
        
        table = [[c.strip() for c in l.split('   ') if c.strip() != ''] for l in lines]
        
        disciplines = {}
        discipline_order = []

        for i in range(len(table)):
            
            if i % 2 == 0:
                for j in range(1, len(table[i])):
                    code = table[i][j]
                    if code != '-----':
                        discipline_order.append((code, j, table[i][0]))
            else:
                for j in range(1, len(table[i])):
                    room = table[i][j]
                    (code, d, h) = discipline_order[j-1]
                    if code in disciplines:
                        disciplines[code].add_day_hour(room, d, convert_number(h))
                    else:
                        disciplines[code] = Discipline(code, room, d, convert_number(h))
                discipline_order = []
                
        retorno = [ disciplines[d].to_item() for d in disciplines]
    except Exception as e:
        print(str(type(e)) + " " + str(e))
        raise Exception('Nao foi possivel coneverter o arquivo')

    if not retorno:
        raise Exception('Arquivo nao possui nenhuma aula registrada')
    return retorno
