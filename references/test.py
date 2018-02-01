from refWizard import referenceWizard

r=referenceWizard("template.tex",fname_exclude="packages.bib")
print "OUTPUT:\n\n"
print r.bibs
