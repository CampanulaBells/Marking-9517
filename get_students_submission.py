# A small tool to make making easier
# 20/06/2020
# Written by CampanulaBells, https://github.com/CampanulaBells/
import pandas as pd
import numpy as np
import os
import shutil
import sys
import zipfile
import tarfile

class Config:
    defalt_path = './lab1'
    debug = False

def extract_students_submissions_single_zip(path = './', studentIDs = None):
    if path[-1] != '/':
        path = path + '/'
    file_list = os.listdir(path)
    # Traverse zip files (which downloaded from OneDrive) under current directory.
    students_found = []
    for file_name in file_list:
        if len(file_name.split('.')) != 1:
            continue
        student_id = file_name
        student_path = path + student_id
        if student_id not in studentIDs:
            # Remove folder
            shutil.rmtree(student_path)
            continue
        students_found.append(student_id)
        # Extract submission.tar
        try:
            submission_tar_path = path +  student_id + '/submission.tar'
            submission_tar = tarfile.open(submission_tar_path)
            task_names = submission_tar.getnames()
            submission_tar.extractall(path + student_id)
            # Extract student's submission
            for task_name in task_names:
                task_path = student_path + '/' + task_name
                student_zip = zipfile.ZipFile(task_path)
                student_zip.extractall(student_path)
                # Delete task.zip
                student_zip.close()
                os.remove(task_path)
            # Finshed. Close submission.tar
            submission_tar.close()
            # Delete submission.tar
            os.remove(submission_tar_path)
            if Config.debug:
                break
        except:
            pass
    print('submission not found:')
    for student in studentIDs:
        if student not in students_found:
            print(student)


def get_studentIDs(filename = './my_student.csv', splitter = '\t'):
    students_file = pd.read_csv(filename, splitter)
    students_id = [x[1:] for x in students_file['Student ID']]
    return students_id

if __name__ == '__main__':
    argv = sys.argv
    path = Config.defalt_path
    print(argv)

    if len(argv) < 2:
        print("usage: python getsub.py [student id] [path]")
        exit(1)
    studentID_file = argv[1]
    if len(argv) == 2:
        print('Extract students\'s files from default path: \'{}\''.format(Config.defalt_path))
    else:
        print('Extract students\'s files from ' + '\'{}\''.format(argv[2]))
        path = argv[2]
    print('Extracting...')
    id_list = get_studentIDs(studentID_file)
    extract_students_submissions_single_zip(path, id_list)
    print('Done! ')
