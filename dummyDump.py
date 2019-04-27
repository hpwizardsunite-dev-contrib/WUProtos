# Credits to Celandro https://www.pokebattler.com/ for this script.

import os
import re

TOP_PACKAGE = 'wuprotos'
INPUT_FILE = 'base/raw_protos.proto' # v0.6.0_beta.proto is optimized raw
OUTPUT_DIR = 'dummyDump'


def main():
    with open(INPUT_FILE, "r") as f:
        contents = f.readlines()
        splits = splitContents(contents)
        import_map = createImportMap(splits)
        for split in splits:
            writeSplit(OUTPUT_DIR, import_map, split)


def writeSplit(output_dir, import_map, split):
    package_name = ".".join(split['package_hierarchy'])
    header = """syntax = "proto3";

"""
    if len(split['package_hierarchy']) > 0:
        header = header + """package {package_name};

""".format(package_name=package_name)

    # print(split) # Debug mode
    directory = output_dir
    for package in split['package_hierarchy']:
        directory = os.path.join(directory, package)

    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

    file_name = os.path.join(directory, split['name'] + ".proto")
    with open(file_name, "w") as output:
        output.writelines(header)
        output.writelines(list(map(lambda x: import_map[x],
                                   filter(lambda x: x in import_map, split['imports']))))
        output.writelines(split['content'])


def createImportMap(splits):
    map = {}
    for split in splits:
        map[split['name']] = 'import "' + '/'.join(split['package_hierarchy']) + '/' + split['name'] + '.proto";\n'

    return map


def splitContents(contents):
    splits = []
    i = -1
    current_split = {}
    in_one_of = False

    for content in contents:
        if content.startswith('// ref:'):
            if i >= 0:
                splits.append(current_split)
            i = i + 1
            fqn = content[8:]
            package_hierarchy = [TOP_PACKAGE] + fqn.split('.')
            name = package_hierarchy.pop()[:-1]
            package_hierarchy = list(map(lambda x: x.lower(), package_hierarchy))
            current_split = {
                'name': name,
                'package_hierarchy': package_hierarchy,
                'content': [],
                'imports': {}
            }
        else:
            if i >= 0:
                if in_one_of:
                    if ("}" in content):
                        in_one_of = False
                else:
                    if ("Case {" in content):
                        in_one_of = True  # need to skip the one ofs
                    else:
                        protoImport = findImport(content)
                        if protoImport:
                            package = protoImport.group(1)
                            name = protoImport.group(2);
                            if package == 'i':
                                package = None
                                name = 'i' + name

                            if (package):
                                content = content.replace(package, TOP_PACKAGE + "." + package, 1)
                            current_split['imports'][name] = 1

                        current_split['content'].append(content)

    return splits


def findImport(content):
    # packages have at least one dot. Classes start with an upper case
    # Match 1 is the package. Match 2 is the class
    matchObj = re.match(r'.*\s([a-z/.]*)([A-Z]+[a-z]+\w+).*\d+;', content)

    return matchObj


if __name__ == "__main__":
    main()
