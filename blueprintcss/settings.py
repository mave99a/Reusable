from ragendja.settings_post import settings

settings.add_uncombined_app_media('blueprintcss')

settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'blueprintcss/screen.css'
)
