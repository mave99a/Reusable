from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'jquerylib/jquery.js',
    'jquerylib/jquery.fixes.js',
    'jquerylib/jquery.ajax-queue.js',
    'jquerylib/jquery.bgiframe.js',
    'jquerylib/jquery.livequery.js',
    'jquerylib/jquery.form.js',
)
