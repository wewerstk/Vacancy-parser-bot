from bs4 import BeautifulSoup
import aiohttp

class HabrParser():
    def __init__(self):
        self.url = "https://career.habr.com/vacancies"
        self.qid = [4, 5]
        self.stack = {
            "django": 1075,
            "fastapi": 1349, 
            "postgresql": 537,
            "sqlite": 1019,
            "redis": 1, 
            "git": 947,
            "ci/cd": 1173,
            "django orm": 1737,
            "kafka": 1187,
            "rabbitmq": 184, 
            "celery": 488,
            "docker": 1067,
        }
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        self.stack_keywords = list(self.stack.keys())

    async def get_vacancies(self, query="python", salary="150000"):
        msg = []
        for q in self.qid:
            params = {
                "q": query,
                "salary": salary,
                "type": "all",
                "qid": q
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers, params=params) as response:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        for card in soup.select("div.vacancy-card"):
                            title = card.select_one("div.vacancy-card__title").text.strip()
                            link = "https://career.habr.com" + card.select_one("a.vacancy-card__title-link")["href"]
                            company = card.select_one("div.vacancy-card__company-title").text.strip()
                            description = card.select_one("div.vacancy-card__skills").text.strip().lower()
                            salary = card.select_one("div.basic-salary").text
                            date = card.select_one("time.basic-date").text
                            if any(skill in description for skill in self.stack_keywords):
                                msg.append(
                                    f"📌 <b>{title }</b>\n"
                                    f"💰 Зарплата: <b>{salary}</b>\n"
                                    f"👾 Работодатель: {company}\n"
                                    f"🔗 {link}\n"
                                    f"<i>Опубликована {date}</i>"
                                )   
                                break  
                            
        return "\n\n".join(msg)
            
