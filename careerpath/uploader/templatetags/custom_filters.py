from django import template
import markdown as md
import re

register = template.Library()

@register.filter(name='bold_text')
def bold_text(value):
    """
    Converts **text** to <b>text</b>
    """
    pattern = re.compile(r'\*\*(.*?)\*\*')
    return pattern.sub(r'<b>\1</b>', value)


@register.filter(name='markdown')
def markdown(value):
    """
    Converts Markdown text to HTML
    """
    return md.markdown(value)