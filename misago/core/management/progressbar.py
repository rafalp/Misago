import time


def show_progress(command, step, total, since=None):
    progress = step * 100 // total
    filled = progress // 2
    blank = 50 - filled

    template = "\r%(step)s (%(progress)s%%) [%(progressbar)s]%(estimation)s"
    variables = {
        "step": str(step).rjust(len(str(total))),
        "progress": str(progress).rjust(3),
        "progressbar": "".join(["=" * filled, " " * blank]),
        "estimation": get_estimation_str(since, progress, step, total),
    }

    command.stdout.write(template % variables, ending="")
    command.stdout.flush()


def get_estimation_str(since, progress, step, total):
    if not since:
        return ""

    progress_float = float(step) * 100.0 / float(total)
    if progress_float == 0:
        return " --:--:-- est."

    step_time = (time.time() - since) / progress_float
    estimated_time = (100 - progress) * step_time
    clock = time.strftime("%H:%M:%S", time.gmtime(estimated_time))
    return " %s est." % clock
