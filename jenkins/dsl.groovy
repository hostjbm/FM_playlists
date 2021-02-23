job("FM_playlists") {
	description()
	keepDependencies(false)
	scm {
		git {
			remote {
				github("hostjbm/FM_playlists", "https")
			}
			branch("*/master")
		}
	}
	disabled(false)
	concurrentBuild(false)
	steps {
		shell("/bin/bash start_cron.sh")
	}
	publishers {
		archiveArtifacts {
			pattern("*.tar.gz")
			allowEmpty(false)
			onlyIfSuccessful(false)
			fingerprint(false)
			defaultExcludes(true)
		}
	}
	wrappers {
		preBuildCleanup {
			deleteDirectories(false)
			cleanupParameter()
		}
	}
}
