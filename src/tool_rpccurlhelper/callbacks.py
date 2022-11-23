from pywebio import output

@output.use_scope('app')
def what( cmd: str):
    output.put_text("what: {}".format(cmd))
