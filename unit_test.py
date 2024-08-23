# 단위테스트
# 함수의 이름 앞에 test가 붙어야된다
# 함수의 동작을 테스트 
    # 내부 내용은 관심없음
    # 함수의 동작 입력과 출력만 정상작동되는지 확인
from funtion import list_reset,page,pageation

def sum(a=int,b=int)-> int:
    return a+b
sum('3','4')


def test_sum():
    assert sum(3,4)==7
    assert sum(3,5)==8

def test_list_reset():
   boards,bno=list_reset(17)
#    assert len(boards)==17
#    assert bno==18

def test_page():
    boards,bno=list_reset(123)
    r1=page(boards=boards,pageno=1)
    r2=page(boards=boards,pageno=6)
    r3=page(boards=boards,pageno=13)
    # assert r1[0].get('bno')==123
    # assert r2[0].get('bno')==73
    # assert r3[0].get('bno')==3
    # assert len(r3)==3

def test_pageation():
    boards,bno= list_reset(123)
    (back,start,end,next)=pageation(boards=boards,pageno=1)
    assert(back,start,end,next) ==(0,1,5,6)
    (back,start,end,next)=pageation(boards=boards,pageno=6)
    assert(back,start,end,next) ==(5,6,10,11)
    (back,start,end,next)=pageation(boards=boards,pageno=11)
    assert(back,start,end,next) ==(10,11,13,0)

