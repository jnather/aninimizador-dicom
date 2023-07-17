import os
import pydicom
from pydicom import dcmread, dcmwrite
from pydicom.dataelem import DataElement

def anonymize_dicom_file(filename, output_dir):
    # load the dicom file
    ds = dcmread(filename)

    # list of tags from patient and general study module attributes which are responsible for privacy
    tags_to_anonymize = ['PatientName', 'PatientID', 'PatientBirthDate', 'PatientSex', 
                         'PatientAge', 'OtherPatientIDs', 'OtherPatientNames', 
                         'IssuerOfPatientID', 'PatientMotherBirthName',
                         'MedicalRecordLocator', 'ReferencedPatientPhotoSequence',
                         'PatientTelephoneNumbers', 'PatientAddress',
                         'StudyID', 'AccessionNumber', 'OtherStudyNumbers']

    for tag in tags_to_anonymize:
        if tag in ds:
            ds.data_element(tag).value = ''

    # retrieve SOPInstanceUID and set as new filename
    new_filename = ds.SOPInstanceUID + ".dcm"
    new_filepath = os.path.join(output_dir, new_filename)

    # save the anonymized dicom file in output directory
    dcmwrite(new_filepath, ds)

def find_and_anonymize_dcm_files(root_dir, output_dir):
    dicom_subfolders = []
    
    for dirName, subdirList, fileList in os.walk(root_dir):
        dicom_files = [file for file in fileList if ".dcm" in file.lower()]
        if len(dicom_files) > 1:
            dicom_subfolders.append(dirName)
        #else:
            for filename in dicom_files:
                print('Found DICOM file: ', os.path.join(dirName, filename))
                anonymize_dicom_file(os.path.join(dirName, filename), output_dir)

    print("Subfolders with more than one DICOM file:")
    for folder in dicom_subfolders:
        print(folder)

root_dir = 'in_folder/' # specify your path here
output_dir = 'out_folder/' # specify your path here

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

find_and_anonymize_dcm_files(root_dir, output_dir)
