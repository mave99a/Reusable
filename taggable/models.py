from google.appengine.ext import db

def cleanup(tags):
    ''' cleanup: remove duplicate, strip spaces, and remove empty'''
    cleanedtags = filter(lambda tag: tag!='', list(set([tag.strip() for tag in tags])))    
    return cleanedtags
    
class Taggable(db.Model):
    target = db.ReferenceProperty(db.Model)
    tags = db.StringListProperty()
        
    @classmethod
    def get_taggable(cls, obj):
        try: 
           return (obj.taggable_set)[0]
        except:
            return None
    
    @classmethod
    def get_by_tag(cls, tag):
       tag = tag.strip()
       return Taggable.all().filter('tags =', tag) 
   
    @classmethod
    def clear_tags(cls, obj):
        '''clear_tags: remove all tag from an object'''
        taggable = Taggable.get_taggable(obj)
        if taggable is not None: 
            Tag.removeset(taggable.tags) #decrease counter for all tags
            taggable.delete()
                    
        return taggable
        
    @classmethod
    def add_tags(cls, obj, tags):
        tags = cleanup(tags)
        taggable = Taggable.get_taggable(obj)
        if taggable is None: 
          taggable = Taggable(target = obj, tags = tags)
          Tag.addset(tags)           
        else: 
            for tag in tags:
               if tag not in taggable.tags:
                   taggable.tags.append(tag)
                   Tag.add(tag) #increase the counter
        taggable.put()
        return taggable
       
    @classmethod
    def remove_tags(cls, obj, tags):
        tags = cleanup(tags)
        taggable = Taggable.get_taggable(obj)
        if taggable is not None: 
            for tag in tags: 
                if tag in taggable.tags: 
                    taggable.tags.remove(tag)
                    Tag.remove(tag) # decrease the counter
            
            if len(taggable.tags) == 0 : 
                taggable.delete()
            else:
                taggable.put()
        return taggable
    
   
class Tag(db.Model):
    name = db.StringProperty(required = True)      
    count = db.IntegerProperty(default = 0)
    # create time
    ctime = db.DateTimeProperty(auto_now_add=True)   
    #last update time
    mtime = db.DateTimeProperty(auto_now=True)    
    # language, for filtering and automatic translation support
    lang = db.StringProperty(required=True, default='en') 
    
    @classmethod
    def get_tag(cls, tag):
        tag = Tag.all().filter('name =', tag)
        return tag.get()
    
    @classmethod
    def add(cls, tagname):
        tag = cls.get_tag(tagname)
        if tag is None:
            tag = Tag(name=tagname, count=1)
        else:
            tag.count +=1
        tag.put()
    
    @classmethod
    def remove(cls, tagname):
        tag = cls.get_tag(tagname)
        if tag is not None:
            tag.count -=1
            if (tag.count >0):
                tag.put()
            else:
                tag.delete()
    
    @classmethod
    def addset(cls, tags):
        for tag in tags:
            cls.add(tag)
    
    @classmethod
    def removeset(cls, tags):
        for tag in tags: 
            cls.remove(tag)
            
    @classmethod
    def cloud(cls, n):
       return Tag.all().order('name')
    
class UserTag(Tag):
    pass
