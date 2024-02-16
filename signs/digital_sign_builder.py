import requests
import os
import time
import difflib

json_url = "https://library.iit.edu/api/v1/slides_rest"
hours_url = "https://iit.libcal.com/api_hours_today.php?iid=5544&lid=0&format=json&systemTime=0"
template_filepath = "template.html"
cta_flag = True

def dru_slides_builder(json_url):
    slides_call = requests.get(json_url)
    if slides_call.status_code == 200:
        web_slides_dict = slides_call.json()

    slides_list = []
    slides = ''

    for i in web_slides_dict:
        image_url = i["field_image"]
        title = i['title_1']
        if image_url != '':
            section = f'<section data-background-image={image_url} data-background-size="contain, 100%"></section>'
            slides_list.append(section)

    for i in slides_list:
        slides += ("\t\t\t\t\t\t" + i + "\n")

    slides = "<div class=\"slides\">\n" + slides[:-1]

    return slides

def build_slides_html(template_filepath, slides, hours_url, cta_flag):

    hours_call = requests.get(hours_url)
    if hours_call.status_code == 200:
        hours_dict = hours_call.json()

    with open(template_filepath, 'r') as template:
        slides_html = template.read()

    content = "<div class=\"slides\">"

    hours_div = '<div id="todays_hours">'
    hours_statement = '''<div id=\"todays_hours\">
                <p>{todays_hours}</p>
                '''

    if hours_dict['locations'][0]['times']['status'] == '24hours':
        todays_hours = "Today's Library Hours: 24 Hours"

    else:
        openfrom = hours_dict['locations'][0]['times']['hours'][0]['from']
        opento = hours_dict['locations'][0]['times']['hours'][0]['to']
        todays_hours = "Today's Library Hours: {openfrom} - {opento}"
        todays_hours = todays_hours.format(openfrom=openfrom, opento=opento)

    hours_statement = hours_statement.format(todays_hours=todays_hours)

    slides_html = slides_html.replace(content, slides)

    if cta_flag == False:
        sidebar_right = "<div id=\"sidebar-right\">"
        sidebar_right_hidden = "<div id=\"sidebar-right\" class=\"hidden\">"
        slides_html = slides_html.replace(sidebar_right, sidebar_right_hidden)

    slides_html = slides_html.replace(hours_div, hours_statement)

    return slides_html


def cleanup():
    age = 3
    current_time = time.time()
    day = 86400
    files = os.listdir()
    oldfiles = []

    for i in files:

        if i.endswith(".old"):
            oldfiles.append(i)
            oldfiles.sort()

    for j in oldfiles[:-1]:
        file_path = os.path.join(os.getcwd(), j)
        file_time = os.stat(file_path).st_mtime
        print(file_path, file_time)

        if (file_time < current_time - day * age):
            print(f" Delete : {file_path}")
            os.remove(file_path)

def filediff(old_path, new_path):
    with open(old_path, 'r') as old_file, open(new_path) as new_file:
        old_contents = old_file.readlines()
        new_contents = new_file.readlines()

    is_different = difflib.Differ()
    diff = list(is_different.compare(old_contents, new_contents))

    if diff:
        return True

    else:
        return False

root_dir = '/var/www/html/new_signs/'
file_ext = '.html'
old_filename = 'index'
old_path = root_dir + old_filename + file_ext
new_path = old_path + '.temp'
compare = False

with open(old_path, 'r') as old_file:
    slides = dru_slides_builder(json_url)
    content = build_slides_html(template_filepath, slides, hours_url, cta_flag)

    if old_file.read() != content:
        compare = True

if compare == True:
    with open(new_path, 'w') as file:
        file.write(content)
    current_time = time.strftime("%d-%H-%M")
    os.rename(old_path, old_path + current_time + '.old')
    os.rename(new_path, old_path)

clean_dir = cleanup()
