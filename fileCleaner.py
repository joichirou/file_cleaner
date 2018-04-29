# -*- coding: utf-8 -*-

import datetime
import filecmp
import logging
import os
import shutil
import time
import fileCleanerConfig as config


class FileCleaner(object):
    u"""不要なファイルを一か所にまとめる"""

    def __init__(self):
        self.sep = os.sep
        self.test_mode = False
        now = datetime.datetime.now()
        file_name = 'log%s%s.log' % (self.sep, now.strftime('%Y-%m-%d'))
        logging.basicConfig(filename=file_name, level=logging.DEBUG)
        self.save_dir = '%s%s' % (config.SAVE_DIR, now.strftime('%Y-%m-%d'))
        self.ignore_files = self._load_files(config.IGNORE_FILE)        
        self._create_save_dir(self.save_dir)

    def _create_save_dir(self, save_dir):
        u"""保存ディレクトリを作成する

        :param str save_dir: 保存ディレクトリの絶対パス 
        """
        try:
            if os.path.exists(save_dir):
                logging.info('save directory: %s' % save_dir)
                return
            os.mkdir(save_dir)
            logging.info('create save directory: %s' % save_dir)
        except:
            raise

    def execute(self):
        try:
            start_time = time.time()
            now = datetime.datetime.now()
            logging.info('%s ---start---' % now.strftime('%Y/%m/%d %H:%M:%S'))
            ignore_files = self._load_files(config.IGNORE_FILE)
            list_dirs = os.listdir(config.TARGET_DIR)
            logging.info('target lists: %s' % len(list_dirs))
            for list_dir in list_dirs:
                file_path = os.path.join(config.TARGET_DIR, list_dir)
                if os.path.isdir(file_path):
                    for file_name in os.listdir(file_path):
                        self._file_clean(list_dir , file_name)
                else:
                    self._file_clean('', list_dir)
            end_time = time.time()
            logging.info('execute time: (%.2fsec)' % (end_time - start_time))
            logging.info('%s ---end---' % now.strftime('%Y/%m/%d %H:%M:%S'))
        except Exception as e:
            logging.WARNING(e)
            print(e)
            raise

    def _load_files(self, file_name):
        u"""処理対象外ファイルを読み込む

        :param str file_name: ファイル名

        :return: 対象外ファイルリスト
        :rtype : list
        """
        try:
            ignore_files = []
            if not os.path.exists(file_name):
                return ignore_files
            file = open(file_name)
            ignore_files = file.readlines()
            file.close()
            return ignore_files
        except:
            raise

    def _is_ignore(self, chk_file, ignore_files):
        u"""対象外ファイル判定

        :param str  chk_file    : 判定対象ファイル 
        :param list ignore_files: 対象外ファイルリスト 
        """
        try:
            # To Do
            return False
        except:
            raise

    def _file_clean(self, dir_name, file_name):
        u"""ファイルを目的の場所に移動させる

        :param str dir_name  : ディレクトリ名
        :param str file_name : ファイル名 
        """
        try:
            copy_src_file = os.path.join(config.TARGET_DIR, dir_name, file_name)
            # check ignore lists
            if self._is_ignore(copy_src_file, self.ignore_files):
                logging.info('ignore file: %s' % file_name)
                return
            # copy
            copy_dest_file = os.path.join(self.save_dir, dir_name, file_name)
            if dir_name:
                copy_dest_dir = os.path.join(self.save_dir, dir_name)
                if not os.path.exists(copy_dest_dir):
                    os.mkdir(copy_dest_dir)
            shutil.copy2(copy_src_file, copy_dest_file)
            # check
            if not filecmp.cmp(copy_src_file, copy_dest_file):
                logging.info('find diff file: %s' % copy_src_file)
                return
            if self.test_mode:
                return
            # remove
            # ToDo
        except:
            raise

if __name__ == '__main__':
    from optparse import OptionParser
    option_parser = OptionParser()
    option_parser.add_option('--test',
                             dest='test_mode',
			     type='string',
                             help='test mode',
			     default=False)
    options, args = option_parser.parse_args()
    print('testMode=%s' % options.test_mode)
    file_cleaner = FileCleaner()
    file_cleaner.test_mode = options.test_mode
    file_cleaner.execute()
