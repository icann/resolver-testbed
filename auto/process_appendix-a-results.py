#!/usr/bin/env python

from collections import defaultdict

results = defaultdict(lambda: defaultdict(dict))
for ln in open('ansible/results/rssac028-appendix-a.txt'):
	_, sc, sz, test, dt, sw= ln.rstrip('\n').split('\t')
	results[sw][sc][test] = sz

scenarios = sorted({ sc for sw, x in results.items()
                        for sc, y in x.items() })
tests = sorted({ test for sw, x in results.items()
                      for sc, y in x.items() for test in y.keys() })
tests = tests[-1:1:-1] + tests[:2]
cols = ['Scenario'] + tests

for sw in results.keys():
	print('## %s\n' % sw)
	print('| %s |' % ' | '.join(cols))
	print('|-%s-|' % '-|-'.join(['-' * len(col) for col in cols]))
	for sc in scenarios:
		sizes = results.get(sw, {}).get(sc, {})
		print( '| %s | %s |' 
		     % ( sc.ljust(len('Scenario'))
		       , ' | '.join([ sizes.get(test, '-').ljust(len(test))
		                      for test in tests ])))
	print('\n')

