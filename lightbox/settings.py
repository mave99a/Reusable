from ragendja.settings_post import settings

settings.add_uncombined_app_media('lightbox')

settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'lightbox/sexylightbox.css'
)

settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'lightbox/sexylightbox.v2.3.jquery.js',
    'lightbox/jquery.easing.1.3.js'
)
