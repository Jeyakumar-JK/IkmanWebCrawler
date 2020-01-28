

class IkmanTag:

    def __init__(self, tag):
        self.tag = None
        self.text = 'Not Specified'
        self.assign(tag)

    def assign(self, tag):
        self.tag = tag
        if hasattr(tag, 'text'):
            self.text = tag.text
        else:
            self.text = 'Not Specified'

    def find_tag(self, seek_tag, seek_class = None):
        if self.tag is not None:
            if seek_class is None:
                self.assign(self.tag.find(seek_tag))
            else:
                self.assign(self.tag.find(seek_tag, seek_class))
        return self

