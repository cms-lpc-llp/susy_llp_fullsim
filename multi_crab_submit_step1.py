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
    config.JobType.psetName = '/afs/cern.ch/user/j/jmao/work/public/releases/cms-llp/CMSSW_9_4_12/src/SUS-RunIIFall17DRPremix-00183_1_cfg.py'
    config.JobType.numCores = 1
    config.section_("Data")
    config.Data.inputDBS = 'phys03'
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 1 #when splitting is 'Automatic', this represents jobs target runtime(minimum 180)
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
    mode_list = ["n3n2-n1-zll-hbb"]
    #mode_list = ["x1n2-n1-wlv-hbb"]
    for i in range(len(mode_list)):
	mode = mode_list[i]
	for mchi in mchi_list:
	    for pl in pl_list:
		spec = mode+"_mh{}_pl{}_ev{}".format(mchi,pl,ev)
		name = mode+"_mchi{}_pl{}_ev{}".format(mchi,pl,ev)
		

    		config.General.requestName = 'CMSSW_9_4_12_'+name+'_DR_CaltechT2'
		#/x1n2-n1-wlv-hbb_mh200_pl1000_ev100000/jmao-crab_CMSSW_9_4_12_x1n2-n1-wlv-hbb_mchi200_pl1000_ev100000_GENSIM_CaltechT2_RAWSIMoutput-56f095f35a9341c180b52cbb6bb9c0cb/USER
		config.Data.inputDataset = '/'+spec+'/jmao-crab_CMSSW_9_4_12_'+name+'_GENSIM_CaltechT2_RAWSIMoutput-56f095f35a9341c180b52cbb6bb9c0cb/USER' 
		config.Data.outLFNDirBase = '/store/group/phys_exotica/jmao/aodsim/RunIIFall17/DR/MSSM-1d-prod/'
		#config.JobType.numCores = 8
		config.JobType.maxMemoryMB = 10000
		if "x1n2" in mode:
			config.Data.outLFNDirBase = '/store/group/phys_exotica/jmao/aodsim/RunIIFall17/DR/MSSM-2d-prod/'
		#print(config.Data.inputDataset)
		#print(config.Data.outLFNDirBase)
		submit(config)

