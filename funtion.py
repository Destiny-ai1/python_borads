# 리스트 초기화 함수 만들기
from datetime import datetime
from math import ceil
from constants import PAGE_SIZE,BLOCK_SIZE


def list_reset(size=int)->tuple:
    boards=[]
    datetime.now()
    for i in range ( 1, size+1):
        new_boards={'bno':i, 'title':f'{i}번글', 'content': f'{i}번글입니다', 'nickname': 'NYS', 
            'writetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,'password':'1234'}                      # ('%Y년-%m월-%d %H:%M:%S') xxxx년-00월-00일 / xx시xx분xx초
        boards.insert(0,new_boards)                                                                           #새로운 보드를 제일 앞에 추가하는 방법 (역순으로 )
    return(boards,size+1)


def page(boards=list, pageno=int)->list:                                          
    stat_index= (pageno-1)*PAGE_SIZE
    end_index=stat_index+PAGE_SIZE-1
    size=len(boards)
    if end_index>size:
        end_index=size-1
    return boards[stat_index:end_index+1]


def pageation(boards=list,pageno=int):
    text_ea=len(boards)
    page_ea= ceil(text_ea/PAGE_SIZE)
#페이지 번호가 페이지의 갯수보다 크다면 마지막 페이지로    
    if pageno>page_ea:
        pageno=page_ea

    back= (ceil(pageno/BLOCK_SIZE)-1)*BLOCK_SIZE
    start=back+1
    end=back+BLOCK_SIZE
    next= end+1

    if end>page_ea:
        end=page_ea
        next=0
    return(back,start,end,next)