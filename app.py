from flask import Flask, render_template, request
from DBcm import UseDatabase
from vsearch import search_vowels

app = Flask(__name__)



app.config['dbconfig'] = {'host': 'localhost',
                        'user': 'root',
                        'password': 'svetlana19',
                        'database': 'vsearchlogdb',}



def log_request(req:'flask_rquest', res: str) -> None:
    """Журналирует веб-запрос и возвращает результат"""

    with UseDatabase(app.config['dbconfig']) as cursor:

        _SQL = """insert into log
                    (phrase, letters, ip, browsers_string, results)
                    values
                    (%s, %s, %s, %s, %s)"""

        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res,))





@app.route('/search_vowels', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Ваш результат'
    results = str(search_vowels(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Добро пожаловать на мою страницу поиска букв в фразе')

@app.route('/viewlog')
def view_the_log() -> 'html':

   with UseDatabase(app.config['dbconfig']) as cursor:
    _SQL = """select phrase, letters, ip, browsers_string, return, from log"""
    cursor.execute(_SQL)
    contents = cursor.fetchall()
    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template ('viewlog.html',
                            the_title='View Log',
                            the_row_titles=titles,
                            the_data=contents,)


if __name__ == '__main__':
    app.run(debug=True)
