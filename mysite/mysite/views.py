from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from pymongo import MongoClient
import re
import time
from bson.objectid import ObjectId
from django.shortcuts import render_to_response
import requests

client = MongoClient('10.183.222.106',27017)

def timetransfer(realtime):
    shi=time.mktime(time.strptime(realtime,'%Y-%m-%d %H:%M:%S'))
    print(shi)
    shiliu=hex(int(shi))
    print(shiliu)
    b = shiliu[2:] + "6f2047a994b9cfed"
    mongotime = ObjectId(b)
    return mongotime


def http(request):
    realbegintime = '2017-01-01 00:00:00'
    realendtime = '2018-01-01 00:00:00'
    return render_to_response('http.html',{})

def tiaojian(ziduanname,tj,message,total_searchdict,collection_useraction):
    message += '\n\n'
    tj_searchdict = dict(total_searchdict,**tj)
    tj_number = collection_useraction.find(tj_searchdict).count()
    exist_searchdict = tj_searchdict.copy()
    kong_searchdict = tj_searchdict.copy()
    exist_searchdict[ziduanname]={'$exists':'true'}
    ziduan_number = collection_useraction.find(exist_searchdict).count()
    kong_searchdict[ziduanname] = {'$in':['-','']}
    kong_number = collection_useraction.find(kong_searchdict).count()
    distinctvalues = collection_useraction.distinct(ziduanname,tj_searchdict)
    if ziduan_number == tj_number:
        if kong_number != 0:
            message += (ziduanname +':Fail  (' + str(tj) + '时,' + str(kong_number) + '条数据上报空/-);' )
        else:
            message += (ziduanname + ': Pass  (上报' + ziduanname + '的数据是' + str(ziduan_number) +'条，等于上报' + str(tj) + '的数据量);')

    else:
        message += (ziduanname +':Fail  (' + str(tj) + '时, %s 条数据没报 %s 字段' % (tj_number-ziduan_number, ziduanname)+')')
        if kong_number != 0:
            message += (' (' + str(tj) + '时,' + str(kong_number) + '条数据上报空/-);' )
    message += str(distinctvalues[0:5])
    return message

def thirteennumber(ziduanname,message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction):
    message += '\n\n'
    exist_searchdict[ziduanname]={'$exists':'true'}
    ziduan_number = collection_useraction.find(exist_searchdict).count()
    value_searchdict[ziduanname] = {'$regex':'^\d\d\d\d\d\d\d\d\d\d\d\d\d$'}
    value_number = collection_useraction.find(value_searchdict).count()
    distinctvalues = collection_useraction.distinct(ziduanname,value_searchdict)
    if ziduan_number == total_number:
        if value_number == ziduan_number:
            message += (ziduanname + ': Pass  (上报' + ziduanname + '是13位整数的的数据是' + str(value_number) +'条，等于总数据量);')
        else:
            message += (ziduanname +':Fail  (上报的数据中，' + str(ziduan_number-value_number) + '条数据上报的不是13位整数);' )

    else:
        message += (ziduanname + ':Fail %s 条数据没报 %s 字段' % (total_number-ziduan_number, ziduanname))
    message += str(distinctvalues[0:5])
    return message
def twelfthnumber(ziduanname,message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction):
    message += '\n\n'
    exist_searchdict[ziduanname]={'$exists':'true'}
    ziduan_number = collection_useraction.find(exist_searchdict).count()
    value_searchdict[ziduanname] = {'$regex':'^\d\d\d\d\d\d\d\d\d\d\d\d$'}
    value_number = collection_useraction.find(value_searchdict).count()
    distinctvalues = collection_useraction.distinct(ziduanname,value_searchdict)
    if ziduan_number == total_number:
        if value_number == ziduan_number:
            message += (ziduanname + ': Pass  (上报' + ziduanname + '是12位整数的的数据是' + str(value_number) +'条，等于总数据量);')
        else:
            message += (ziduanname +':Fail  (上报的数据中，' + str(ziduan_number-value_number) + '条数据上报的不是12位整数);' )

    else:
        message += (ziduanname + ':Fail %s 条数据没报 %s 字段' % (total_number-ziduan_number, ziduanname))
    message += str(distinctvalues[0:5])
    return message

def listvalue(ziduanname,ziduanvalue,message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction):
    message += '\n\n'
    exist_searchdict[ziduanname]={'$exists':'true'}
    ziduan_number = collection_useraction.find(exist_searchdict).count()
    value_searchdict[ziduanname] = {'$in':ziduanvalue}
    value_number = collection_useraction.find(value_searchdict).count()
    distinctvalues = collection_useraction.distinct(ziduanname,value_searchdict)
    if value_number == total_number:
        message += (ziduanname + ': Pass  (上报' + ziduanname +' in' + str(ziduanvalue) +'的数据是' + str(value_number) +'条，等于总数据量)')
    else:
        if value_number < ziduan_number:
            allvalue = collection_useraction.distinct(ziduanname,total_searchdict)
            for each in ziduanvalue:
                if each in allvalue:
                    allvalue.remove(each)
            message += (ziduanname +':Fail  (上报的数据中，' + str(ziduan_number-value_number) + '条数据上报为' + str(allvalue)+ ')')
        if ziduan_number < total_number:
            message += (ziduanname + ':Fail %s 条数据没报 %s 字段' % (total_number-ziduan_number, ziduanname))
    message += str(distinctvalues[0:5])
    return message

def certainvalue(ziduanname,ziduanvalue,message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction):
    message += '\n\n'
    exist_searchdict[ziduanname]={'$exists':'true'}
    ziduan_number = collection_useraction.find(exist_searchdict).count()
    value_searchdict[ziduanname] = ziduanvalue
    print(value_searchdict)
    #print(total_searchdict)
    value_number = collection_useraction.find(value_searchdict).count()
    print(value_number)
    if value_number == ziduan_number:
        message += (ziduanname + ': Pass  (上报' + ziduanname +'=' + ziduanvalue+'的数据是' + str(value_number) +'条，等于总数据量)')
    else:
        if value_number < ziduan_number:
            allvalue = collection_useraction.distinct(ziduanname,total_searchdict)
            print(allvalue)
            if ziduanvalue in allvalue:
                allvalue.remove(ziduanvalue)
            message += (ziduanname +':Fail  (上报的数据中，' + str(ziduan_number-value_number) + '条数据上报为' + str(allvalue)+ ')')
        if ziduan_number < total_number:
            message += '%s 条数据没报 %s 字段' % (total_number-ziduan_number, ziduanname)
    return message

def shangbao(ziduanname,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction):
    message += '\n\n'
    exist_searchdict[ziduanname]={'$exists':'true'}
    ziduan_number = collection_useraction.find(exist_searchdict).count()
    kong_searchdict[ziduanname] = {'$in':['','-']}
    kong_number = collection_useraction.find(kong_searchdict).count()
    distinctvalues = collection_useraction.distinct(ziduanname,total_searchdict)
    if ziduan_number == total_number:
        if kong_number != 0:
            message += (ziduanname + ': Fail (' + str(kong_number) +'条数据上报空/-);')
        else:
            message += (ziduanname + ': Pass  (上报' + ziduanname + '的数据是' + str(ziduan_number) +'条，等于总数据量,且没有上报空/-的数据);')
    else:
        message += (ziduanname + ': Fail  (上报' + ziduanname + '的数据是' + str(ziduan_number) +'条，' + str(total_number-ziduan_number) +
        '条数据没有上报' + ziduanname + '字段;')
        if kong_number != 0:
            message += (';且在上报的数据中有' + str(kong_number) +'条数据上报空/-);')
    message += str(distinctvalues[0:5])
    return message

def uuid(db,total_searchdict,collection_useraction):
    message1 = '\n\n'
    collection_useraction1 = db['pl']
    pldistinctvalues = collection_useraction1.distinct('uuid',total_searchdict)
    distinctvalues = collection_useraction.distinct('uuid',total_searchdict)
    rightvalues = []
    wrongvalues = []
    if distinctvalues != []:
        for each in distinctvalues:
            if each in pldistinctvalues:
                rightvalues.append(each)
            else:
                wrongvalues.append(each)
        if wrongvalues != []:
            message1 += ('uuid:Fail 这些uuid不是来自play接口:' + str(wrongvalues))
        if rightvalues != []:
            message1 += ('这些uuid来自play接口:' + str(rightvalues))
    else:
        message1 += '此接口没有上报uuid'
    return message1,rightvalues

def result(request):
    realbegintime = '2017-01-01 00:00:00'
    realbegintime = request.GET['begintime']
    realendtime = request.GET['endtime']
    begintime= timetransfer(realbegintime)
    endtime= timetransfer(realendtime)
    db_name = request.GET['gongnengji']
    p1 = request.GET['p1']
    p2 = request.GET['p2']
    p3 = request.GET['p3']
    app = request.GET['app']
    app_name = request.GET['app_name']
    cde = request.GET['cde']
    if db_name == '' or p1 == '' or p2 == '':
        message ='Please offer gongnengji,p1 and p2 at least请至少输入功能集,p1和p2'
    else:
        db = client[db_name]
        if request.GET.get('env'):
            collection_useraction = db['env']
        if request.GET.get('lg'):
            collection_useraction = db['lg']
        if request.GET.get('pl'):
            if p1 == '3':
                collection_useraction = db['cloud_pl']
            else:
                collection_useraction = db['pl']
        if request.GET.get('op'):
            collection_useraction = db['op']
        if request.GET.get('er'):
            collection_useraction = db['er']
        if request.GET.get('pgv'):
            collection_useraction = db['pgv']
        if request.GET.get('qy'):
            collection_useraction = db['qy']
        auid = request.GET['auid']
        if auid == '':
            total_searchdict = {'_id':{'$gt':begintime,'$lt':endtime}}
            total_number = collection_useraction.find(total_searchdict).count()
            if total_number == 0:
                message = '你设置的条件没有数据哈！！！'
                return render_to_response('http.html',locals())
            else:
                message = '你测试的是功能集 %s 中, %s 至 %s 的 %s 接口的数据，总数据量是 %s ;' % (db_name,request.GET['begintime'],request.GET['endtime'],collection_useraction,total_number) + str(begintime) + '-----' + str(endtime)
        else:
            total_searchdict = {'_id':{'$gt':begintime,'$lt':endtime},'auid':auid}
            total_number = collection_useraction.find(total_searchdict).count()
            if total_number == 0:
                message = '你设置的条件没有数据哈！！！'
            message = '你测试的是功能集 %s 中, %s 至 %s 的, auid= %s 的数据，总数据量是 %s ;' % (db_name,request.GET['begintime'],request.GET['endtime'],auid,total_number) + str(begintime) + '-----' + str(endtime)
        certainvaluelist = {'p1':p1,'p2':p2,'p3':p3,'app':app,'app_name':app_name}
        listvaluelist = {'nt':['2g','3g','4g','network','none','nont','wifi','wired']}
        thirteennumberlist = ['ctime','stime']
        twelfthnumberlist = ['r']
        shangbaolist = ['apprunid','auid','lc']
        lunbodianbo = request.GET['lunbodianbo']
        lunbozhibo = request.GET['lunbozhibo']
        for each in certainvaluelist:
            exist_searchdict = total_searchdict.copy()
            value_searchdict = total_searchdict.copy()
            message = certainvalue(each,certainvaluelist[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
        for each in listvaluelist:
            exist_searchdict = total_searchdict.copy()
            value_searchdict = total_searchdict.copy()
            message = listvalue(each,listvaluelist[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
        for each in thirteennumberlist:
            exist_searchdict = total_searchdict.copy()
            value_searchdict = total_searchdict.copy()
            message = thirteennumber(each,message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
        for each in twelfthnumberlist:
            exist_searchdict = total_searchdict.copy()
            value_searchdict = total_searchdict.copy()
            message = twelfthnumber(each,message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
        for each in shangbaolist:
            exist_searchdict = total_searchdict.copy()
            kong_searchdict = total_searchdict.copy()
            message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)

        TVZiDuan = ['mac','install_id']
        MobileZiDuan = ['im','imsi','wmac','install_id']
        duan = request.GET['duan']
        if duan == 'TV':
            for each in TVZiDuan:
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
        if duan == 'Mobile':
            for each in MobileZiDuan:
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)

        Android = ['android_id','serialno']
        IOS = ['idfa']
        os = request.GET['os']
        if os == 'Android':
            for each in Android:
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
        if os == 'IOS':
            for each in IOS:
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
        leshishipingandroid_env = ['cs']
        leshishipingmobile_env = ['pcode']
        leshishipingandroid = request.GET['leshishipingandroid']
        leshishipingmobile = request.GET['leshishipingmobile']

        if request.GET.get('env') or request.GET.get('lg') or request.GET.get('er'):
            shangbaolist_envlger = ['os']
            TVZiDuan_envlger = ['bd','model']
            MobileZiDuan_envlger = ['bd','model']
            HTMLZiDuan_envlger = ['br']
            listvaluelist = {'xh':['0','1','2','3','4','5','16','17','18','19']}
            for each in listvaluelist:
                exist_searchdict = total_searchdict.copy()
                value_searchdict = total_searchdict.copy()
                message = listvalue(each,listvaluelist[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)

            for each in shangbaolist_envlger:
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
            if duan == 'TV':
                for each in TVZiDuan_envlger:
                    exist_searchdict = total_searchdict.copy()
                    kong_searchdict = total_searchdict.copy()
                    message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
            if duan == 'Mobile':
                for each in MobileZiDuan_envlger:
                    exist_searchdict = total_searchdict.copy()
                    kong_searchdict = total_searchdict.copy()
                    message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
            if duan == 'HTML':
                for each in HTMLZiDuan_envlger:
                    exist_searchdict = total_searchdict.copy()
                    kong_searchdict = total_searchdict.copy()
                    message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
            if request.GET.get('env') or request.GET.get('lg'):
                message = tiaojian('ssid',{'nt':'wifi'},message,total_searchdict,collection_useraction)
                if leshishipingandroid == 'y':
                    for each in ['cs']:
                        exist_searchdict = total_searchdict.copy()
                        kong_searchdict = total_searchdict.copy()
                        message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)

        if request.GET.get('env') or request.GET.get('lg') or request.GET.get('er') or request.GET.get('pgv') or request.GET.get('op') or request.GET.get('pl'):
            if leshishipingmobile == 'y':
                for each in ['pcode']: #bianliang
                    exist_searchdict = total_searchdict.copy()
                    kong_searchdict = total_searchdict.copy()
                    message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
        if request.GET.get('qy'):
            for each in ['ref','sid','p','q','pos','rt']: #bianliang
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
            listvaluelist = {'ty':['0','1']}
            for each in listvaluelist:
                exist_searchdict = total_searchdict.copy()
                value_searchdict = total_searchdict.copy()
                message = listvalue(each,listvaluelist[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
            message = tiaojian('clk',{'ty':'1'},message,total_searchdict,collection_useraction)

        if request.GET.get('er'):
            for each in ['err']: #bianliang
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
        if request.GET.get('pl'):
            message = tiaojian('source',{'owner':'0'},message,total_searchdict,collection_useraction)
            message = tiaojian('st',{'ty':'2'},message,total_searchdict,collection_useraction)
            message = tiaojian('prl',{'ac':'play'},message,total_searchdict,collection_useraction)
            message += 'prl的值必须in["0","1"]'
            message = tiaojian('pay',{'ac':'play'},message,total_searchdict,collection_useraction)
            message += 'pay的值必须in ["0","1","2","3"]'
            message = tiaojian('joint',{'ac':'play'},message,total_searchdict,collection_useraction)
            message += 'joint的值必须in ["0","1","2"]'
            message = tiaojian('pt',{'ac':'time'},message,total_searchdict,collection_useraction)
            message = tiaojian('mid',{'owner':'0'},message,total_searchdict,collection_useraction)
            if lunbodianbo == 'y':
                message = tiaojian('vid',{'owner':'1','ty':{'$in':['0','2']}},message,total_searchdict,collection_useraction)
                message = tiaojian('pid',{'owner':'1','ty':{'$in':['0','2']}},message,total_searchdict,collection_useraction)
                message = tiaojian('zid',{'owner':'1','ty':{'$in':['0','2']}},message,total_searchdict,collection_useraction)
                message = tiaojian('cid',{'owner':'1','ty':{'$in':['0','2']}},message,total_searchdict,collection_useraction)
            else:
                message = tiaojian('vid',{'owner':'1','ty':{'$in':['0']}},message,total_searchdict,collection_useraction)
                message = tiaojian('pid',{'owner':'1','ty':{'$in':['0']}},message,total_searchdict,collection_useraction)
                message = tiaojian('zid',{'owner':'1','ty':{'$in':['0']}},message,total_searchdict,collection_useraction)
                message = tiaojian('cid',{'owner':'1','ty':{'$in':['0']}},message,total_searchdict,collection_useraction)

            if lunbozhibo == 'y':
                message = tiaojian('lid',{'ty':{'$in':['2','1']}},message,total_searchdict,collection_useraction)
            else:
                message = tiaojian('lid',{'ty':{'$in':['1']}},message,total_searchdict,collection_useraction)
            listvaluelist = {'ty':['0','1','2','3','4','5']}
            for each in listvaluelist:
                exist_searchdict = total_searchdict.copy()
                value_searchdict = total_searchdict.copy()
                message = listvalue(each,listvaluelist[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
            listvaluelist1 = {'ac':['ac_start','ac_end','sload','resume','endSlide','startSlide','psbs','upR','upState','loadend','launch','init','mload',
'gslb','cload','play','time','block','eblock','finish','end','tg','pa','jump','drag','cp']}
            for each in listvaluelist1:
                exist_searchdict = total_searchdict.copy()
                value_searchdict = total_searchdict.copy()
                message = listvalue(each,listvaluelist1[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
            listvaluelist2 = {'owner':['0','1']}
            for each in listvaluelist2:
                exist_searchdict = total_searchdict.copy()
                value_searchdict = total_searchdict.copy()
                message = listvalue(each,listvaluelist2[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
            listvaluelist3 = {'ipt':['0','1','2']}
            for each in listvaluelist3:
                exist_searchdict = total_searchdict.copy()
                value_searchdict = total_searchdict.copy()
                message = listvalue(each,listvaluelist3[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
            for each in ['vt','pv','uuid','ch']: #bianliang
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao(each,message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
            if cde == 'y':
                message = tiaojian('caid',{'ac':'init'},message,total_searchdict,collection_useraction)
                message = tiaojian('cdev',{'ac':'init'},message,total_searchdict,collection_useraction)
            if duan == 'TV':
                listvaluelist4 = {'utype':['children','male','female']}
                for each in listvaluelist4:
                    exist_searchdict = total_searchdict.copy()
                    value_searchdict = total_searchdict.copy()
                    message = listvalue(each,listvaluelist4[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
            if duan == 'HTML':
                certainvaluelist1 = {'key':'letv01'}
                for each in certainvaluelist1:
                    exist_searchdict = total_searchdict.copy()
                    value_searchdict = total_searchdict.copy()
                    message = certainvalue(each,certainvaluelist1[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)



        if request.GET.get('pgv'):
            listvaluelist = {'ct':['1','2','3','4','5']}
            for each in listvaluelist:
                exist_searchdict = total_searchdict.copy()
                value_searchdict = total_searchdict.copy()
                message = listvalue(each,listvaluelist[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
            if duan == 'HTML':
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao('cur_url',message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)
            message = tiaojian('mid',{'owner':'0'},message,total_searchdict,collection_useraction)
        if request.GET.get('op'):
            tuijianlist = ['area','bucket','rank','reid']
            for each in tuijianlist:
                message = tiaojian(each,{'acode':'17'},message,total_searchdict,collection_useraction)
            message = tiaojian('mid',{'owner':'0'},message,total_searchdict,collection_useraction)
            listvaluelist = {'acode':['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
               '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64']}

            for each in listvaluelist:
                exist_searchdict = total_searchdict.copy()
                value_searchdict = total_searchdict.copy()
                message = listvalue(each,listvaluelist[each],message,total_number,exist_searchdict,value_searchdict,total_searchdict,collection_useraction)
            if duan == 'HTML':
                exist_searchdict = total_searchdict.copy()
                kong_searchdict = total_searchdict.copy()
                message = shangbao('cur_url',message,total_number,exist_searchdict,kong_searchdict,total_searchdict,collection_useraction)

        if request.GET.get('pgv') or request.GET.get('op') or request.GET.get('env') or request.GET.get('lg') or request.GET.get('qy') or request.GET.get('er'):
            message1,rightvalues = uuid(db,total_searchdict,collection_useraction)
            if request.GET.get('er'):
                if rightvalues != []:
                    message1 += '\n\n'
                    panduan = 0
                    for each in collection_useraction.find({'uuid':{'$in':rightvalues}}):
                        if 'et' in each.keys():
                            if each['et'] != 'pl':
                                message1 += 'et:Fail 播放错误没有上报et=pl'
                                panduan = 1
                                break
                        else:
                            message1 += 'et: Fail 上报uuid的数据没有上报et字段'
                            panduan = 1
                            break
                    if panduan == 0:
                        message1 += 'et: Pass 上报uuid的数据都上报了et=pl'





    return  render_to_response('http.html',locals())
