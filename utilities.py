# function that extracts the txt file data
def extract_data(file_name):
    f = open('test-files/{}.txt'.format(file_name), 'r')
    return f.read()
