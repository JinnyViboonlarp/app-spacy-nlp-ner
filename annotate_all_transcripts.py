import os
import sys

from mmif.serialize import Mmif, Annotation
from mmif.vocabulary import AnnotationTypes, DocumentTypes
from lapps.discriminators import Uri

def create_input_mmif_files(uncased_choice = False):

    def create_mmif_str(infile):
        mmif = Mmif(validate=False)
        view = mmif.new_view()
        view.new_contain(DocumentTypes.TextDocument)
        ann = view.new_annotation(DocumentTypes.TextDocument, 'td1')
        with open(infile, 'r') as fh_in:
            text = fh_in.read()
        ann.properties["text"] = {"@value": text} # can't use add_property module since a dict-type property is not allowed.
        mmif_str = mmif.serialize(pretty=True)
        return mmif_str
    
    if(uncased_choice):
        text_dir = 'transcripts-uncased'
        out_dir = 'input-mmif-uncased'
    else:
        text_dir = 'transcripts'
        out_dir = 'input-mmif'
    for text_name in os.listdir(text_dir):
        if(text_name.endswith(".txt")):
            infile = text_dir + '/' + text_name
            outfile = out_dir + '/' + (os.path.splitext(text_name))[0] + '.json'
            mmif_str = create_mmif_str(infile)
            with open(outfile, 'w') as fh_out:
                fh_out.write(mmif_str)

def annotate_input_mmif_files_without_docker(uncased_choice = False):
    # this module is used to test the clams app on all transcripts, without Docker  
    if(uncased_choice):
        in_dir = 'input-mmif-uncased'
        out_dir = 'output-mmif-uncased'
    else:
        in_dir = 'input-mmif'
        out_dir = 'output-mmif'
    for mmif_name in os.listdir(in_dir):
        if(mmif_name.endswith(".json")):
            in_path = in_dir + '/' + mmif_name
            out_path = out_dir + '/' + mmif_name
            if(uncased_choice):
                os.system("python app.py -t -u --dep "+in_path+" "+out_path)
            else:
                os.system("python app.py -t --dep "+in_path+" "+out_path)

def annotate_input_mmif_files(uncased_choice = False):
    # this module is used to test the clams app on all transcripts, with Docker
    # the docker container must first be running
    # The commands are "docker build -t clams-spacy-nlp -f Dockerfile-cased ." (or Dockerfile-uncased if truecase option) \
    # and then "docker run --rm -d -p 5000:5000 clams-spacy-nlp"
    if(uncased_choice):
        in_dir = 'input-mmif-uncased'
        out_dir = 'output-mmif-uncased'
    else:
        in_dir = 'input-mmif'
        out_dir = 'output-mmif'  
    for mmif_name in os.listdir(in_dir):
        if(mmif_name.endswith(".json")):
            in_path = in_dir + '/' + mmif_name
            out_path = out_dir + '/' + mmif_name
            os.system('curl -H "Accept: application/json" -X POST -d@' + in_path + ' http://0.0.0.0:5000/?pretty=True -o ' + out_path)

def create_uncased_transcripts():
    in_dir = 'transcripts'
    out_dir = 'transcripts-uncased'
    for name in os.listdir(in_dir):
        if(name.endswith(".txt")):
            in_path = in_dir + '/' + name
            out_path = out_dir + '/' + name
            infile = open(in_path, 'r')
            text = infile.read()
            infile.close()
            text = text.lower()
            outfile = open(out_path, 'w')
            outfile.write(text)
            outfile.close()

if __name__ == "__main__":

    #create_uncased_transcripts()
    #create_input_mmif_files(uncased_choice = True)
    #annotate_input_mmif_files_without_docker()
    annotate_input_mmif_files(uncased_choice = True)
