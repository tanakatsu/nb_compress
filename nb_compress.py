import json
import re
import argparse


def compress_output(output):
    if "text" in output:
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
    elif "data" in output:
        output_data = output["data"]
        if "image/png" in output_data:
            output_data["image/png"] = ""
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('-o', '--output', type=str)
    args = parser.parse_args()

    with open(args.file) as f:
        data = json.load(f)

    cells = []
    for cell in data["cells"]:
        if cell["cell_type"] == "code":
            outputs = cell["outputs"]
            if len(outputs) > 0:
                cell["outputs"] = [compress_output(o) for o in outputs]
        cells.append(cell)
    data["cells"] = cells

    if args.output:
        with open(args.output, "w") as f:
            jsonStr = json.dumps(data)
            f.write(jsonStr)

if __name__ == '__main__':
    main()
