import matplotlib.pyplot as plt
import numpy as np

def doseRisk(age, expAge, dose, beta, eta, gamma):
	eStar = (expAge - 30)/10 if (expAge < 30) else 0
	
	exRisk = beta[0]*dose*np.exp(gamma[0]*eStar)*np.power((age/60.),eta[0])
	#print(np.exp(gamma*eStar))
	#sprint(np.power((age/60.),eta))
	#print(eStar, age, exRisk)
	
	sigGamma = np.power(eStar*exRisk,2)*np.power((gamma[1]-gamma[2])/2.0,2)
	sigEta = np.power((eta[0]/age)*exRisk,2)*np.power((eta[1]-eta[2])/2.0,2)
	sigBeta = np.power(exRisk,2)*np.power((beta[1]-beta[2])/2.0,2)
	
	sigRisk = np.sqrt( sigGamma + sigEta + sigBeta )
	return exRisk, sigRisk

def plotRiskBounded(attainedAge, exposureAge, dose, beta, eta, gamma, axis, isMale=True, lnStyle='-'):
	pltLabel = "Male" if (isMale) else "Female"
	
	pltLabel = pltLabel + " (Exposure at {0:d} years)".format(exposureAge)

#	print(beta)
#	print(eta)
#	print(gamma)
	#print(beta[0])
	#print(np.power(attainedAge,eta[0]))
	risk, sigRisk = doseRisk(attainedAge, exposureAge, dose, beta, \
		eta, gamma)
#	riskLO = doseRisk(attainedAge, exposureAge, dose, beta[1], \
#		eta[1], gamma[1])
#	riskHI = doseRisk(attainedAge, exposureAge, dose, beta[2], \
#		eta[2], gamma[2])
	
	lnColor = ''
	if(isMale):
		lnColor = 'tab:blue'
	else:
		lnColor = 'tab:red'
		
	ax.plot(attainedAge, risk, label=pltLabel, ls=lnStyle,color=lnColor)
	
	#print(ax)
	ax.fill_between(attainedAge, risk-sigRisk, risk+sigRisk, interpolate=True,alpha=0.2)
	#plt.plot(attainedAge, d, label=None)
	#ax.plot(attainedAge, riskLO)	
	#ax.plot(attainedAge, riskHI)
		

	
fig, ax = plt.subplots()
	

beta_male_incidence_ERR = (0.33, 0.24, 0.47)
beta_female_incidence_ERR = (0.57, 0.44, 0.74)

eta_incidence_ERR = (-1.4, -2.2, -0.7)

gamma_incidence = (-0.3, -0.51, -0.10)

attainedAge = np.linspace(30,90,100)
dose = 1 # 20 mSv

plotRiskBounded(attainedAge, 10, dose, beta_male_incidence_ERR, eta_incidence_ERR, gamma_incidence, ax, isMale=True)
plotRiskBounded(attainedAge, 10, dose, beta_female_incidence_ERR, eta_incidence_ERR, gamma_incidence, ax, isMale=False)

#plotRiskBounded(attainedAge, 20, dose, beta_male_incidence_ERR, eta_incidence_ERR, gamma_incidence, ax, isMale=True, lnStyle='--')
#plotRiskBounded(attainedAge, 20, dose, beta_female_incidence_ERR, eta_incidence_ERR, gamma_incidence, ax, isMale=False, lnStyle='--')

#plotRiskBounded(attainedAge, 31, dose, beta_male_incidence_ERR, eta_incidence_ERR, gamma_incidence, ax, isMale=True, lnStyle=':')
#plotRiskBounded(attainedAge, 31, dose, beta_female_incidence_ERR, eta_incidence_ERR, gamma_incidence, ax, isMale=False, lnStyle=':')




ax.legend()
plt.show()