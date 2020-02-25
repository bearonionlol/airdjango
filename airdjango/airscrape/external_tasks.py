# from requests_html import HTMLSession
#
# def get_rendered_html(url, selector, conn):
#     session = HTMLSession()
#     r = session.get(url)
#     r.html.render()
#     pstring = r.html.find(selector, first=True).text
#     conn.send(pstring)
#     conn.close()



from requests_html import HTMLSession
import sys

def get_rendered_html(url, selector):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    pstring = r.html.find(selector, first=True).text
    return pstring

if __name__ == '__main__':
    url = sys.argv[1]
    selector = sys.argv[2]
    pstring = get_rendered_html(url, selector)
    print(pstring, end='')