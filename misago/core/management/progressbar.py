import time


def show_progress(command, step, total, since=None):
    progress = step * 100 / total
    filled = progress / 2
    blank = 50 - filled

    line = '\r%s%% [%s%s]'
    rendered_line = line % (str(progress).rjust(3), '=' * filled, ' ' * blank)

    if since:
        if step > 0:
            estimated_time = ((time.time() - since) / step) * (total - step)
            clock = time.strftime('%H:%M:%S', time.gmtime(estimated_time))
            rendered_line = '%s %s est.' % (rendered_line, clock)
        else:
            rendered_line = '%s --:--:-- est.' % rendered_line

    command.stdout.write(rendered_line, ending='')
    command.stdout.flush()
