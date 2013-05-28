class Listener:
    def __repr__(self):
        #return self.__dict__
        return ("<Instance of %s,address %s:\n%s>"%(self.__class__.__name__,id(self),self.attrnames()))

    

    def __str__(self):
        #return self.__dict__
        return ("<Instance of %s,address %s:\n%s>"%(self.__class__.__name__,id(self),self.attrnames()))
    def append(self,other,force=False):
        for i in other.__dict__:
            if i in self.__dict__.keys() and not force:
                continue
            setattr(self,i,other.__dict__[i])
    def attrnames(self):
        result=""
        for attr in sorted(self.__dict__.keys()):
            try:
                if attr[:2]=="__":
                    result=result+"\tname %s=<build-in>\n"%attr
                else:
                    result=result+"\tname %s=%s\n"%(attr,self.__dict__[attr])
            except:
                mx_info.logger.debug(self.__dict__)
                mx_info.logger.error("Exception has occured" ,exc_info=1)
                #traceback.print_exc()
        return result
class Information(Listener):
    pass

