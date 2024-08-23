from flask import request,render_template,get_flashed_messages,Flask,flash,redirect
from datetime import datetime
from funtion import list_reset,page,pageation
from constants import SECRET_KEY

app= Flask(__name__)

boards,bno=list_reset(123)

app.secret_key=SECRET_KEY

@app.route('/')
def list():
    try:                            
        pageno=int(request.args.get('pageno'))                                         
        if pageno<0 :                               #pageno<0 예외를 개발자가 발생시켜버려라 if pageno<0 raise ValueError}
            raise ValueError
    except TypeError:
        pageno=1                                    #list?로 넘어오면 pageno가 없다 (TypeError)  대처 방법 = pageno=1로 지정해둬라
    except:   
        return redirect('/')                        #list?pageno=aaa 로 넘어오면 int로 변환 못한거니(ValueError) 

    result_set=page(boards=boards,pageno=pageno)
    (back,start,end,next)= pageation(boards=boards, pageno=pageno)
    return render_template("list.html",back=back,start=start,end=end,next=next, 
    pageno=pageno, boards=result_set)

@app.route('/write',methods=['GET'])
def write_get():
    messages=get_flashed_messages()
    messages=''
    if len(messages)>0:
        messages[0]
    return render_template('write.html',messages=messages)

#flash() 로 저장한 값들을 리스트로 전달된다.
#flash() 로 전달된 값이 없는경우에는[] => 저장된 메세지를 꺼내서 html로 전달한다.

# python의 scope 함수이고 변수의 사용범위 
# 함수에 속하지않은 변수를 전역(global),함수 안에 속해있는 변수를 지역(local)
# 함수 내부에서 전역 변수를 사용하려면 global로 지정한다
# int, float,bool

@app.route('/write',methods=['POST'])
def write_POST():
    global bno
    writetime= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title=request.form.get('title')
    content= request.form.get('content')
    nickname= request.form.get('nickname')
    if not title or not content or not nickname:
        flash('제목, 내용 , 닉네임 을 필수로 입력하세요')
        return redirect('/write')
    new_board = {'bno':bno, 'title':title , 'nickname':nickname, 'content':content, 'writetime':writetime}
    bno+=1
    boards.insert(0,new_board)
    return redirect('/')

@app.route('/read')
def read():
  try :
    bno=int(request.args.get('bno'))
  except (ValueError,TypeError):              #예외상황일때
    flash('정상 적인 글이 아닙니다.')
    return redirect('/')
  
  for board in boards:
        if (board['bno']==bno):
            return render_template('read.html',board=board)
  flash('정상 적인 글이 아닙니다.')             #정상적인 상황일때
  return redirect('/')
    
# @app.route("/update")
# def update_get():
#   try :
#     bno = int(request.args.get('bno'))
#   except (TypeError, ValueError):
#     flash('글을 찾을 수 없습니다')
#     return redirect("/")  
#   for board in boards:
#     if board.get('bno')==bno:
#       return render_template("update.html", board=board)
#   flash('글을 찾을 수 없습니다')    
#   return redirect("/")  

# @app.route("/update", methods=['POST'])
# def update_post():
#   try :
#     bno = int(request.form.get('bno'))
#   except (TypeError, ValueError):
#     flash('잘못된 작업입니다')
#     return redirect("/")  
  
#   title = request.form.get('title')
#   content = request.form.get('content')

#   if not title or not content:
#     flash('제목, 내용은 필수입력입니다')
#     return redirect("/update")

#   for board in boards:
#     if board.get('bno')==bno:
#       board['title'] = title
#       board['content'] = content
#       board['writetime'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
#       break
#   return redirect("/")

# @app.route("/delete", methods=['POST'])
# def delete():
#   try :
#     bno = int(request.form.get('bno'))
#   except (TypeError, ValueError):
#     flash('잘못된 작업입니다')
#     return redirect("/")  
  
#   for index in range(0, len(boards)):
#     if boards[index].get('bno')==bno:
#       del boards[index]
#       break
#   return redirect("/")

app.run(debug=True,port=8081)