import sys
import hashlib

def file_hash( input_filename, output_filename=None, has_sha256=False, has_md5=False, has_blake2b256=False):
    """计算文件的HASH值"""
    fpi = open(input_filename, 'rb')

    if output_filename:
        fpo = open(output_filename, 'w')
    else:
        fpo = sys.stdout

    if (has_sha256 or has_md5 or has_blake2b256) == False:
        has_sha256 = has_md5 = has_blake2b256 = True

    if has_sha256:
        h_sha256 = hashlib.sha256()
    if has_md5:
        h_md5 = hashlib.md5()
    if has_blake2b256:
        h_blake2b256 = hashlib.blake2b(digest_size=32)

    while True:
        c = fpi.read(10240)
        if not c:
            break

        if has_md5:
            h_md5.update(c)
        if has_sha256:
            h_sha256.update(c)
        if has_blake2b256:
            h_blake2b256.update(c)

    if has_sha256:
        fpo.write("SHA256:" + h_sha256.hexdigest() + '\n')
    if has_md5:
        fpo.write("MD5:" + h_md5.hexdigest() + '\n')
    if has_blake2b256:
        fpo.write("BLAKE2b-256:" + h_blake2b256.hexdigest() + '\n')

    fpi.close()
    fpo.close()

def main_use_argparse():
    import argparse

    parser = argparse.ArgumentParser(description="计算文件的HASH值")
    parser.add_argument("--md5", "--MD5", action="store_true", help="运行MD5算法")
    parser.add_argument("--sha256", "--SHA256", action="store_true", help="运行SHA256算法")
    parser.add_argument("--blake2b256", "--Blake2b256","--BLAKE2B-256", action="store_true", help="运行BLAKE2B256算法")
    parser.add_argument("-f", "--filename", required=True, action="store", help="输入文件名")
    parser.add_argument("-o", "--output_filename", action="store", help="输出文件名")

    args = parser.parse_args()

    file_hash( input_filename = args.filename,
               output_filename = args.output_filename,
               has_sha256=args.sha256,
               has_md5=args.md5,
               has_blake2b256=args.blake2b256)

def main_use_getopt():
    import getopt

    def usage():
        print("usage: %s -f FILENAME [-h] [--md5] [--sha256] [--blake2b256] [-o OUTPUT_FILENAME]"%(sys.argv[0]))

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hf:o:",
                                   ['filename=',
                                    'output_filename=',
                                    'md5',
                                    'MD5',
                                    'sha256',
                                    'SHA256',
                                    'blake2b256',
                                    'Blake2b256',
                                    'BLAKE2B256'
                                    ])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    input_filename=output_filename=None
    has_sha256 = has_md5 = has_blake2b256 = False
    for op, value in opts:
        if op == '-h':
            usage()
            sys.exit(2)
        elif op=='-f' or op=='--filename':
            input_filename = value
        elif op=='-o' or op=='--output_filename':
            output_filename = value
        elif op=='--md5' or op=='--MD5':
            has_md5=True
        elif op=='--sha256' or op=='--SHA256':
            has_sha256=True
        elif op=='--blake2b256' or op=='--Blake2b256' or op=='--BLAKE2B256':
            has_blake2b256=True
    if not input_filename:
        usage()
        sys.exit(2)

    file_hash( input_filename = input_filename,
               output_filename = output_filename,
               has_sha256=has_sha256,
               has_md5=has_md5,
               has_blake2b256=has_blake2b256)

if __name__ == "__main__":

    # 使用argparse库
    main_use_argparse()

    # 使用getopt库
    # main_use_getopt()
