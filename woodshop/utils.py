import os
import sys
import glob
import json
import datetime
import shutil
import re
import glob
import subprocess

templateBaseDir = ''
baseProjectDir = ''
workspaceTemplateFile = ''

# udate this dictionary with artist folder locations for the createArtistFolder method
artistDirDict = {'CG Artists':'production/cg/rnd','Design Artists':'design/work'}

# update this dictionary with any sequence template folder names in the format of {'<tokenName>':'<template_dir_name>'}
templateDirDict = {'Design Artists':'designArtist_template','CG Artists':'cgArtist_template','cgSeq':'cg_seq_shot_template','compSeq':'comp_seq_shot_template','cgAsset':'cg_asset_template'}

if os.name == 'nt':
    templateBaseDir = '//buzzsaw.la.woodshop.tv/buzzsaw/WoodShop_Internal/Pipeline/templates'
    baseProjectDir = '//buzzsaw.la.woodshop.tv/buzzsaw/WoodShop_Projects'
    workspaceTemplateFile = '//buzzsaw.la.woodshop.tv/buzzsaw/WoodShop_Internal/Pipeline/templates/template_workspace.mel'
elif os.name == 'posix':
    templateBaseDir = '/buzzsaw/WoodShop_Internal/Pipeline/templates'
    baseProjectDir = '/buzzsaw/WoodShop_Projects'
    workspaceTemplateFile = '/buzzsaw/WoodShop_Internal/Pipeline/templates/template_workspace.mel'
else:
    templateBaseDir = '/Volumes/buzzsaw/WoodShop_Internal/Pipeline/templates'
    baseProjectDir = '/Volumes/buzzsaw/WoodShop_Projects'
    workspaceTemplateFile = '/Volumes/buzzsaw/WoodShop_Internal/Pipeline/templates/template_workspace.mel'

def returnJobDirNames():
    jobNameList = []
    for curDir in glob.glob(os.path.join(baseProjectDir, '*')):
        if os.path.basename(curDir)[2:4] == 'WS':
            jobNameList.append(os.path.basename(curDir))
    jobNameList.sort()
    return jobNameList

def makeShotNumList(shotNumText):
    shotNumPad = int(MainWindow.spinBox_shtNumPad.value())
    shotNumBy = int(MainWindow.spinBox_shtByNum.value())
    shotNumList = []
    if '-' in shotNumText:
        minShot = int(shotNumText.split('-')[0])
        maxShot = int(shotNumText.split('-')[1]) + 1
        for i in range(minShot, maxShot):
            curShotNum = str(i*shotNumBy).rjust(shotNumPad, '0')
            shotNumList.append(curShotNum)
    elif ',' in shotNumText:
        shotNumList = shotNumText.split(',')

    return shotNumList


def createArtistFolder(curProjectPath, artistNameList, artistType):

    for artistName in artistNameList:
        artistName = artistName.replace(' ','_')
        designArtistPath = os.path.join(curProjectPath, artistDirDict[artistType], artistName).replace('\\','/')
        if os.path.exists(designArtistPath):
            shutil.move(designArtistPath, '{}_{}'.format(designArtistPath, datetime.datetime.now().strftime('%Y%m%d%H%M%S')))

        designArtistTemplatePath = os.path.join(templateBaseDir, templateDirDict[artistType]).replace('\\','/')
        for dirName, subdirList, fileList in os.walk(designArtistTemplatePath, topdown=False):
            newAristDir = dirName.replace(designArtistTemplatePath, designArtistPath).replace('\\','/')
            if os.path.exists(newAristDir):
                pass
            else:
                os.makedirs(newAristDir)
            if newAristDir[-5:] == '/maya':
                writeWorkspaceFile(curProjectPath, newAristDir)

    msgBox = QtGui.QMessageBox()
    msgBox.setText("          Success!          ")
    msgBox.exec_()
    

def createShotFolders(templateType, seqPath, seqPrefix, shotNumList, curProjectPath):
    ''' createShotFolder - create the folders in 'cg' under each shot numbered folder
        for a given sequence
    '''
    shotTemplateBaseDir = ''
    shotTempDirList = []
    if templateType in templateDirDict.keys():
        shotTemplateBaseDir = os.path.join(templateBaseDir, templateDirDict[templateType]).replace('\\','/')
    else:
        return

    for curShotNum in shotNumList:
        curShotPath = os.path.join(seqPath, '{}_{}'.format(seqPrefix, curShotNum)).replace('\\','/')
        if os.path.exists(curShotPath):
            shutil.move(curShotPath, '{}_{}'.format(curShotPath, datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        else:
            os.makedirs(curShotPath)
        for dirName, subdirList, fileList in os.walk(shotTemplateBaseDir, topdown=False):
            curShotTempDir = dirName.replace(shotTemplateBaseDir, curShotPath).replace('\\','/')
            if os.path.exists(curShotTempDir):
                pass
            else:
                os.makedirs(curShotTempDir)
            if fileList:
                for curFile in fileList:
                    shutil.copy2(os.path.join(dirName, curFile), os.path.join(curShotTempDir, curFile))
            if curShotTempDir[-5:] == '/maya':
                writeWorkspaceFile(curProjectPath, curShotTempDir)


def createSeqFolder(seqPrefix, shotNumList,curProjectPath):
    ''' createSeqFolder - create a sequence folder with seqPrefix as the name, then
        create a shot folder for each shot in shotNumList
    '''
    seqDirList = []
    for dirName, subdirList, fileList in os.walk(curProjectPath, topdown=False):
        if dirName.replace('\\','/')[-4:] == '/seq':
            seqDirList.append(dirName.replace('\\','/'))
    if seqDirList:
        for curSeqDir in seqDirList:
            if '/cg/' in curSeqDir:
                curSeqPath = os.path.join(curSeqDir, seqPrefix).replace('\\','/')
                createShotFolders('cgSeq', curSeqPath, seqPrefix, shotNumList, curProjectPath)
            elif '/comp/' in curSeqDir:
                curSeqPath = os.path.join(curSeqDir, seqPrefix).replace('\\','/')
                createShotFolders('compSeq', curSeqPath, seqPrefix, shotNumList, curProjectPath)
            else:
                curSeqPath = os.path.join(curSeqDir, seqPrefix).replace('\\','/')
                createShotFolders('none', curSeqPath, seqPrefix, shotNumList, curProjectPath)

    msgBox = QtGui.QMessageBox()
    msgBox.setText("          Success!          ")
    msgBox.exec_()
    

def createProjectFolder(projectNum, projectName, seqPrefix='', shotNumList=[]):
    ''' createProjectFolder - creates the project folder tree based on the template
        in the templateBaseDir
    '''
    seqDirList = []
    # create project dir list
    curProjectPath = os.path.join(baseProjectDir, '{}_{}'.format(projectNum, projectName)).replace('\\','/')
    if os.path.exists(curProjectPath):
        pass
    else:
        os.makedirs(curProjectPath)
    projTemplateBaseDir = os.path.join(templateBaseDir, 'project_template').replace('\\','/')
    for dirName, subdirList, fileList in os.walk(projTemplateBaseDir, topdown=False):
        newProjDir = dirName.replace(projTemplateBaseDir, curProjectPath).replace('\\','/')
        if newProjDir[-4:] == '/seq':
            seqDirList.append(newProjDir)
        if os.path.exists(newProjDir):
            pass
        else:
            os.makedirs(newProjDir)
        if fileList:
            for curFile in fileList:
                shutil.copy2(os.path.join(dirName, curFile), os.path.join(newProjDir, curFile))

    msgBox = QtGui.QMessageBox()
    msgBox.setText("          Success!          ")
    msgBox.exec_()
    newJobListItem = QtGui.QListWidgetItem('{}_{}'.format(projectNum, projectName))
    MainWindow.curJobList.addItem(newJobListItem)
    MainWindow.curJobList.setCurrentItem(newJobListItem)
    

    return 1

def writeWorkspaceFile(projectBaseDir, wsOutfilePath):
    workspaceDict = {
        'WS_SOURCEIMAGES':'production/cg/assets/sourceimages'
    }

    if os.path.exists(workspaceTemplateFile):
        tempWSfile = open(workspaceTemplateFile, 'r+')
        wsSource = tempWSfile.read()
        for curPattern in workspaceDict.keys():
            rePattern = re.compile(curPattern)
            replaceString = os.path.join(projectBaseDir, workspaceDict[curPattern]).replace('\\','/')
            wsSource = rePattern.sub(replaceString, wsSource)
            newWSfile = open(os.path.join(wsOutfilePath, 'workspace.mel'), 'w')
            newWSfile.write(wsSource)
            newWSfile.close()


def createProject():
    jobNum = MainWindow.jobNumTxt.text()
    jobName = MainWindow.jobNameTxt.text()
    createProjectFolder(jobNum, jobName)

def createShots():
    if MainWindow.curJobList.selectedItems():
        curSelectedJob = MainWindow.curJobList.selectedItems()[0].text()
        curProjectPath = os.path.join(baseProjectDir, curSelectedJob).replace('\\','/')
        seqPrefix = MainWindow.le_seqPrefix.text()
        shotNumTxt = MainWindow.le_shotNumList.text()
        shotNumList = makeShotNumList(shotNumTxt)
        createSeqFolder(seqPrefix, shotNumList, curProjectPath)

def createArtistFoldersBtn():
    artistType = MainWindow.artistTypeCombo.currentText()
    if MainWindow.curJobList.selectedItems():
        curSelectedJob = MainWindow.curJobList.selectedItems()[0].text()
        curProjectPath = os.path.join(baseProjectDir, curSelectedJob).replace('\\','/')
        artistNameList = []
        if MainWindow.artistList.selectedItems():
            for curArtistItem in MainWindow.artistList.selectedItems():
                artistNameList.append(curArtistItem.text())

        createArtistFolder(curProjectPath, artistNameList, artistType)
