import os

optab = {
    "STOP": ("IS", "00"), "ADD": ("IS", "01"), "SUB": ("IS", "02"),
    "MULT": ("IS", "03"), "MOVER": ("IS", "04"), "MOVEM": ("IS", "05"),
    "COMP": ("IS", "06"), "BC": ("IS", "07"), "DIV": ("IS", "08"),
    "READ": ("IS", "09"), "PRINT": ("IS", "10"), "START": ("AD", "01"),
    "END": ("AD", "02"), "ORIGIN": ("AD", "03"), "EQU": ("AD", "04"),
    "LTORG": ("AD", "05"), "DC": ("DL", "01"), "DS": ("DL", "02")
}

regtab = {"AREG": 1, "BREG": 2, "CREG": 3, "DREG": 4}
condtab = {"LT": 1, "LE": 2, "EQ": 3, "GT": 4, "GE": 5, "ANY": 6}

def get_opcode(opcode): return optab.get(opcode)
def get_reg(reg): return regtab.get(reg, -1)
def get_cond(cond): return condtab.get(cond, -1)

def find_in_table(sym, table, index=1): 
    return next((i for i, entry in enumerate(table) if entry[index] == sym), -1)

def resolve_expression(expr, symtab):
    try: return int(expr)
    except ValueError:
        parts = expr.split('+')
        base_address = next((e[2] for e in symtab if e[1] == parts[0].strip()), None)
        return base_address + int(parts[1]) if base_address else None

def handle_literal_declaration(littab, pooltab, lc):
    for i, entry in enumerate(littab):
        if entry[2] == -1:
            littab[i] = (entry[0], entry[1], lc)
            lc += 1
    pooltab.append(len(pooltab) + 1)
    return lc

def main():
    project_path = r"D:\FILES\CODES\pyton notes"
    asm_path, ic_path, st_path, lt_path, pt_path = [os.path.join(project_path, f) for f in ["input.asm", "ic.txt", "symtable.txt", "littable.txt", "pooltable.txt"]]

    LC, symtab, littab, pooltab, scnt, lcnt = 0, [], [], [], 0, 0

    with open(asm_path, 'r') as asm, open(ic_path, 'w') as ic, open(st_path, 'w') as st, open(lt_path, 'w') as lt, open(pt_path, 'w') as pt:
        for line in asm:
            tokens = line.split()
            label, opcode, *operands = (tokens + ["NAN"] * 3)[:3]
            op = get_opcode(opcode)
            if not op: continue

            if label != "NAN" and find_in_table(label, symtab) == -1:
                symtab.append((scnt + 1, label, LC))
                scnt += 1

            if opcode == "START":
                LC = int(operands[0])
                ic.write(f"---\t({op[0]},{op[1]}) (C,{operands[0]}) NAN\n")
            elif opcode == "END":
                ic.write(f"---\t({op[0]},{op[1]}) NAN NAN\n")
                LC = handle_literal_declaration(littab, pooltab, LC)
                break
            elif opcode == "LTORG":
                ic.write(f"---\t({op[0]},{op[1]}) NAN NAN\n")
                LC = handle_literal_declaration(littab, pooltab, LC)
            elif opcode == "ORIGIN":
                LC = resolve_expression(operands[0], symtab)
            else:
                lc, LC = LC, LC + (int(operands[0]) - 1 if opcode == "DS" else 1)
                if opcode in ["DS", "DC"]:
                    ic.write(f"{lc}\t({op[0]},{op[1]}) (C,{operands[0].strip('()')}) NAN\n")
                else:
                    op1_code = get_reg(operands[0]) if opcode != "BC" else get_cond(operands[0])
                    if operands[1].startswith("="):
                        if find_in_table(operands[1], littab) == -1:
                            littab.append((lcnt + 1, operands[1], -1))
                            lcnt += 1
                        op2_code = f"(L,{find_in_table(operands[1], littab) + 1})"
                    else:
                        sym_idx = find_in_table(operands[1], symtab)
                        if sym_idx == -1:
                            symtab.append((scnt + 1, operands[1], -1))
                            scnt += 1
                        op2_code = f"(S,{sym_idx + 1 if sym_idx != -1 else scnt})"
                    ic.write(f"{lc}\t({op[0]},{op[1]}) ({op1_code}) {op2_code}\n")

        for table, f in [(symtab, st), (littab, lt), (pooltab, pt)]:
            for entry in table:
                f.write(f"{entry[0]}\t{entry[1]}\t{entry[2]}\n" if isinstance(entry, tuple) else f"#{entry}\n")

if __name__ == "__main__":
    main()
