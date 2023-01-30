from fastapi import FastAPI, Depends, Request, Form
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database.base import get_db
from .models import Publication
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER


app = FastAPI()

# подключаем статик файлы и шаблонизатор джинджа
app.mount('/static', StaticFiles(directory='my_site/static'), name='static')
templates = Jinja2Templates(directory='my_site/templates')

# и дальше идет логика сайта (всё почти как в Джанго)

# чтение данных из бд
# db_session.query(Question).filter(Question.id == 1).first()
# db_session.query(Question).filter(Question.title == 'Название').all()
# db_session.query(Question).filter(Question.topic_id == 2).order_by(Question.id.desc()).limit(10).all()
# и всё в таком духе

@app.get('/')
async def home(request: Request, db_session: Session = Depends(get_db)):
    publications = db_session.query(Publication).all()
    return templates.TemplateResponse('my_site/index.html', {'request':request, 'publications':publications})


# добавить запись в бд при помощи формочки из index.html
# title и content - инпуты в формочке html
@app.post('/add')
async def add_post(request: Request, title: str = Form(...), content: str = Form(...), db_session: Session = Depends(get_db)):
    new_publication = Publication(title=title, content=content)
    db_session.add(new_publication)
    db_session.commit()

    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


# удаление из бд
@app.get('/delete/{id}')
async def delete(request: Request, id: int, db_session: Session = Depends(get_db)):
    publication = db_session.query(Publication).filter_by(id=id).first()
    db_session.delete(publication)
    db_session.commit()

    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


# изменение (это метод гет, т.е. чтобы просто получить html)
@app.get('/change/{id}')
async def change(request: Request, id: int, db_session: Session = Depends(get_db)):
    publication = db_session.query(Publication).filter_by(id=id).first()
    return templates.TemplateResponse('my_site/change.html', {'request':request, 'publication':publication})


# изменение (метод пост, т.е. пользователь отправил формочку)
@app.post('/change/{id}')
async def change_post(request: Request, id: int, title: str = Form(...), content: str = Form(...), db_session: Session = Depends(get_db)):
    publication = db_session.query(Publication).filter_by(id=id).first()
    publication.title = title
    publication.content = content
    db_session.commit()

    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)

    


