import os
import datetime
import markdown

from static_resume import base_processors


DEFAULT_LANGUAGE = 'en'
language = os.environ.get('RESUME_LANG', DEFAULT_LANGUAGE)


def proc_heading(key: str, values: dict) -> dict:
    """Get heading"""

    final_html = \
        '<div class="col-lg-3" id="presa-img">' \
        '<img src="{}" alt="me" style="width: 260px; height: 260px">' \
        '</div>'.format(values['picture'])

    final_html += '<div class="col-lg-6 col-md-12" id="presa-txt">{}</div>'.format(markdown.markdown(values['text']))

    contact_block = \
        '<div class="mail-and-twitter-large">' \
        '<h4>Email</h4><p><a href="mailto:{0}">{0}</a></p>' \
        '<h4>Twitter</h4><p><a href="https://twitter.com/{1}">@{1}</a></p>' \
        '</div>'\
        '<span class="mail-and-twitter-small">' \
        '<a href="mailto:{0}" title="Email" class="contact-link contact-link-mail">' \
        '<span class="fas fa-envelope-open"></span></a>' \
        '<a href="https://twitter.com/{1}" title="Twitter" class="contact-link contact-link-twitter">' \
        '<span class="fab fa-twitter"></span></a>' \
        '</span><p>'.format(values['email'], values['twitter'])

    for k, v in values['find_me'].items():
        contact_block += '<a href="{1}" title="{0}" class="contact-link contact-link-{0}">' \
                         '<span class="{2}"></span></a>'.format(k, v['link'], v['icon'])

    contact_block += '</p>'

    final_html += '<div class="col-lg-3 col-md-12" id="contacts">{}</div>'.format(contact_block)

    return {key: final_html}


def proc_research_topics(key: str, value: dict) -> dict:
    """Get resarch topics"""

    final_html = '<h2><span class="fa fa-search" aria-hidden="true"></span> {}</h2>'.format(value['title'])
    return {key: final_html + markdown.markdown(value['text'])}


def proc_publications(key: str, value: dict) -> dict:
    """Get publications"""

    final_html = '<h2><span class="fas fa-microscope" aria-hidden="true"></span> {}</h2>'.format(value['title'])

    for publication in value['list']:
        final_html += \
            '<p>{authors}. ' \
            '"{title}". ' \
            '<em>{journal}</em> <b>{volume}</b>, {page} ({year}). ' \
            '<a href="http://dx.doi.org/{doi}">{doi}</a>.</p>'.format(**publication)

    return {key: final_html}


def proc_skills(key: str, value: dict) -> dict:
    final_html = '<h2><span class="fas fa-puzzle-piece" aria-hidden="true"></span>  {}</h2>'.format(value['title'])

    for section in value['list']:
        final_html += '<h3>{}</h3>'.format(section['name'])
        if 'values' in section:
            final_html += '<div class="skills-container">'
            for skill, val in section['values'].items():
                final_html += \
                    '<p class="skill">{} ' \
                    '<span class="bar-border"><span class="bar-value" style="width:{}%"></span></span>' \
                    '</p>'.format(skill, val/5*100)
            final_html += "</div>"

        if 'post' in section:
            final_html += '<p>{}</p>'.format(markdown.markdown(section['post']))

    return {key: final_html}


def proc_interests(key: str, value: dict) -> dict:
    final_html = '<h2><span class="fas fa-heart" aria-hidden="true"></span> {}</h2>'.format(value['title'])

    for section in value['list']:
        final_html += markdown.markdown('**{}:** {}'.format(section['name'], section['text']))

    return {key: final_html}


def proc_experiences(key: str, value: dict) -> dict:
    final_html = \
        '<h2><span class="fas fa-chart-line" aria-hidden="true"></span> {}</h2>' \
        '<div class="exp-border">'.format(value['title'])

    for section in value['list']:
        final_html += '<h3>{}</h3>{}'.format(
            section['when'], markdown.markdown(section['what']))

    final_html += '</div>'

    return {key: final_html}


def proc_zds(key: str, value: dict) -> dict:
    final_html = \
        '<h2><span class="fas fa-comments" aria-hidden="true"></span> {}</h2>' \
        '{}' \
        '<ul>'.format(value['title'], markdown.markdown(value['pre']))

    for section in value['list']:
        final_html += '<li>{}</li>'.format(markdown.markdown(section))

    final_html += '</ul>'

    return {key: final_html}


CONFIG = {
    'DATA_FILE': 'site_files/resume_{}.yaml'.format(language),
    'TEMPLATE_FILE': 'site_files/template.html',
    'STYLE_FILE': 'site_files/style.css',
    'ASSETS_DIR': 'site_files/assets',
    'OUTPUT_FILE': 'index.html' if language == DEFAULT_LANGUAGE else '{}.html'.format(language),
    'OUTPUT_DIR': 'pages/',
    'PROCESSORS': {
        'footer': base_processors.proc_md,
        'now': lambda k, v: {k: datetime.datetime.now().strftime(v)},
        'heading': proc_heading,
        'research_topics': proc_research_topics,
        'publications': proc_publications,
        'skills': proc_skills,
        'interests': proc_interests,
        'experiences': proc_experiences,
        'ZdS': proc_zds
    }
}