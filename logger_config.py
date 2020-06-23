#created by rayane866(rynpix)
import logging

def main(log_name:str, max_lines:int):
    global logger, log_list

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_list = []

    fh = logging.FileHandler(log_name)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    class ContextFilter(logging.Filter):
        def filter(self, record):
            with open(log_name, "r") as log:
                lines = log.readlines()
            with open(log_name, "w") as log:
                if len(lines) > (max_lines-1):
                    nls = record.msg.count("\n")
                    if nls != 0:
                        log.writelines(lines[len(lines)-(max_lines-1)+nls:])
                    else:        
                        log.writelines(lines[len(lines)-(max_lines-1):])
                else:
                    log.writelines(lines)
            
            log = {"level" : record.levelname, "msg" : record.msg}
            log_list.append(log)

            return True

    line_filer = ContextFilter()
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addFilter(line_filer)

