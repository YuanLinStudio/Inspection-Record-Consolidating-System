import os
import shutil

import pandas


class AttachmentMatch:

    dataFrame = []
    fileList = list()
    hashDict = dict()
    archivedPath = ''
    dir = ''

    def __init__(self):

        pass

    def operate(self, dataFrame, dir):

        self.dataFrame = dataFrame
        self.dir = dir

        # 将 dataFrame 按原始记录编号从大到小排列
        self.dataFrame = self.dataFrame.sort_values(
            by=['原始记录编号'], ascending=[False])

        self.fileList = self.getFileList(dir)

        self.makeHashDict()

        self.matchOriginalRecord()

        self.archive()

        # 将 dataFrame 恢复顺序，按序号从大到小排列
        self.dataFrame = self.dataFrame.sort_values(
            by=['序号'], ascending=[True])

        return self.dataFrame

    def getHashDict(self):

        return self.hashDict

    def getFileList(self, dir) -> list:

        fileList = list()

        for root, dirs, files in os.walk(dir):

            if files is not None:

                for file in files:

                    fileList.append(root + '\\' + file)

        return fileList

    def makeHashDict(self):

        for fileDir in self.fileList:

            hash = fileDir.split('_')[-1].split('.')[0]

            dirDict = dict()
            dirDict['dir'] = fileDir
            dirDict['filename'] = fileDir.split('\\')[-1]
            dirDict['ext'] = fileDir.split('.')[-1]

            if dirDict['ext'] in ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG',
                                  'bmp', 'BMP', 'tif', 'TIF', 'tiff', 'TIFF']:

                dirDict['filetype'] = '图'

            elif dirDict['ext'] in ['gif', 'GIF', 'mp4', 'MP4', 'mov', 'MOV']:

                dirDict['filetype'] = '视频'

            else:

                dirDict['filetype'] = '附件'

            self.hashDict[hash] = dirDict

    def matchOriginalRecord(self):

        # 仅筛选有附件的记录
        validDataFrame = self.dataFrame[self.dataFrame['附件个数'] > 0]

        validDataFrame.apply(lambda dataFrame: self.__matchOriginalRecord(
            dataFrame['附件 1'], dataFrame['原始记录编号'], 1), axis=1)

        validDataFrame.apply(lambda dataFrame: self.__matchOriginalRecord(
            dataFrame['附件 2'], dataFrame['原始记录编号'], 2), axis=1)

    def __matchOriginalRecord(self, fileName, originalRecord, attachmentSlot):

        if fileName is None:
            return

        if fileName == '':
            return

        hash = fileName.split('_')[-1].split('.')[0]

        hashItem = self.hashDict.get(hash)

        if hashItem is not None:

            originalRecordDict = {'No': originalRecord, 'Slot': attachmentSlot}

            # 添加到第一个原始记录列表
            hashItem['originalRecord'] = originalRecordDict

            # 添加到全部原始记录列表
            record = hashItem.get('allRecords')

            if record is not None:
                hashItem['allRecords'].append(originalRecordDict)

            else:
                hashItem['allRecords'] = [originalRecordDict]

    def archive(self):

        self.dataFrame['附件'] = ''

        # 新建目录
        self.archivedPath = self.dir + '\\已匹配附件\\'

        if not os.path.exists(self.archivedPath):

            os.makedirs(self.archivedPath)

        for hash, item in self.hashDict.items():

            originalRecord = item.get('originalRecord')

            if originalRecord is None:
                continue

            record = self.dataFrame[self.dataFrame['原始记录编号']
                                    == originalRecord['No']]

            # 复制一份到指定目录
            originalFile = item['dir']
            archivedFile = self.archivedPath + \
                item.get('filetype') + str('%d' %
                                           record['序号']) + '.' + item['ext']

            if originalRecord['Slot'] == 1:

                # 更新 dataFrame 附件信息
                self.dataFrame.loc[self.dataFrame['原始记录编号'] == originalRecord['No'],
                                '附件'] = archivedFile.split('\\')[-1].split('.')[0]

            else:

                archivedFile = self.archivedPath + \
                    item.get('filetype') + str('%d' %
                                               record['序号']) + ' (2).' + item['ext']

                '''
                # 更新 dataFrame 附件信息
                self.dataFrame.loc[self.dataFrame['原始记录编号'] == originalRecord['No'],
                                   '附件'] = ','.join([self.dataFrame.loc[self.dataFrame['原始记录编号'] == originalRecord['No'],
                                                                        '附件'].to_string(header=False, index=False), archivedFile.split('\\')[-1].split('.')[0]])
                '''

            # 若存在同名文件
            if os.path.isfile(archivedFile):
                
                print('%s 已被覆盖' % archivedFile)

            # 复制文件
            shutil.copyfile(originalFile, archivedFile)

            # 更新 Json 文件
            self.hashDict[hash]['archivedDir'] = archivedFile
            self.hashDict[hash]['archivedFilename'] = archivedFile.split(
                '\\')[-1]


if __name__ == '__main__':

    am = AttachmentMatch()

    ls = am.getFileList(
        r'C:\Users\yuanl\Downloads\腾讯问卷\问卷#4165188 - 西安地铁服务监督员检查记录提交系统')
    am.makeHashDict()
