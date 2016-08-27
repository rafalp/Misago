import time


def show_progress(command, step, total, since=None):
    progress = step * 100 // total
    filled = progress // 2
    blank = 50 - filled

    line = '\r%s%% [%s%s]'
    rendered_line = line % (str(progress).rjust(3), '=' * filled, ' ' * blank)

    if since:
        progress_float = float(step) * 100.0 / float(total)
        if progress_float > 0:
            step_time = (time.time() - since) / progress_float
            estimated_time = (100 - progress) * step_time
            clock = time.strftime('%H:%M:%S', time.gmtime(estimated_time))
            rendered_line = '%s %s est.' % (rendered_line, clock)
        else:
            rendered_line = '%s --:--:-- est.' % rendered_line

    command.stdout.write(rendered_line, ending='')
    command.stdout.flush()
