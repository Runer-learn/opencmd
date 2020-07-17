# -*- coding:utf8 -*-
import os;
import sys
import io;
import math;
import subprocess;

root = os.path.dirname(os.path.abspath(__file__));

configFile='.opencmd';
configPath=root+'/'+configFile;

configSetting=dict({});
# fin=os.open(configPath,'r');
fin=None;

cd='.';

# ''.strip()
def parseConfigLine(line):
    lines=line.split('=');
    if len(lines)>=2:
        return dict.fromkeys([lines[0].strip().rstrip()],lines[1].strip().rstrip());
    return {};


try:
    with open(configPath,'r') as fin:
        line=fin.readline();
        # dic_tmp=parseConfigLine(line);
        # configSetting.update(dic_tmp);
        while line!='':
            if line!='\n' and line!='\r' and line!='\t':
                dic_tmp=parseConfigLine(line);
                configSetting.update(dic_tmp);
            line=fin.readline();
except IOError:
    fin=None;
    print("配置文件%s读取失败"%configPath)



# with fin=os.open(configPath,'r'):
#     pass;

if fin!=None:
    # os.close(fin);
    fin=None;


def has_key(dic,key):
    try:
        dic[key];
        return True;
    except Exception:
        return False;

def list_find(lists,key):
    try:
        return lists.index(key);
        # return True;
    except Exception:
        return -1;

class CMDTag(object):
    def __init__(self,cmdTags=[]):
        super().__init__();
        self.CmdTags=cmdTags;
    
    def isCmdEq(self,cmd):
        # return False;
        try:
            index=self.CmdTags.index(cmd);
            if index<0:
                return False;
            return True;
        except Exception :
            return False;
        

    def RunCmd(self,*args):
        pass;

class RunCmdList(object):
    def __init__(self):
        super().__init__();
        self.Cmds=[];
    
    def findCmdObj(self,cmd):
        for obj in self.Cmds:
            # print(cmd);
            if obj and obj.isCmdEq and obj.isCmdEq(cmd):
                return obj;
        return None;
    
    def registerCmd(self,cmdTagAct):
        self.Cmds.append(cmdTagAct);


class HelpCmd(CMDTag):
    def __init__(self):
        super().__init__(cmdTags=['h','H','help','Help','HELP','-h','-H'])
    def RunCmd(self,*args):
        print('''opencmd -H(help)|O(open)|A(add)|D(delete) [name|name dir path]

opencmd -H|-h|help 打印帮助信息
eg: >opencmd -h

opencmd -v|-V|version  查看命令版本
eg: >opencmd -v

opencmd -O|-o|open|[NULL] name 打开name代表的指定目录|文件
eg: >opencmd -o hello

opencmd -OE|-oe|opene| name 打开name代表的指定目录|文件在文件浏览器
eg: >opencmd -oe hello

opencmd -A|-a|add  name dirpath 注册指定名称和目录路径
eg: >opencmd -a test d:\test

opencmd -R|-r|read  查看注册的名称和目录
eg: >opencmd -r

opencmd -D|-d|delete name  删除已注册的名称/目录(文件)
eg: >opencmd -d test''');


class AddCmd(CMDTag):
    def __init__(self):
        super().__init__(cmdTags=['a','add','Add','ADD','-a','-A']);
    def RunCmd(self,args):
        # (cmds)=args;
        length=len(args);
        # print(root,args,len(args));
        fin_file=open(configPath,'a+');
        if length==2:
            flage=self.RunAddCmd(args[0],args[1],fin_file);
            if flage:
                configSetting.setdefault(args[0],self.getAbsortPath(args[1]));
            # pass;
        elif length>2:
            count=math.floor(length/2);
            for i in range(count):
                (seqkey,seqvalue)=(2*i,2*i+1);
                flage=self.RunAddCmd(args[seqkey],args[seqvalue],fin_file);
                if flage:
                    configSetting.setdefault(args[seqkey],self.getAbsortPath(args[seqvalue]));
            # pass;
        else:
            pass;
        # os.close(fin_file);
        fin_file=None;

    def RunAddCmd(self,key,value,fin):
        if has_key(configSetting,key):
            print('cmd %s key has registered!'%key);
        else:
            if fin!=None:
                try:
                    fin.writelines('\n'+key+' = '+self.getAbsortPath(value)+'\n');
                    return True;
                except Exception:
                    print('cmd %s write fail'%s);
            else:
                print('写入文件失败');
        return False;
                
    def getAbsortPath(self,path):
        if path==None:
            return os.path.abspath(cd);
        if os.path.isabs(path):
            return path;
        elif path.startswith('.'):
            return os.path.abspath(path)
        else:
            return os.path.join(os.path.abspath(cd),path);

class OpenCmd(CMDTag):
    def __init__(self):
        super().__init__(cmdTags=['o','open','Open','OPEN','-o','-O']);
    def RunCmd(self,args):
        lenght=len(args);
        if lenght==0:
            print('参数异常!');
        else:
            for name in args:
                if has_key(configSetting,name):
                    path=configSetting[name];
                    print(path)
                    subprocess.Popen("cmd  'cd %s'"%path, creationflags=subprocess.CREATE_NEW_CONSOLE,cwd=path)

class DeleteCmd(CMDTag):
    def __init__(self):
        super().__init__(cmdTags=['d','delete','Delete','DELETE','-d','-D']);
    def RunCmd(self,args):
        lenght=len(args);
        if lenght==0:
            print('参数异常!');
        else:
            deleteLines=[];
            for name in args:
                if has_key(configSetting,name):
                    deleteLines.append(name);
            self.RunDeleteCmd(deleteLines);

    def RunDeleteCmd(self,dellines):
        try:
            lines=[];
            with open(configPath,'r') as fin:
                lines=fin.readlines();
            with open(configPath,'w') as fwrit:
                writelines=[];
                for tline in lines:
                    line_split=tline.split('=');
                    # print(line_split[0].strip(),lines);
                    if list_find(dellines,line_split[0].strip().rstrip())>=0:
                        if has_key(configSetting,line_split[0].strip().rstrip()):
                            del configSetting[line_split[0].strip().rstrip()];
                        continue;
                    else:
                        writelines.append(tline);
                fwrit.writelines(writelines);
        except IOError:
            fin=None;
            print("配置文件%s读取失败"%configPath)

class ReadCmd(CMDTag):
    def __init__(self):
        super().__init__(cmdTags=['r','read','Read','READ','-r','-R']);
    def RunCmd(self,args):
        for key in configSetting.keys():
            print("%s \t:\t %s"%(key,configSetting[key]))

class VersionCmd(CMDTag):
    def __init__(self):
        super().__init__(cmdTags=['v','V','Version','version','-v','-V']);
    def RunCmd(self,args):
        print('''
        @开发人员   ：lihaifeng
        @版本   :v0.0.1
        @开发日期   :2020/07/17
        ''')

class OpenExportCmd(CMDTag):
    def __init__(self):
        super().__init__(cmdTags=['oe','opene','OpenE','OPENE','-oe','-OE']);
    def RunCmd(self,args):
        lenght=len(args);
        print(args);
        if lenght==0:
            print('参数异常!');
        else:
            for name in args:
                if has_key(configSetting,name):
                    path=configSetting[name];
                    subprocess.Popen(r'explorer   "%s"'%path,cwd=path)

def parseCmd(cmd):
    # print(cmd);
    cd=cmd[1];
    result= cmd[2:];
    # print(result);
    if len(result)<=0:
        return None;
    return result;

def registerCmd(cmdFactory):
    # pass;
    cmdFactory.registerCmd(HelpCmd());
    cmdFactory.registerCmd(AddCmd());
    cmdFactory.registerCmd(OpenCmd());
    cmdFactory.registerCmd(DeleteCmd());
    cmdFactory.registerCmd(ReadCmd());
    cmdFactory.registerCmd(OpenExportCmd());
    cmdFactory.registerCmd(VersionCmd());

def runCmd(cmd):
    cmds=parseCmd(cmd);
    if cmds==None:
        print('cmd counts except.');
        return;
    cmdRunFactory=RunCmdList();
    registerCmd(cmdRunFactory);
    cmdObj=cmdRunFactory.findCmdObj(cmds[0]);
    # print(cmdObj);
    if cmdObj==None:
        print('命令不存在，请使用-h查看帮助\n');
    else:
        cmdObj.RunCmd(cmds[1:]);


if __name__=='__main__':
    # print(sys.argv);
    runCmd(sys.argv);