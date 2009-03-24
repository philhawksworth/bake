import sys, os, re

# setup and read parameters
recipe = sys.argv[1]
filePaths = list()
ingredients = dict()
template = ''


def parseRecipe(recipe):
	global template
	global filePaths
	
	try:
		f = open(recipe, 'r')
	except IOError:
		print 'Oooops! Couldn\'t open ', recipe
	else:
		for line in f:
			line = line.rstrip("\n")
			if line == "":
				break
			args = line.split(": ")	
			if args[0] == "recipe":
				# parse and ub recipes found.
				parseRecipe(args[1])
			elif args[0] == 'template':
				# set the template to populate.
				template = args[1]
			else:
				# record the items to include.
				filePaths.append(args)


def collectIngredients():
	for item in filePaths:
		ingredients[item[0]] = ""
	for item in filePaths:
		print "adding " + item[0] + ": " + item[1]
		ingredients[item[0]] += open(item[1], 'r').read() + '\n'


def populateTemplate():
	global filePaths, recipe
	outputFile = recipe.rstrip(".recipe")
	templateFile = open(template, 'r').read()
	
	# inspect template for sections to populate.
	pattern = re.compile('(<!-- @@)(.*)(@@ -->)')
	sections = pattern.finditer(templateFile)
	for match in sections:
		templateFile = templateFile.replace(match.group(0), ingredients[match.group(2)])

	# write output
	print "Creating " + outputFile
	out = open(outputFile, 'w')
	out.write(templateFile)


# get started
print "Baking: " + recipe
parseRecipe(recipe)
collectIngredients()
populateTemplate()
