#!/usr/bin/env python

import os


def main():
    input_file = 'base/v0.6.0_beta.proto'
    output_dir = 'dumpBase'
    with open(input_file, "r") as f:
        contents = f.readlines()
        splits = splitContents(contents)
        for split in splits:
            writeSplit(output_dir, split)


def writeSplit(output_dir, split):
    header = """
syntax = "proto3";
package WUProtos.DumpBase;

""".format(package_name=".".join(split['package_hierarchy']))

    # print(split) # Debug mode
    directory = output_dir

    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

    file_name = os.path.join(directory, split['name'] + ".proto")
    with open(file_name, "w") as output:
        output.writelines(header)
        output.writelines(split['content'])


def splitContents(contents):
    splits = []
    i = -1
    current_split = {}
    for content in contents:
        if content.startswith('// ref:'):
            if i >= 0:
                splits.append(current_split)
            i = i + 1
            fqn = content[8:]
            package_hierarchy = fqn.split('.')
            name = package_hierarchy.pop()[:-1]
            current_split = {
                'name': name,
                'package_hierarchy': package_hierarchy,
                'content': []
            }
        else:
            if i >= 0:
                current_split['content'].append(content)

    return splits


if __name__ == "__main__":
    main()
