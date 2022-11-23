from pywebio import output

def what( cmd: str):
    output.put_text("what: {}".format(cmd))
