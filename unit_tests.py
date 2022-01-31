########################################
# Unit Tests
########################################

def check_admission_id(request):
    # ensure that 'admission_id' and 'patient_id' is included in the request
    if "admission_id" not in request:
        request.update({"admission_id": None})
        error = "Field `admission_id` missing from request: {}".format(request)
        return False, error
    if type(request["admission_id"]) != int:
        error = "Field `admission_id` must be of type int and cannot be empty: {}".format(request)
        return False, error
    if "patient_id" not in request:
        request.update({"patient_id": None})
        error = "Field `patient_id` missing from request: {}".format(request)
        return False, error
    if type(request["patient_id"]) != int:
        error = "Field `patient_id` must be of type int and cannot be empty: {}".format(request)
        return False, error
    return True, ""

def check_valid_column(observation):
    #Validates that our observation has all the required columns
    valid_columns = {'patient_id', 'race', 'gender', 'age', 'weight', 'admission_type_code', 'discharge_disposition_code', 
                     'admission_source_code', 'time_in_hospital', 'payer_code', 'medical_specialty',
                     'has_prosthesis', 'complete_vaccination_status', 'num_lab_procedures', 'num_procedures', 'num_medications',
                     'number_outpatient', 'number_emergency', 'number_inpatient', 'diag_1', 'diag_2', 'diag_3', 'number_diagnoses', 
                     'blood_type', 'hemoglobin_level', 'blood_transfusion', 'max_glu_serum', 'A1Cresult', 'diuretics', 'insulin',
                     'change', 'diabetesMed'}
    
    keys = set(observation.keys())
    
    if len(valid_columns - keys) > 0: 
        missing = valid_columns - keys
        error = "Please include the following columns in your request (even if they are empty): {}".format(missing)
        return False, error
    return True, ""

# Categorical

def check_categorical_data(observation):
    # validate that fields expected to be string are string
    # the pipeline handles unknown values as a separate category (either unknown or none)
    string_columns = ['race', 'gender', 'age', 'weight', 'payer_code', 'medical_specialty',
                     'complete_vaccination_status', 'diag_1', 'diag_2', 'diag_3', 
                     'blood_type', 'max_glu_serum', 'A1Cresult', 'diuretics', 'insulin',
                     'change', 'diabetesMed']
    invalid_column_list = []
    for column in string_columns:
        if observation[column]:
            if type(observation[column]) != str:
                invalid_column_list.append(column)
    if len(invalid_column_list) > 0:
        error = "The following column values should be in string format (include an empty string for missing data): {}".format(invalid_column_list)
        return False, error   

    return True, ""

# Boolean
def check_boolean_data(observation):
    # checks to make sure boolean data is present
    # pipeline handles unknown values
    boolean_columns = ['has_prosthesis', 'blood_transfusion']
    invalid_column_list = []
    for column in boolean_columns:
        if observation[column]:
            if type(observation[column]) != bool:
                invalid_column_list.append(column)
    if len(invalid_column_list) > 0:
        error = "The following column values should be in boolean format (): {}".format(invalid_column_list)
        return False, error
 
    return True, ""

# Numerical
def check_numerical_data(observation):
    # checks numerical columns for validity
    # does not handle the numerical categories here (just confirms if digits)
    num_columns = ['admission_source_code', 'time_in_hospital', 'num_procedures', 'num_medications',
                    'number_outpatient', 'number_emergency', 'number_inpatient', 'number_diagnoses',
                    'admission_type_code', 'discharge_disposition_code', 'num_lab_procedures', 'hemoglobin_level']
    
    invalid_column_list = []
    for column in num_columns:
        if observation[column]:  
            try:
                float(observation[column])
            except:
                invalid_column_list.append(column)
    if len(invalid_column_list) > 0:
        error = "The following column values should be numerical: {}".format(invalid_column_list)
        return False, error
 
    return True, ""

def check_num_cat_data(observation):
    # checks numerical columns for validity
    # does not handle the numerical categories here (just confirms if digits)
    if observation['admission_type_code']:
        if observation['admission_type_code'] not in list(range(1, 9)):
            error = "admission_type_code invalid, should be one of: {}, or left empty if unknown".format(list(range(1, 9)))
            return False, error
 
    if observation['admission_source_code']:
        if observation['admission_source_code'] not in list(range(1, 27)):
            error = "admission_source_code invalid, should be one of: {}, or left empty if unknown".format(list(range(1, 27)))
            return False, error

    if observation['discharge_disposition_code']:
        if observation['discharge_disposition_code'] not in list(range(1, 30)):
            error = "discharge_disposition_code invalid, should be one of: {}, or left empty if unknown".format(list(range(1, 30)))
            return False, error

    return True, ""

########################################
# End Unit Tests
########################################
