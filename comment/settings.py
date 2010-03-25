from ragendja.settings_post import settings

settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'comment/css/screen.css'
)

settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'comment/js/comment.js',
)