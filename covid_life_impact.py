
le = 0 # life expectancy at birth

def leab(gdp):
    # gdp per capita
    return 75.49- 48270/(gdp+1200)+0.0001401*gdp

uk_gdp = 40000

# look at a 5% drop

print("loss of life is: {0:.1f}".format(leab(uk_gdp)-leab(uk_gdp*0.95)))
