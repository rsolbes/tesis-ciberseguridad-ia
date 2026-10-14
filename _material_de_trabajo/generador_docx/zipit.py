import zipfile, os, sys
src, dst = sys.argv[1], sys.argv[2]
orig = zipfile.ZipFile(sys.argv[3])
names = orig.namelist()  # keep original order, [Content_Types].xml first
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
    done = set()
    for n in names:
        p = os.path.join(src, n)
        if os.path.exists(p): z.write(p, n); done.add(n)
    for root, _, files in os.walk(src):
        for f in files:
            n = os.path.relpath(os.path.join(root, f), src).replace(os.sep, '/')
            if n not in done: z.write(os.path.join(root, f), n)
print('zipped', dst)
