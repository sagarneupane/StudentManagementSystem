from django.template.defaultfilters import filesizeformat
# from django.utils.translation import ugettext_lazy as _
from django.db.models import FileField
from django.forms import forms

class ContentRestrictiononFileField(FileField):
    def __init__(self, *args , **kwargs):
        self.content_types =  kwargs.pop("content_types",[])
        self.max_upload_size = kwargs.pop("max_upload_size",0)
        # print(self.content_types)
        # print(self.max_upload_size)
        super(ContentRestrictiononFileField, self).__init__(*args, **kwargs)
 
    def clean(self,*args,**kwargs):
        data = super(ContentRestrictiononFileField,self).clean(*args,**kwargs)
        # print("Your Data",data)
        file = data.file
        # print("Your File",file)
        try:
            content_type = file.content_type
            print("Uploaded File Content Type",content_type)
            print("Our Restrictions On content types",self.content_types)
            
            print(content_type in self.content_types)
            # print(file.size)
            if content_type in self.content_types:
                
                if file.size > self.max_upload_size:
                    raise forms.ValidationError(("Please keep filesize under %s. Current Filesize is %s") %(filesizeformat(self.max_upload_size),
                                                                                                             filesizeformat(file.size)))
                
            else:
                raise forms.ValidationError('Filetype not supported. please upload your file in PDF, jpeg and docx')
                    
        except AttributeError:
            pass

        return data