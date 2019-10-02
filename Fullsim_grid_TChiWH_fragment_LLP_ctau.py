import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

import math
baseSLHATable="""
BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
   1000001     1.00000000E+05   # ~d_L
   2000001     1.00000000E+05   # ~d_R
   1000002     1.00000000E+05   # ~u_L
   2000002     1.00000000E+05   # ~u_R
   1000003     1.00000000E+05   # ~s_L
   2000003     1.00000000E+05   # ~s_R
   1000004     1.00000000E+05   # ~c_L
   2000004     1.00000000E+05   # ~c_R
   1000005     1.00000000E+05   # ~b_1
   2000005     1.00000000E+05   # ~b_2
   1000006     1.00000000E+05   # ~t_1
   2000006     1.00000000E+05   # ~t_2
   1000011     1.00000000E+05   # ~e_L
   2000011     1.00000000E+05   # ~e_R
   1000012     1.00000000E+05   # ~nu_eL
   1000013     1.00000000E+05   # ~mu_L
   2000013     1.00000000E+05   # ~mu_R
   1000014     1.00000000E+05   # ~nu_muL
   1000015     1.00000000E+05   # ~tau_1
   2000015     1.00000000E+05   # ~tau_2
   1000016     1.00000000E+05   # ~nu_tauL
   1000021     1.00000000E+05   # ~g
   1000022     %MLSP%           # ~chi_10
   1000023     %MN2%            # ~chi_20
   1000025     1.00000000E+05   # ~chi_30
   1000035     1.00000000E+05   # ~chi_40
   1000024     %MN2%            # ~chi_1+
   1000037     1.00000000E+05   # ~chi_2+

# DECAY TABLE
#         PDG            Width
DECAY   1000001     0.00000000E+00   # sdown_L decays
DECAY   2000001     0.00000000E+00   # sdown_R decays
DECAY   1000002     0.00000000E+00   # sup_L decays
DECAY   2000002     0.00000000E+00   # sup_R decays
DECAY   1000003     0.00000000E+00   # sstrange_L decays
DECAY   2000003     0.00000000E+00   # sstrange_R decays
DECAY   1000004     0.00000000E+00   # scharm_L decays
DECAY   2000004     0.00000000E+00   # scharm_R decays
DECAY   1000005     0.00000000E+00   # sbottom1 decays
DECAY   2000005     0.00000000E+00   # sbottom2 decays
DECAY   1000006     0.00000000E+00   # stop1 decays
DECAY   2000006     0.00000000E+00   # stop2 decays
DECAY   1000011     0.00000000E+00   # selectron_L decays
DECAY   2000011     0.00000000E+00   # selectron_R decays
DECAY   1000012     0.00000000E+00   # snu_elL decays
DECAY   1000013     0.00000000E+00   # smuon_L decays
DECAY   2000013     0.00000000E+00   # smuon_R decays
DECAY   1000014     0.00000000E+00   # snu_muL decays
DECAY   1000015     0.00000000E+00   # stau_1 decays
DECAY   2000015     0.00000000E+00   # stau_2 decays
DECAY   1000016     0.00000000E+00   # snu_tauL decays
DECAY   1000021     0.00000000E+00   # gluino decays
DECAY   1000022     0.00000000E+00   # neutralino1 decays
DECAY   1000023     %CTAU%   # neutralino2 decays
   0.00000000E+00   3    1000022   5   -5
   1.00000000E+00     2    1000022    25
DECAY   1000024     0.10000000E+00   # chargino1+ decays
   0.00000000E+00   3    1000022   12   -11
   1.00000000E+00     2    1000022    24
DECAY   1000025     0.00000000E+00   # neutralino3 decays
DECAY   1000035     0.00000000E+00   # neutralino4 decays
DECAY   1000037     0.00000000E+00   # chargino2+ decays
"""
def matchParams(mass):
  if mass < 124: return 76,0.64
  elif mass < 151: return 76, 0.6
  elif mass < 176: return 76, 0.57
  elif mass < 226: return 76, 0.54
  elif mass < 326: return 76, 0.51
  elif mass < 451: return 76, 0.48
  elif mass < 651: return 76, 0.45
  else: return 76, 0.42

# weighted average of matching efficiencies for the full scan
# must equal the number entered in McM generator params
mcm_eff = 0.469

model = "TChiWH_WToLNu_HToBB"
process = "C1N2"

# Parameters that define the grid in the bulk and diagonal
class gridBlock:
  def __init__(self, xmin, xmax, xstep, ystep):
    self.xmin = xmin
    self.xmax = xmax
    self.xstep = xstep
    self.ystep = ystep

mchargino_max = 225##real importan parameter
scanBlocks = []
scanBlocks.append(gridBlock(200, mchargino_max, 25, 25))#importan parameter for the grid

minDM = 126 #(higgs mass + 1GeV minumum mass splitting)
maxDM = mchargino_max-1
ymin, ymax = 0, mchargino_max

# Number of events for mass point, in thousands
def events(dm):
  if (mx-my)<maxDM: return 100
  else: return 30
  
# -------------------------------
#    Constructing grid
# -------------------------------

# ctau, width
hBarCinGeVmm = 1.973269788e-13

decay_length_power = 4
gevWidth = []
for i in range(3,decay_length_power):
  print i
  gevWidth.append( math.pow(10,i) )
scanBlocks = []
print gevWidth

# mass points
cols = []
Nevents = []
xmin, xmax = 9999, 0
for block in scanBlocks:
  for mx in range(block.xmin, block.xmax, block.xstep):
    xmin = min(xmin, block.xmin)
    xmax = max(xmax, block.xmax)
    #if mx == 125: mx = 127.
    print "mx, xmin, xmax", mx, xmin, xmax
    col = []
    my = 0
    # Adding bulk points
#    if (mx-block.xmin)%block.xstep == 0:
#      if mx == 125: mx = 127
#      for my in range(ymin, ymax, block.ystep):
#        if my == 0: my = 1
#        if mx-my == 125: my = my-1
#        print "Y:", my, "X: ", mx
#        #print "chek y: ", mx-my, maxDM
#        if my > ymax or mx-my > maxDM or mx-my < minDM : continue
#        nev = events(mx-my)
#        col.append([mx,my, nev])
#        print "Append: ", mx, my, nev
    #if my !=  mx-minDM and mx-minDM <= ymax and not (mx-my) > 126:
    #  my = mx-minDM
    #  nev = events(mx-my)
    #  col.append([mx,my, nev])
    my = 1
    nev = events(mx-my)
    col.append([mx,my, nev])
    print "Append: ", mx, my, nev
    cols.append(col)

mpoints = []
for col in cols: 
  mpoints.extend(col)
  #print col
  #print mpoints

# add shifted point
# mpoints.append([127,0,100])


allPointsTChiLL = []
for ctau0 in gevWidth:
	for point in mpoints:
            mn2, mlsp = point[0], point[1]
            print mn2,mlsp,ctau0
	    qcut, tru_eff = matchParams(mchi)
	    wgt = point[2]*(mcm_eff/tru_eff)
            allPointsTChiLL.append(point+[wgt])
            ctau = hBarCinGeVmm / ctau0
	    
	    externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
	        args =  cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.4.2/sus_sms/LO_PDF/SMS-%s/v1/SMS-%s_mC1-%i_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz' % (process,process,mchi)),
	        nEvents = cms.untracked.uint32(5000),
	        numberOfParameters = cms.uint32(1),
	        outputFile = cms.string('cmsgrid_final.lhe'),
	        scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
	    )

            if mlsp==0: mlsp = 1
            slhatable = baseSLHATable.replace('%MN2%','%e' % mn2)
            slhatable = slhatable.replace('%MLSP%','%e' % mlsp)
            slhatable = slhatable.replace('%CTAU%','%e' % ctau)


	    basePythiaParameters = cms.PSet(
	        pythia8CommonSettingsBlock,
	        pythia8CP5SettingsBlock,
	        JetMatchingParameters = cms.vstring(
	            'JetMatching:setMad = off',
	            'JetMatching:scheme = 1',
	            'JetMatching:merge = on',
	            'JetMatching:jetAlgorithm = 2',
	            'JetMatching:etaJetMax = 5.',
	            'JetMatching:coneRadius = 1.',
	            'JetMatching:slowJetPower = 1',
	            'JetMatching:qCut = %.0f' % qcut, #this is the actual merging scale
	            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
	            'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
	            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
	            '6:m0 = 172.5',
                    '24:onMode = off', # w lepton filter
                    '24:onIfAny = 11 13 15',
	            '25:onMode = off',
	            '25:onIfMatch = 5 -5',
	    	'Check:abortIfVeto = on',
	            '25:doForceWidth = true',
	            '25:mWidth = 2.0',
	            '25:mMin = 30.0',
	            '25:m0 = 125.0',
	        ), 
	        parameterSets = cms.vstring('pythia8CommonSettings',
	    			        'pythia8CP5Settings',
	                                    'JetMatchingParameters'
	        )
	    )
	    
	    particleList = [1000023]
	    for p in particleList:
	       basePythiaParameters.pythia8CommonSettings.extend([str(p)+':tau0 = %e' % ctau0])
	    basePythiaParameters.pythia8CommonSettings.extend(['ParticleDecays:tau0Max = 1000.1'])
	    basePythiaParameters.pythia8CommonSettings.extend(['LesHouches:setLifetime = 2'])
	    basePythiaParameters.pythia8CommonSettings.extend(['RHadrons:allow = on'])
	    
	    generator = cms.EDFilter("Pythia8HadronizerFilter",
	      maxEventsToPrint = cms.untracked.int32(1),
	      pythiaPylistVerbosity = cms.untracked.int32(1),
	      filterEfficiency = cms.untracked.double(1.0),
	      pythiaHepMCVerbosity = cms.untracked.bool(False),
	      comEnergy = cms.double(13000.),
              ConfigDescription = cms.string('%s_%i_%i_%i' % (model, mn2, mlsp,ctau0)),
	      SLHATableForPythia8 = cms.string('%s' % slhatable),
	      PythiaParameters = basePythiaParameters,
	    )

print len(allPointsTChiLL)
