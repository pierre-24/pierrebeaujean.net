import os

language = os.environ.get('RESUME_LANG', 'en')

CONFIG = {
    'DATA_FILE': 'site_files/resume_{}.yaml'.format(language),
    'TEMPLATE_FILE': 'site_files/template.html',
    'STYLE_FILE': 'site_files/style.css'
}