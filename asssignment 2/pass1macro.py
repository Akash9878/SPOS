import re

def main():
    # Open files
    with open("macro_input.asm", "r") as br, \
         open("mnt.txt", "w") as mnt, \
         open("mdt.txt", "w") as mdt, \
         open("kpdt.txt", "w") as kpdt, \
         open("pntab.txt", "w") as pnt, \
         open("intermediate.txt", "w") as ir:

        pntab = {}
        line = None
        Macroname = None
        mdtp = 1
        kpdtp = 0
        paramNo = 1
        pp = 0
        kp = 0
        flag = 0

        for line in br:
            line = line.strip()
            parts = re.split(r'\s+', line)

            if parts[0].upper() == "MACRO":
                flag = 1
                line = next(br).strip()
                parts = re.split(r'\s+', line)
                Macroname = parts[0]

                if len(parts) <= 1:
                    mnt.write(f"{parts[0]}\t{pp}\t{kp}\t{mdtp}\t{kp if kp == 0 else kpdtp + 1}\n")
                    continue

                for i in range(1, len(parts)):  # Processing parameters
                    parts[i] = re.sub(r'[&,]', '', parts[i])
                    if '=' in parts[i]:
                        kp += 1
                        keywordParam = parts[i].split('=')
                        pntab[keywordParam[0]] = paramNo
                        paramNo += 1
                        kpdt.write(f"{keywordParam[0]}\t{keywordParam[1] if len(keywordParam) == 2 else '-'}\n")
                    else:
                        pntab[parts[i]] = paramNo
                        paramNo += 1
                        pp += 1

                mnt.write(f"{parts[0]}\t{pp}\t{kp}\t{mdtp}\t{kp if kp == 0 else kpdtp + 1}\n")
                kpdtp += kp

            elif parts[0].upper() == "MEND":
                mdt.write(line + "\n")
                flag = kp = pp = 0
                mdtp += 1
                paramNo = 1
                pnt.write(Macroname + ":\t")
                for key in pntab:
                    pnt.write(f"{key}\t")
                pnt.write("\n")
                pntab.clear()

            elif flag == 1:
                for i in range(len(parts)):
                    if '&' in parts[i]:
                        parts[i] = re.sub(r'[&,]', '', parts[i])
                        mdt.write(f"(P,{pntab[parts[i]]})\t")
                    else:
                        mdt.write(parts[i] + "\t")
                mdt.write("\n")
                mdtp += 1

            else:
                ir.write(line + "\n")

    print("Macro Pass 1 Processing done. :)")

if __name__ == "__main__":
    main()
