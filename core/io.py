"""Global IO variables."""

output_buf = ''

input_buf = ''

args = []

def clean():
    """Resets all IO buffers."""

    global output_buf, input_buf, args
    output_buf = ''
    input_buf = ''
    args = []