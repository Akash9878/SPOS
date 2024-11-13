import re

class MNTEntry:
    def __init__(self, name, pp, kp, mdtp, kpdtp):
        self.name = name
        self.pp = pp
        self.kp = kp
        self.mdtp = mdtp
        self.kpdtp = kpdtp

def main():
    # Open files
    with open("intermediate.txt", "r") as irb, \
         open("mdt.txt", "r") as mdtb, \
         open("kpdt.txt", "r") as kpdtb, \
         open("mnt.txt", "r") as mntb, \
         open("pass2.txt", "w") as fr:

        mnt = {}
        aptab = {}
        aptab_inverse = {}

        mdt = []
        kpdt = []

        # Reading MDT file
        mdt = [line.strip() for line in mdtb]

        # Reading KPDT file
        kpdt = [line.strip() for line in kpdtb]

        # Reading MNT file
        for line in mntb:
            parts = line.split()
            mnt[parts[0]] = MNTEntry(parts[0], int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))

        # Reading Intermediate file and processing
        for line in irb:
            line = line.strip()
            parts = re.split(r'\s+', line)
            if parts[0] in mnt:
                entry = mnt[parts[0]]
                pp = entry.pp
                kp = entry.kp
                kpdtp = entry.kpdtp
                mdtp = entry.mdtp
                param_no = 1

                # Processing positional parameters
                for i in range(1, pp + 1):
                    if param_no < len(parts):
                        parts[param_no] = parts[param_no].replace(",", "")
                        aptab[param_no] = parts[param_no]
                        aptab_inverse[parts[param_no]] = param_no
                        param_no += 1
                    else:
                        print(f"Warning: Positional parameter {param_no} missing in intermediate line")

                # Processing keyword parameters
                j = kpdtp - 1
                for i in range(kp):
                    if j < len(kpdt):
                        temp = kpdt[j].split("\t")
                        if len(temp) == 2:
                            aptab[param_no] = temp[1]
                            aptab_inverse[temp[0]] = param_no
                            j += 1
                            param_no += 1
                        else:
                            print(f"Warning: Keyword parameter format incorrect at index {j}")
                    else:
                        print(f"Warning: No more keyword parameters available in kpdt at index {j}")

                # Replacing parameters in the intermediate code
                for i in range(pp + 1, len(parts)):
                    parts[i] = parts[i].replace(",", "")
                    splits = parts[i].split("=")
                    if len(splits) == 2:
                        name = re.sub(r'&', '', splits[0])
                        if name in aptab_inverse:
                            aptab[aptab_inverse[name]] = splits[1]
                        else:
                            print(f"Warning: Parameter name '{name}' not found in aptab_inverse")
                    else:
                        print(f"Warning: Incorrect parameter replacement format in {parts[i]}")

                # Writing to the output file
                i = mdtp - 1
                while i < len(mdt) and not mdt[i].upper().startswith("MEND"):
                    splits = re.split(r'\s+', mdt[i])
                    fr.write("+")
                    for k in range(len(splits)):
                        if "(P," in splits[k]:
                            splits[k] = re.sub(r'[^\d]', '', splits[k])  # Extract number
                            value = aptab.get(int(splits[k]), "UNKNOWN")
                            fr.write(f"{value}\t")
                        else:
                            fr.write(f"{splits[k]}\t")
                    fr.write("\n")
                    i += 1

                aptab.clear()
                aptab_inverse.clear()
            else:
                fr.write(line + "\n")

    print("Macro Pass 2 Processing done. :)")

if __name__ == "__main__":
    main()
