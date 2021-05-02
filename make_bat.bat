@rem Make bundle batch files
python py/gitbundle_sample.py ./gitbundle_config.json --update-repo --mode=genbat

@rem Run bundle output batch
bat_out/git_bundle_out.bat

@rem Run bundle merge batch 
@rem bat_out/git_bundle_in.bat