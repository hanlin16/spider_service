# coding:utf-8

import json


class paramater:
    categoryName = ''
    title = ''
    author = ''
    editor = ''
    description = ''
    text = ''
    cover = ''
    tags = ''
    copied = 'on'
    source = ''
    sourceUrl = ''
    importDateStr = ''

    def __init__(self, categoryName, title,
                 author, editor,
                 description, text,
                 cover, tags, source, sourceUrl, importDateStr):
        self.categoryName = categoryName
        self.title = title
        self.author = author
        self.editor = editor
        self.description = description

        self.text = text
        self.cover = cover
        self.tags = tags
        self.source = source
        self.sourceUrl = sourceUrl

        self.importDateStr = importDateStr
        #logger.info("初始化paramater类")


p = paramater('categoryName', 'title',
              'author', 'editor',
              'description', 'text',
              'cover', 'tags', 'source', 'sourceUrl', 'importDateStr')

overdict = p.__dict__
result = json.dumps(overdict, ensure_ascii=False)
#logger.info(result)
