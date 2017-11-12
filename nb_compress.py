import json
import re
import argparse


def compress_output(output, mode):
    if "text" in output and mode['first_last_epoch']:
        text = output["text"]
        mask = False
        _text = []
        for line in text:
            m = re.search('^Epoch (\d+)/(\d+)', line)
            if m:
                total = m.group(2)
                cur = m.group(1)
                if cur == "2":
                    mask = True
                elif cur == total:
                    mask = False
            if not mask:
                _text.append(line)
        output["text"] = _text

    if "traceback" in output and mode['no_traceback']:
        output["traceback"] = []

    if "data" in output and mode['no_image']:
        output_data = output["data"]
        if "image/png" in output_data:
            output_data["image/png"] = ""

    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='input ipython notebook file')
    parser.add_argument('-o', '--output', type=str, required=True, help='output filename')
    parser.add_argument('--first-last-epoch', action='store_true')
    parser.add_argument('--no-image', action='store_true')
    parser.add_argument('--no-traceback', action='store_true')
    parser.add_argument('--no-execution-count', action='store_true')
    args = parser.parse_args()

    mode = {}
    mode['first_last_epoch'] = args.first_last_epoch
    mode['no_image'] = args.no_image
    mode['no_traceback'] = args.no_traceback
    mode['no_execution_count'] = args.no_execution_count

    if mode['first_last_epoch']:
        print('Apply filter: first_last_epoch')
    if mode['no_image']:
        print('Apply filter: no_image')
    if mode['no_traceback']:
        print('Apply filter: no_tracekback')
    if mode['no_execution_count']:
        print('Apply filter: no_execution_count')

    with open(args.file) as f:
        data = json.load(f)

    cells = []
    for cell in data["cells"]:
        if cell["cell_type"] == "code":
            outputs = cell["outputs"]
            if len(outputs) > 0:
                cell["outputs"] = [compress_output(o, mode) for o in outputs]
            if mode['no_execution_count']:
                cell["execution_count"] = None

        cells.append(cell)
    data["cells"] = cells

    if args.output:
        with open(args.output, "w") as f:
            jsonStr = json.dumps(data)
            f.write(jsonStr)
            print('Finished.')

if __name__ == '__main__':
    main()
