import psycopg2

class DBManager:
    """Класс подключения к БД PostgreSQL"""

    def __init__(self, params):
        """Инициализатор класса"""
        self.conn = psycopg2.connect(dbname='hh', **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получение списка всех компаний и количества вакансий у каждой компании
        """
        self.cur.execute("""
        SELECT employers.employer_name, COUNT(vacancy.employer_id)
        FROM employers
        JOIN vacancy USING (employer_id)
        GROUP BY employers.employer_name
        ORDER BY COUNT DESC
        """)

        return self.cur.fetchall()

    def get_all_vacancies(self):
        """
        Получение списка всех вакансий с указанием названий компании,
        вакансии и зарплаты, а также ссылки на вакансию
        """
        self.cur.execute("""
        SELECT employers.employer_name, vacancy_name, salary, vacancy_url
        FROM vacancy
        JOIN employers USING (employer_id)
        ORDER BY salary desc""")
        return self.cur.fetchall()

    def get_avg_salary(self):
        """
        Получение средней зарплаты по вакансиям
        """
        self.cur.execute("""
        SELECT avg(salary) from vacancy""")
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """
        Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        self.cur.execute("""
        SELECT vacancy_name, salary
        FROM vacancy
        GROUP BY vacancy_name, salary
        ORDER BY salary DESC
        """)
        return self.cur.fetchall()


    def get_vacancies_with_keyword(self, keyword):
        """
        Получение списка всех вакансий, в названии которых содержатся переданные в метод слова
        """
        request_sql = """
        SELECT * FROM vacancy
        WHERE LOWER (vacancy_name) LIKE %s
        """
        self.cur.execute(request_sql, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()
