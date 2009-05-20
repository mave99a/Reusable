from ragendja.settings_post import *

add_uncombined_app_media(globals(), 'blueprintcss')

add_app_media(globals(), 'combined-%(LANGUAGE_DIR)s.css',
    'blueprintcss/screen.css'
)
