from requests_html import HTMLSession

def get_rendered_html(url, selector, conn):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    pstring = r.html.find(selector, first=True).text
    conn.send(pstring)
    conn.close()