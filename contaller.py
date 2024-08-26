from flask import request,render_template,get_flashed_messages,Flask,flash,redirect
from datetime import datetime
from funtion import list_reset,page,pageation
from constants import SECRET_KEY

app= Flask(__name__)

boards,bno=list_reset(123)

app.secret_key=SECRET_KEY

@app.route('/')
def list():
  messages = get_flashed_messages()
  if len(messages)>0:
    message = messages[0]
  else:
    message = ''
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
  return render_template("list.html",back=back,start=start,end=end,next=next, pageno=pageno, boards=result_set, message=message)

@app.route('/write',methods=['GET'])
def write_get():
  messages = get_flashed_messages()
  if len(messages)>0:
    message = messages[0]
  else:
    message = ''
  return render_template('write.html',message=message)

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
  password = request.form.get('password')

  if not title or not content or not nickname or not password:
    flash('제목, 내용 , 닉네임, 비밀번호 을 필수로 입력하세요')
    return redirect('/write')
  new_board = {'bno':bno, 'title':title , 'nickname':nickname, 'content':content, 'writetime':writetime , 'password':password}
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

@app.route('/update')
def update_get():
  messages = get_flashed_messages()
  if len(messages)>0:
    message = messages[0]
  else:
    message = ''
  try :
    bno=int(request.args.get('bno'))
  except (ValueError,TypeError):              
    flash('비정상 적인 글 입니다.')
    return redirect('/')
  
  for board in boards:
    if (board['bno']==bno):
      return render_template('update.html',board=board , message=message)
  flash('비정상 적인 글 입니다.')             
  return redirect('/')

@app.route('/update',methods=['POST'])
def update_post():
  # bno에서 받아온값이 없거나 잘못된경우 
  try :
    bno=int(request.form.get('bno'))
  except (ValueError,TypeError):              
    flash('비정상 적인 글 입니다.')
    return redirect('/')
  
  #title과 content ,비밀번호 주어진 값을 꺼낸다  /만약 값이 비었으면 update로 돌린다
  title = request.form.get('title')
  content = request.form.get('content')
  password = request.form.get('password')
  if not title or not content or not password:
     flash('글을 확인하세요')
     return redirect(f'/update?bno={bno}')
  
  #bno로 글을 찾아서 비밀번호를 비교하고  제목과 내용을 수정하세요
  for board in boards:
     if board.get('bno')==bno:
        if board.get('password')!=password:
           flash('비밀번호 확인하세요')
           return redirect(f'/update?bno={bno}')
        board['title']= title
        board['content']= content
        break
  return redirect('/')

@app.route('/delete',methods=['POST'])
def delete():
  try :
    bno=int(request.form.get('bno'))
  except (ValueError,TypeError):              
    flash('비정상 적인 글 입니다.')
    return redirect('/')
  
  # 삭제하기위해서 비밀번호만 꺼내온다/ 값이 없으면 update로 보낸다
  password = request.form.get('password')
  if not password:
     flash('비밀번호를 확인하세요.')
     return redirect(f'/update?bno={bno}')
  
  #bno로 찾아서 비밀번호가 일치하면 삭제
  # list에서 삭제하기
  for i in range(0,len(boards)):
     if boards[i].get('bno')==bno:
        if boards[i].get('password')!=password:
          flash('비밀번호가 틀렷습니다.')
          return redirect(f'/update?bno={bno}')
        del boards[i]
        break
  return redirect('/')

app.run(debug=True,port=8081)