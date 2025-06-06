import aiohttp
from datetime import datetime

class hhParse():
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.stack = [
            "django", "drf", "fastapi", "postgresql", "sqlite", "redis", "git",
            "ci/cd", "django orm", "kafka", "rabbitmq", "celery", "docker",
            "юнит тесты", "unit", "тесты"
        ]
        self.query = " OR ".join(self.stack)
        self.params = {
            "text": "Python AND (middle OR middle/senior OR middle+/senior OR senior) AND (NOT Lead OR NOT Лид) AND ("+self.query+")",
            "salary": "150000",
            "currancy": "RUR",
        }
        self.headers = {
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    async def get_data(self):
          async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params, headers=self.headers) as resp:
                return await resp.json()
            
    async def the_latest(self):
        data = await self.get_data()
        vacancies = data.get("items", [])
        msg = []
        count = 0
        for vacancy in vacancies:
            salary = vacancy.get('salary')
            if salary:
                salary_from = salary.get('from')
                salary_to = salary.get('to')

                name = vacancy.get('name')
                company = vacancy.get('employer', {}).get('name')
                link = vacancy.get('alternate_url')
                
                raw_time = vacancy.get('published_at')  

                if raw_time and raw_time.endswith('+030'):
                    raw_time = raw_time.replace('+030', '+03:00')

                date = datetime.fromisoformat(raw_time)
                only_date = date.date() 
                if salary_from and salary_to:
                    salary_str = f"от {salary_from} до {salary_to}"
                elif salary_from:
                    salary_str = f"от {salary_from}"
                elif salary_to:
                    salary_str = f"до {salary_to}"
                else:
                    salary_str = "не указана"
        
                msg.append(
                                f"📌 <b>{name}</b>\n"
                                f"💰 Зарплата: <b>{salary_str}</b>\n"
                                f"👾 Работодатель: {company}\n"
                                f"🔗 {link}\n"
                                f"<i>Опубликована {only_date}</i>"
                            )     
                count+=1
                if count > 1:
                    break

        return "\n\n".join(msg)

