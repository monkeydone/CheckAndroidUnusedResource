#!/usr/bin/env python
#coding:utf-8

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
