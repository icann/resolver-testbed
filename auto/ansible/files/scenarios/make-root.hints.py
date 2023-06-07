#!/usr/bin/env python3

import glob, math

def next_rr(fi):
	return next(fi).rstrip().split('\t')

def get_glue(rr, fi, rs_names):
	txt = ''
	nses_printed = set()
	try:
		while True:
			if rr[0].upper() in rs_names \
			and (rr[3] == 'A' or rr[3] == 'AAAA'):
				name = rr[0].upper()
				if name not in nses_printed:
					txt += '.%s%s\tIN\tNS\t%s\n' \
					     % ( '\t' * math.ceil(len(name) / 8)
					       , rr[1], name )
					nses_printed.add(name)
				txt += '\t'.join([name] + rr[1:]) + '\n'
			rr = next_rr(fi)
	except StopIteration:
		pass
	return txt
	

for fn in sorted(glob.glob('*-root')):
	sc = fn.split('-')[0]
	rs_files  = set(glob.glob(sc + '-*'))
	rs_files -= { fn, sc + '-net', sc + '-root.hints' }
	root = iter(open(fn))
	rr = next_rr(root)
	root_ns_set = list()
	while rr[0] != '.' or rr[3] != 'NS':
		rr = next_rr(root)
	while rr[0] == '.' and rr[3] == 'NS':
		root_ns_set.append(rr)
		rr = next_rr(root)
	rs_names = [name.upper() for owner, ttl, clas, typ, name in root_ns_set]
	if not rs_files:
		txt = get_glue(rr, root, rs_names)
	else:
		txt = ''
		for rs_file in sorted(rs_files):
			fi = iter(open(rs_file))
			txt += get_glue(next_rr(fi), fi, rs_names)
	
	open(sc + '-root.hints', 'w').write(txt)
