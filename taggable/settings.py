from ragendja.settings_post import settings

settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'taggable/css/tags.css'
)

settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'taggable/js/tags.js',
)