# susy_llp_fullsim
SUSY LLP Fullsim signal generation

# PPD RunII guideline
https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable

Take 2017 condition.

# Setup

```
export SCRAM_ARCH=slc6_amd64_gcc630
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW CMSSW_9_4_12
cd CMSSW_9_4_12/src
eval `scram runtime -sh`

mkdir -p Configuration/GenProduction/python/
```

# step 0: LHE, GEN, SIM

seed=$(($(date +%s) % 100 + 1))

cmsDriver.py Configuration/GenProduction/python/SUS-RunIIFall17wmLHEGS-00161-fragment.py --fileout file:SUS-RunIIFall17wmLHEGS-00161.root --mc --eventcontent RAWSIM,LHE --datatier GEN-SIM,LHE --conditions 94X_mc2017_realistic_v17 --beamspot Realistic25ns13TeVEarly2017Collision --step LHE,GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2017 --python_filename SUS-RunIIFall17wmLHEGS-00161_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${seed})" -n 10

cmsRun SUS-RunIIFall17wmLHEGS-00161_1_cfg.py

#step 1: DIGI

cmsDriver.py step1 --fileout file:SUS-RunIIFall17DRPremix-00183_step1.root  --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-MCv2_correctPU_94X_mc2017_realistic_v9-v1/GEN-SIM-DIGI-RAW" --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 94X_mc2017_realistic_v17 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:2e34v40 --nThreads 8 --datamix PreMix --era Run2_2017 --python_filename SUS-RunIIFall17DRPremix-00183_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 10

#Step 2: RECO --> AODSIM

cmsDriver.py step2 --filein file:SUS-RunIIFall17DRPremix-00183_step1.root --fileout file:SUS-RunIIFall17DRPremix-00183.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 94X_mc2017_realistic_v17 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 8 --era Run2_2017 --python_filename SUS-RunIIFall17DRPremix-00183_2_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 10

