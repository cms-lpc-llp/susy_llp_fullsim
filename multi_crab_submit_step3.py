if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    #from CRABClient.UserUtilities import config
    #config = config()
    from WMCore.Configuration import Configuration
    config = Configuration()

    config.section_("General")
    config.General.workArea = 'crab'
    config.General.transferOutputs = True
    config.General.transferLogs = True

    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = '/afs/cern.ch/user/j/jmao/work/public/releases/cms-llp/CMSSW_9_4_12/src/crab_scripts/Fullsim_step3_cfg.py'
    config.JobType.numCores = 1
    config.section_("Data")
    config.Data.inputDBS = 'phys03'
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 4 #when splitting is 'Automatic', this represents jobs target runtime(minimum 180)
    config.Data.publication = True
    config.Data.ignoreLocality = True

    config.section_("Site")
    config.Site.storageSite = 'T2_US_Caltech'
    config.Site.whitelist = ['T2_US_Caltech']
    config.Site.ignoreGlobalBlacklist = True
    
    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################
    ev = 100000
    mchi_list = [200]
    pl_list = [1000]
    mode_list = ["n3n2-n1-hbb-hbb"]
    for i in range(len(mode_list)):
	mode = mode_list[i]
	for mchi in mchi_list:
	    for pl in pl_list:
		spec = mode+"_mh{}_pl{}_ev{}".format(mchi,pl,ev)
		name = mode+"_mchi{}_pl{}_ev{}".format(mchi,pl,ev)
		if pl==0:
			spec = mode+"_mh{}_prompt_ev{}".format(mchi,ev)
			name = mode+"_mchi{}_prompt_ev{}".format(mchi,ev)
		if 'wlv' in mode:
			name = mode+"_mchi{}__mlsp150_pl{}_ev{}".format(mchi,pl,ev)
		
		
    		config.General.requestName = 'CMSSW_9_4_12_'+name+'_MINIAODSIM_CaltechT2'
		#config.Data.inputDataset = ''
		config.Data.inputDataset = '/n3n2-n1-hbb-hbb_mh200_pl1000_ev100000/jmao-crab_CMSSW_9_4_12_n3n2-n1-hbb-hbb_mchi200_pl1000_ev100000_AODSIM_CaltechT2-37ac8d442b9840be1abba4facfa67e70/USER'
		#config.Data.inputDataset = '/n3n2-n1-hbb-hbb_mh300_pl1000_ev100000/jmao-crab_CMSSW_9_4_12_n3n2-n1-hbb-hbb_mchi300_pl1000_ev100000_AODSIM_CaltechT2-37ac8d442b9840be1abba4facfa67e70/USER'
		#config.Data.inputDataset = '/n3n2-n1-hbb-hbb_mh400_pl1000_ev100000/jmao-crab_CMSSW_9_4_12_n3n2-n1-hbb-hbb_mchi400_pl1000_ev100000_AODSIM_CaltechT2-37ac8d442b9840be1abba4facfa67e70/USER'
		#config.Data.inputDataset = '/n3n2-n1-hbb-hbb_mh200_prompt_ev100000/jmao-crab_CMSSW_9_4_12_n3n2-n1-hbb-hbb_mchi200_prompt_ev100000_AODSIM_CaltechT2-37ac8d442b9840be1abba4facfa67e70/USER'
		#config.Data.inputDataset = '/n3n2-n1-hbb-hbb_mh300_prompt_ev100000/jmao-crab_CMSSW_9_4_12_n3n2-n1-hbb-hbb_mchi300_prompt_ev100000_AODSIM_CaltechT2-37ac8d442b9840be1abba4facfa67e70/USER'
		#config.Data.inputDataset = '/n3n2-n1-hbb-hbb_mh400_prompt_ev100000/jmao-crab_CMSSW_9_4_12_n3n2-n1-hbb-hbb_mchi400_prompt_ev100000_AODSIM_CaltechT2-37ac8d442b9840be1abba4facfa67e70/USER'
		config.Data.outLFNDirBase = '/store/group/phys_exotica/jmao/aodsim/RunIISummer16/MINIAODSIM/MSSM-1d-prod/'
		if mode=="x1n2-n1-wlv-hbb" : 
			config.Data.outLFNDirBase = '/store/group/phys_exotica/jmao/aodsim/RunIISummer16/MINIAODSIM/MSSM-2d-prod/'
		config.JobType.maxMemoryMB = 5000
		print(config.Data.inputDataset)
		print(config.JobType.psetName)
		print(config.General.requestName)
		submit(config)

