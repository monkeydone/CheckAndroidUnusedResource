#!/usr/bin/env python
#coding:utf-8


import os
import re
import glob
import subprocess


"""
1.获取资源所有文件
2.查找资源文件是否被引用过
3.如果未被引用则列出
"""


def processCmd(cmd):
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    return p.stdout.read()

def getAllFiles(path,suffix):
    a=[]
    for root,dirs,files in os.walk(path):
        #print root
        for i in files:
            if i.endswith(suffix):
                x="%s/%s"%(root,i)
                a.append(x)
    return a

class SourceObject:
    def __init__(self,sourcepath):
        self.sourcepath=sourcepath
        self.sourcename=sourcepath.split("/")[-1].split(".")[0]


class ResourceObject:
    def __init__(self,resourcepath,resourcetype):
        self.resourcepath=resourcepath
        self.resourcename=self.getResourceName(resourcepath)
        self.java_reference=r"R.%s.%s\b"%(resourcetype,self.resourcename)
        self.xml_reference=r"@%s/%s\b"%(resourcetype,self.resourcename)
    def getResourceName(self,resourcepath):
        #filename=resourcepath.split("/")[-1]
        #print filename
        #print filename.split(".")[0]
        return resourcepath.split("/")[-1].split(".")[0]

excludelist=["classes.dex","\\\.class",".svn","test","Test","Sample","sample","import"]

def checkResourceFileReference(reference,destpath):
    return checkFileReference(reference,destpath)

def checkSourceFileReference(source,sourcepath,destpath):
    result=""
    a=checkFileReference(source,destpath)
    for i in a.split("\n"):
        if i.strip() == "":
            continue
        #print "match",i.strip()
        j=i.split(":")
        #print "bb","i=",i,"filename=",reference.split(r"\b")[1],"path=",j[0],reference.split(r"\b")[1] in j[0]
        if sourcepath in j[0]:
            continue
        result+=i
    return result


def checkFileReference(reference,destpath):
    excludecmd=""
    for i in excludelist:
        excludecmd+=" | grep -v %s"%(i)
    #print excludecmd
    cmd="egrep '%s' %s -r %s"%(reference,destpath,excludecmd)
    a=processCmd(cmd)
    print reference,cmd,a,a.split("\n")
    return a


def isNotAllow(filepath,excludelist):
    a=False
    for i in excludelist:
        if i in filepath:
            #print "allow",filepath,a
            a=True
            break
    return a

def handleSource(source_list,project_path):
    for i in source_list:
        #print i.__dict__
        if "test" in i.sourcepath:
            continue
        if "sample" in i.sourcepath:
            continue
        #print i.sourcepath
        if i.sourcename=="":
            print i.sourcepath
            break
        a=checkSourceFileReference(r"\b%s\b"%(i.sourcename),i.sourcename,project_path)
        #print i.sourcename,a
        if a.strip() == "":
            srcpath=i.sourcepath
            destpath=i.sourcepath.replace(i.sourcename,"test_%s"%(i.sourcename))
            cmd="mv %s %s"%(srcpath,destpath)
            print "move %s to %s"%(srcpath,destpath)
            #utils.processCmd(cmd)

def handleResource(resource_list,project_path):
    #drawable_list=androidSourceStruct.drawable_png_map["/home/lijunjie/work/android/MxBrowser6/res/drawable-hdpi"]
    for i in resource_list:
        #print i.resourcename,i.resourcename.startswith("test")
        if i.resourcename.startswith("test"):
            continue
        a=checkResourceFileReference(i.java_reference,project_path)
        #print "ttt",i.java_reference,"result=",a
        if a.strip() == "":
            b=checkResourceFileReference(i.xml_reference,project_path)
            #print "bbb",i.xml_reference,"result=",b
            if b.strip() == "":
                srcpath=i.resourcepath
                destpath=i.resourcepath.replace(i.resourcename,"test_%s"%(i.resourcename))
                cmd="mv %s %s"%(srcpath,destpath)
                print "move %s to %s"%(srcpath,destpath)
                #print cmd
                
                #utils.processCmd(cmd)
     


class AndroidSourceStruct:
    def __init__(self,path):
        self.path=path
        self.source_dir="%s/src"%(path)
        self.resource_dir="%s/res"%(path)
        self.drawable_list=self.getDrawableDirList(path)
        self.drawable_xml_map={}
        self.drawable_png_map={}
        for i in self.drawable_list:
            drawable_xml_files,drawable_png_files=self.getDrawableFileList(i)
            self.drawable_xml_map[i]=self.createResourceObjectList(drawable_xml_files,"drawable")
            self.drawable_png_map[i]=self.createResourceObjectList(drawable_png_files,"drawable")

        self.layout_files=self.createResourceObjectList(self.getLayoutFileList(path),"layout")
        self.source_files=self.getSourceFileList(path)
    def createResourceObjectList(self,resource_files,resource_type):
        a=[]
        for i in resource_files:
            a.append(self.createResourceObject(i,resource_type))
        return a

    def handleResource(self):
        layout_list=self.layout_files
        handleSource(self.source_files,self.path)
        handleResource(layout_list,self.path)
        for i in self.drawable_png_map.itervalues():
            handleResource(i,self.path)
        pass

    def createResourceObject(self,resource_path,resource_type):
        ro=ResourceObject(resource_path,resource_type)
        return ro

    def getDrawableDirList(self,path):
        drawable_dir="%s/res/drawable*"%(path)
        return glob.glob(drawable_dir)
    def getDrawableFileList(self,drawable_dir):
        drawable_xml_dir="%s/*.xml"%(drawable_dir)
        drawable_png_dir="%s/*.png"%(drawable_dir)
        drawable_xml_files=glob.glob(drawable_xml_dir)
        drawable_png_files=glob.glob(drawable_png_dir)
        #print drawable_xml_files
        #print drawable_png_files
        return drawable_xml_files,drawable_png_files
    def getLayoutFileList(self,path):
        layout_dir="%s/res/layout/*"%(path)
        return glob.glob(layout_dir)
    def getSourceFileList(self,path):
        source_dir="%s/src/"%(path)
        #print source_dir
        a=[]
        for root,dirs,files in os.walk(source_dir):
            if ".svn" in root :
                continue
            #print root,dirs
            for i in files:
                a.append(SourceObject("%s/%s"%(root,i)))
        return a
            

        
def checkReference(filename,reference):
    f=open(filename,"r")
    content=f.read()
    r=r"%s\b"%reference
    p=re.compile(r)
    a=p.findall(content)
    if a:
        return filename,reference,a
    else:
        return None

def getResourceDirs(path,resourcename):
    a=[]
    for root,dirs,files in os.walk(path):
        for i in dirs:
            if resourcename in i:
                x="%s/%s"%(root,i)
                a.append(x)
    return a

def main():
    import sys
    if len(sys.argv)==2:
        ass=AndroidSourceStruct(sys.argv[1])
        #handleSource(ass.source_files,ass.path)
        ass.handleResource()

    print sys.argv


    pass
def testAllDrawable():
    path="./dest/svnproject/res/drawable/"
    for i in getAllFiles(path,"png"):
        for j in i.split(":"):
            print j


def testCheckResource():
    path="/home/lijunjie/work/android/MxBrowser6/"
    res1="/home/lijunjie/work/android/MxBrowser6//res/layout/download_view_bottom.xml"
    a=ResourceObject("/home/lijunjie/work/android/MxBrowser6/res/drawable-mdpi/find_btn_close_panel.png","drawable")
    b=ResourceObject("/home/lijunjie/work/android/MxBrowser6/res/drawable-mdpi/find_btn_close_panel11.9.png","drawable")
    #handleResource([ResourceObject(res1,"drawable"),a,b],path)
    handleResource([ResourceObject(res1,"layout")],path)
    #a,b,c=checkReference(path,filename)
    #print a,b,c

def testCheckFileReference():
    a=checkFileReference("@drawable/account_avatar","./dest/svnproject/")

    print a
def testReferenceObject():
    a=ResourceObject("./dest/svnproject/res/drawable-mdpi/find_btn_close_panel.png","drawable")
    b=ResourceObject("./dest/svnproject/res/drawable-mdpi/find_btn_close_panel.9.png","drawable")
    print a.__dict__
    print b.__dict__

def testAndroidSourceStruct():
    androidSourceStruct=AndroidSourceStruct("/home/lijunjie/work/android/MxBrowser6")
    #print androidSourceStruct.__dict__
    #print androidSourceStruct.source_files
    #print androidSourceStruct.layout_files
    #print "map",androidSourceStruct.drawable_png_map
    drawable_list=androidSourceStruct.drawable_png_map["/home/lijunjie/work/android/MxBrowser6/res/drawable-hdpi"]
    #handleResource(drawable_list,androidSourceStruct.path)
    layout_list=androidSourceStruct.layout_files
    handleResource(layout_list,androidSourceStruct.path)

    source_list=androidSourceStruct.source_files
    androidSourceStruct.handleResource()
    #for i in source_list:
        #print i.__dict__
    #handleSource(source_list,androidSourceStruct.path)
                
def testCheckSource():
    #sourcepath="/home/lijunjie/work/android/MxBrowser6/src/com/mx/browser/clientviews/MxSlidableScreenClientView.java"
    sourcepath2="/home/lijunjie/work/android/MxBrowser6/src/com/mx/browser/clientviews/MxNavigationClientView.java"
    sourcepath="/home/lijunjie/work/android/MxBrowser6//src/com/mx/core/MxMenuBase.java"
    project_path="/home/lijunjie/work/android/MxBrowser6/"
    handleSource([SourceObject(sourcepath),SourceObject(sourcepath2)],project_path)





if __name__== "__main__":
    #main()
    testCheckResource()
    #testCheckSource()
    #testReferenceObject()
    #testAllDrawable()
    #testAndroidSourceStruct()
    #testCheckFileReference()
