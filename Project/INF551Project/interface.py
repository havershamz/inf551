import os
import re
import string
from collections import Counter
from pprint import pprint
import arrow

import boto3
import PyPDF2
import epub_meta
import ebooklib
from ebooklib import epub
import bs4
from nltk.corpus import stopwords

import firebase_admin
from firebase_admin import credentials
from bottle import route, run, request

from firebase import Firebase

cred = credentials.Certificate('./inf551-6b09f-firebase-adminsdk-w0uz8-e8bb4df6e9.json')
firebase_admin.initialize_app(cred)

s3 = boto3.client('s3',
                  aws_access_key_id="AKIAJEUD2E7XNUYVYXPQ",
                  aws_secret_access_key="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")


@route('/upload', method='POST')
def func():
    uploads = request.files.getall('file')
    for upload in uploads:
        _, ext = os.path.splitext(upload.filename)
        ext = ext.strip(".")
        path = os.path.join("/tmp", upload.filename)
        if os.path.exists(path):
            os.remove(path)

        upload.save("/tmp/")
        handle(path, ext.lower())
        filename = upload.filename
        bucket_name = 'inf551project2018'
        s3.upload_file(path, bucket_name, filename)

        os.remove(path)
    return render_template("test.html", arguments)
    return "Succeed"


class MetaData:

    def __init__(self):
        self.translate = {
            "Category": "category",
            "Create Date": "create",
            "Creator": "creators",
            "Authors": "creators",
            "File Modify Date": "modify",
            "Modify Date": "modify",
            "File Name": "name",
            "File Size": "size",
            "File Type": "type",
            "File Type Extension": "extension",
            "Language": "language",
            "Publisher": "publisher",
            "Title": "title",
            "Type": "type",
            "Page Count": "pages",
            "Producer": "publisher",
            "Key Words": "kwd",
            "Summary": "summary",
        }
        self.data = {}
        self.stopwords = stopwords.words('english') + list(string.punctuation)

    def extract(self, path):
        pass


class EPUBMetaData(MetaData):

    def __init__(self):
        super(EPUBMetaData, self).__init__()
        self.translate.update({
            "authors": "creators",
            "description": "description",
            "language": "language",
            "publisher": "publisher",
            "title": "title",
            "toc": "TOC",
            "file_size_in_bytes": "size",
            "epub_version": "version",
            "publication_date": "date"
        })

    def extract(self, path):

        book = epub.read_epub(path)
        for k, v in epub_meta.get_epub_metadata(path).items():
            if v is None:
                continue
            k = re.sub("[/.]", "-", k).strip()
            if isinstance(v, str):
                v = re.sub("[/.]", "-", v).strip()
            self.data[self.translate.get(k, k.lower())] = v

        documents = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        self.data["kwd"] = Counter()

        for document in documents:
            if not document.is_chapter():
                continue
            doc = document.get_body_content()
            soup = bs4.BeautifulSoup(doc, "lxml")
            words = [i for i in soup.text.lower().split(" ") if i not in self.stopwords and len(i) > 2]
            self.data["kwd"].update(Counter(words))

        self.data['create'] = arrow.now(tz='US/Pacific').format()
        self.data["chapters"] = len(self.data["TOC"])
        self.data['kwd'] = [re.sub("[/.]", "-", k).strip() for k, v in (self.data['kwd']).most_common(5)]
        self.data['language'] = 'en-US'

        return self.data


class PDFMetaData(MetaData):

    def __init__(self):
        super(PDFMetaData, self).__init__()
        self.translate.update({
            "CreationDate": "create",
            "ModDate": "modify",
            "PTEX.Fullbanner": "banner",
            "Trapped": "trapped"
        })

    def extract(self, path):
        pdf = PyPDF2.PdfFileReader(open(path, "rb"))

        for k, v in pdf.getDocumentInfo().items():
            k = re.sub("[/.]", "-", k).strip()
            if isinstance(v, str):
                v = re.sub("[/.]", "-", v).strip()
            self.data[self.translate[k]] = v

        self.data["pages"] = pdf.getNumPages()

        content = ""
        for page in range(self.data["pages"]):
            content += pdf.getPage(0).extractText()

        words = [i for i in content.split(" ") if i not in self.stopwords and len(i) > 2]

        self.data["kwd"] = list(set(re.sub("[/.]", "-", k).strip() for k, v in Counter(words).most_common(10)))
        self.data["title"] = re.sub("[/.]", "-", os.path.split(path)[-1]).strip()
        self.data['language'] = 'en-US'
        self.data["chapters"] = -1
        self.data['create'] = arrow.now(tz='US/Pacific').format()
        return self.data


class Extractor(object):
    def __init__(self):
        pass

    @staticmethod
    def extract(path, file_format=None):
        if file_format is None:
            file_format = os.path.split(path)[-1].split(".")[-1].lower()
        ans = None
        if file_format == "epub":
            ans = EPUBMetaData().extract(path)
        elif file_format == "pdf":
            ans = PDFMetaData().extract(path)
        return ans


def handle(local_name, extension):
    if os.path.exists(local_name):
        meta_data = Extractor.extract(local_name, extension)
        meta_data = {k: v for k, v in meta_data.items() if not isinstance(v, bytes)}
        meta_data["link"] = "https://s3-us-west-1.amazonaws.com/inf551project2018/{0}".format(local_name)

        if 'publisher' not in meta_data or meta_data.get('publisher') == "":
            meta_data['publisher'] = 'Unknown'
        if 'creators' not in meta_data or meta_data.get('creators', []) == []:
            meta_data['creators'] = ['Unknown']
        meta_data['creators'] = [c.replace(".", "_") for c in meta_data['creators']]

        firebase = Firebase("https://inf551-6b09f.firebaseio.com/", "WetOGYV7WIk2ZSuMp9RZ1UkzHhU9Js58iS5CTShk")
        previous = firebase.get(node="/epub")
        if previous:
            for book_id, book_value in previous.items():
                if book_value.get('title', "") == meta_data.get('title'):
                    print("Duplicate")
                    return

        response = firebase.post(node="/epub", data=meta_data)

        for kwd in meta_data.get("kwd", []):
            original_data = firebase.get(node="/keywords/" + kwd)
            if not original_data:
                original_data = []
            original_data.append(response)
            firebase.put(node="/keywords/" + kwd, data=original_data)
            # Authors
        for author in meta_data.get("creators", []):
            original_data = firebase.get(node="/authors/" + author)
            if not original_data:
                original_data = []
            original_data.append(response)
            firebase.put(node="/authors/" + author, data=original_data)
            # Language
        lan = meta_data.get("language", "en-US")
        original_data = firebase.get(node="/languages/" + lan)
        if not original_data:
            original_data = []
        original_data.append(response)
        firebase.put(node="/languages/" + lan, data=original_data)

        # Publisher
        pub = meta_data.get("publisher", "Unknown")
        original_data = firebase.get(node="/publishers/" + pub)
        if not original_data:
            original_data = []
        original_data.append(response)
        firebase.put(node="/publishers/" + pub, data=original_data)
        pprint(meta_data.keys())
        return


if __name__ == "__main__":

    run(host='0.0.0.0', port=8080)
