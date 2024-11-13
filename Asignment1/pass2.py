import os

def table_lookup(table_file, num):
    with open(table_file, 'r') as table:
        for line in table:
            no, name, addr = line.split()
            if no == num:
                return addr
    return "NAN"

def main():
    project_path = r"D:\FILES\CODES\pyton notes"
    ic_path = os.path.join(project_path, "ic.txt")
    st_path = os.path.join(project_path, "symtable.txt")
    lt_path = os.path.join(project_path, "littable.txt")
    mc_path = os.path.join(project_path, "machine_code.txt")

    with open(ic_path, 'r') as ic, open(mc_path, 'w') as mc:
        print("\n -- ASSEMBLER PASS-2 OUTPUT --\n")
        print("LC\t<INTERMEDIATE CODE>\t\t\tLC\t<MACHINE CODE>\n")
        for line in ic:
            lc, ic1, ic2, ic3 = line.split()
            mc_line = ""
            if ic1.startswith("(AD") or (ic1.startswith("(DL") and ic1.endswith("02)")):
                mc_line = "-No Machine Code-"
            elif ic1.startswith("(DL,01)"):
                mc_line = f"00\t0\t00{ic2[3]}"
            else:
                if ic1 == "(IS,00)":
                    mc_line = f"{ic1[4:6]}\t0\t000"
                elif ic2.startswith("(S"):
                    addr = table_lookup(st_path, ic2[4])
                    mc_line = f"{ic1[4:6]}\t0\t{addr}"
                else:
                    if ic3.startswith("(S"):
                        addr = table_lookup(st_path, ic3[4])
                    else:
                        addr = table_lookup(lt_path, ic3[4])
                    mc_line = f"{ic1[4:6]}\t{ic2[1]}\t{addr}"

            print(f"{lc}\t{ic1}\t{ic2}\t{ic3}\t\t\t{lc}\t{mc_line}\n")
            mc.write(f"{lc}\t{mc_line}\n")

if __name__ == "__main__":
    main()
