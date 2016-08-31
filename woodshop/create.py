from django.db import models
from lumberyard.models import Jobs, Sequence, Renders, Tasks
import random
import glob
import os
import datetime

def date_plus_30():
    thisValue = datetime.date.today()+datetime.timedelta(days=30)
    return thisValue

def createDBJobs(curJobNum, curJobName):
    curJob = Jobs(
        job_num=curJobNum,
        job_name=curJobName,
        producer_id = 3,
        delivery_specs_id = 1,
        lead_3D_id = 4,
        lead_2D_id = 4,
    )

    curJob.save()

    return [curJob.job_num, curJob.job_name]

def createDBSeq(CurSeqName, curJobPk, curSeqList):
    taskPKList = [curTask.pk for curTask in Tasks.objects.all()]
    for curSeqNum in curSeqList:
        randNumTasks = random.randint(1,3)
        tasksList = [random.choice(taskPKList) for cur in range(randNumTasks)]
        curSeq = Sequence(
            job = curJobPk,
            Sequence_name = CurSeqName,
            sequence_num = curSeqNum,
            sequence_length = random.randint(27,253),
            tasks = tasksList,
            notes = "fantastic work, as always"
        )

def getSeqNumbers():
    seqDict = {}
    for curProject in glob.glob(os.path.join('/','buzzsaw','WoodShop_Projects','*')):
        if os.path.isdir(curProject):
            if glob.glob(os.path.join(curProject, 'production', 'cg','seq', '*')):
                curProjectNum = os.path.basename(curProject)[:7]
                if Jobs.objects.filter(job_num = curProjectNum):
                    print curProjectNum
                    curProjectObj = Jobs.objects.filter(job_num = curProjectNum)[0]
                for curSeqNamePath in glob.glob(os.path.join(curProject, 'production', 'cg','seq', '*')):
                    curSeqName = os.path.basename(curSeqNamePath)
                    print curSeqName
                    if glob.glob(os.path.join(curSeqNamePath, '*')):
                        print '\t', curSeqNamePath
                        for curSeqNumPath in glob.glob(os.path.join(curSeqNamePath, '*')):
                            if os.path.basename(curSeqNumPath).split('_')[1]:
                                curSeqNum = os.path.basename(curSeqNumPath).split('_')[1]    
                                print '\t\t', curSeqNum
                                if Sequence.objects.filter(job=curProjectObj, sequence_name = curSeqName, sequence_num = curSeqNum):
                                    print '*** exists ***'
                                    pass
                                else:
                                    print '\t\t\t*** new ****'
                                    newSeq = Sequence(
                                        job=curProjectObj,
                                        sequence_name = curSeqName,
                                        sequence_num = curSeqNum,
                                        sequence_length=128, 
                                        due_date = date_plus_30(), 
                                    )
                                    newSeq.save()
            """
            if glob.glob(os.path.join(curProject, 'production', 'comp','seq', '*')):
                for curSeqNamePath in glob.glob(os.path.join(curProject, 'production', 'comp','seq', '*')):
                    print curProject
                    print os.path.basename(curSeqNamePath)
                    for curSeqNumPath in glob.glob(os.path.join(curSeqNamePath, '*')):
                        if os.path.basename(curSeqNumPath).split('_')[1]:
                            print '\t', os.path.basename(curSeqNumPath).split('_')[1]
                        else:
                            print 'DAMN'
            """