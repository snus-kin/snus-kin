"""
    Add my blog RSS to my Github Profile
"""
import pathlib
import re
import requests
import feedparser

BLOG_FEED = "https://snufk.in/blog/rss.xml"
WTTR_MOON = "https://wttr.in/Leeds?format=%m"
ROOT = pathlib.Path(__file__).parent.resolve()


def replace_chunk(content, marker, chunk, inline=False):
    """ Replace a matching chunk in the Readme Markdown """
    regex = re.compile(
        r"<!\-\- {start} starts \-\->.*<!\-\- {end} ends \-\->"
        .format(start=marker, end=marker),
        re.DOTALL,
    )

    if not inline:
        chunk = "\n{}\n".format(chunk)

    chunk = "<!-- {start} starts -->{chunk}<!-- {end} ends -->" \
            .format(start=marker, chunk=chunk, end=marker)
    return regex.sub(chunk, content)


def get_blog_entries():
    """ Get blog entries and return as a list of dictionaries """
    blog_entries = feedparser.parse(BLOG_FEED)["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"],
            "published": entry["published"][:16]
        } for entry in blog_entries
    ]


def get_moon_text():
    """ Get the moon text, perhaps more to be done here """
    return requests.get(WTTR_MOON).text


if __name__ == "__main__":
    readme = ROOT / "README.md"
    readme_content = readme.open().read()

    entries = get_blog_entries()[:5]

    ENTRIES_MD = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry)
         for entry in entries]
    )

    rewritten = replace_chunk(readme_content, "blog", ENTRIES_MD)

    moon = get_moon_text()

    rewritten = replace_chunk(rewritten, "moon", moon)

    readme.open("w").write(rewritten)
