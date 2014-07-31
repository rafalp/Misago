def show_progress(command, step, total):
    progress = step * 100 / total
    filled = progress / 2
    blank = 50 - filled

    line = '\r%s%% [%s%s]'
    rendered_line = line % (str(progress).rjust(3), '=' * filled, ' ' * blank)
    command.stdout.write(rendered_line, ending='')
    command.stdout.flush()
