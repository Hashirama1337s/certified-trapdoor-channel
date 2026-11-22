import json, sys
src, dst, claim = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(src))
assert "claimed_rho_upper" not in d
d["claimed_rho_upper"] = claim
json.dump(d, open(dst, "w"))
print("wrote", dst)
