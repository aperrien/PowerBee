from DBInterface import fetchSubmissionComments, fetchSubmissionData
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def front():
    return 'Front Page'

@app.route('/submissionTest/<submissionID>')
def getTestSubmission(submissionID):
    st = fetchSubmissionComments(submissionID)
    return st

@app.route('/submission/<submissionID>')
def getSubmission(submissionID):
    subdata = fetchSubmissionData(submissionID)
    template = render_template('SubmissionViewerTemplate.html', subdata=subdata)
    return template
