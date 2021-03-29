import argparse
import enum
import os
import re

imageNameHash = {}
imageLocalNameHash = {}

# Add Pattern as you needed
pattern1 = re.compile(r'MGIMAGE\(@\"(.*?)\"\)')
pattern2 = re.compile(r'\[UIImage imageNamed:@\"(.*?)\"\]')



patternArray = [pattern1,pattern2]
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help ="Project Root Path")
    parser.add_argument("-a", help ="Assets.xcassets Path")
    args = parser.parse_args()
    if args.p is None:
        print("Project Root Path None!")
        exit(0)
    if os.path.exists(args.p) == False:
        print("Project Root Path Not Exists!")
        exit(0)
    if args.a is None:
        print("Assets.xcassets Path None!")
        exit(0)
    if os.path.exists(args.a) == False:
        print("Assets.xcassets Path Not Exists!")
        exit(0)

    for root,dirs,files in os.walk(args.p):
        for name in files:
            if name.endswith(".m") or name.endswith(".swift"):
                lines = ""
                with open(os.path.join(root,name),'r') as codeContent:
                    lines = codeContent.readlines()
                
                for line in lines:

                    for pattern in patternArray:
                        results = pattern.findall(line)
                        if results:
                            for result in results:
                                imageNameHash[result] = result

    for root,dirs,files in os.walk(args.a):
        for name in dirs:
            if name.endswith(".imageset") and '_dark' not in name:
                imageLocalNameHash[name.replace('.imageset','')] = name.replace('.imageset','')

    imageNotUse = []

    for key,value in enumerate(imageLocalNameHash):
        if value not in imageNameHash:
            imageNotUse.append(value)

    print(imageNotUse)
    
