import requests
import bs4
import os


def parser(url) -> None:
    path = '/home/mamba/habr-articles'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    element = soup.find(id="post-content-body")
    write_path = get_text(path, element, soup)
    get_images(write_path, element, soup)


def name_format(name: str):
    format_name = name.replace(' ', '_')
    format_name = format_name.replace('/', "_")
    return format_name


def get_text(path, element, soup):
    text = element.find(xmlns="http://www.w3.org/1999/xhtml").find_all(['h1', 'h2',
                                                                        'h3', 'h4', 'p'])
    header = soup.find(class_='tm-title').find('span').text
    header = name_format(header)
    write_path = f"{path}/{header[:50]}"
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    with open(f'{write_path}/{header[:50]}.md', 'w') as f:
        for i in text:
            f.write(f"{i.text}\n\n")

    return write_path


def get_images(path, element, soup):
    images = element.find_all('img')
    if not os.path.exists(f"{path}/images"):
        os.mkdir(f"{path}/images")
    for i in images[0:]:

        text = bs4.BeautifulSoup(str(i), 'html.parser')
        current_img = [text.img.get('src'), text.img.get('title')]
        response = requests.get(current_img[0])
        if current_img[1] is None:
            current_img[1] = current_img[0].split('/')[-1]
        with open(f"{path}/images/{current_img[1][0:32]}...", "wb") as f:
            f.write(response.content)


if __name__ == '__main__':
    url = str(input())
    parser(url)
