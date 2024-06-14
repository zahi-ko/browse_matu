import os
import re

import bs4
import requests

def login(s: requests.Session, username: str, password: str) -> bool:
    login_url = "http://matu.uestc.edu.cn:80/aptat/user/dologin.action"
    login_data = {
        "user.Login": username,
        "user.Password": password,
    }
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    })
    r = s.post(login_url, data=login_data, allow_redirects=True)
    return r.ok

def collectLinks(s: requests.Session, resp: requests.Response, pattern: str = "") -> list:
    links = set()

    soup = bs4.BeautifulSoup(resp.text, "lxml")
    links.update([ a['href'] for a in soup.find_all("a", href=re.compile(pattern)) ])

    maxpage = getMaxPage(soup)
    if maxpage > 1:
        for i in range(2, maxpage + 1):
            r = s.get(turnPageURL(resp.url, i))
            soup = bs4.BeautifulSoup(r.text, "lxml")
            links.update([ a['href'] for a in soup.find_all("a", href=re.compile(pattern)) ])
    
    return links

def patternSelector(pattern_name: str) -> str:
    if pattern_name == "class":
        # 作业列表
        return r'liststudenttaskgroup\?_class\.id=(\d+)$'
    elif pattern_name == "group":
        # 题目列表
        return r'listTaskGroup_Task\?taskGroup\.id=(\d+)$'
    elif pattern_name == "task":
        # 已提交情况
        return r'listttudenttaskgrouptaskassignmentforstudent\?taskGroupTask\.id=(\d+)$'
    elif pattern_name == "detail":
        # 题目信息
        return r'taskdetail\?taskid=(\d+)&taskGroupTask\.id=(\d+)&taskGroup\.id=(\d+)$'
    else:
        return ''

def turnPageURL(url: str, page: int) -> str:
    return url + f"&page={page}"

def readTable(text: str, url: str) -> dict:
    res = {
        'codelink': None,
        'id': None,
    }
    soup = bs4.BeautifulSoup(text, "lxml")
    rows = soup.find("table", class_="newfont03").find_all("tr")
    for row in rows[2:]:
        cells = [i.div for i in row.find_all("td")]
        if cells[5].string.strip() == '100':
            res['id'] = cells[0].string.strip()
            res['codelink'] = cells[-1].find_all("span")[-1].a["href"]
            break
    return res

def collectInfo(s: requests.Session, url: str) -> dict:
    r = s.get(url)
    info = {
        'id': None,
        'name': None,
        'description': None,
    }

    if not r.ok:
        return info

    soup = bs4.BeautifulSoup(r.text, "lxml")
    info['id'] = soup.find("label", class_="text").string
    info['name'] = soup.find("legend").string
    info['description'] = soup.find("pre").string

    return info

def downloadFile(s: requests.Session, url: str, path: str, name: str) -> bool:
    r = s.get(url, allow_redirects=True)
    if r.ok:
        with open(os.path.join(path, name), "wb") as f:
            f.write(r.content)
        return True
    else:
        return False

def recordInfo(s: requests.Session, taskid: str | int, path: str) -> None:
    if isinstance(taskid, int):
        taskid = str(taskid)
    taskurl = f"http://matu.uestc.edu.cn/aptat/task/taskdetail?taskid={taskid}"

    info = collectInfo(s, taskurl)
    with open(os.path.join(path, f"{taskid}.txt"), "w", encoding='utf-8') as f:
        f.write(f"题目编号: {info['id']}\n")
        f.write(f"题目名称: {info['name']}\n")
        f.write(f"题目信息: {info['description']}\n")

def getMaxPage(soup: bs4.BeautifulSoup) -> int:
    page = soup.find("span", class_="right-text09")

    return int(page.text) if page else 1

def main():
    """
    主函数，用于执行程序的主要逻辑。

    :return: None
    """
    s = requests.Session()
    dpath = r"path to save your code"
    rpath = r"path to save problem information"
    domain = "http://matu.uestc.edu.cn"
    if not login(s, "your username", "your password"):
        print("登录失败")
        return

    # 获取作业列表
    r = s.get("http://matu.uestc.edu.cn/aptat/course/liststudentclass", allow_redirects=True)
    classlinks = collectLinks(s, r, patternSelector("class"))

    # 获取题目列表
    for i in classlinks:
        r = s.get(domain + i)
        grouplinks = collectLinks(s, r, patternSelector("group"))

        # 获取已提交情况
        for j in grouplinks:
            r = s.get(domain + j)
            tasklinks = collectLinks(s, r, patternSelector("task"))

            # 获取题目信息
            for k in tasklinks:
                r = s.get(domain + k)
                info = readTable(r.text, k)
                if info['codelink']:
                    if downloadFile(s, domain + info['codelink'], dpath, f"{info['id']}.cpp"):
                        recordInfo(s, info['id'], rpath)

if __name__ == "__main__":
    main()