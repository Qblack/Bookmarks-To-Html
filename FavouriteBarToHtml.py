__author__ = 'Q'

import os
import getpass


def fill_in_ascii(phrase):
    for character in phrase:
        if not character.isalnum() and not character.isspace():
            if character != '.':
                phrase = phrase.replace(character, "&#{ascii}".format(ascii=ord(character)), 1)
    return phrase


def get_link_url(link_name, directory):
    title = link_name[:-4]
    link_path = os.path.join(directory, link_name)
    body = open(link_path).readlines()
    link_url = ''

    for line in body:
        token = 'URL='
        if line.startswith(token):
            link_url = line[len(token):].strip()
            link_url = link_url.replace("&", "&#26")
            link_url = link_url.replace("<", "&#60")
            link_url = link_url.replace(">", "&#62")
            title = fill_in_ascii(title)
            link_url = ('{0}'.format(link_url))

    return link_url, title


def write_bookmarks(file_name, path):
    with open(file_name, 'tw', encoding='utf-8') as fh:
        fh.write("<!DOCTYPE html>\n")
        fh.write("<html>\n")
        fh.write("<head>\n")
        fh.write("<title>{user}'s Links</title>\n".format(user=username))
        fh.write("</head>\n")
        fh.write("<body>\n")

        for root, dirs, links in os.walk(path):
            directory = os.path.split(root)[1]
            fh.write("<dl>\n")

            fh.write("\t<dt><h3>{header}</h3></dt>\n".format(header=directory))
            for link in links:
                if link.endswith('.url'):
                    url, name = get_link_url(link, root)
                    fh.write('\t<dd><a href="{url}">{title}</a></dd>\n'.format(url=url, title=name))

            fh.write("</dl>\n")
        fh.write("</body>")
        fh.write("</html>")


if __name__ == '__main__':
    username = getpass.getuser()
    DRIVE = r'C:\\'
    bar_path = os.path.join(DRIVE, "Users", username, "Favorites", "Links")
    file = "bookmarks.html"
    write_bookmarks(file, bar_path)
